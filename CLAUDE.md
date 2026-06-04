# CLAUDE.md — Nexus

## O que é o Nexus

O **Nexus** é o sistema de gestão de conhecimento e estudo do **CAD BM Rafael**,
cadete do CFO Turma 16 do CBMPA. Foi projetado para transformar materiais de estudo
em conhecimento estruturado e persistente, acessível em qualquer dispositivo.

---

## Arquitetura do sistema

```
Nexus/                          ← Raiz do projeto (você está aqui)
├── CLAUDE.md                   ← Este arquivo
├── _entradas/                  ← PDFs novos chegam aqui
├── .claude/skills/             ← Skills do sistema
│
├── Nexus_Obsidian/             ← Vault do Obsidian (arquivos .md leves)
│   ├── MOC_CFO.md              ← Mapa geral de todo o conhecimento
│   └── Periodo0N/              ← Pastas por período do CFO
│       └── 0N_[SIGLA]/         ← Pastas por disciplina (criadas sob demanda)
│           ├── MOC_[SIGLA].md  ← Mapa da disciplina
│           ├── resumo_[SIGLA].md
│           ├── pontos_chave/
│           │   └── 0N_[assunto].md
│           └── VC0X/           ← Materiais de prova (criados sob demanda)
│               ├── revisao_VC0X.md
│               ├── audio_VC0X.txt
│               ├── simulado_VC0X.html
│               └── flashcard_VC0X.html
│
└── Nexus_Materiais/            ← PDFs originais (fora do Obsidian)
    └── Periodo0N/
        └── 0N_[SIGLA]/
```

---

## Caminhos absolutos

- **Raiz:** `~/Library/CloudStorage/GoogleDrive-rafaelras.94@gmail.com/Meu Drive/Nexus`
- **Entradas:** `Nexus/_entradas/`
- **Obsidian:** `Nexus/Nexus_Obsidian/`
- **Materiais:** `Nexus/Nexus_Materiais/`
- **Skills:** `Nexus/.claude/skills/`
- **Repositório GitHub:** `https://github.com/RafaelARKHE/Nexus`

---

## Quem sou eu

- **Nome:** CAD BM Rafael
- **Instituição:** CBMPA — Corpo de Bombeiros Militar do Pará
- **Curso:** CFO — Curso de Formação de Oficiais
- **Turma:** 16 | **Período atual:** 1º Período
- **Duração total:** 2 anos, 4 períodos
- **Local:** Academia Bombeiro Militar (ABM) — IESP, Marituba/PA
- **Supervisor:** 2º Ten QOABM Jean Carvalho Corrêa

---

## Disciplinas do 1º Período (19 no total)

| Sigla  | Disciplina                                |
|--------|-------------------------------------------|
| TFM    | TFM I                                     |
| NAT    | Natação Utilitária                        |
| DPIBM  | DPIBM                                     |
| HCBMPA | História do CBMPA                         |
| ETICA  | Ética e Cidadania                         |
| TLTI   | Telecomunicações e TI                     |
| IM     | Instrução Militar I                       |
| ANFI   | Anatomia e Fisiologia                     |
| APHR   | APH e Resgate I                           |
| DH     | Direitos Humanos                          |
| DC     | Direito Constitucional                    |
| DA     | Direito Administrativo I                  |
| LBI    | Legislação Básica Institucional           |
| FCIU   | Fundamentos do Combate ao Incêndio Urbano |
| FSALT  | Fundamentos de Salvamento Terrestre       |
| FSV    | Fundamentos de Salvamento Veicular        |
| FSAL   | Fundamentos de Salvamento em Altura       |
| FSAQ   | Fundamentos de Salvamento Aquático        |
| OAC    | OAC                                       |

---

## Skills disponíveis

### Fluxo Diário
| Skill | Gatilho | Função |
|---|---|---|
| `documento_entrada` | "documento novo" | Classifica e direciona PDFs novos |
| `leitura_aprofundada` | Automático ou "leitura aprofundada [disciplina]" | Processa PDF e gera resumo e pontos-chave |
| `resumo_geral` | Acionada pela leitura_aprofundada | Gera/atualiza resumo_[SIGLA].md |
| `pontos_chave` | Acionada pela leitura_aprofundada | Gera arquivos de pontos-chave por assunto |

### Fluxo de Prova
| Skill | Gatilho | Função |
|---|---|---|
| `revisao_prova` | "tenho prova de [disciplina]" | Skill-mãe — orquestra geração dos artefatos |
| `gerar_revisao` | Selecionado em revisao_prova | Documento unificado focado no escopo |
| `gerar_audio` | Selecionado em revisao_prova | Roteiro de áudio ~4.000 palavras / 30 min |
| `gerar_simulado` | Selecionado em revisao_prova | 30 questões interativas em HTML |
| `gerar_flashcards` | Selecionado em revisao_prova | Cartões de memorização interativos em HTML |

---

## Convenções do sistema

- **Pastas de disciplina:** prefixo numérico sequencial dentro do período — `01_LBI`, `02_ANFI`
- **Pastas criadas sob demanda** — nunca criar pasta ou arquivo vazio
- **Arquivos de prova:** `VC0X` — numerado pela avaliação
- **Arquivos .md:** kebab-case — `01_hierarquia-disciplina.md`
- **PDFs originais:** sempre em `Nexus_Materiais/` — nunca em `Nexus_Obsidian/`
- **Arquivos de estudo:** sempre em `Nexus_Obsidian/` — nunca misturar com PDFs

---

## Cabeçalho padrão Nexus (YAML frontmatter)

Todo arquivo gerado pelo sistema deve começar com:

```yaml
---
sistema: Nexus
tipo: [resumo | pontos_chave | revisao_prova | audio_prova | simulado | flashcard]
disciplina: [NOME_COMPLETO]
sigla: [SIGLA]
periodo: Periodo0N
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
---
```

---

## Como trabalhar comigo

- **Autonomia na forma** — estrutura, formato e organização são decisão sua
- **Perguntar quando faltar conteúdo essencial** — ex: situação real de um memorando
- **Material incompleto ou ambíguo** — perguntar antes de prosseguir
- **Nunca alucinar** — sinalizar incerteza explicitamente em vez de afirmar com falsa segurança
- **Nunca sobrescrever** — sempre acrescentar ao existente
- **Relatório ao final** — sempre informar o que foi feito em cada fluxo

---

## O que NÃO existe neste sistema

- Relatórios SISCOB
- Arquivos vazios — tudo é criado com conteúdo no momento certo
- PDFs em Nexus_Obsidian
- Arquivos .md em Nexus_Materiais
