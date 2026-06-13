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
├── _modelos/                   ← Templates institucionais (.pptx etc. — nunca alterar)
├── .claude/skills/             ← Skills do sistema
│
├── Nexus_Obsidian/             ← Vault do Obsidian (arquivos .md leves)
│   ├── MOC_CFO.md              ← Mapa geral de todo o conhecimento
│   ├── Pensamento/             ← Raciocínio consolidado (criada sob demanda)
│   │   ├── MOC_Pensamentos.md  ← Mapa de todo raciocínio registrado
│   │   └── AAAA-MM-DD_tema.md  ← Arquivos de pensamento consolidado
│   ├── Disciplinar/            ← Anotações de comportamento escolar e justificativas
│   │   ├── MOC_Disciplinar.md  ← Painel: anotações, descontos, padrões de reincidência
│   │   ├── base/               ← CEDCBMPA Livro IV, Anexo I (descontos), Manual do Aluno, guia de justificativa
│   │   └── anotacoes/          ← Uma anotação por arquivo: AAAA-MM-DD_CODIGO_anotacao-NNN.md
│   └── Periodo0N/              ← Pastas por período do CFO
│       └── 0N_[SIGLA]/         ← Pastas por disciplina (criadas sob demanda)
│           ├── MOC_[SIGLA].md  ← Mapa da disciplina
│           ├── resumo_[SIGLA].md
│           ├── pontos_chave/
│           │   └── 0N_[assunto].md
│           ├── Apresentacoes/  ← Roteiros de trabalhos/seminários (criada sob demanda)
│           │   └── roteiro_[tema].md
│           └── VC0X/           ← Materiais de prova (criados sob demanda)
│               ├── revisao_VC0X.md
│               ├── audio_VC0X.txt
│               ├── simulado_VC0X.html
│               ├── flashcard_VC0X.html
│               └── estudo_de_caso_VC0X.html   ← provas com processo (XABCDE etc.)
│
└── Nexus_Materiais/            ← PDFs originais e binários gerados (fora do Obsidian)
    ├── Disciplinar/            ← Manual do Aluno (PDF) e prints originais de anotações
    │   └── anotacoes/          ← AAAA-MM-DD_CODIGO_anotacao-NNN.png
    └── Periodo0N/
        └── 0N_[SIGLA]/
            └── Apresentacoes/  ← .pptx finais de trabalhos/seminários (criada sob demanda)
                └── [tema]/
                    └── apresentacao_[tema].pptx
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
| `documento_entrada` | "documento novo" | Classifica e direciona novos documentos (PDF, PPTX, imagens QIS) |
| `qis_para_calendario` | Automático via `documento_entrada` ou "qis calendário" | Converte QIS em eventos no Google Calendar |
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
| `gerar_estudo_de_caso` | Selecionado em revisao_prova (provas com processo) | Casos interativos em HTML que treinam o processo passo a passo (XABCDE e afins) — abas Para fixar / Indo além / Glossário, tema escuro |

### Camada de Raciocínio
| Skill | Gatilho | Função |
|---|---|---|
| `consulta_nexus` | "nexus, [dúvida]" · "me explica [conceito]" · "tenho dúvida sobre [tema]" | Busca inteligente em 3 camadas — responde dúvidas com contexto do CBMPA |
| `consolidar` | "consolidar" · "salvar raciocínio" · "dúvida sanada" | Sintetiza sessão de consulta em arquivo permanente de Pensamento |

### Trabalhos e Apresentações
| Skill | Gatilho | Função |
|---|---|---|
| `slides_cfo` | "fazer slides", "criar apresentação", "trabalho em grupo", "seminário" | Gera apresentação `.pptx` institucional (modelo ABM) + roteiro rastreável em `Apresentacoes/` |

### Vida Disciplinar
| Skill | Gatilho | Função |
|---|---|---|
| `anotacao_disciplinar` | "fui anotado" · "justificar anotação" · print de anotação detectado pela `documento_entrada` | Verifica enquadramento/desconto no Anexo I do CEDCBMPA, entrevista sobre os fatos, classifica (justificável/atenuável/assumir) e redige justificativa no padrão e-mail militar |

---

## Convenções do sistema

