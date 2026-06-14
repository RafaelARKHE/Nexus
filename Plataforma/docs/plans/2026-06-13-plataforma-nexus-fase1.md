# Plataforma Nexus — Plano de Implementação (Fase 1, Plano 1)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir o núcleo da Plataforma Nexus — um gerador Python que varre o vault e produz um `index.html` estático e autocontido (Radar + Mapa de Conhecimento + listas de Fluxogramas/Legislação/Pensamentos, com conteúdo `.md` renderizado dentro do app), mais a skill `atualizar_plataforma` que regenera tudo sob demanda.

**Architecture:** Um script Python (stdlib pura, zero dependências externas) varre `Nexus_Obsidian/`, lê o frontmatter dos `.md`, e monta um único `Plataforma/index.html` com TODOS os dados, CSS, JS e o conteúdo dos `.md` embutidos inline (`window.NEXUS_DATA = {...}`) — porque o WebKit do iOS bloqueia `fetch()` de `file://`. Os dados do Radar (aulas da semana, VCs futuras) vêm do Google Calendar via MCP, consultados pela skill `atualizar_plataforma` (não pelo script) e passados ao gerador como um `radar.json`. A fonte da verdade continua sendo os `.md` versionados; a plataforma é só leitura.

**Tech Stack:** Python 3.13 (stdlib: `unittest`, `pathlib`, `json`, `re`, `html`, `argparse`), HTML/CSS/JS vanilla (tema escuro), `marked.min.js` vendorizado e embutido para render de Markdown. Sem npm, sem servidor, sem pyyaml, sem pytest.

**Escopo e decisões herdadas do spec** (`Plataforma/docs/2026-06-13-plataforma-nexus-design.md`):
- Este Plano 1 cobre: gerador + app estático + skill `atualizar_plataforma` (regeneração **manual completa**). Já entrega plataforma funcional.
- O Plano 2 (follow-up, fora deste documento) cobre a integração automática nas 6 skills existentes (`leitura_aprofundada`, `pontos_chave`, `resumo_geral`, `qis_para_calendario`, `revisao_prova`, `consolidar`).
- **Simplificação por YAGNI:** não há atualização "incremental parcial" do índice. O gerador sempre faz varredura completa (o vault tem ~130 arquivos, parse instantâneo). O que o Plano 2 acrescenta é apenas o *gatilho automático*, chamando o mesmo gerador.
- Disciplinar fica **fora** da plataforma (já coberto pelo dashboard da ABM).

---

## Estrutura de arquivos

```
Nexus/Plataforma/
├── docs/                              # specs e planos (já existe)
├── config/
│   └── disciplinas.json               # lista mestre período→disciplinas (p/ cards "sem material")
├── gerador/
│   ├── __init__.py
│   ├── frontmatter.py                 # parser de frontmatter YAML-simples (stdlib)
│   ├── varredura.py                   # vault → dict de índice (disciplinas, pensamentos, etc.)
│   └── montar.py                      # índice + radar + assets → string do index.html
├── gerar_indice.py                    # CLI: amarra varredura + montar, escreve index.html
├── app/
│   ├── template.html                  # casca HTML com marcadores {{...}}
│   ├── estilo.css                     # tema escuro, sidebar
│   ├── app.js                         # render de Radar/Mapa/disciplina/listas a partir de NEXUS_DATA
│   └── vendor/
│       └── marked.min.js              # renderizador Markdown vendorizado
├── tests/
│   ├── __init__.py
│   ├── fixtures/vault/                # vault falso mínimo p/ testes de varredura
│   ├── test_frontmatter.py
│   ├── test_varredura.py
│   └── test_montar.py
└── index.html                         # GERADO (commitado — é o que sincroniza via Drive/Git)
```

Responsabilidades:
- `frontmatter.py` — só parsing de frontmatter. Entrada: texto do arquivo. Saída: `(dict_meta, corpo)`.
- `varredura.py` — só conhecimento da estrutura do vault. Entrada: caminho do vault + config. Saída: dict de índice serializável.
- `montar.py` — só montagem do HTML. Entrada: dict de índice + radar + caminhos dos assets. Saída: string HTML autocontida.
- `gerar_indice.py` — CLI/orquestração. Lê args, chama varredura e montar, escreve arquivo.
- `app/*` — fontes do front-end; o gerador as **inlina** no `index.html` (nada é carregado via `src`/`href`/`fetch` em runtime).

---

## Notas para quem implementa (domínio Nexus)

- **Raiz do projeto:** `~/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus`. Todos os comandos rodam a partir dela salvo indicação contrária.
- **Frontmatter padrão Nexus:** bloco entre `---` no topo do `.md`. Campos relevantes: `tipo`, `disciplina`, `sigla`, `periodo`, `assunto`, `prefixo`, `versao`, `atualizado_em`, `criado_em`, `arquivo_origem`. Valores são `chave: valor` simples; listas aparecem só como `[]` (vazias). Um parser próprio resolve — **não** instalar pyyaml.
- **Estrutura de disciplina:** `Nexus_Obsidian/Periodo0N/NN_SIGLA/` contém `resumo_SIGLA.md`, `MOC_SIGLA.md`, `pontos_chave/<NN_Tema>/<NN_assunto>.md` e pastas `VC0X/` com `revisao_VC0X.md`, `audio_VC0X.txt`, `simulado_VC0X.html`, `flashcard_VC0X.html`, `fluxograma_VC0X.html` (nem todos sempre presentes). Pode haver variações como `simulado_VC01_v2.html` — pegar a versão de maior sufixo quando houver `_vN`.
- **Pensamentos:** `Nexus_Obsidian/Pensamento/AAAA-MM-DD_tema.md` (hoje só existe `MOC_Pensamentos.md` — a varredura deve lidar com zero pensamentos sem quebrar).
- **Git:** trabalhar sempre na `main`. Cada Task termina em commit. Prefixo `sync:` é proibido (reservado ao hook). Não fazer `push` em cada task — o push final fica na Task de verificação (ou quando o executor decidir), para não poluir o remoto a cada passo.
- **Verificação visual:** o front-end não tem testes automatizados (caráter visual). A garantia é abrir `index.html` no navegador (Mac e iPhone). O gerador, esse sim, é testado.

---

## Task 1: Esqueleto de pacote + config de disciplinas

**Files:**
- Create: `Plataforma/gerador/__init__.py` (vazio)
- Create: `Plataforma/tests/__init__.py` (vazio)
- Create: `Plataforma/config/disciplinas.json`
- Create: `Plataforma/.gitignore`

- [ ] **Step 1: Criar os `__init__.py` vazios**

```bash
cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus"
mkdir -p Plataforma/gerador Plataforma/tests/fixtures Plataforma/config Plataforma/app/vendor
touch Plataforma/gerador/__init__.py Plataforma/tests/__init__.py
```

- [ ] **Step 2: Criar `Plataforma/config/disciplinas.json`** (lista mestre — alimenta os cards "sem material")

