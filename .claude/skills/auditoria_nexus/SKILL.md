---
name: auditoria_nexus
description: >
  Skill de integridade do sistema Nexus. Acionar sempre que o usuário disser
  "auditar nexus", "auditoria", "rodar auditoria", "verificar integridade",
  "checar consistência", "está tudo certo no sistema?", "tem algo fora do lugar?",
  "varredura", ou pedir uma conferência geral do vault/MOCs/git. Faz uma varredura
  SOMENTE-LEITURA em 5 camadas (estrutura física, frontmatter, links, MOC↔realidade,
  git/sync), ancorada nos arquivos reais — não nas premissas do CLAUDE.md — e
  apresenta um relatório por severidade. Opcionalmente, só após confirmação item a
  item, aplica correções mecânicas e sem risco (linha faltante em MOC, campo
  derivável de frontmatter, recálculo de descontos do Disciplinar). Acionar também
  como conferência de rotina antes de fechar a semana de estudos.
---

# AUDITORIA_NEXUS

Skill que verifica se o Nexus continua íntegro: nada de binário no vault, nada de
estudo solto em Materiais, frontmatter coerente, links que resolvem, MOCs batendo
com os arquivos reais e a sincronização do GitHub em ordem. **Por padrão não escreve
nada** — só lê e relata. Correção é uma segunda etapa, opt-in e item a item.

---

## Caminhos do sistema

- Motor de varredura: `Nexus/.claude/skills/auditoria_nexus/scripts/auditoria.py`
- Alvos: `Nexus/Nexus_Obsidian/` (vault) e `Nexus/Nexus_Materiais/` (binários)
- Pivôs da camada 4: `MOC_CFO.md`, cada `MOC_[SIGLA].md`, `MOC_Pensamentos.md`,
  `Disciplinar/MOC_Disciplinar.md` + `Disciplinar/anotacoes/`
- Sync: `.claude/hooks/sync.log` e o estado de `origin/main`

---

## Ativação

Gatilhos: "auditar nexus", "rodar auditoria", "verificar integridade",
"checar consistência", "está tudo certo no sistema?", "tem algo fora do lugar?",
"varredura geral". Também é a skill certa para uma conferência de rotina antes de
sincronizar ou fechar a semana.

---

## O que a varredura cobre — 5 camadas

1. **Estrutura física** — binário (.pdf/.pptx/.png) dentro do vault; `.md` dentro
   de material de disciplina (`Materiais/Periodo0N/`); pasta/arquivo vazio; nome de
   topo reservado (`Nexus_Obsidian`/`Nexus_Materiais`) aninhado onde não devia;
   template de `_modelos/` alterado; nomenclatura de pasta de disciplina e de
   anotação fora do padrão; lock `~$*.pptx` do Office.
   → `MOC_*.md` de espaço (ex.: `Administrativo/MOC_Adm.md`) é **legítimo** e não acusa.
2. **Frontmatter** — bloco YAML presente; `tipo` dentro do conjunto realmente usado
   (inclui a família `moc_*`); campos-núcleo presentes; datas em DD/MM/AAAA;
   `atualizado_em ≥ criado_em` e não no futuro.
3. **Links** — todo `[[wikilink]]` resolve por **basename** (estilo Obsidian,
   tolerando os dois estilos de caminho e aliases `[[alvo|texto]]`); quebrados viram aviso.
4. **MOC ↔ realidade** (a mais importante) — pontos-chave órfãos (existem mas não
   estão no MOC) e fantasmas (no MOC mas não existem); artefatos VC conferidos
   **contra o MOC da disciplina** (não contra lista fixa de nomes); contagem `N PK`
   do MOC_CFO vs arquivos reais; e no **Disciplinar**, recálculo da soma de descontos
   a partir das anotações reais + aritmética da nota + pareamento print↔registro.
