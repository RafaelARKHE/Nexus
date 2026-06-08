---
name: slides_cfo
description: >
  Gera apresentações institucionais em .pptx para trabalhos, seminários e
  apresentações do CFO/CBMPA, com base no modelo padrão da ABM. Aplica estrutura
  narrativa por tipo de disciplina e tipologia de slides por função, redigindo o
  conteúdo já no registro humanizado e passando o roteiro por um gate mecânico
  objetivo (densidade de travessão, frases de preenchimento) antes de gerar o
  binário — não depende só da autopercepção de quem escreveu.
  Acionada por "fazer slides", "criar apresentação", "montar apresentação",
  "trabalho em grupo", "seminário" ou qualquer pedido de .pptx com conteúdo de
  disciplina do CFO.
---

# SLIDES_CFO

Gera apresentações institucionais em `.pptx` para o CFO/CBMPA, com base no
modelo padrão da ABM. Aplica estrutura narrativa e tipologia de slides por
função — redigindo o conteúdo **já no registro humanizado desde a primeira
linha**, em vez de escrever genérico e corrigir depois.

---

## Arquivos gerados

- `Nexus_Obsidian/Periodo0N/0N_[SIGLA]/Apresentacoes/roteiro_[tema].md` — roteiro vivo e rastreável, com cabeçalho Nexus
- `Nexus_Materiais/Periodo0N/0N_[SIGLA]/Apresentacoes/[tema]/apresentacao_[tema].pptx` — entregável final (binário)

> O par roteiro (`.md`) + apresentação (`.pptx`) espelha o padrão PDF↔resumo do
> sistema: o binário pesado fica fora do vault (em `Nexus_Materiais/`), e o
> conteúdo vivo, rastreável e linkável ao MOC da disciplina fica no Obsidian.

---

## Fonte de dados

- `resumo_[SIGLA].md` da disciplina — primeira fonte de conteúdo
- Arquivos de `pontos_chave/` relevantes ao tema
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica
- Material fornecido pelo usuário (enunciado de trabalho, apostila, conteúdo livre) —
  quando o instrutor não disponibilizar material sobre o tema, **sinalizar a lacuna
  explicitamente no roteiro** em vez de inventar conteúdo

---

## Template institucional

`_modelos/Slide - Modelo Padrão.pptx` — modelo oficial da ABM. Nunca alterar
estrutura de cabeçalho, cores ou fontes (ver regras fixas abaixo).

---

## Cabeçalho padrão Nexus (para `roteiro_[tema].md`)

```yaml
---
sistema: Nexus
tipo: apresentacao
disciplina: [NOME_COMPLETO]
sigla: [SIGLA]
periodo: Periodo0N
tema: [Tema/Unidade da apresentação]
tipo_entrega: [oral | escrito]
arquivo_gerado: Nexus_Materiais/Periodo0N/0N_SIGLA/Apresentacoes/[tema]/apresentacao_[tema].pptx
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
pensamentos_relacionados: []
---
```

---

## Ativação

Gatilhos que disparam esta skill:
- "fazer slides", "criar apresentação", "montar apresentação"
- qualquer pedido de `.pptx` com conteúdo de disciplina do CFO
- "apresentação para a turma", "trabalho em grupo", "seminário"

---

## Regras fixas — nunca negociáveis

| Regra | Valor |
|---|---|
| Template obrigatório | `_modelos/Slide - Modelo Padrão.pptx` |
| Fonte | Cambria em todos os slides |
| Cores | Vermelho institucional `C00000`, branco, preto — nunca alterar |
| Cabeçalho | Preservar exatamente: brasão CBMPA, logo Defesa Civil, escudo ABM, texto institucional |
| Output | Sempre `.pptx` — nunca HTML, nunca React, nunca PDF |
| Idioma | Português brasileiro, registro formal militar |

---

## Fluxo obrigatório — execute nesta ordem

### 1. Coletar informações mínimas

Antes de gerar qualquer slide, confirmar:
- **Disciplina** — nome exato e sigla Nexus
- **Tema/Unidade** — título da apresentação
- **Tipo de entrega** — oral (apresentação para a turma) ou escrito (entrega ao instrutor)
- **Conteúdo-fonte** — buscar primeiro em `resumo_[SIGLA].md` e `pontos_chave/`;
  complementar com material fornecido pelo usuário quando necessário