```json
{
  "Periodo01": {
    "rotulo": "1º Período",
    "disciplinas": [
      { "sigla": "TFM",    "nome": "TFM I" },
      { "sigla": "NAT",    "nome": "Natação Utilitária" },
      { "sigla": "DPIBM",  "nome": "DPIBM" },
      { "sigla": "HCBMPA", "nome": "História do CBMPA" },
      { "sigla": "ETICA",  "nome": "Ética e Cidadania" },
      { "sigla": "TLTI",   "nome": "Telecomunicações e TI" },
      { "sigla": "IM",     "nome": "Instrução Militar I" },
      { "sigla": "ANFI",   "nome": "Anatomia e Fisiologia" },
      { "sigla": "APHR",   "nome": "APH e Resgate I" },
      { "sigla": "DH",     "nome": "Direitos Humanos" },
      { "sigla": "DC",     "nome": "Direito Constitucional" },
      { "sigla": "DA",     "nome": "Direito Administrativo I" },
      { "sigla": "LBI",    "nome": "Legislação Básica Institucional" },
      { "sigla": "FCIU",   "nome": "Fundamentos do Combate ao Incêndio Urbano" },
      { "sigla": "FSALT",  "nome": "Fundamentos de Salvamento Terrestre" },
      { "sigla": "FSV",    "nome": "Fundamentos de Salvamento Veicular" },
      { "sigla": "FSAL",   "nome": "Fundamentos de Salvamento em Altura" },
      { "sigla": "FSAQ",   "nome": "Fundamentos de Salvamento Aquático" },
      { "sigla": "OAC",    "nome": "OAC" }
    ]
  }
}
```

- [ ] **Step 3: Criar `Plataforma/.gitignore`** (ignorar artefatos de brainstorm e build temporário do radar)

```gitignore
# dados temporários do radar (gerados pela skill a cada execução)
radar.json
# artefatos do companion de brainstorm
.superpowers/
```

> Nota: `index.html` **NÃO** é ignorado — ele é o produto e precisa sincronizar via Git/Drive.

- [ ] **Step 4: Commit**

```bash
git add Plataforma/gerador/__init__.py Plataforma/tests/__init__.py Plataforma/config/disciplinas.json Plataforma/.gitignore
git commit -m "feat(plataforma): esqueleto de pacote e config de disciplinas

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 2: Parser de frontmatter

**Files:**
- Create: `Plataforma/gerador/frontmatter.py`
- Test: `Plataforma/tests/test_frontmatter.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# Plataforma/tests/test_frontmatter.py
import unittest
from Plataforma.gerador.frontmatter import parse_frontmatter


class TestFrontmatter(unittest.TestCase):
    def test_extrai_campos_e_corpo(self):
        texto = (
            "---\n"
            "sistema: Nexus\n"
            "tipo: resumo\n"
            "disciplina: Legislação Básica Institucional\n"
            "sigla: LBI\n"
            "versao: 5.0\n"
            "atualizado_em: 06/06/2026\n"
            "pensamentos_relacionados: []\n"
            "---\n"
            "\n"
            "# Resumo — LBI\n"
            "Conteúdo aqui.\n"
        )
        meta, corpo = parse_frontmatter(texto)
        self.assertEqual(meta["tipo"], "resumo")
        self.assertEqual(meta["sigla"], "LBI")
        self.assertEqual(meta["versao"], "5.0")
        self.assertEqual(meta["pensamentos_relacionados"], [])
        self.assertEqual(corpo.strip(), "# Resumo — LBI\nConteúdo aqui.")

    def test_sem_frontmatter_retorna_meta_vazio(self):
        texto = "# Só um título\nsem frontmatter\n"
        meta, corpo = parse_frontmatter(texto)
        self.assertEqual(meta, {})
        self.assertEqual(corpo, texto)

    def test_remove_aspas_dos_valores(self):
        texto = '---\ntema: "Hierarquia e Disciplina"\n---\ncorpo\n'
        meta, _ = parse_frontmatter(texto)
        self.assertEqual(meta["tema"], "Hierarquia e Disciplina")
```

- [ ] **Step 2: Rodar o teste e confirmar que falha**

Run: `cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus" && python3 -m unittest Plataforma.tests.test_frontmatter -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'Plataforma.gerador.frontmatter'`

- [ ] **Step 3: Implementar `frontmatter.py`**

```python
# Plataforma/gerador/frontmatter.py
"""Parser mínimo de frontmatter no padrão Nexus (YAML simples, stdlib pura)."""
from __future__ import annotations


def parse_frontmatter(texto: str) -> tuple[dict, str]:
    """Separa o bloco de frontmatter (entre '---') do corpo.

    Retorna (meta, corpo). Se não houver frontmatter, meta={} e corpo=texto original.
    Só trata 'chave: valor' simples e listas vazias '[]' — suficiente para o Nexus.
    """
    if not texto.startswith("---"):
        return {}, texto

    linhas = texto.splitlines()
    # primeira linha é '---'; procurar o fechamento
    fim = None
    for i in range(1, len(linhas)):
        if linhas[i].strip() == "---":
            fim = i
            break
    if fim is None:
        return {}, texto

    meta: dict = {}
    for linha in linhas[1:fim]:
        if not linha.strip() or ":" not in linha:
            continue
        chave, _, valor = linha.partition(":")
        chave = chave.strip()
        valor = valor.strip()
        if valor == "[]":
            meta[chave] = []
        else:
            if len(valor) >= 2 and valor[0] in "\"'" and valor[-1] == valor[0]:
                valor = valor[1:-1]
            meta[chave] = valor

    corpo = "\n".join(linhas[fim + 1:])
    return meta, corpo
```

- [ ] **Step 4: Rodar o teste e confirmar que passa**

Run: `python3 -m unittest Plataforma.tests.test_frontmatter -v`
Expected: PASS (3 testes OK)

- [ ] **Step 5: Commit**

```bash
git add Plataforma/gerador/frontmatter.py Plataforma/tests/test_frontmatter.py
git commit -m "feat(plataforma): parser de frontmatter (stdlib)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 3: Fixture de vault falso para testes de varredura

**Files:**
- Create: `Plataforma/tests/fixtures/vault/Periodo01/03_LBI/resumo_LBI.md`
- Create: `Plataforma/tests/fixtures/vault/Periodo01/03_LBI/pontos_chave/01_Lei-9161-2021/01_hierarquia.md`
- Create: `Plataforma/tests/fixtures/vault/Periodo01/03_LBI/VC01/revisao_VC01.md`
- Create: `Plataforma/tests/fixtures/vault/Periodo01/03_LBI/VC01/simulado_VC01.html`
- Create: `Plataforma/tests/fixtures/vault/Periodo01/03_LBI/VC01/simulado_VC01_v2.html`
- Create: `Plataforma/tests/fixtures/vault/Pensamento/2026-06-10_proporcionalidade.md`
- Create: `Plataforma/tests/fixtures/config/disciplinas.json`

- [ ] **Step 1: Criar o resumo de fixture**

```markdown
---
sistema: Nexus
tipo: resumo
disciplina: Legislação Básica Institucional
sigla: LBI
periodo: Periodo01
versao: 5.0
atualizado_em: 06/06/2026
---

# Resumo — LBI
Texto do resumo de teste.
```

- [ ] **Step 2: Criar o ponto-chave de fixture**

```markdown
---
sistema: Nexus
tipo: pontos_chave
disciplina: Legislação Básica Institucional
sigla: LBI
periodo: Periodo01
assunto: Hierarquia e Disciplina
prefixo: 01
atualizado_em: 05/06/2026
versao: 1.0
---

# Hierarquia e Disciplina
Ponto-chave de teste.
```

- [ ] **Step 3: Criar os arquivos de VC de fixture**

`revisao_VC01.md`:
```markdown
---
sistema: Nexus
tipo: revisao_prova
sigla: LBI
periodo: Periodo01
---
# Revisão VC01
```

`simulado_VC01.html`:
```html
<!doctype html><title>Simulado VC01</title>
```

`simulado_VC01_v2.html`:
```html
<!doctype html><title>Simulado VC01 v2</title>
```

- [ ] **Step 4: Criar o pensamento de fixture**

```markdown
---
sistema: Nexus
tipo: pensamento
periodo: Periodo01
criado_em: 10/06/2026
pensamentos_relacionados: []
---

