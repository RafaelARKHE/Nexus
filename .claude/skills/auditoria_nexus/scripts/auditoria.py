#!/usr/bin/env python3
r"""
auditoria.py — motor de varredura SOMENTE-LEITURA do sistema Nexus.

OBJETIVO: ancorar a integridade do Nexus na realidade dos arquivos, não nas
premissas do CLAUDE.md. Faz uma varredura em 5 camadas (estrutura física,
frontmatter, links, MOC↔realidade, git/sync) e imprime um relatório com
severidades (🔴 erro / 🟡 aviso / 🔵 info), erros primeiro, agrupado por camada.

NÃO faz: nada de escrita. Não move, renomeia, apaga, nem edita arquivo algum.
Não commita. As correções (sempre mecânicas, item a item, após confirmação)
são aplicadas pela skill `auditoria_nexus` via a ferramenta de edição do Claude,
usando as dicas de correção (campo `fix`) que este script emite — é por isso que
o motor é puro leitor: a garantia de "nunca alterar sem confirmação" mora aqui.

DECISÕES ANCORADAS NO SISTEMA REAL (não no idealizado do CLAUDE.md):
  - `.md` em Materiais só é erro dentro de `Periodo0N/`; `MOC_*.md` de espaço
    (ex.: Administrativo/MOC_Adm.md) é legítimo.
  - Nome de artefato VC NÃO é validado contra lista fixa: um arquivo VC só é
    "fora do padrão" se também não estiver referenciado no MOC da disciplina
    (simulado_VC01_v2.html e fluxograma_VC02.html são reais e legítimos).
  - Wikilinks resolvem por BASENAME (estilo Obsidian), tolerando os dois estilos
    em uso (raiz-do-vault e `../`) e aliases `[[alvo|texto]]`.
  - O esquema de frontmatter válido é o REALMENTE observado (família `moc_*`),
    não o bloco do CLAUDE.md — que está defasado e é sinalizado como aviso.

USO:
    python3 auditoria.py                # varredura completa, todas as camadas
    python3 auditoria.py --rapido       # só camada 4 (MOC) + camada 5 (git)
    python3 auditoria.py --camada 4     # uma camada específica (1..5)
    python3 auditoria.py APHR           # escopo a uma disciplina (sigla)

Saída: relatório em texto + código de saída (0 = sem 🔴; 1 = há 🔴).
"""

import argparse
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, date

# ── Constantes do sistema ────────────────────────────────────────────────────

BINARIOS = (".pdf", ".pptx", ".png", ".jpeg", ".jpg", ".docx", ".xlsx")
OBSIDIAN = "Nexus_Obsidian"
MATERIAIS = "Nexus_Materiais"
RESERVADOS = (OBSIDIAN, MATERIAIS)

# tipos de frontmatter realmente observados no sistema (06/2026)
TIPOS_VALIDOS = {
    "moc_geral", "moc_disciplina", "moc_pensamentos", "moc_administrativo",
    "disciplinar", "resumo", "pontos_chave", "revisao_prova",
    "apresentacao", "pensamento", "audio_prova", "simulado", "flashcard",
}
TIPOS_MOC = {"moc_geral", "moc_disciplina", "moc_pensamentos", "moc_administrativo"}
# tipos que exigem versao + disciplina + sigla
TIPOS_ESTUDO = {"resumo", "pontos_chave", "revisao_prova", "apresentacao"}

DATA_RE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
ANOTACAO_NOME_RE = re.compile(r"^\d{4}-\d{2}-\d{2}_[A-Z]\d+_anotacao-\d+\.md$")
PREFIXO_DISC_RE = re.compile(r"^\d{2}_[A-Z]+$")
KEBAB_RE = re.compile(r"^[0-9a-z]+(?:[-_][0-9a-z]+)*$")  # tolera _ de prefixo numérico
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")
PK_COUNT_RE = re.compile(r"(\d+)\s*PK")
DESCONTO_RE = re.compile(r"-(\d+),(\d+)")

