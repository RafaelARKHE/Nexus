---
name: pontos_chave
description: >
  Skill de geração de arquivos de pontos-chave por assunto no sistema Nexus.
  Acionada automaticamente pela skill LEITURA_APROFUNDADA. Também acionar quando
  o usuário pedir "pontos-chave de [assunto]", "criar pontos-chave", "destacar
  pontos importantes". Gera arquivos organizados em subpastas temáticas dentro de
  pontos_chave/, com prefixo numérico definindo a ordem lógica de estudo dentro
  de cada tema.
---

# PONTOS_CHAVE

Skill de geração de arquivos de pontos-chave por assunto de uma disciplina,
organizados em subpastas por tema.

---

## Estrutura de pastas

```
pontos_chave/
├── 01_[TEMA-A]/
│   ├── 01_[assunto].md
│   └── 02_[assunto].md
├── 02_[TEMA-B]/
│   └── 01_[assunto].md
└── 03_[TEMA-C]/
    ├── 01_[assunto].md
    └── 02_[assunto].md
```

**O "tema" é determinado pela natureza da disciplina:**
- Para disciplinas com múltiplos documentos/leis (ex: LBI) → uma subpasta por documento/lei
- Para disciplinas com um único documento mas múltiplos temas (ex: APHR) → uma subpasta por tema clínico/conceitual
- Para disciplinas com apenas 1 tema identificável → arquivos direto em `pontos_chave/` sem subpasta

**Caminho completo:**
`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/pontos_chave/0N_[TEMA]/0N_[NOME_ASSUNTO].md`

---

## Nomenclatura das subpastas de tema

- Prefixo numérico sequencial dentro de `pontos_chave/`: `01_`, `02_`, `03_`...
- Nome descritivo em kebab-case, com maiúscula inicial: `01_Choque-e-Hemorragia/`
- Para leis: incluir número e sigla — ex: `01_Lei-9161-2021-CEDCBMPA/`
- Para unidades: incluir título da unidade — ex: `02_Bombeiros-no-Brasil/`

**Prefixo numérico dentro de cada subpasta:** reinicia em `01` para cada tema.
Os arquivos dentro de `02_Choque-e-Hemorragia/` começam em `01_`, não em `05_`.

---

## Critério de criação de arquivos

Um assunto vira arquivo próprio quando for um **conceito autônomo** — pode ser
estudado de forma independente sem depender de outro para fazer sentido.

Assuntos com forte interdependência são **agrupados no mesmo arquivo**.

Exemplos:
- Hierarquia e Disciplina → mesmo arquivo (interdependentes)
- Sistema Circulatório e Sistema Respiratório → arquivos separados (autônomos)

---

## Cabeçalho padrão Nexus (YAML frontmatter)

```yaml
---
sistema: Nexus
tipo: pontos_chave
disciplina: [NOME_COMPLETO_DA_DISCIPLINA]
sigla: [SIGLA]
periodo: Periodo0N
tema: [NOME_DA_SUBPASTA_SEM_PREFIXO]
assunto: [NOME_DO_ASSUNTO]
prefixo: "[01]"
arquivo_origem: [NOME_DO_PDF_OU_LEI]
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
moc_cfo: sim
moc_materia: sim
pensamentos_relacionados: []
---
```

---

## Estrutura do arquivo

```markdown
# [Nome do Assunto]
> Disciplina: [SIGLA] | Tema: [TEMA] | Origem: [NOME_DO_PDF] | Criado em: [DATA]

---

## Conceitos Fundamentais
Os conceitos base sem os quais o assunto não se sustenta.
Direto ao ponto — sem introdução.

## Detalhamento
Aprofundamento dos conceitos fundamentais.
Inclui exceções, casos especiais e nuances relevantes.

## Aplicação Prática
Como esse assunto aparece na realidade do CBMPA.
Exemplos operacionais e institucionais quando possível.

## Conexões
Links para outros arquivos do Obsidian relacionados.
Formato: [[Periodo0N/0N_SIGLA/pontos_chave/0N_TEMA/arquivo]]
Se LEITURA_APROFUNDADA passou contexto de pensamentos relacionados, referenciar:
[[Pensamento/AAAA-MM-DD_tema]] (apenas para arquivos que JÁ EXISTEM no sistema)

## Pontos de Atenção
O que o Nexus identificou como crítico para prova ou aplicação prática.
```

---

## Atualização do MOC da disciplina

O MOC deve refletir a estrutura por tema, com uma seção `###` por subpasta:

```markdown
## Pontos-Chave por Tema

### 01 — [Nome do Tema]
> Origem: `nome-do-arquivo-fonte`

| # | Assunto | Arquivo |
|---|---|---|
| 01 | [Assunto] | [[...pontos_chave/01_TEMA/01_assunto]] |

### 02 — [Outro Tema]
...
```

---

## Diretrizes de conteúdo

- Filtro de relevância: incluir apenas o que é essencial para o CFO/CBMPA
- Agrupamento por afinidade conceitual — não por ordem de aparição no PDF
- Linguagem direta — sem rodeios
- Imagens: incluir quando for insubstituível (diagrama anatômico, mapa cartográfico)
  Formato: `![descrição](caminho/relativo/imagem.png)`

---

## Regras críticas

- Nunca criar arquivo sem prefixo numérico
- O prefixo dentro de cada subpasta de tema **reinicia em 01** — não é global
- Se o material tiver apenas 1 tema identificável → criar arquivos direto em `pontos_chave/` sem subpasta
- Nunca sobrescrever arquivo existente — se assunto já existe, acrescentar nova seção com marcação de data e origem
- **Links `[[...]]` do Obsidian apenas para arquivos que JÁ EXISTEM no sistema**
- Para conexões com disciplinas ainda sem material, usar texto simples: `` `Periodo0N/??_SIGLA/arquivo` *(pendente)* ``
- Nomear arquivos em kebab-case: `01_sistema-circulatorio.md`
- Nomear subpastas em PascalKebab: `01_Choque-e-Hemorragia/`