- **Instrutor e posto** — para a capa (se não informado, deixar placeholder visível)
- **Data** — mês/ano

Se qualquer item estiver faltando e for indispensável, perguntar uma vez. Nunca inventar.

### 2. Determinar o tipo de entrega

| Oral | Escrito |
|---|---|
| Máx. 4 blocos de informação por slide | Até 6 blocos por slide |
| Frase-âncora obrigatória por slide de conteúdo | Referências visíveis quando relevante |
| Texto curto — o apresentador completa oralmente | Texto mais denso — o slide é lido sem apresentador |
| Ritmo: ~1,5 min por slide de conteúdo | Sem restrição de ritmo |

### 3. Internalizar o registro de redação — ler `humanizar.md` ANTES de escrever

Esta etapa vem antes de qualquer rascunho — inclusive antes do roteiro.

`humanizar.md` não é um filtro de correção a ser aplicado depois que o conteúdo
já existe — é o **guia de composição** que define como cada frase nasce. Virar
checklist de auditoria pós-escrita gera retrabalho (escrever, depois reescrever
o que soou artificial). Em vez disso, os 13 critérios entram como regras de
redação desde a primeira linha do roteiro:
- já variar o número e o comprimento dos blocos por slide (nunca o mesmo padrão repetido)
- já cortar conclusões embutidas e qualificações defensivas em excesso
- já evitar frases de preenchimento ("vale ressaltar que...", "nesse contexto...")
- já escrever com verbo, sem o esquematismo de "termo: explicação"
- já variar o tom entre tipos de slide (Definição ≠ Aplicação Operacional ≠ Argumento)
- já decidir a quantidade de itens pelo conteúdo — não por padrões mecânicos (3 itens, label+dois pontos, tabela-síntese)
- já evitar travessão como conectivo universal e frases de efeito/aforismos —
  escrever como o cadete explicaria o assunto a um colega, com ponto, vírgula,
  "porque", "mas", não com floreio retórico (critério 13)

A pergunta-guia ao escrever cada bloco: **"um cadete que domina o assunto
escreveria assim?"** — não "isso soa natural?".

**Atenção:** os tiques de travessão e frase de efeito (critério 13) são os
mais difíceis de autodetectar — soam naturais para quem está escrevendo no
momento. Por isso, mesmo seguindo este guia à risca na composição, o gate
mecânico da etapa 7 abaixo **não é dispensável**.

### 4. Arquitetar o roteiro e registrar em `roteiro_[tema].md`

Ler `roteiro.md` e montar a sequência de slides **antes de escrever o conteúdo
de cada um**. Gravar essa arquitetura em
`Nexus_Obsidian/Periodo0N/0N_[SIGLA]/Apresentacoes/roteiro_[tema].md`, com o
cabeçalho Nexus acima — esse arquivo funciona como **plano revisável**: o cadete
aprova ou ajusta o roteiro antes de qualquer slide ser gerado. O próprio roteiro
já é redigido no registro internalizado na etapa 3 — não é um rascunho a ser
"humanizado" depois.

Estrutura mínima obrigatória:
1. Capa
2. Objetivos / Conteúdo a ser abordado
3–N. Slides de conteúdo (usar `tipos-de-slide.md` — para cada um, registrar o
   tipo escolhido, a frase-âncora e **de qual `resumo_[SIGLA].md` ou
   `pontos_chave/*.md` veio o conteúdo**)
N+1. Encerramento

### 5. Escolher o layout de cada slide

Para cada slide de conteúdo, ler `tipos-de-slide.md` e declarar o tipo antes de preencher.
**Proibido usar o mesmo layout mais de 3 vezes seguidas.**

### 6. Preencher o conteúdo

Escrever o conteúdo de cada slide já no registro definido na etapa 3 — não um
rascunho genérico a ser revisado depois. Regras de preenchimento:
- Cada slide responde a **uma pergunta**. Definir qual antes de escrever.
- Frase-âncora: a ideia central do slide em uma linha, posicionada no início do corpo.
- Negrito apenas em termos técnicos, artigos de lei e conceitos-chave — não em todo label.
- Variar comprimento de frases dentro do slide.
- Nunca terminar todo bullet com conclusão embutida.