SEV_ERRO, SEV_AVISO, SEV_INFO = "🔴", "🟡", "🔵"
SEV_ORDEM = {SEV_ERRO: 0, SEV_AVISO: 1, SEV_INFO: 2}


class Finding:
    def __init__(self, sev, camada, msg, alvo="", fix=""):
        self.sev = sev
        self.camada = camada
        self.msg = msg
        self.alvo = alvo
        self.fix = fix


findings = []


def add(sev, camada, msg, alvo="", fix=""):
    findings.append(Finding(sev, camada, msg, alvo, fix))


# ── Utilidades ───────────────────────────────────────────────────────────────

def repo_root():
    # .../.claude/skills/auditoria_nexus/scripts/auditoria.py → 4 níveis acima
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.abspath(os.path.join(here, "..", "..", "..", ".."))


def git_tracked(root):
    try:
        out = subprocess.run(["git", "-C", root, "ls-files"],
                             capture_output=True, text=True, timeout=30)
        return set(out.stdout.splitlines())
    except Exception:
        return set()


def walk_files(root, scope_dirs):
    for base in scope_dirs:
        full = os.path.join(root, base)
        if not os.path.isdir(full):
            continue
        for dirpath, dirnames, filenames in os.walk(full):
            if ".obsidian" in dirpath or "/.git" in dirpath:
                continue
            dirnames[:] = [d for d in dirnames if d not in (".obsidian", ".git")]
            for fn in filenames:
                yield os.path.join(dirpath, fn)


def rel(root, path):
    return os.path.relpath(path, root)


def parse_frontmatter(path):
    """Retorna dict do bloco YAML simples no topo, ou None se ausente."""
    try:
        with open(path, encoding="utf-8") as f:
            first = f.readline()
            if first.strip() != "---":
                return None
            data, raw = {}, []
            for line in f:
                if line.strip() == "---":
                    break
                raw.append(line)
            for line in raw:
                if ":" in line and not line.startswith(" "):
                    k, _, v = line.partition(":")
                    data[k.strip()] = v.strip()
            return data
    except Exception:
        return None


def parse_data(s):
    try:
        return datetime.strptime(s, "%d/%m/%Y").date()
    except Exception:
        return None


