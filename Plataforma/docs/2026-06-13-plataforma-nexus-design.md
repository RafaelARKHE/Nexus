# Plataforma Nexus — Documento de Design

> Data: 13/06/2026
> Status: aprovado para escrita de plano de implementação
> Origem: sessão de brainstorm (skill `superpowers:brainstorming`)

---

## 1. Propósito

A **Plataforma Nexus** é o **centro de comando do conhecimento** do CAD BM Rafael —
uma camada de visualização e navegação sobre o conhecimento que já vive nos arquivos
`.md` do Nexus. Nasce de uma dor concreta: o vault Obsidian cresce em pastas e não há
visão de conjunto, nem um lugar que **chame atenção para o que precisa ser estudado agora**.

A plataforma não serve apenas ao período atual do CFO — é projetada para acompanhar a
**carreira inteira** como bombeiro militar, à medida que o repositório de técnicas,
processos, fluxogramas e legislações cresce.

### Princípio inegociável

A **fonte da verdade continua sendo os arquivos `.md` versionados no Git** do Nexus.
A plataforma é uma **camada de leitura/visualização gerada a partir deles** — nunca
escreve conhecimento, nunca substitui o vault.

---

## 2. Arquitetura

### Natureza: hub estático, sem servidor

- HTML/CSS/JS puro — **sem build com npm, sem servidor rodando**.
- **Tema escuro**, no mesmo padrão visual já usado nos simulados/flashcards/fluxogramas
  do Nexus.
- Abre como **arquivo local** no navegador, tanto no Mac quanto no iPhone. A pasta
  sincroniza via Google Drive (igual ao resto do Nexus), então o acesso multi-dispositivo
  vem "de graça" — sem manter nada no ar.

### Restrição técnica decisiva: dados embutidos no HTML

No iOS, **todos os navegadores** (Safari, Chrome, Firefox) são obrigados a usar o motor
WebKit, que **bloqueia `fetch()` de arquivos `file://`**. Portanto:

> O índice de dados gerado a partir do vault + calendário é **embutido diretamente no
> HTML** (ex: `window.NEXUS_DATA = {...}`) pelo script de geração — **nunca** carregado
> via `fetch` de um JSON externo.

### Localização no sistema de arquivos

A plataforma vive **dentro do repositório Nexus**, em `Nexus/Plataforma/`:

- Um único Git, um único fluxo de sync.
- As skills do Nexus atualizam o índice e fazem commit junto com o resto, no fluxo
  `commit + push` já existente.
- Toda a plataforma — **incluindo este documento de design**, em `Nexus/Plataforma/docs/` —
  fica dentro do repositório Nexus e é versionada junto com o resto.
- A pasta separada "Plataforma Nexus" (no Google Drive, fora do repositório Nexus) deixa
  de ser usada e pode ser removida — nada da plataforma vive nela.

### Caminho de evolução

Se um dia for desejável acesso "de qualquer lugar sem depender da sincronização do Drive",
a mesma pasta estática pode ser publicada no GitHub Pages — **sem mudar a arquitetura de
dados**.

---

## 3. Modelo de dados (índice gerado)

Um script de geração varre `Nexus_Obsidian/` e consulta o Google Calendar para montar um
índice estruturado, que é embutido no HTML.

### Por disciplina

Derivado do frontmatter padrão Nexus (`sigla`, `disciplina`, `periodo`, `tipo`, `assunto`,
`prefixo`, `atualizado_em`, `versao`, `arquivo_origem`):

- **Resumo**: existe? versão? data de atualização.
- **Pontos-chave** agrupados por tema/lei (prefixo + assunto + lista de arquivos).
- **Materiais de prova por VC**: detecta quais artefatos existem em cada pasta `VCXX/`
  (revisão, áudio, simulado, flashcards, fluxograma).

### Radar (consulta ao Google Calendar)

Mesma fonte que a skill `qis_para_calendario` já escreve:

- **Aulas da semana atual** → lista de siglas com "aula esta semana".
- **VCs futuras** → lista de siglas com data da VC e dias restantes.

O radar é alimentado pelo fluxo semanal: ao atualizar o QIS no sistema, as matérias da
semana entram como prioridade (estudar antes da aula) e as matérias com VC marcada ganham
**destaque diferenciado**, que intensifica conforme a data se aproxima.

### Pensamentos

Lista a partir de `Pensamento/*.md` — tema, data e disciplinas relacionadas (via
`pensamentos_relacionados`).

### Fluxogramas / Legislação

Índices simples na primeira fase: lista dos arquivos `fluxograma_VC0X.html` existentes e
dos pontos-chave classificados como legislação/lei. Estrutura básica pronta para essas
seções evoluírem depois, mas exibição ainda mínima nesta fase.

---

## 4. Geração e atualização

Modelo **híbrido** (varredura completa + integração incremental):

### Skill nova: `atualizar_plataforma` (varredura completa)

