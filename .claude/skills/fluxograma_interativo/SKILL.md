---
name: fluxograma_interativo
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera um fluxograma interativo em
  HTML para disciplinas cujo conteúdo é um PROCESSO com ramificações (protocolos,
  fluxos de decisão, sequências obrigatórias) — ex: APH/XABCDE, combate a incêndio,
  salvamento, procedimentos administrativos por etapas. Acionada pela skill
  REVISAO_PROVA (opção dedicada a provas com processos) ou diretamente quando o
  usuário pedir "gerar fluxograma interativo", "treinar o processo", "fluxograma
  da VC0X", "casos da VC0X". O aluno escolhe um caso e conduz o processo passo a
  passo: cada acerto fixa a etapa no fluxo e revela a próxima; a alternativa
  errada explica a armadilha sem avançar. Funciona offline no Mac e iPhone via
  navegador, em tema escuro (padrão Nexus).
---

# FLUXOGRAMA_INTERATIVO

Sub-skill geradora do **fluxograma interativo** — treino ativo
de um **processo decisório** (protocolo/fluxo), não apenas memorização de fatos.

Use esta skill quando a matéria da prova é um **grande processo com ramificações**
e o professor cobra o domínio de **todo o fluxo** do início ao desfecho. Quando a
prova é de conteúdo factual/conceitual sem um processo central, prefira
GERAR_SIMULADO e GERAR_FLASHCARDS.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/fluxograma_VC0X.html`

Frontmatter (em comentário HTML no topo): `tipo: fluxograma`, `tema: escuro`.

---

## Fonte de dados

- `revisao_VC0X.md` da mesma avaliação (principal)
- `pontos_chave/*.md` da disciplina, quando precisar de detalhe de uma etapa
- PDF original em `Nexus_Materiais/` apenas para confirmar uma informação específica

Nunca alucinar conteúdo: todo número, sequência e classificação deve sair do
material processado. Conferir os dados sensíveis contra a fonte antes de fechar.

---

## Conceito do artefato

Cada **caso** é uma situação concreta da realidade da disciplina (uma ocorrência,
uma vistoria, um procedimento) que o aluno conduz do começo ao fim. O processo se
**constrói passo a passo**: a cada etapa surge uma pergunta com alternativas em
forma de balão; acertar fixa a etapa no fluxo (com seta de conexão) e revela a
próxima; errar mostra a armadilha e mantém o aluno na mesma etapa. Ao final, um
**desfecho** narra o resultado e o desempenho.

### Regras estruturais (não negociáveis)

1. **Tema escuro como padrão do Nexus** — todo artefato HTML gerado pelo sistema
   usa tema escuro (fundo grafite quente, vermelho institucional, verde/teal de
   apoio), para leitura confortável em ambientes escuros.
2. **Cada caso percorre o PROCESSO COMPLETO** — todas as etapas/letras do
   protocolo do início ao desfecho (ex: em APH, X→A→B→C→D→E, além de cena e
   biomecânica). A prova prática cobra o fluxo inteiro; nenhum caso pode pular
   etapas do processo.
3. **A alternativa correta acende na própria posição** — não realocar para o topo.
   Ao acertar, todas as alternativas são comentadas no lugar onde estão.
4. **Comentário por alternativa** — certa e erradas. As erradas devem ser
   **distratores fundamentados**: conceitos reais aplicados no contexto errado, que
   tentam fazer o aluno **pular uma etapa importante** ou inverter a técnica. Cada
   comentário explica *por que parece plausível* e *qual conceito real distorce*.
5. **Distribuição de casos por cobertura** — gerar tantos casos quantos forem
   necessários para varrer as situações distintas que podem ser cobradas
   (diferentes mecanismos, tipos de quadro, decisões-chave). O número de casos
   depende do número de situações possíveis no escopo, não de um valor fixo.

### Bloco de 3 abas (aparece após o aluno escolher a resposta)

Espelha os nomes do GERAR_SIMULADO para fixação por familiaridade:

1. **Para fixar** — o **CONCEITO do porquê** daquela conduta foi a correta (o
   princípio que a sustenta), **não** uma lista de dados nem um glossário. Responde
   "por que essa técnica, e não outra?".
2. **Indo além desta questão** — a **conexão** daquela decisão com outro
   conhecimento estudado (etapa anterior/posterior do mesmo processo, par conceitual
   confundível, cruzamento com outra disciplina).
3. **Glossário** — significado dos **termos técnicos** e **expansão das siglas**
   usados nas abas "Para fixar" e "Indo além". Esta aba é **gerada automaticamente**:
   um dicionário único (`GLOSSARIO`) é varrido contra o texto das duas primeiras
   abas, listando só os termos que de fato aparecem — assim nunca fica
   dessincronizada. Quando a etapa não tem jargão, exibir "Sem siglas ou termos
   técnicos nesta etapa".

Há ainda um **glossário completo** (todo o dicionário, com busca) acessível pela
tela inicial.

---

## Arquitetura técnica (data-driven)

Todo o conteúdo vive separado do motor de renderização — é o que permite
generalizar para qualquer disciplina trocando apenas os dados:

- `GLOSSARIO` — array `{t, d}` (termo, definição com expansão da sigla). Fonte única
  do glossário completo e da aba Glossário automática.
- `CASOS` — array de casos. Cada caso:
  `{ id, titulo, chamado, tags[], vinheta, passos[], desfecho }`.
- Cada passo:
  `{ etapa, pergunta, opcoes:[{t, ok, c}], fixar, alem }`
  onde `c` = comentário da alternativa, `fixar` = aba "Para fixar" (conceito),
  `alem` = aba "Indo além desta questão".
- `ET` — mapa etapa→cor (badge/borda).

Motor genérico (reutilizável entre disciplinas):
- embaralha as alternativas a cada passo;
- no acerto, marca a correta em verde **na posição**, comenta todas, monta o bloco
  de 3 abas e calcula a aba Glossário por varredura (`usaTermo` com fronteira de
  palavra, incluindo acentos `À-ÿ`; remove termo que é substring de outro presente);
- no erro, comenta apenas a alternativa errada e mantém o passo;
- progresso e casos concluídos salvos em `localStorage` (retoma no Mac/iPhone);
- nós já construídos ficam clicáveis para reabrir conduta + as 3 abas.

> **Modelo de referência:** o primeiro artefato deste tipo é
> `Periodo01/01_APHR/VC02/fluxograma_VC02.html` (APH, VC02). Reusar seu motor e
> CSS como base; só o conteúdo de `GLOSSARIO` e `CASOS` muda por disciplina.

---

## Diretrizes de conteúdo

### Casos
- Cada caso ambientado numa **situação real** da disciplina/profissão (no CBMPA:
  ocorrência, vistoria, procedimento operacional, relação de comando).
- A **vinheta** apresenta o cenário com os dados clínicos/operacionais que o aluno
  vai usar nas decisões.
- O conjunto de casos deve cobrir os **mecanismos/quadros distintos** do escopo,
  priorizando os que a prova confunde (ex., em APH: contuso×penetrante,
  hipovolêmico×neurogênico×obstrutivo, via aérea por edema×por queda da língua).

### Comentários de alternativa
- Correta: explicar o **porquê** da conduta, conectando ao princípio do processo.
- Erradas: distrator fundamentado — nomear o conceito real que está sendo aplicado
  fora de hora (ex: "abrir o A antes do X" é a armadilha de pular a etapa que mata
  mais rápido). Evitar "está errada porque sim".

### Aba "Para fixar"
- Conceito/princípio, em 2–3 frases. Responde "por que esta técnica?". Não listar
  números soltos como cartão de dados — isso é papel do glossário/material de revisão.

### Aba "Indo além desta questão"
- Conexão com um conceito vizinho do mesmo escopo, ou com outra disciplina (campo
  "Conexões com Outras Disciplinas" do `revisao_VC0X.md`, quando existir).

### Glossário (dicionário)
- Definições curtas e em linguagem simples; toda sigla expandida. Cobrir os termos
  que aparecem nas abas "Para fixar"/"Indo além" de todos os passos.

### Linguagem
- Formal e objetiva (padrão institucional). Comentários em tom de revisão (explicam
  o "porquê"), não de gabarito seco.

---

## Compatibilidade Mac e iPhone

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Tema escuro via variáveis CSS; fontes legíveis (texto ~14px, alternativas ~14.5px).
- Botões/alvos de toque com altura mínima de ~48px; sem interações hover-only.
- Testado para Safari iOS — sem APIs não suportadas (evitar lookbehind em regex).
- Layout fluido com `max-width` para desktop.

---

## Validação antes de fechar

Rodar uma checagem (mesma usada no modelo de referência) confirmando:
- cada caso percorre **todas** as etapas do processo;
- exatamente **1 alternativa correta** por passo e **comentário em todas**;
- **`fixar` e `alem`** presentes e substantivos em todo passo;
- a aba **Glossário** de cada passo casa termos reais do dicionário (ou exibe a
  mensagem de ausência quando a etapa não tem jargão);
- sem **chaves duplicadas** no `GLOSSARIO`.

---

## Encerramento (padrão Nexus)

Ao concluir, atualizar o `MOC_[SIGLA].md` (linha do artefato na seção VC0X) e
fazer **commit + push** na `main` com mensagem semântica (`feat(SIGLA): ...`),
confirmando o push no relatório final.