### 7. Gate mecânico + auditoria final — sobre o roteiro, antes de gerar o `.pptx`

Duas verificações distintas, **ambas obrigatórias**, rodadas no texto do
roteiro (mais barato corrigir markdown do que reabrir XML depois):

**a) Gate mecânico (objetivo — não depende de "será que ficou bom?")**
- `grep -c '—'` no texto de cada slide de conteúdo: mais de 1 ocorrência é
  bandeira vermelha (critério 13 de `humanizar.md`; exceção: travessão de
  atribuição de citação direta)
- busca pelas frases de preenchimento do critério 8 ("vale ressaltar que...",
  "nesse contexto...") — qualquer ocorrência é para cortar
- contagem de bullets `**Termo:** explicação` — se for maioria, é excesso (critério 2)

Encontrou? Corrige ali mesmo, no roteiro, antes de seguir — não é uma
"observação para depois". Este gate existe porque os tiques de travessão e
frase de efeito **não são autodetectáveis por quem os escreveu**: soam
naturais no momento da escrita, e é exatamente por isso que escapam de uma
leitura "internalizada", por mais cuidadosa que tenha sido a composição.

**b) Auditoria de conjunto (de leitura — padrões que só aparecem em grupo)**
- Os slides de conteúdo têm o mesmo número/formato de bullets entre si? (critério 1)
- Algum padrão mecânico se repetiu sem querer — sempre 3 itens, mesmo layout
  em sequência? (critérios 9, 12, regra de sequenciamento de `tipos-de-slide.md`)
- O tom varia entre tipos de slide, ou tudo soa enciclopédico igual? (critério 5)
- Algum slide de síntese virou tabela-comparativa de 5+ linhas? (critério 7)
- Alguma frase de efeito ou aforismo passou pela leitura frase a frase? (critério 13)

Se a etapa 3 foi seguida à risca, a auditoria de leitura deve raramente
encontrar algo — mas o gate mecânico do item (a) roda sempre, mesmo assim.
Não pular nenhuma das duas, mesmo sob pressão de tempo.

### 8. Empacotar e entregar

Seguir o workflow de edição XML do skill `pptx` nativo (`editing.md`):
1. Unpack do template `_modelos/Slide - Modelo Padrão.pptx`
2. Duplicar slides conforme necessário
3. Reordenar no `presentation.xml`
4. Editar conteúdo slide a slide
5. `clean.py` → `pack.py`
6. QA visual: converter para imagens e inspecionar
7. Salvar o resultado em `Nexus_Materiais/Periodo0N/0N_[SIGLA]/Apresentacoes/[tema]/apresentacao_[tema].pptx`

### 9. Fechar o roteiro com o resultado final

Atualizar `roteiro_[tema].md`:
- preencher `arquivo_gerado` com o caminho final do `.pptx`
- atualizar `atualizado_em`
- registrar notas de revisão relevantes (ex.: pontos sinalizados para conferência
  pela equipe, lacunas de conteúdo assumidas, decisões de roteiro)

### 10. Nova versão em caso de retrabalho

Se a apresentação for revisada após feedback do instrutor ou nova rodada de
ajustes, **incrementar `versao` no roteiro** (1.0 → 2.0) e abrir uma seção
"Histórico de versões" registrando o que mudou e por quê. O `.pptx` em
`Apresentacoes/[tema]/` é sempre o entregável corrente (substituído a cada
nova versão), mas o roteiro preserva o histórico — nunca sobrescrever sem
deixar rastro da evolução.

---

## O que esta skill não faz

- Não altera o cabeçalho institucional
- Não muda cores ou fontes do template
- Não gera HTML, React ou qualquer formato que não seja `.pptx`
- Não inventa conteúdo — trabalha apenas com o material já curado no Nexus ou fornecido pelo usuário, sinalizando lacunas explicitamente
- Não inclui slides do tipo "Quadro-síntese comparativo" com tabelas completas — esse formato é marcador de IA; usar em vez disso o tipo `Síntese` de `tipos-de-slide.md`