Relê todo `Nexus_Obsidian/`, consulta o Calendar, regenera o índice embutido e os HTMLs
da plataforma do zero. Acionada com "atualizar plataforma". Útil após edições manuais no
Obsidian ou para reconstruir o estado completo.

### Integração incremental nas skills existentes

As skills que criam/atualizam conteúdo passam a, ao final do fluxo normal, atualizar as
partes correspondentes do índice (a disciplina que mudou, o radar da semana etc.) — sem
reescrever tudo. Skills afetadas:

- `leitura_aprofundada`, `pontos_chave`, `resumo_geral`
- `qis_para_calendario`
- `revisao_prova`
- `consolidar`

### Sincronização

Em ambos os casos, o resultado entra no **commit + push** já existente ao final do fluxo —
a plataforma sincroniza automaticamente como o resto do Nexus (sempre direto na `main`,
mensagens semânticas, prefixo `sync:` reservado ao hook).

---

## 5. Estrutura de telas

### Layout geral

Sidebar fixa de navegação + área central, tema escuro. Ícones geométricos minimalistas
(sem emojis coloridos), no espírito de um centro de comando técnico:

| Ícone | Seção |
|-------|-------|
| ⊚ | Radar |
| ⬢ | Mapa de Conhecimento |
| ⟁ | Fluxogramas |
| ⚖ | Legislação |
| ◈ | Pensamentos |

> Nota: a seção **Disciplinar foi deliberadamente excluída** — já é acompanhada pelo
> dashboard próprio da plataforma da ABM.

### ⊚ Radar (tela inicial)

Primeiro lugar ao abrir a plataforma. Destaca:

- Disciplinas com **aula esta semana** (estudar antes).
- **VCs chegando**, com urgência visual crescente conforme a data se aproxima.

Estado vazio quando não há nada chamando atenção ("nada chamando atenção esta semana").

### ⬢ Mapa de Conhecimento

- **Grade de cards por disciplina**, agrupada por período.
- Cada card mostra cobertura (nº de pontos-chave, versão do resumo) e destaque de radar
  quando aplicável.
- Disciplinas sem material aparecem **esmaecidas/diferenciadas** (equivalente ao
  `🔲 sem material` do `MOC_CFO.md` atual).
- Clique abre a **página da disciplina**: resumo geral, pontos-chave por tema/lei, e
  materiais de prova por VC (revisão / áudio / simulado / flashcards / fluxograma).

### ⟁ Fluxogramas · ⚖ Legislação · ◈ Pensamentos

Presentes na sidebar desde o início (a navegação faz parte da identidade do hub), mas na
**primeira fase exibem listagens simples** — links diretos para os HTMLs/arquivos
existentes. O tratamento visual dedicado que cada uma merece fica para **fases seguintes,
com specs próprias**.

---

## 6. Fases

- **Fase 1 (este spec)**: Radar e Mapa de Conhecimento completos; Fluxogramas, Legislação
  e Pensamentos como listagens simples. Skill `atualizar_plataforma` + integração
  incremental nas skills existentes.
- **Fases seguintes**: cada uma das seções de listagem simples ganha tratamento visual
  dedicado com sua própria identidade, em specs próprios.

---

## 7. Tratamento de erros e verificação

### Erros

- **Frontmatter ausente/inconsistente**: o script de geração ignora o arquivo problemático
  e o sinaliza no relatório final — não quebra a geração inteira. Alinhado ao princípio
  "nunca alucinar, sinalizar incerteza explicitamente".
- **Calendário sem eventos / indisponível**: o Radar exibe estado vazio, não erro.
- **Disciplina sem material**: card esmaecido/diferenciado, não erro.

### Verificação

- `atualizar_plataforma` e as integrações incrementais terminam com **relatório** do que
  foi gerado/atualizado (padrão de relatório do Nexus, incluindo confirmação de commit +
  push).
- A verificação prática é **abrir a plataforma no navegador** (Mac e iPhone) e confirmar
  visualmente. Não há testes automatizados, dado o caráter visual/estático do projeto.

---

## 8. Decisões registradas (e o que foi descartado)

- **Estático, sem servidor** (vs. servidor local na rede): escolhido por aproveitar a
  sincronização do Drive já existente e funcionar offline em qualquer dispositivo.
- **Dados embutidos no HTML** (vs. `fetch` de JSON): obrigatório pela restrição do WebKit
  no iOS para arquivos `file://`.
- **Plataforma dentro do repositório Nexus** (vs. pasta separada com Git próprio ou sem
  Git): um único fluxo de sync, coerente com "fonte da verdade são os `.md` versionados".
- **Sem "status de estudo" pessoal** (vs. campo de progresso/revisão espaçada): o estudo é
  por demanda, guiado pela proximidade da VC — o que importa não é "o que já estudei", e
  sim "o que merece minha atenção agora". O radar substitui o conceito de status.
- **Disciplinar fora da plataforma**: já coberto pelo dashboard da ABM.