5. **Git/sync** — working tree sujo; excesso de commits `sync:` na semana;
   `CONFLITO/ERRO` no `sync.log` (falha de rede é só info); divergência com `origin/main`.

---

## Modos de execução

| Comando | Escopo |
|---|---|
| `python3 .claude/skills/auditoria_nexus/scripts/auditoria.py` | varredura completa (1–5) |
| `... auditoria.py --rapido` | só camada 4 (MOC) + 5 (git) — as de maior valor |
| `... auditoria.py --camada N` | uma camada específica (1..5) |
| `... auditoria.py SIGLA` | escopo a uma disciplina (ex.: `APHR`) |

O script é o **motor read-only**: ele lê, calcula e imprime o relatório com
severidades (🔴 erro = viola regra do CLAUDE.md · 🟡 aviso = provável drift ·
🔵 info), erros primeiro, agrupado por camada, terminando com contagem. Itens com
correção mecânica disponível vêm marcados com `✎`.

---

## Fluxo

### 1. Rodar a varredura
Executar o script no modo pedido (completo por padrão; `--rapido` se o usuário só
quer "o essencial"; escopo por sigla se citou uma disciplina). Rodar via Bash a
partir da raiz do Nexus.

### 2. Relatar
Repassar o relatório ao usuário, **erros primeiro**, agrupado por camada, com a
contagem final. Não inventar achados além dos que o script emitiu. Se algo for
ambíguo (ex.: artefato VC não referenciado que talvez seja descartável), apresentar
como pergunta, não como veredito.

### 3. Oferecer correção (opcional)
Se houver itens marcados com `✎`, oferecer corrigi-los. **Só prosseguir após
confirmação, e item a item** — nunca em lote. Cada correção é aplicada por você com
a ferramenta de edição, jamais pelo script:

- **linha faltante em MOC** — inserir a entrada na tabela/seção certa, no formato
  vigente daquele MOC (wikilink no mesmo estilo dos vizinhos);
- **campo derivável de frontmatter** — preencher `atualizado_em` (data de hoje),
  ou outro campo cujo valor seja inequívoco a partir do próprio arquivo;
- **recálculo do Disciplinar** — corrigir a linha de total de descontos e a
  aritmética da nota a partir da soma real das anotações.

A contagem `N PK` em prosa do MOC_CFO e a freshness de status narrativo **não são
auto-corrigidas** — apresentar como aviso para o usuário editar à mão.

### 4. Fechamento
- **Sem correção:** auditoria **não gera commit**. Encerrar com o relatório.
- **Com correção:** commit semântico (`fix(MOC): ...`, `fix(disciplinar): ...` ou
  `docs: ...` conforme o caso) + `git push origin main`, e confirmar o push no relatório.

---

## Regras críticas

- **Read-only é o padrão.** Sem confirmação explícita, a skill só lê e relata.
- **Correção é mecânica e sem risco, item a item.** Nunca em lote.
- **NUNCA** mover, renomear ou apagar arquivo.
- **NUNCA** tocar em conteúdo de estudo, de pensamento ou de justificativa
  disciplinar — corrigir índice/metadado/soma, jamais reescrever o que foi pensado.
- **NUNCA** mexer em `_modelos/` nem em qualquer binário.
- **Ancorar na realidade, não no CLAUDE.md.** Onde o sistema real diverge do
  documentado (frontmatter de MOC, tipos de artefato VC, `.md` legítimo em
  Materiais/Administrativo), a verdade é o arquivo — o motor já trata essas exceções.
  Se a divergência for do próprio CLAUDE.md (doc defasado), sinalizar como aviso.
- **Auditoria sem correção não commita.** Só há commit+push quando algo foi corrigido.

---

## Relatório de encerramento

Ao final, informar: modo rodado, contagem 🔴/🟡/🔵, os achados que importam,
quais correções foram aplicadas (se houve) e a confirmação do commit + push —
ou a constatação explícita de que nada foi alterado e, portanto, nada foi commitado.