# Proporcionalidade no poder de polícia
Raciocínio de teste.
```

- [ ] **Step 5: Criar `Plataforma/tests/fixtures/config/disciplinas.json`**

```json
{
  "Periodo01": {
    "rotulo": "1º Período",
    "disciplinas": [
      { "sigla": "LBI", "nome": "Legislação Básica Institucional" },
      { "sigla": "TFM", "nome": "TFM I" }
    ]
  }
}
```

- [ ] **Step 6: Commit**

```bash
git add Plataforma/tests/fixtures
git commit -m "test(plataforma): fixture de vault falso para varredura

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 4: Varredura do vault → índice

**Files:**
- Create: `Plataforma/gerador/varredura.py`
- Test: `Plataforma/tests/test_varredura.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# Plataforma/tests/test_varredura.py
import json
import unittest
from pathlib import Path

from Plataforma.gerador.varredura import varrer_vault

FIXTURES = Path(__file__).parent / "fixtures"


class TestVarredura(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = json.loads((FIXTURES / "config" / "disciplinas.json").read_text("utf-8"))
        cls.indice = varrer_vault(FIXTURES / "vault", config)

    def test_periodos_presentes(self):
        periodos = {p["periodo"]: p for p in self.indice["periodos"]}
        self.assertIn("Periodo01", periodos)
        self.assertEqual(periodos["Periodo01"]["rotulo"], "1º Período")

    def test_disciplina_com_material(self):
        disc = self._disc("LBI")
        self.assertTrue(disc["tem_material"])
        self.assertEqual(disc["disciplina"], "Legislação Básica Institucional")
        self.assertIsNotNone(disc["resumo"])
        self.assertEqual(disc["resumo"]["versao"], "5.0")

    def test_disciplina_sem_material_aparece(self):
        disc = self._disc("TFM")
        self.assertFalse(disc["tem_material"])
        self.assertIsNone(disc["resumo"])
        self.assertEqual(disc["temas"], [])

    def test_pontos_chave_agrupados_por_tema(self):
        disc = self._disc("LBI")
        self.assertEqual(len(disc["temas"]), 1)
        tema = disc["temas"][0]
        self.assertEqual(tema["pasta"], "01_Lei-9161-2021")
        self.assertEqual(len(tema["pontos"]), 1)
        self.assertEqual(tema["pontos"][0]["assunto"], "Hierarquia e Disciplina")
        self.assertIn("Ponto-chave de teste", tema["pontos"][0]["conteudo"])

    def test_vc_detecta_artefatos_e_pega_versao_maior(self):
        disc = self._disc("LBI")
        self.assertEqual(len(disc["vcs"]), 1)
        vc = disc["vcs"][0]
        self.assertEqual(vc["id"], "VC01")
        self.assertIsNotNone(vc["revisao"])
        self.assertIsNone(vc["audio"])
        # deve preferir o _v2 ao simulado base
        self.assertTrue(vc["simulado"].endswith("simulado_VC01_v2.html"))

    def test_pensamentos(self):
        self.assertEqual(len(self.indice["pensamentos"]), 1)
        p = self.indice["pensamentos"][0]
        self.assertIn("Proporcionalidade", p["titulo"])
        self.assertIn("Raciocínio de teste", p["conteudo"])

    def test_caminhos_sao_relativos_a_partir_de_plataforma(self):
        # caminhos no índice devem começar com '../Nexus_Obsidian/' p/ funcionar a partir de Plataforma/
        disc = self._disc("LBI")
        self.assertTrue(disc["resumo"]["caminho"].startswith("../Nexus_Obsidian/"))

    def _disc(self, sigla):
        for p in self.indice["periodos"]:
            for d in p["disciplinas"]:
                if d["sigla"] == sigla:
                    return d
        self.fail(f"disciplina {sigla} não encontrada")
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m unittest Plataforma.tests.test_varredura -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'Plataforma.gerador.varredura'`

- [ ] **Step 3: Implementar `varredura.py`**

```python
# Plataforma/gerador/varredura.py
"""Varre o vault Obsidian e monta o dicionário de índice da Plataforma."""
from __future__ import annotations

import re
from pathlib import Path

from Plataforma.gerador.frontmatter import parse_frontmatter

# os artefatos de prova procurados em cada pasta VC0X, por chave lógica
_PADROES_VC = {
    "revisao": r"revisao_{vc}(?:_v(\d+))?\.md$",
    "audio": r"audio_{vc}(?:_v(\d+))?\.txt$",
    "simulado": r"simulado_{vc}(?:_v(\d+))?\.html$",
    "flashcards": r"flashcard_{vc}(?:_v(\d+))?\.html$",
    "fluxograma": r"fluxograma_{vc}(?:_v(\d+))?\.html$",
}


def _rel(caminho: Path, vault: Path) -> str:
    """Caminho relativo a partir de Plataforma/ (que é irmã de Nexus_Obsidian)."""
    return "../" + vault.name + "/" + caminho.relative_to(vault).as_posix()


def _ler(caminho: Path) -> tuple[dict, str]:
    return parse_frontmatter(caminho.read_text("utf-8"))


def _escolher_versao(caminhos: list[Path]) -> Path | None:
    """Dentre arquivos equivalentes (com/sem _vN), devolve o de maior versão."""
    if not caminhos:
        return None

    def chave(c: Path) -> int:
        m = re.search(r"_v(\d+)\.", c.name)
        return int(m.group(1)) if m else 1

    return sorted(caminhos, key=chave)[-1]


def _varrer_vcs(pasta_disc: Path, vault: Path) -> list[dict]:
    vcs = []
    for vc_dir in sorted(pasta_disc.glob("VC*")):
        if not vc_dir.is_dir():
            continue
        vc_id = vc_dir.name
        registro = {"id": vc_id}
        for chave, padrao in _PADROES_VC.items():
            regex = re.compile(padrao.format(vc=re.escape(vc_id)))
            achados = [f for f in vc_dir.iterdir() if regex.search(f.name)]
            escolhido = _escolher_versao(achados)
            registro[chave] = _rel(escolhido, vault) if escolhido else None
        vcs.append(registro)
    return vcs


def _varrer_pontos_chave(pasta_disc: Path, vault: Path) -> list[dict]:
    raiz = pasta_disc / "pontos_chave"
    if not raiz.is_dir():
        return []
    temas = []
    for tema_dir in sorted(p for p in raiz.iterdir() if p.is_dir()):
        pontos = []
        for md in sorted(tema_dir.glob("*.md")):
            meta, corpo = _ler(md)
            pontos.append({
                "assunto": meta.get("assunto", md.stem),
                "prefixo": meta.get("prefixo", ""),
                "caminho": _rel(md, vault),
                "conteudo": corpo,
            })
        temas.append({"pasta": tema_dir.name, "pontos": pontos})
    return temas


def _varrer_disciplina(pasta_disc: Path, sigla: str, nome: str, vault: Path) -> dict:
    resumo = None
    arq_resumo = pasta_disc / f"resumo_{sigla}.md"
    if arq_resumo.is_file():
        meta, corpo = _ler(arq_resumo)
        resumo = {
            "versao": meta.get("versao", ""),
            "atualizado_em": meta.get("atualizado_em", ""),
            "caminho": _rel(arq_resumo, vault),
            "conteudo": corpo,
        }
    temas = _varrer_pontos_chave(pasta_disc, vault)
    vcs = _varrer_vcs(pasta_disc, vault)
    return {
        "sigla": sigla,
        "disciplina": nome,
        "tem_material": pasta_disc.is_dir() and (resumo is not None or bool(temas) or bool(vcs)),
        "resumo": resumo,
        "temas": temas,
        "vcs": vcs,
    }


def _achar_pasta_disciplina(vault: Path, periodo: str, sigla: str) -> Path | None:
    base = vault / periodo
    if not base.is_dir():
        return None
    for p in base.iterdir():
        if p.is_dir() and p.name.endswith(f"_{sigla}"):
            return p
    return None


def _varrer_pensamentos(vault: Path) -> list[dict]:
    pasta = vault / "Pensamento"
    if not pasta.is_dir():
        return []
    pensamentos = []
    for md in sorted(pasta.glob("*.md")):
        if md.name.startswith("MOC"):
            continue
        meta, corpo = _ler(md)
        titulo = corpo.lstrip().splitlines()[0].lstrip("# ").strip() if corpo.strip() else md.stem
        pensamentos.append({
            "titulo": titulo,
            "criado_em": meta.get("criado_em", ""),
            "relacionados": meta.get("pensamentos_relacionados", []),
            "caminho": _rel(md, vault),
            "conteudo": corpo,
        })
    return pensamentos


def varrer_vault(vault: Path, config: dict) -> dict:
    """Monta o índice completo a partir do vault + config de disciplinas."""
    vault = Path(vault)
    periodos = []
    for periodo, dados in sorted(config.items()):
        disciplinas = []
        for d in dados["disciplinas"]:
            sigla = d["sigla"]
            pasta = _achar_pasta_disciplina(vault, periodo, sigla)
            if pasta is not None:
                disciplinas.append(_varrer_disciplina(pasta, sigla, d["nome"], vault))
            else:
                disciplinas.append({
                    "sigla": sigla, "disciplina": d["nome"],
                    "tem_material": False, "resumo": None, "temas": [], "vcs": [],
                })
        periodos.append({"periodo": periodo, "rotulo": dados["rotulo"], "disciplinas": disciplinas})

    return {"periodos": periodos, "pensamentos": _varrer_pensamentos(vault)}
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `python3 -m unittest Plataforma.tests.test_varredura -v`
Expected: PASS (todos os testes OK)

- [ ] **Step 5: Commit**

```bash
git add Plataforma/gerador/varredura.py Plataforma/tests/test_varredura.py
git commit -m "feat(plataforma): varredura do vault para indice

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 5: Derivar Fluxogramas e Legislação a partir do índice

