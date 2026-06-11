---
name: anotacao_disciplinar
description: >
  Skill do espaço Disciplinar do sistema Nexus. Acionar sempre que o usuário disser
  "fui anotado", "nova anotação", "justificar anotação", "anotação na plataforma",
  "recebi uma anotação", ou quando a skill DOCUMENTO_ENTRADA detectar print de
  anotação da plataforma livro.cfo-cbmpa.com.br em _entradas/. Verifica enquadramento
  e desconto contra o Anexo I do CEDCBMPA, entrevista o cadete sobre os fatos,
  classifica (justificável/atenuável/assumir) e, havendo amparo, redige justificativa
  no padrão e-mail militar dentro do prazo de 48h. Também atualiza o desfecho quando
  o usuário informar "anotação anulada/mantida/retificada/deferida".
---

# ANOTACAO_DISCIPLINAR

Skill de tratamento de anotações de comportamento escolar do CFO. Transforma o print
da anotação em registro permanente, verifica a legalidade do lançamento e produz a
justificativa quando — e somente quando — houver amparo nos fatos.

---

## Caminhos do sistema

- Base de conhecimento: `Nexus/Nexus_Obsidian/Disciplinar/base/`
  - `01_regime-comportamento-escolar.md` — rito legal (Arts. 159-177 do CEDCBMPA)
  - `02_tabela-anotacoes-descontos.md` — Anexo I completo (códigos × descontos)
  - `05_guia-justificativa.md` — checklist, classificação e template do e-mail militar
- Registros: `Nexus/Nexus_Obsidian/Disciplinar/anotacoes/AAAA-MM-DD_CODIGO_anotacao-NNN.md`
- Prints originais: `Nexus/Nexus_Materiais/Disciplinar/anotacoes/AAAA-MM-DD_CODIGO_anotacao-NNN.png`
- Painel: `Nexus/Nexus_Obsidian/Disciplinar/MOC_Disciplinar.md`

---

## Modalidade 1 — Nova anotação (fluxo principal)

### Passo 1 — Extração do print
Ler a imagem e extrair: ID da anotação, status, oficial do dia, lançado por, infração
(código + descrição + pontos), data do fato, data de aprovação, prazo, descrição do fato.
Se algum campo estiver ilegível, perguntar ao usuário — nunca inferir.

### Passo 2 — Verificação formal
Conferir contra `02_tabela-anotacoes-descontos.md` e `01_regime-comportamento-escolar.md`:
1. Código existe no Anexo I?
2. Descrição lançada corresponde ao texto do código?
3. Desconto lançado bate com a tabela?
4. O fato descrito se encaixa no código (ou caberia em código mais leve)?
5. Quem observou o fato tinha competência para anotar (Art. 165)?
6. Notificação e prazo de 48h respeitados (Art. 169)?

**Qualquer divergência aqui é fundamento objetivo de justificativa ou de pedido de
retificação (Art. 172, II) — sinalizar com destaque no relatório.**

### Passo 3 — Entrevista sobre os fatos
Fazer 3 a 5 perguntas dirigidas (preferir AskUserQuestion quando disponível):
- O fato aconteceu como descrito?
- A responsabilidade era do cadete naquele momento (escala, equipe, distribuição de tarefas)?
- Havia ordem, autorização ou circunstância que ampare a conduta?
- Existe evidência ou testemunha (escala publicada, QIS, mensagem, colegas)?

**Regra absoluta: a justificativa nasce dos fatos informados pelo cadete. Nunca
inventar, embelezar ou sugerir versão não confirmada — faltar com a verdade é
transgressão, e pedido de revisão sem fundamento é anotável (G15, 1,0 pt).**

### Passo 4 — Classificação
Conforme `05_guia-justificativa.md`:
- **Justificável** — fato não ocorreu / responsabilidade não era do cadete / havia
  amparo → redigir defesa;
- **Atenuável** — fato ocorreu com contexto sério → redigir reconhecimento + contexto;
- **Assumir** — sem amparo → recomendar NÃO justificar, registrar a lição e encerrar.
  Explicar o porquê ao usuário (credibilidade + risco G15). A decisão final é dele.

### Passo 5 — Redação (se justificável ou atenuável)
Usar o template do `05_guia-justificativa.md`:
- Vocativo ao oficial correto (confirmar destinatário com o usuário na 1ª vez);
- Sempre 3ª pessoa ("este cadete"); fatos objetivos e verificáveis; 3-4 parágrafos;
- Fechar reconhecendo a autoridade do oficial e a legitimidade do ato;
- Assinatura: `CAD BM 557 Rafael` / `CFO BM - Turma 16`;
- **Formato de entrega obrigatório:** o texto final vai em **bloco de código**
  (cercado por ```), nunca em citação com `>`, com **cada parágrafo em linha única**
  (sem quebras manuais no meio da frase) — garante copiar/colar limpo na plataforma.
  Vale tanto no arquivo da anotação quanto na resposta ao usuário no chat;
- Entregar o texto pronto para colar na plataforma e alertar para o prazo de 48h.

### Passo 6 — Registro
1. Mover o print de `_entradas/` para `Nexus_Materiais/Disciplinar/anotacoes/`
   renomeado como `AAAA-MM-DD_CODIGO_anotacao-NNN.png` (data do fato);
2. Criar `Nexus_Obsidian/Disciplinar/anotacoes/AAAA-MM-DD_CODIGO_anotacao-NNN.md`
   com frontmatter padrão (tipo: disciplinar) e seções: dados do lançamento,
   verificação formal, versão dos fatos, classificação, justificativa enviada,
   desfecho (pendente), lição (pendente);
3. Atualizar `MOC_Disciplinar.md`: linha na tabela de anotações, soma de descontos,
   tabela de padrões por seção do Anexo I.

---

## Modalidade 2 — Atualização de desfecho

**Gatilho:** "anotação deferida/anulada", "mantiveram a anotação", "retificaram para [código]".

1. Localizar o arquivo da anotação em `Disciplinar/anotacoes/`;
2. Atualizar as seções **Desfecho** e **Lição** (perguntar ao usuário a lição se não
   estiver óbvia) e o `atualizado_em` do frontmatter;
3. Atualizar status e saldo no `MOC_Disciplinar.md` (anotação anulada → desconto sai
   da soma; retificada → ajustar código e valor).

---

## Relatório de encerramento

- Anotação registrada (nº, código, desconto) e resultado da verificação formal;
- Classificação atribuída e por quê;
- Justificativa redigida (texto completo) ou recomendação de assumir;
- Prazo restante para envio na plataforma;
- Arquivos criados/movidos e MOC atualizado;
- Padrão de reincidência, se houver (ex.: 2ª anotação da seção F no mês).

---

## Regras críticas

- Nunca redigir justificativa sem a versão dos fatos confirmada pelo cadete;
- Nunca recomendar justificar quando não há amparo — dizer claramente que o melhor é assumir;
- Nunca sobrescrever registro de anotação existente — desfecho e lição são acréscimos;
- Print original sempre em `Nexus_Materiais/` — nunca em `Nexus_Obsidian/`;
- Sempre alertar o prazo de 48h logo no início do atendimento.