def read_text(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""


# ── CAMADA 1 — Estrutura física ──────────────────────────────────────────────

def camada1(root, tracked):
    C = "1 · Estrutura física"

    for path in walk_files(root, [OBSIDIAN]):
        r = rel(root, path)
        if path.lower().endswith(BINARIOS):
            add(SEV_ERRO, C, f"Binário dentro do vault Obsidian (deveria estar em {MATERIAIS}/)", r)

    for path in walk_files(root, [MATERIAIS]):
        r = rel(root, path)
        fn = os.path.basename(path)
        if fn.endswith(".md"):
            # legítimo: MOC de espaço fora de Periodo0N (ex.: Administrativo/MOC_Adm.md)
            dentro_periodo = re.search(r"Periodo\d{2}", r) is not None
            if dentro_periodo:
                add(SEV_ERRO, C, f".md dentro de material de disciplina (estudo vai no vault Obsidian)", r)
            # MOC_*.md de espaço → ok, silêncio
        if fn.startswith("~$") and fn.lower().endswith(".pptx"):
            add(SEV_INFO, C, "Lock temporário do Office (gitignorado) — fechar o arquivo no PowerPoint", r)

    # Nome reservado aninhado (árvore-fantasma do vault dentro de Materiais ou vice-versa)
    for base in RESERVADOS:
        full = os.path.join(root, base)
        for dirpath, dirnames, _ in os.walk(full):
            for d in dirnames:
                if d in RESERVADOS:
                    add(SEV_ERRO, C,
                        f"Pasta de topo reservada '{d}' aninhada onde não devia (provável comando rodado no diretório errado)",
                        rel(root, os.path.join(dirpath, d)))

    # Pastas vazias
    for base in [OBSIDIAN, MATERIAIS]:
        full = os.path.join(root, base)
        for dirpath, dirnames, filenames in os.walk(full):
            if ".obsidian" in dirpath:
                continue
            if not dirnames and not [f for f in filenames if f != ".DS_Store"]:
                add(SEV_AVISO, C, "Pasta vazia (o Nexus não mantém pastas vazias)", rel(root, dirpath))

    # _modelos alterado (working tree)
    try:
        out = subprocess.run(["git", "-C", root, "status", "--porcelain", "_modelos"],
                             capture_output=True, text=True, timeout=30)
        for line in out.stdout.splitlines():
            add(SEV_ERRO, C, "Template institucional em _modelos/ com alteração não commitada (nunca alterar)",
                line[3:].strip())
    except Exception:
        pass

    # Nomenclatura de pastas de disciplina e de anotações
    for periodo in _periodos(root):
        for disc in sorted(os.listdir(periodo)):
            p = os.path.join(periodo, disc)
            if os.path.isdir(p) and not disc.startswith(".") and not PREFIXO_DISC_RE.match(disc):
                add(SEV_AVISO, C, "Pasta de disciplina fora do padrão '0N_SIGLA'", rel(root, p))
    anot = os.path.join(root, OBSIDIAN, "Disciplinar", "anotacoes")
    if os.path.isdir(anot):
        for fn in os.listdir(anot):
            if fn.endswith(".md") and not ANOTACAO_NOME_RE.match(fn):
                add(SEV_AVISO, C, "Anotação fora do padrão 'AAAA-MM-DD_CODIGO_anotacao-NNN.md'",
                    rel(root, os.path.join(anot, fn)))


def _periodos(root):
    base = os.path.join(root, OBSIDIAN)
    for d in sorted(os.listdir(base)) if os.path.isdir(base) else []:
        if re.match(r"^Periodo\d{2}$", d):
            yield os.path.join(base, d)


# ── CAMADA 2 — Frontmatter ───────────────────────────────────────────────────

def camada2(root):
    C = "2 · Frontmatter"
    for path in walk_files(root, [OBSIDIAN, MATERIAIS]):
        if not path.endswith(".md"):
            continue
        r = rel(root, path)
        fm = parse_frontmatter(path)
        if fm is None:
            add(SEV_ERRO, C, "Sem bloco de frontmatter YAML no topo", r,
                fix="inserir cabeçalho padrão Nexus")
            continue
        tipo = fm.get("tipo", "")
        if not tipo:
            add(SEV_ERRO, C, "Frontmatter sem campo 'tipo'", r)
        elif tipo not in TIPOS_VALIDOS:
            add(SEV_AVISO, C, f"tipo '{tipo}' não reconhecido pelo sistema", r)

        for campo in ("sistema", "criado_em", "atualizado_em"):
            if campo not in fm:
                add(SEV_AVISO, C, f"Frontmatter sem campo '{campo}'", r,
                    fix=f"adicionar {campo}")
        if tipo in TIPOS_ESTUDO:
            for campo in ("disciplina", "sigla", "versao"):
                if campo not in fm:
                    add(SEV_AVISO, C, f"tipo '{tipo}' deveria ter '{campo}'", r)

        c, a = parse_data(fm.get("criado_em", "")), parse_data(fm.get("atualizado_em", ""))
        for campo in ("criado_em", "atualizado_em"):
            v = fm.get(campo)
            if v and not DATA_RE.match(v):
                add(SEV_AVISO, C, f"{campo}='{v}' fora do formato DD/MM/AAAA", r)
        if c and a and a < c:
            add(SEV_ERRO, C, f"atualizado_em ({fm['atualizado_em']}) anterior a criado_em ({fm['criado_em']})", r)
        if a and a > date.today():
            add(SEV_AVISO, C, f"atualizado_em ({fm['atualizado_em']}) está no futuro", r)


# ── CAMADA 3 — Links ─────────────────────────────────────────────────────────

def build_basename_index(root):
    idx = defaultdict(list)
    for path in walk_files(root, [OBSIDIAN]):
        base = os.path.splitext(os.path.basename(path))[0]
        idx[base].append(rel(root, path))
    return idx


def resolve_link(target, idx):
    """Estilo Obsidian: corta alias após |, âncora após #, usa o basename."""
    t = target.split("|")[0].split("#")[0].strip()
    if not t:
        return None  # link só de âncora interna
    base = os.path.splitext(os.path.basename(t))[0]
    return idx.get(base)


def camada3(root, idx):
    C = "3 · Links"
    for path in walk_files(root, [OBSIDIAN]):
        if not path.endswith(".md"):
            continue
        r = rel(root, path)
        text = read_text(path)
        for m in WIKILINK_RE.finditer(text):
            target = m.group(1)
            hits = resolve_link(target, idx)
            if hits is None:
                continue
            if not hits:
                ctx = target.split("|")[0]
                if "pendente" in target.lower():
                    continue
                add(SEV_AVISO, C, f"Wikilink quebrado [[{ctx}]] (nenhum arquivo com esse nome)", r)
            elif len(hits) > 1:
                ctx = target.split("|")[0].split("#")[0]
                if "/" not in ctx:  # ambíguo só importa se o link não desambiguou por caminho
                    add(SEV_INFO, C, f"Wikilink [[{ctx}]] ambíguo: {len(hits)} arquivos com esse nome", r)


# ── CAMADA 4 — MOC ↔ realidade ───────────────────────────────────────────────

def camada4(root, idx, scope):
    C = "4 · MOC ↔ realidade"

    # 4a — MOCs de disciplina: órfãos e fantasmas em pontos_chave + scaffold
    for periodo in _periodos(root):
        for disc in sorted(os.listdir(periodo)):
            dpath = os.path.join(periodo, disc)
            if not os.path.isdir(dpath) or not PREFIXO_DISC_RE.match(disc):
                continue
            sigla = disc.split("_", 1)[1]
            if scope and sigla.upper() != scope.upper():
                continue
            moc = os.path.join(dpath, f"MOC_{sigla}.md")
            resumo = os.path.join(dpath, f"resumo_{sigla}.md")
            if not os.path.isfile(moc):
                add(SEV_ERRO, C, f"Disciplina {sigla} sem MOC_{sigla}.md", rel(root, dpath))
                continue
            if not os.path.isfile(resumo):
                add(SEV_AVISO, C, f"Disciplina {sigla} sem resumo_{sigla}.md", rel(root, dpath))

            moc_text = read_text(moc)
            referenciados = set()
            for m in WIKILINK_RE.finditer(moc_text):
                base = os.path.splitext(os.path.basename(m.group(1).split("|")[0].split("#")[0]))[0]
                referenciados.add(base)
            # também conta menções a arquivos em crase (`...html`, `...txt`)
            for m in re.finditer(r"`([^`]+\.(?:html|txt|md))`", moc_text):
                referenciados.add(os.path.splitext(os.path.basename(m.group(1)))[0])

            # pontos-chave órfãos (existem mas não no MOC)
            pk_dir = os.path.join(dpath, "pontos_chave")
            for dirpath, _, files in os.walk(pk_dir):
                for fn in files:
                    if fn.endswith(".md"):
                        base = os.path.splitext(fn)[0]
                        if base not in referenciados:
                            add(SEV_AVISO, C, f"Ponto-chave órfão em {sigla} (existe, mas não está no MOC)",
                                rel(root, os.path.join(dirpath, fn)),
                                fix=f"adicionar linha no MOC_{sigla}.md")

            # artefatos VC órfãos (arquivos VC fora do MOC = nomenclatura via MOC, não lista fixa)
            for dirpath, _, files in os.walk(dpath):
                if os.path.basename(dirpath).startswith("VC"):
                    for fn in files:
                        if fn == ".DS_Store":
                            continue
                        base = os.path.splitext(fn)[0]
                        if base not in referenciados:
                            add(SEV_AVISO, C, f"Artefato VC não referenciado no MOC de {sigla}",
                                rel(root, os.path.join(dirpath, fn)),
                                fix=f"referenciar em MOC_{sigla}.md ou confirmar como descartável")

            # fantasmas: links do MOC que não resolvem
            for m in WIKILINK_RE.finditer(moc_text):
                hits = resolve_link(m.group(1), idx)
                if hits == []:
                    add(SEV_AVISO, C, f"MOC de {sigla} aponta para arquivo inexistente: [[{m.group(1).split('|')[0]}]]",
                        rel(root, moc))

    # 4b — MOC_CFO: links resolvem + contagem de PK na prosa
    if not scope:
        cfo = os.path.join(root, OBSIDIAN, "MOC_CFO.md")
        if os.path.isfile(cfo):
            for line in read_text(cfo).splitlines():
                links = WIKILINK_RE.findall(line)
                # status pode declarar a contagem por documento (LBI: 6+5+6+4+5) → somar tudo
                pks = [int(x) for x in PK_COUNT_RE.findall(line)]
                for lk in links:
                    hits = resolve_link(lk, idx)
                    if hits == []:
                        add(SEV_AVISO, C, f"MOC_CFO aponta para MOC inexistente: [[{lk.split('|')[0]}]]",
                            "Nexus_Obsidian/MOC_CFO.md")
                    if pks and hits:
                        # casa a contagem ao primeiro link de disciplina da linha
                        mdir = os.path.dirname(os.path.join(root, hits[0]))
                        pk_dir = os.path.join(mdir, "pontos_chave")
                        real = sum(1 for dp, _, fs in os.walk(pk_dir) for f in fs if f.endswith(".md"))
                        declarado = sum(pks)
                        if real and declarado != real:
                            add(SEV_AVISO, C,
                                f"MOC_CFO declara {declarado} PK mas há {real} em {os.path.basename(mdir)} (status em prosa — revisar à mão)",
                                "Nexus_Obsidian/MOC_CFO.md")

    # 4c — Disciplinar: pareamento, recálculo de descontos, aritmética da nota
    if not scope or scope.upper() in ("DISC", "DISCIPLINAR"):
        camada4_disciplinar(root, C)


def camada4_disciplinar(root, C):
    disc = os.path.join(root, OBSIDIAN, "Disciplinar")
    anot_md = os.path.join(disc, "anotacoes")
    anot_png = os.path.join(root, MATERIAIS, "Disciplinar", "anotacoes")
    moc = os.path.join(disc, "MOC_Disciplinar.md")

    md_bases, png_bases = set(), set()
    if os.path.isdir(anot_md):
        md_bases = {os.path.splitext(f)[0] for f in os.listdir(anot_md) if f.endswith(".md")}
    if os.path.isdir(anot_png):
        png_bases = {os.path.splitext(f)[0] for f in os.listdir(anot_png) if f.endswith(".png")}
    for b in md_bases - png_bases:
        add(SEV_AVISO, C, "Anotação registrada sem print original (.png) em Materiais", b)
    for b in png_bases - md_bases:
        add(SEV_AVISO, C, "Print de anotação sem registro (.md) no vault", b)

    if not os.path.isfile(moc):
        return
    text = read_text(moc)

    # IDs de anotação citados na tabela do MOC vs arquivos reais
    ids_moc = set(re.findall(r"anotacao-(\d+)", text))
    ids_arq = set(re.findall(r"anotacao-(\d+)", " ".join(md_bases)))
    for i in ids_arq - ids_moc:
        add(SEV_ERRO, C, f"Anotação #{i} existe mas não está na tabela do MOC_Disciplinar",
            "Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md", fix="adicionar linha na tabela")
    for i in ids_moc - ids_arq:
        add(SEV_AVISO, C, f"MOC_Disciplinar cita anotação #{i} sem arquivo correspondente",
            "Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md")

    # Recálculo da soma de descontos a partir das linhas da tabela (coluna Desconto)
    soma = 0
    for line in text.splitlines():
        if line.startswith("|") and "anotacao-" in line:
            m = DESCONTO_RE.search(line)
            if m:
                soma += int(m.group(1)) * 10 + int(m.group(2))  # décimos, sem float
    soma_str = f"{soma // 10},{soma % 10}"

    mtot = re.search(r"[Tt]otal de descontos.*?(\d+),(\d+)", text)
    if mtot:
        declarado = int(mtot.group(1)) * 10 + int(mtot.group(2))
        if declarado != soma:
            decl_str = f"{declarado // 10},{declarado % 10}"
            add(SEV_ERRO, C,
                f"Total de descontos no MOC_Disciplinar diz {decl_str} mas as anotações somam {soma_str}",
                "Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md",
                fix=f"corrigir total para {soma_str}")

    # Aritmética da nota: base − total = nota
    mnota = re.search(r"(\d+),(\d+)\s*[−-]\s*(\d+),(\d+)\s*=\s*(\d+),(\d+)", text)
    if mnota:
        base = int(mnota.group(1)) * 10 + int(mnota.group(2))
        menos = int(mnota.group(3)) * 10 + int(mnota.group(4))
        res = int(mnota.group(5)) * 10 + int(mnota.group(6))
        if base - menos != res:
            esperado = f"{(base - menos)//10},{(base - menos)%10}"
            add(SEV_ERRO, C, f"Aritmética da nota incorreta no MOC_Disciplinar (deveria dar {esperado})",
                "Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md", fix=f"corrigir resultado para {esperado}")
        elif menos != soma:
            add(SEV_AVISO, C,
                f"Linha da nota usa total {menos//10},{menos%10} divergente da soma real {soma_str}",
                "Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md")


# ── CAMADA 5 — Git / sync ────────────────────────────────────────────────────

def camada5(root):
    C = "5 · Git / sync"

    def git(*args):
        try:
            return subprocess.run(["git", "-C", root, *args],
                                  capture_output=True, text=True, timeout=30).stdout
        except Exception:
            return ""

    dirty = [l for l in git("status", "--porcelain").splitlines()]
    if dirty:
        add(SEV_AVISO, C, f"Working tree com {len(dirty)} alteração(ões) não commitada(s) "
                          f"(todo fluxo deveria terminar com commit + push)", "")

    log7 = git("log", "--since=7 days ago", "--oneline").splitlines()
    sync_n = sum(1 for l in log7 if re.search(r"\b[0-9a-f]+ sync:", l))
    if sync_n > 3:
        add(SEV_AVISO, C,
            f"{sync_n} commits 'sync:' nos últimos 7 dias — a rede de segurança está cobrindo "
            f"fluxos que não fecharam com commit manual",
            "")

    # Divergência com origin/main
    git("fetch", "origin", "main", "--quiet")
    ahead = git("rev-list", "--count", "origin/main..HEAD").strip()
    behind = git("rev-list", "--count", "HEAD..origin/main").strip()
    if ahead and ahead != "0":
        add(SEV_AVISO, C, f"{ahead} commit(s) à frente de origin/main (push pendente)", "")
    if behind and behind != "0":
        add(SEV_INFO, C, f"{behind} commit(s) atrás de origin/main (pull pendente)", "")

    # sync.log: só as tags do próprio script; fatal de rede é info
    logf = os.path.join(root, ".claude", "hooks", "sync.log")
    if os.path.isfile(logf):
        linhas = read_text(logf).splitlines()[-60:]
        for l in linhas:
            if "CONFLITO:" in l:
                add(SEV_ERRO, C, f"sync.log registrou conflito: {l.strip()[:120]}", "")
            elif re.search(r"\bERRO:", l):
                add(SEV_AVISO, C, f"sync.log registrou erro: {l.strip()[:120]}", "")
            elif "AVISO:" in l and "rebase em andamento" in l:
                add(SEV_AVISO, C, f"sync.log: {l.strip()[:120]}", "")
        fatais = sum(1 for l in linhas if l.startswith("fatal:"))
        if fatais:
            add(SEV_INFO, C, f"{fatais} falha(s) de rede recentes no sync.log (sem conexão na hora) — sem ação", "")


# ── Relatório ────────────────────────────────────────────────────────────────

def relatorio():
    por_camada = defaultdict(list)
    for f in findings:
        por_camada[f.camada].append(f)

    n = {SEV_ERRO: 0, SEV_AVISO: 0, SEV_INFO: 0}
    for f in findings:
        n[f.sev] += 1

    print("\n" + "=" * 70)
    print(" AUDITORIA NEXUS — varredura somente-leitura")
    print("=" * 70)
    print(f" {SEV_ERRO} {n[SEV_ERRO]} erro(s)   {SEV_AVISO} {n[SEV_AVISO]} aviso(s)   {SEV_INFO} {n[SEV_INFO]} info")
    print("=" * 70)

    if not findings:
        print("\n✅ Nenhuma inconsistência encontrada. Sistema íntegro.\n")
        return

    for camada in sorted(por_camada):
        itens = sorted(por_camada[camada], key=lambda f: SEV_ORDEM[f.sev])
        print(f"\n── Camada {camada} " + "─" * (max(0, 56 - len(camada))))
        for f in itens:
            alvo = f"  → {f.alvo}" if f.alvo else ""
            print(f"  {f.sev} {f.msg}{alvo}")
            if f.fix:
                print(f"      ✎ correção possível: {f.fix}")

    print("\n" + "=" * 70)
    print(f" Resumo: {SEV_ERRO} {n[SEV_ERRO]}  ·  {SEV_AVISO} {n[SEV_AVISO]}  ·  {SEV_INFO} {n[SEV_INFO]}")
    if n[SEV_ERRO] or n[SEV_AVISO]:
        print(" Há itens com correção mecânica disponível (marcados com ✎).")
        print(" A correção é feita item a item, só após sua confirmação. Auditoria não commita.")
    print("=" * 70 + "\n")


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser(description="Auditoria somente-leitura do Nexus.")
    ap.add_argument("escopo", nargs="?", default=None,
                    help="sigla da disciplina para limitar o escopo (ex.: APHR)")
    ap.add_argument("--rapido", action="store_true",
                    help="só camada 4 (MOC) + camada 5 (git)")
    ap.add_argument("--camada", type=int, choices=range(1, 6),
                    help="roda apenas a camada indicada (1..5)")
    args = ap.parse_args()

    root = repo_root()
    if not os.path.isdir(os.path.join(root, OBSIDIAN)):
        print(f"ERRO: não encontrei {OBSIDIAN}/ em {root}", file=sys.stderr)
        sys.exit(2)

    if args.camada:
        camadas = {args.camada}
    elif args.rapido:
        camadas = {4, 5}
    else:
        camadas = {1, 2, 3, 4, 5}

    tracked = git_tracked(root)
    idx = build_basename_index(root) if camadas & {3, 4} else {}

    if 1 in camadas and not args.escopo:
        camada1(root, tracked)
    if 2 in camadas and not args.escopo:
        camada2(root)
    if 3 in camadas and not args.escopo:
        camada3(root, idx)
    if 4 in camadas:
        camada4(root, idx, args.escopo)
    if 5 in camadas and not args.escopo:
        camada5(root)

    relatorio()
    sys.exit(1 if any(f.sev == SEV_ERRO for f in findings) else 0)


if __name__ == "__main__":
    main()