**Files:**
- Modify: `Plataforma/gerador/varredura.py` (acrescentar `derivar_secoes`)
- Test: `Plataforma/tests/test_varredura.py` (acrescentar teste)

Justificativa: as seções "Fluxogramas" e "Legislação" da sidebar são *vistas derivadas* do mesmo índice — fluxogramas são os artefatos `fluxograma_VC0X.html` já mapeados nas VCs; legislação são os temas de pontos-chave cujo nome remete a lei/decreto. Manter como derivação evita duplicar varredura.

- [ ] **Step 1: Acrescentar teste**

```python
# acrescentar em Plataforma/tests/test_varredura.py
from Plataforma.gerador.varredura import derivar_secoes


class TestDerivarSecoes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        config = json.loads((FIXTURES / "config" / "disciplinas.json").read_text("utf-8"))
        indice = varrer_vault(FIXTURES / "vault", config)
        cls.secoes = derivar_secoes(indice)

    def test_legislacao_capta_tema_de_lei(self):
        legis = self.secoes["legislacao"]
        self.assertTrue(any(item["sigla"] == "LBI" for item in legis))
        self.assertTrue(any("Lei-9161" in item["pasta"] for item in legis))

    def test_fluxogramas_vazio_quando_nao_ha(self):
        # a fixture LBI/VC01 não tem fluxograma → lista vazia
        self.assertEqual(self.secoes["fluxogramas"], [])
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m unittest Plataforma.tests.test_varredura.TestDerivarSecoes -v`
Expected: FAIL com `ImportError: cannot import name 'derivar_secoes'`

- [ ] **Step 3: Implementar `derivar_secoes` em `varredura.py`**

```python
# acrescentar ao final de Plataforma/gerador/varredura.py

# termos que indicam que um tema de pontos-chave é legislação
_TERMOS_LEGISLACAO = ("lei", "decreto", "estatuto", "codigo", "código", "constitui", "regulamento")


def derivar_secoes(indice: dict) -> dict:
    """Deriva as vistas 'fluxogramas' e 'legislacao' a partir do índice principal."""
    fluxogramas = []
    legislacao = []
    for periodo in indice["periodos"]:
        for disc in periodo["disciplinas"]:
            for vc in disc["vcs"]:
                if vc.get("fluxograma"):
                    fluxogramas.append({
                        "sigla": disc["sigla"], "disciplina": disc["disciplina"],
                        "vc": vc["id"], "caminho": vc["fluxograma"],
                    })
            for tema in disc["temas"]:
                nome = tema["pasta"].lower()
                if any(t in nome for t in _TERMOS_LEGISLACAO):
                    legislacao.append({
                        "sigla": disc["sigla"], "disciplina": disc["disciplina"],
                        "pasta": tema["pasta"], "qtd_pontos": len(tema["pontos"]),
                    })
    return {"fluxogramas": fluxogramas, "legislacao": legislacao}
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `python3 -m unittest Plataforma.tests.test_varredura -v`
Expected: PASS (todos os testes, incluindo os novos)

- [ ] **Step 5: Commit**

```bash
git add Plataforma/gerador/varredura.py Plataforma/tests/test_varredura.py
git commit -m "feat(plataforma): derivar secoes de fluxogramas e legislacao

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 6: Assets do front-end — template, CSS e renderizador Markdown vendorizado

**Files:**
- Create: `Plataforma/app/template.html`
- Create: `Plataforma/app/estilo.css`
- Create: `Plataforma/app/vendor/marked.min.js` (baixado)

- [ ] **Step 1: Vendorizar o `marked.min.js`** (renderizador Markdown, versão fixada)

```bash
cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus"
curl -fsSL https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js -o Plataforma/app/vendor/marked.min.js
test -s Plataforma/app/vendor/marked.min.js && head -c 60 Plataforma/app/vendor/marked.min.js
```
Expected: imprime o começo do arquivo minificado (não vazio). Se offline, baixar `marked@12.0.2` por outro meio e salvar nesse caminho.

- [ ] **Step 2: Criar `Plataforma/app/template.html`** (casca com marcadores que o gerador substitui)

```html
<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Nexus · Centro de Comando</title>
<style>/*{{ESTILO}}*/</style>
</head>
<body>
<aside id="sidebar">
  <div class="brand">NEXUS</div>
  <nav>
    <a href="#radar"      class="nav-item" data-sec="radar"><span class="ic">⊚</span> Radar</a>
    <a href="#mapa"       class="nav-item" data-sec="mapa"><span class="ic">⬢</span> Mapa de Conhecimento</a>
    <a href="#fluxogramas" class="nav-item" data-sec="fluxogramas"><span class="ic">⟁</span> Fluxogramas</a>
    <a href="#legislacao" class="nav-item" data-sec="legislacao"><span class="ic">⚖</span> Legislação</a>
    <a href="#pensamentos" class="nav-item" data-sec="pensamentos"><span class="ic">◈</span> Pensamentos</a>
  </nav>
  <div class="rodape">Atualizado em <span id="gerado-em"></span></div>
</aside>
<main id="conteudo"></main>
<script>window.NEXUS_DATA = /*{{DADOS}}*/ null;</script>
<script>/*{{MARKED}}*/</script>
<script>/*{{APP}}*/</script>
</body>
</html>
```

- [ ] **Step 3: Criar `Plataforma/app/estilo.css`** (tema escuro, sidebar fixa, responsivo)