- **Pastas de disciplina:** prefixo numérico sequencial dentro do período — `01_LBI`, `02_ANFI`
- **Pastas criadas sob demanda** — nunca criar pasta ou arquivo vazio
- **Arquivos de prova:** `VC0X` — numerado pela avaliação
- **Arquivos .md:** kebab-case — `01_hierarquia-disciplina.md`
- **PDFs originais:** sempre em `Nexus_Materiais/` — nunca em `Nexus_Obsidian/`
- **Arquivos de estudo:** sempre em `Nexus_Obsidian/` — nunca misturar com PDFs
- **VC nos documentos e eventos** = Verificação Corrente (nunca "Verificação de Conhecimento")
- **Templates institucionais:** sempre em `_modelos/` — nunca alterar estrutura, cores ou fontes
- **Apresentações (`.pptx`):** par binário/rastreável espelhando PDF↔resumo —
  o `.pptx` final fica em `Nexus_Materiais/.../Apresentacoes/[tema]/apresentacao_[tema].pptx`,
  o roteiro vivo e linkável ao MOC fica em `Nexus_Obsidian/.../Apresentacoes/roteiro_[tema].md`.
  Em caso de retrabalho, o roteiro ganha nova versão (`versao: 2.0` + histórico de
  versões) — o `.pptx` é substituído como entregável corrente, mas o roteiro preserva o histórico

### Sincronização com GitHub

O Nexus trabalha **sempre direto na `main`** — não criar branches `feat/`.

- **Todo fluxo que modifica arquivos termina com commit e push:** ao concluir
  qualquer skill ou tarefa que crie/altere arquivos, fazer commit com mensagem
  semântica no padrão do histórico (`feat(SIGLA): ...`, `fix: ...`, `docs: ...`)
  e em seguida `git push origin main`. O relatório final do fluxo confirma o push.
- **Prefixo `sync:` é reservado** ao hook automático — nunca usar em commits manuais.
- **Rede de segurança:** os hooks `SessionStart`/`SessionEnd` executam
  `.claude/hooks/sync_github.sh`, que commita restos não commitados com timestamp,
  faz `pull --rebase` e push. É contingência, não o caminho normal. Em caso de
  conflito o script aborta e registra em `.claude/hooks/sync.log` — avisar o
  usuário se isso aparecer.

### Mapeamento QIS → Sigla Nexus
Algumas abreviações usadas no QIS diferem das siglas do sistema:

| Sigla no QIS | Sigla Nexus | Disciplina              |
|--------------|-------------|-------------------------|
| EC           | ETICA       | Ética e Cidadania       |
| DA I         | DA          | Direito Administrativo I|
| IM I         | IM          | Instrução Militar I     |
| TFM I        | TFM         | TFM I                   |

---

## Cabeçalho padrão Nexus (YAML frontmatter)

Todo arquivo gerado pelo sistema deve começar com:

```yaml
---
sistema: Nexus
tipo: [resumo | pontos_chave | revisao_prova | audio_prova | simulado | flashcard | estudo_caso | pensamento | apresentacao | disciplinar]
disciplina: [NOME_COMPLETO]        # não usado nos tipos pensamento e disciplinar
sigla: [SIGLA]                     # não usado nos tipos pensamento e disciplinar
periodo: Periodo0N
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
pensamentos_relacionados: []       # opcional — preenchido quando existir raciocínio vinculado
---
```

---

## Como trabalhar comigo

- **Autonomia na forma** — estrutura, formato e organização são decisão sua
- **Perguntar quando faltar conteúdo essencial** — ex: situação real de um memorando
- **Material incompleto ou ambíguo** — perguntar antes de prosseguir
- **Nunca alucinar** — sinalizar incerteza explicitamente em vez de afirmar com falsa segurança
- **Nunca sobrescrever** — sempre acrescentar ao existente
- **Relatório ao final** — sempre informar o que foi feito em cada fluxo, incluindo a confirmação do commit + push para o GitHub

---

## O que NÃO existe neste sistema

- Relatórios SISCOB
- Arquivos vazios — tudo é criado com conteúdo no momento certo
- PDFs em Nexus_Obsidian
- Arquivos .md em Nexus_Materiais