```css
:root{
  --bg:#0e1116; --bg-elev:#161b22; --bg-card:#1b212b; --linha:#2a313c;
  --txt:#e6edf3; --txt-fraco:#8b949e; --acento:#3fb6a8; --alerta:#e5534b; --aviso:#d9a441;
}
*{box-sizing:border-box}
body{margin:0;display:flex;min-height:100vh;background:var(--bg);color:var(--txt);
  font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
#sidebar{width:230px;flex:0 0 230px;background:var(--bg-elev);border-right:1px solid var(--linha);
  display:flex;flex-direction:column;padding:18px 12px;position:sticky;top:0;height:100vh}
.brand{font-weight:700;letter-spacing:3px;color:var(--acento);margin:4px 8px 22px}
nav{display:flex;flex-direction:column;gap:4px}
.nav-item{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:8px;
  color:var(--txt-fraco);text-decoration:none;font-weight:500}
.nav-item .ic{font-size:18px;width:22px;text-align:center}
.nav-item:hover{background:var(--bg-card);color:var(--txt)}
.nav-item.ativo{background:var(--bg-card);color:var(--acento)}
.rodape{margin-top:auto;color:var(--txt-fraco);font-size:12px;padding:8px}
#conteudo{flex:1;padding:28px 34px;max-width:1100px}
h1{font-size:22px;margin:0 0 18px}
h2.secao{font-size:13px;text-transform:uppercase;letter-spacing:1px;color:var(--txt-fraco);
  margin:26px 0 12px}
.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}
.card{background:var(--bg-card);border:1px solid var(--linha);border-radius:12px;padding:16px;cursor:pointer}
.card:hover{border-color:var(--acento)}
.card.vazio{opacity:.42;cursor:default}
.card .sigla{font-weight:700;font-size:17px}
.card .meta{color:var(--txt-fraco);font-size:13px;margin-top:6px}
.card.vc{border-color:var(--alerta)}
.card.aula{border-color:var(--aviso)}
.tag{display:inline-block;font-size:11px;padding:2px 8px;border-radius:999px;margin-top:8px}
.tag.vc{background:rgba(229,83,75,.16);color:var(--alerta)}
.tag.aula{background:rgba(217,164,65,.16);color:var(--aviso)}
.radar-item{display:flex;justify-content:space-between;align-items:center;background:var(--bg-card);
  border:1px solid var(--linha);border-left:4px solid var(--aviso);border-radius:10px;padding:14px 16px;margin-bottom:10px}
.radar-item.vc{border-left-color:var(--alerta)}
.dias{font-weight:700}
.vazio-msg{color:var(--txt-fraco);background:var(--bg-card);border:1px dashed var(--linha);
  border-radius:10px;padding:18px;text-align:center}
.lista a{display:block;background:var(--bg-card);border:1px solid var(--linha);border-radius:8px;
  padding:12px 14px;margin-bottom:8px;color:var(--txt);text-decoration:none}
.lista a:hover{border-color:var(--acento)}
.voltar{color:var(--acento);cursor:pointer;display:inline-block;margin-bottom:14px}
.doc{background:var(--bg-card);border:1px solid var(--linha);border-radius:12px;padding:20px 24px;margin-top:14px}
.doc h1,.doc h2,.doc h3{margin-top:18px}
.doc table{border-collapse:collapse;width:100%}
.doc th,.doc td{border:1px solid var(--linha);padding:6px 10px;text-align:left}
.doc code{background:#0e1116;padding:1px 5px;border-radius:4px}
.acordeao{margin-top:10px}
.acordeao>summary{cursor:pointer;padding:10px 0;font-weight:600}
@media(max-width:720px){
  body{flex-direction:column}
  #sidebar{width:100%;height:auto;position:static;flex-direction:row;flex-wrap:wrap;align-items:center;gap:4px}
  #sidebar .brand{margin:0 12px 0 4px}
  #sidebar .rodape{display:none}
  nav{flex-direction:row;flex-wrap:wrap}
  #conteudo{padding:18px}
}
```

- [ ] **Step 4: Commit**

```bash
git add Plataforma/app/template.html Plataforma/app/estilo.css Plataforma/app/vendor/marked.min.js
git commit -m "feat(plataforma): assets do front-end (template, tema escuro, marked vendorizado)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 7: Lógica do front-end (`app.js`)

**Files:**
- Create: `Plataforma/app/app.js`

Sem teste automatizado (camada visual — verificada na Task 10). O código deve ser completo e funcional. Renderiza a partir de `window.NEXUS_DATA`; usa `marked.parse` para os `.md` embutidos; navega entre seções por hash.

- [ ] **Step 1: Criar `Plataforma/app/app.js`**

```javascript
(function () {
  "use strict";
  const D = window.NEXUS_DATA || {};
  const conteudo = document.getElementById("conteudo");
  const geradoEm = document.getElementById("gerado-em");
  if (geradoEm) geradoEm.textContent = D.gerado_em || "—";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"]/g, c =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  }

  // [[wikilink]] vira texto destacado (Fase 1 não resolve link interno)
  function preMd(txt) {
    return String(txt || "").replace(/\[\[([^\]]+)\]\]/g, (_, x) => "**" + x.split("/").pop() + "**");
  }
  function md(txt) {
    try { return window.marked.parse(preMd(txt)); }
    catch (e) { return "<pre>" + esc(txt) + "</pre>"; }
  }

  function todasDisciplinas() {
    const out = [];
    (D.periodos || []).forEach(p => (p.disciplinas || []).forEach(d => out.push(d)));
    return out;
  }
  function discPorSigla(sigla) {
    return todasDisciplinas().find(d => d.sigla === sigla);
  }

  const radar = D.radar || { aulas_semana: [], vcs_futuras: [] };
  function siglaTemAula(s) { return (radar.aulas_semana || []).some(a => a.sigla === s); }
  function siglaTemVc(s) { return (radar.vcs_futuras || []).some(v => v.sigla === s); }

  // ---------- Seções ----------
  function viewRadar() {
    const vcs = radar.vcs_futuras || [];
    const aulas = radar.aulas_semana || [];
    if (!vcs.length && !aulas.length) {
      return '<h1>Radar</h1><div class="vazio-msg">Nada chamando atenção esta semana.</div>';
    }
    let h = "<h1>Radar</h1>";
    if (vcs.length) {
      h += '<h2 class="secao">Verificações chegando</h2>';
      vcs.slice().sort((a, b) => a.dias_restantes - b.dias_restantes).forEach(v => {
        h += `<div class="radar-item vc"><span><b>${esc(v.sigla)}</b> · VC em ${esc(v.data)}</span>` +
             `<span class="dias">${esc(v.dias_restantes)} dia(s)</span></div>`;
      });
    }
    if (aulas.length) {
      h += '<h2 class="secao">Aulas desta semana</h2>';
      aulas.forEach(a => {
        h += `<div class="radar-item"><span><b>${esc(a.sigla)}</b> · ${esc(a.titulo || "aula")}</span>` +
             `<span class="dias">${esc(a.dia || "")}</span></div>`;
      });
    }
    return h;
  }

  function cardDisciplina(d) {
    if (!d.tem_material) {
      return `<div class="card vazio"><div class="sigla">${esc(d.sigla)}</div>` +
             `<div class="meta">${esc(d.disciplina)}</div><div class="meta">sem material</div></div>`;
    }
    const nPontos = (d.temas || []).reduce((s, t) => s + (t.pontos || []).length, 0);
    const classe = siglaTemVc(d.sigla) ? "card vc" : siglaTemAula(d.sigla) ? "card aula" : "card";
    let tag = "";
    if (siglaTemVc(d.sigla)) tag = '<span class="tag vc">VC chegando</span>';
    else if (siglaTemAula(d.sigla)) tag = '<span class="tag aula">aula esta semana</span>';
    return `<div class="${classe}" data-disc="${esc(d.sigla)}">` +
           `<div class="sigla">${esc(d.sigla)}</div>` +
           `<div class="meta">${esc(d.disciplina)}</div>` +
           `<div class="meta">${nPontos} ponto(s)-chave · ${(d.vcs || []).length} VC(s)</div>` +
           tag + "</div>";
  }

  function viewMapa() {
    let h = "<h1>Mapa de Conhecimento</h1>";
    (D.periodos || []).forEach(p => {
      h += `<h2 class="secao">${esc(p.rotulo)}</h2><div class="grade">`;
      (p.disciplinas || []).forEach(d => { h += cardDisciplina(d); });
      h += "</div>";
    });
    return h;
  }

  function viewDisciplina(sigla) {
    const d = discPorSigla(sigla);
    if (!d) return viewMapa();
    let h = `<span class="voltar" data-goto="mapa">← Mapa</span>`;
    h += `<h1>${esc(d.sigla)} — ${esc(d.disciplina)}</h1>`;
    if (d.resumo) {
      h += `<details class="acordeao" open><summary>Resumo geral (v${esc(d.resumo.versao)} · ${esc(d.resumo.atualizado_em)})</summary>` +
           `<div class="doc">${md(d.resumo.conteudo)}</div></details>`;
    }
    if ((d.temas || []).length) {
      h += '<h2 class="secao">Pontos-chave</h2>';
      d.temas.forEach(t => {
        h += `<details class="acordeao"><summary>${esc(t.pasta)} · ${t.pontos.length} ponto(s)</summary>`;
        t.pontos.forEach(p => { h += `<div class="doc">${md(p.conteudo)}</div>`; });
        h += "</details>";
      });
    }
    if ((d.vcs || []).length) {
      h += '<h2 class="secao">Material de prova</h2><div class="lista">';
      d.vcs.forEach(vc => {
        const links = ["revisao", "audio", "simulado", "flashcards", "fluxograma"]
          .filter(k => vc[k])
          .map(k => `<a href="${esc(vc[k])}" target="_blank">${k}</a>`).join(" ");
        h += `<div class="card"><b>${esc(vc.id)}</b><div class="meta lista">${links || "—"}</div></div>`;
      });
      h += "</div>";
    }
    return h;
  }

  function viewLista(titulo, itens, render, vazio) {
    if (!itens || !itens.length) return `<h1>${esc(titulo)}</h1><div class="vazio-msg">${esc(vazio)}</div>`;
    return `<h1>${esc(titulo)}</h1><div class="lista">` + itens.map(render).join("") + "</div>";
  }

  function viewFluxogramas() {
    return viewLista("Fluxogramas", D.fluxogramas,
      f => `<a href="${esc(f.caminho)}" target="_blank"><b>${esc(f.sigla)}</b> · ${esc(f.vc)} — ${esc(f.disciplina)}</a>`,
      "Nenhum fluxograma gerado ainda.");
  }
  function viewLegislacao() {
    return viewLista("Legislação", D.legislacao,
      l => `<a data-goto="disc:${esc(l.sigla)}"><b>${esc(l.sigla)}</b> · ${esc(l.pasta)} (${esc(l.qtd_pontos)} pontos)</a>`,
      "Nenhuma legislação mapeada ainda.");
  }
  function viewPensamentos() {
    return viewLista("Pensamentos", D.pensamentos,
      p => `<a data-pensamento="${esc(p.titulo)}"><b>${esc(p.titulo)}</b><br><span class="meta">${esc(p.criado_em)}</span></a>`,
      "Nenhum pensamento consolidado ainda.");
  }
  function viewPensamento(titulo) {
    const p = (D.pensamentos || []).find(x => x.titulo === titulo);
    if (!p) return viewPensamentos();
    return `<span class="voltar" data-goto="pensamentos">← Pensamentos</span>` +
           `<h1>${esc(p.titulo)}</h1><div class="doc">${md(p.conteudo)}</div>`;
  }

  // ---------- Roteamento ----------
  function marcarNav(sec) {
    document.querySelectorAll(".nav-item").forEach(a =>
      a.classList.toggle("ativo", a.dataset.sec === sec));
  }
  function render() {
    const hash = (location.hash || "#radar").slice(1);
    let sec = hash, html;
    if (hash.startsWith("disc:")) { html = viewDisciplina(hash.slice(5)); sec = "mapa"; }
    else if (hash.startsWith("pensamento:")) { html = viewPensamento(decodeURIComponent(hash.slice(11))); sec = "pensamentos"; }
    else if (hash === "mapa") html = viewMapa();
    else if (hash === "fluxogramas") html = viewFluxogramas();
    else if (hash === "legislacao") html = viewLegislacao();
    else if (hash === "pensamentos") html = viewPensamentos();
    else { html = viewRadar(); sec = "radar"; }
    conteudo.innerHTML = html;
    marcarNav(sec);
    window.scrollTo(0, 0);
  }

  document.addEventListener("click", e => {
    const card = e.target.closest("[data-disc]");
    if (card) { location.hash = "disc:" + card.dataset.disc; return; }
    const goto = e.target.closest("[data-goto]");
    if (goto) { location.hash = goto.dataset.goto; return; }
    const pens = e.target.closest("[data-pensamento]");
    if (pens) { location.hash = "pensamento:" + encodeURIComponent(pens.dataset.pensamento); }
  });
  window.addEventListener("hashchange", render);
  render();
})();
```

- [ ] **Step 2: Commit**

```bash
git add Plataforma/app/app.js
git commit -m "feat(plataforma): logica de render do front-end (app.js)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 8: Montagem do HTML autocontido

**Files:**
- Create: `Plataforma/gerador/montar.py`
- Test: `Plataforma/tests/test_montar.py`

- [ ] **Step 1: Escrever o teste que falha**

```python
# Plataforma/tests/test_montar.py
import json
import unittest
from pathlib import Path

from Plataforma.gerador.montar import montar_html

APP = Path(__file__).resolve().parents[1] / "app"


class TestMontar(unittest.TestCase):
    def setUp(self):
        self.indice = {
            "periodos": [{"periodo": "Periodo01", "rotulo": "1º Período",
                          "disciplinas": [{"sigla": "LBI", "disciplina": "Legislação Básica Institucional",
                                           "tem_material": True, "resumo": None, "temas": [], "vcs": []}]}],
            "pensamentos": [], "fluxogramas": [], "legislacao": [],
        }
        self.radar = {"aulas_semana": [], "vcs_futuras": []}

    def test_html_autocontido(self):
        html = montar_html(self.indice, self.radar, APP, gerado_em="13/06/2026")
        # dados embutidos, não via fetch
        self.assertIn("window.NEXUS_DATA", html)
        self.assertIn('"LBI"', html)
        self.assertIn("13/06/2026", html)
        # nenhum carregamento externo: tudo inline, sem <script src> nem <link>
        # (não checamos a string "https://" porque o banner do marked.min.js a contém)
        self.assertNotIn("<script src", html)
        self.assertNotIn("<link", html)
        # CSS, marked e app inlinados
        self.assertIn("--acento", html)        # do estilo.css
        self.assertIn("marked", html)          # do vendor
        self.assertIn("viewRadar", html)       # do app.js

    def test_radar_entra_no_data(self):
        radar = {"aulas_semana": [{"sigla": "FSV", "titulo": "Salvamento", "dia": "2026-06-13"}],
                 "vcs_futuras": [{"sigla": "LBI", "data": "16/06/2026", "dias_restantes": 3}]}
        html = montar_html(self.indice, radar, APP, gerado_em="13/06/2026")
        self.assertIn('"FSV"', html)
        self.assertIn("dias_restantes", html)
```

- [ ] **Step 2: Rodar e confirmar que falha**

Run: `python3 -m unittest Plataforma.tests.test_montar -v`
Expected: FAIL com `ModuleNotFoundError: No module named 'Plataforma.gerador.montar'`

- [ ] **Step 3: Implementar `montar.py`**

```python
# Plataforma/gerador/montar.py
"""Monta o index.html autocontido: template + CSS + marked + app + dados, tudo inline."""
from __future__ import annotations

import json
from pathlib import Path


def montar_html(indice: dict, radar: dict, app_dir: Path, gerado_em: str) -> str:
    app_dir = Path(app_dir)
    template = (app_dir / "template.html").read_text("utf-8")
    estilo = (app_dir / "estilo.css").read_text("utf-8")
    marked = (app_dir / "vendor" / "marked.min.js").read_text("utf-8")
    app_js = (app_dir / "app.js").read_text("utf-8")

    dados = dict(indice)
    dados["radar"] = radar or {"aulas_semana": [], "vcs_futuras": []}
    dados["gerado_em"] = gerado_em
    # </script> dentro de strings JSON quebraria o bloco <script>; escapar
    dados_json = json.dumps(dados, ensure_ascii=False).replace("</", "<\\/")

    html = template.replace("/*{{ESTILO}}*/", estilo)
    html = html.replace("/*{{MARKED}}*/", marked)
    html = html.replace("/*{{APP}}*/", app_js)
    html = html.replace("/*{{DADOS}}*/ null", dados_json)
    return html
```

- [ ] **Step 4: Rodar e confirmar que passa**

Run: `python3 -m unittest Plataforma.tests.test_montar -v`
Expected: PASS (2 testes OK)

> Atenção: o teste `test_html_autocontido` exige que `Plataforma/app/vendor/marked.min.js` exista (Task 6, Step 1). Se a Task 6 não rodou, esta task falha — execute na ordem.

- [ ] **Step 5: Commit**

```bash
git add Plataforma/gerador/montar.py Plataforma/tests/test_montar.py
git commit -m "feat(plataforma): montagem do index.html autocontido

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 9: CLI `gerar_indice.py`

**Files:**
- Create: `Plataforma/gerar_indice.py`

- [ ] **Step 1: Implementar a CLI**

```python
#!/usr/bin/env python3
# Plataforma/gerar_indice.py
"""Gera Plataforma/index.html a partir do vault e (opcionalmente) de um radar.json.

Uso (a partir da raiz do Nexus):
    python3 -m Plataforma.gerar_indice
    python3 -m Plataforma.gerar_indice --radar Plataforma/radar.json
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

from Plataforma.gerador.varredura import varrer_vault, derivar_secoes
from Plataforma.gerador.montar import montar_html

RAIZ = Path(__file__).resolve().parents[1]          # .../Nexus
PLATAFORMA = RAIZ / "Plataforma"


def main() -> None:
    ap = argparse.ArgumentParser(description="Gera o index.html da Plataforma Nexus.")
    ap.add_argument("--vault", default=str(RAIZ / "Nexus_Obsidian"))
    ap.add_argument("--config", default=str(PLATAFORMA / "config" / "disciplinas.json"))
    ap.add_argument("--radar", default=str(PLATAFORMA / "radar.json"))
    ap.add_argument("--out", default=str(PLATAFORMA / "index.html"))
    args = ap.parse_args()

    config = json.loads(Path(args.config).read_text("utf-8"))
    indice = varrer_vault(Path(args.vault), config)
    indice.update(derivar_secoes(indice))

    radar = {"aulas_semana": [], "vcs_futuras": []}
    radar_path = Path(args.radar)
    if radar_path.is_file():
        radar = json.loads(radar_path.read_text("utf-8"))

    gerado_em = date.today().strftime("%d/%m/%Y")
    html = montar_html(indice, radar, PLATAFORMA / "app", gerado_em=gerado_em)
    Path(args.out).write_text(html, "utf-8")

    n_disc = sum(len(p["disciplinas"]) for p in indice["periodos"])
    n_com = sum(1 for p in indice["periodos"] for d in p["disciplinas"] if d["tem_material"])
    print(f"OK · {args.out}")
    print(f"   {n_disc} disciplinas ({n_com} com material) · "
          f"{len(indice['pensamentos'])} pensamentos · "
          f"{len(indice['fluxogramas'])} fluxogramas · "
          f"{len(radar.get('vcs_futuras', []))} VC(s) no radar")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Rodar a geração real (sem radar) e conferir a saída**

Run: `cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus" && python3 -m Plataforma.gerar_indice`
Expected: imprime `OK · .../Plataforma/index.html` e a linha de contagem (deve listar ~19 disciplinas, com as que têm material > 0). Cria `Plataforma/index.html`.

- [ ] **Step 3: Conferir que o `index.html` é autocontido**

Run: `grep -c "window.NEXUS_DATA" Plataforma/index.html && grep -c "src=\"http" Plataforma/index.html; grep -c "fetch(" Plataforma/index.html`
Expected: primeira linha = `1`; as duas seguintes = `0` (nenhum recurso externo, nenhum fetch).

- [ ] **Step 4: Commit (inclui o index.html gerado)**

```bash
git add Plataforma/gerar_indice.py Plataforma/index.html
git commit -m "feat(plataforma): CLI de geracao + index.html inicial

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 10: Verificação visual no navegador (Mac e iPhone)

**Files:** nenhum (verificação manual).

- [ ] **Step 1: Abrir no Mac**

Run: `open "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus/Plataforma/index.html"`
Conferir:
- Sidebar com os 5 itens (⊚ Radar, ⬢ Mapa, ⟁ Fluxogramas, ⚖ Legislação, ◈ Pensamentos).
- Radar mostra "Nada chamando atenção esta semana" (ainda sem radar.json).
- Mapa: grade de cards por período; disciplinas com material mostram contagem de pontos-chave, sem material aparecem esmaecidas.
- Clicar num card abre a página da disciplina com resumo/pontos-chave renderizados (Markdown formatado, não cru).
- Material de prova: links abrem os HTMLs (simulado/flashcard/fluxograma) em nova aba.
- Fluxogramas / Legislação / Pensamentos listam ou mostram estado vazio.

- [ ] **Step 2: Conferir no iPhone**

Garantir que o Google Drive sincronizou a pasta `Nexus/Plataforma/`. Abrir `index.html` pelo app Arquivos → Chrome/Safari. Conferir layout responsivo (sidebar vira topo) e que o conteúdo `.md` renderiza offline (sem rede).

- [ ] **Step 3: Se algo estiver errado**, ajustar `app/estilo.css` ou `app/app.js`, **regenerar** (`python3 -m Plataforma.gerar_indice`) e repetir. Commitar correções:

```bash
git add Plataforma/app Plataforma/index.html
git commit -m "fix(plataforma): ajustes de layout apos verificacao visual

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 11: Skill `atualizar_plataforma`

**Files:**
- Create: `Nexus/.claude/skills/atualizar_plataforma/SKILL.md`

Esta skill é o gatilho **manual** (Fase 1). Ela orquestra: consultar o Calendar via MCP → montar `radar.json` → rodar o gerador → commit + push. A consulta ao Calendar vive aqui (não no Python) porque o acesso é via MCP do Claude.

- [ ] **Step 1: Criar `Nexus/.claude/skills/atualizar_plataforma/SKILL.md`**

````markdown
---
name: atualizar_plataforma
description: >
  Skill do sistema Nexus que regenera a Plataforma Nexus (centro de comando estático em
  Nexus/Plataforma/index.html) a partir do vault e do Google Calendar. Acionar quando o
  usuário disser "atualizar plataforma", "regenerar plataforma", "atualizar o centro de
  comando", "rebuildar a plataforma", ou ao final de uma sessão de estudo em que ele peça
  para refletir as mudanças na plataforma. Faz varredura completa do vault, monta o radar
  da semana (aulas + VCs) consultando o Calendar via MCP, gera o index.html e faz commit+push.
---

# ATUALIZAR_PLATAFORMA

Regenera o `index.html` da Plataforma Nexus (Fase 1 — gatilho manual de varredura completa).

## Gatilhos
"atualizar plataforma", "regenerar plataforma", "atualizar o centro de comando",
"rebuildar a plataforma".

## Pré-condições
- Estar na raiz do Nexus: `~/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus`
- O pacote `Plataforma/` deve existir (gerador implementado).

## Passos

### 1. Montar o radar a partir do Google Calendar (MCP)
Consultar o calendário `rafaelras.94@gmail.com` (timeZone `America/Belem`) via MCP de
Google Calendar:
- **Aulas da semana atual** (segunda a sábado da semana corrente): para cada evento de
  disciplina, extrair a SIGLA Nexus (aplicar o mapeamento QIS→Nexus do CLAUDE.md:
  EC→ETICA, DA I→DA, IM I→IM, TFM I→TFM). Agrupar por sigla (uma entrada por disciplina).
- **VCs futuras**: eventos cujo título indique Verificação Corrente (VC) com data ≥ hoje.
  Para cada um, calcular `dias_restantes` em relação à data de hoje.

Escrever o arquivo `Plataforma/radar.json` (NÃO versionado — está no .gitignore) no formato:
```json
{
  "aulas_semana": [
    { "sigla": "FSV", "titulo": "Fundamentos de Salvamento Veicular", "dia": "2026-06-13" }
  ],
  "vcs_futuras": [
    { "sigla": "LBI", "data": "16/06/2026", "dias_restantes": 3 }
  ]
}
```
Se o Calendar não tiver eventos relevantes, gravar listas vazias — o Radar exibirá estado
vazio (não é erro).

### 2. Rodar o gerador
```bash
cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus"
python3 -m Plataforma.gerar_indice --radar Plataforma/radar.json
```
Conferir que a saída imprime `OK` e as contagens. Se algum arquivo `.md` tiver frontmatter
inconsistente, o gerador o ignora — relatar quais no relatório final (não interromper).

### 3. Commit + push
```bash
git add Plataforma/index.html Plataforma/config/disciplinas.json
git commit -m "feat(plataforma): atualiza centro de comando (radar + indice)"
git push origin main
```
(NÃO usar prefixo `sync:` — reservado ao hook. NÃO commitar `radar.json`.)

### 4. Relatório final
Informar: nº de disciplinas (com/sem material), nº de pensamentos, nº de fluxogramas,
o que entrou no radar (aulas da semana + VCs com dias restantes), arquivos ignorados por
frontmatter inconsistente (se houver) e a confirmação do commit + push.
````

- [ ] **Step 2: Commit**

```bash
git add .claude/skills/atualizar_plataforma/SKILL.md
git commit -m "feat(plataforma): skill atualizar_plataforma (gatilho manual)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Task 12: Teste end-to-end com radar simulado + documentação

**Files:**
- Test: `Plataforma/tests/test_montar.py` (já cobre montagem); aqui é validação manual do fluxo completo.
- Modify: `Nexus/CLAUDE.md` (registrar a nova skill e a Plataforma)

- [ ] **Step 1: Simular um `radar.json` e regenerar**

```bash
cd "$HOME/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus"
cat > Plataforma/radar.json <<'JSON'
{ "aulas_semana": [ { "sigla": "FSV", "titulo": "Salvamento Veicular", "dia": "2026-06-15" } ],
  "vcs_futuras": [ { "sigla": "LBI", "data": "16/06/2026", "dias_restantes": 3 } ] }
JSON
python3 -m Plataforma.gerar_indice --radar Plataforma/radar.json
```
Abrir `index.html` e confirmar: o Radar agora mostra a VC de LBI (com "3 dia(s)") e a aula
de FSV; no Mapa, o card de LBI ganha a borda/etiqueta de VC e o de FSV a de aula.
Depois apagar o radar de teste: `rm Plataforma/radar.json`.

- [ ] **Step 2: Rodar a suíte completa de testes**

Run: `python3 -m unittest discover -s Plataforma/tests -t . -v`
Expected: todos os testes PASS (frontmatter, varredura, derivar_secoes, montar).

- [ ] **Step 3: Registrar a Plataforma no `CLAUDE.md`**

Acrescentar à seção "Skills disponíveis" do `Nexus/CLAUDE.md` uma nova tabela:

```markdown
### Plataforma (Centro de Comando)
| Skill | Gatilho | Função |
|---|---|---|
| `atualizar_plataforma` | "atualizar plataforma" · "regenerar plataforma" | Regenera `Plataforma/index.html` (Radar + Mapa de Conhecimento) a partir do vault + Google Calendar. Varredura completa, commit + push. |
```

E acrescentar à árvore de arquitetura, sob a raiz `Nexus/`:

```markdown
├── Plataforma/                 ← Centro de comando estático (index.html autocontido)
│   ├── index.html              ← Plataforma gerada (Radar + Mapa); abre no Mac e iPhone
│   ├── gerar_indice.py         ← Gerador (varre o vault, embute dados no HTML)
│   ├── gerador/ · app/ · config/ · tests/ · docs/
```

- [ ] **Step 4: Commit + push final**

```bash
git add CLAUDE.md
git commit -m "docs(plataforma): registra Plataforma e skill atualizar_plataforma no CLAUDE.md

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
git push origin main
```

---

## Verificação de cobertura do spec

| Requisito do spec | Task |
|---|---|
| Hub estático, sem servidor, tema escuro | Tasks 6–9 |
| Dados embutidos no HTML (sem fetch, p/ iOS) | Task 8 (montar) + Task 9 Step 3 (verificação) |
| Vive em `Nexus/Plataforma/`, um só Git/sync | Task 1 + commits em todas |
| Índice por disciplina (resumo, pontos-chave por tema, VCs) | Task 4 |
| Radar (aulas da semana + VCs) via Calendar MCP | Task 11 (skill) + Task 8/9 (consumo) |
| Pensamentos | Task 4 (`_varrer_pensamentos`) + Task 7 (views) |
| Fluxogramas / Legislação como listas | Task 5 + Task 7 |
| Sidebar com ícones ⊚ ⬢ ⟁ ⚖ ◈, sem Disciplinar | Task 6 (template) |
| Mapa = grade de cards; card "sem material" esmaecido | Task 7 (`cardDisciplina`) + Task 1 (config) |
| Skill `atualizar_plataforma` (varredura completa manual) | Task 11 |
| Erros: frontmatter ruim ignorado, calendário vazio = estado vazio | Task 2 (parser tolerante) + Task 11 (radar vazio) + Task 7 (vazio-msg) |
| Verificação visual no navegador (Mac + iPhone) | Task 10, Task 12 |
| Renderização de Markdown dentro do app (decisão da Fase 1) | Task 6 (marked) + Task 7 (`md()`) |

**Fora deste plano (Plano 2 / fases futuras):** integração automática nas 6 skills
existentes; tratamento visual dedicado de Fluxogramas/Legislação/Pensamentos.
