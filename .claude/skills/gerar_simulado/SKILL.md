---
name: gerar_simulado
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera simulado interativo em HTML
  com questões comentadas em formato de revisão — cada alternativa (certa ou errada)
  recebe explicação própria, com cartão de referência técnica e parágrafo de
  aprofundamento conectando o tema a assuntos vizinhos. Acionada pela skill
  REVISAO_PROVA ou diretamente quando o usuário pedir "gerar simulado", "criar
  questões para prova", "simulado da VC0X". Funciona no Mac e iPhone via navegador.
---

# GERAR_SIMULADO

Sub-skill geradora do simulado interativo em HTML — formato de **revisão comentada**,
não apenas de teste de acerto/erro.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/simulado_VC0X.html`

---

## Fonte de dados

- `revisao_VC0X.md` da mesma avaliação
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica

---

## Especificações do simulado

- **Quantidade padrão: 15 questões** de múltipla escolha — usar outro número apenas se o
  usuário pedir explicitamente (ex: "faz um simulado de 10", "quero 30 questões")
- **Alternativas:** 5 por questão (A, B, C, D, E)
- **Nível:** integrado — questões que testam conexões entre conceitos, não memorização isolada
- **Distribuição:** cobrir os tópicos do escopo proporcionalmente, priorizando pares de
  conceitos confundíveis (ex: choque×colisão, primária×secundária, laminado×temperado) —
  são esses pares que mais aparecem em prova e que mais se beneficiam do formato comentado

---

## Comportamento interativo

- Ao clicar em uma alternativa, a questão é travada e exibe um **painel de revisão** com:
  1. **Banner de resultado** — confirma acerto/erro e identifica a alternativa correta
  2. **Análise de cada alternativa** — comentário individual das 5 opções (não só da
     escolhida), com a correta e a escolhida destacadas visualmente
  3. **Bloco "Para fixar"** *(quando houver dado técnico/definição que sustente a resposta)*
     — cartão destacado com a definição exata, número, sequência ou especificação cobrada
  4. **Bloco "Indo além desta questão"** *(quando houver conexão relevante)* — parágrafo
     que liga o tema a um assunto vizinho do mesmo escopo
- Após a revisão, botão "Próxima questão"
- Ao final: placar com total de acertos e percentual
- Botão "Refazer simulado" embaralha questões e alternativas e reinicia

---

## Diretrizes para o conteúdo de cada questão

### Comentário por alternativa (o coração do formato)

Cada uma das 5 alternativas — certa ou errada — recebe seu próprio comentário. Para as
erradas, não basta dizer "está errada": explicar **por que ela parece plausível** e **qual
conceito real ela está confundindo ou distorcendo**. Esse é o mecanismo central do formato:
transforma cada questão em até 5 microrrevisões, não em 1.

Padrão de redação:
- Certa: "Certa. [Por que está certa — conectando à definição/regra do material]."
- Errada: "Errada. [O que a alternativa afirma de plausível] — mas [onde ela inverte,
  confunde ou generaliza indevidamente um conceito real do escopo]."

### Bloco "Para fixar" (referência técnica)

Usar sempre que a resposta se apoiar em um dado preciso do material — definição fechada,
número/especificação técnica, sequência obrigatória, classificação. Transcrever o trecho
quase literalmente do `revisao_VC0X.md` ou `pontos_chave/`, em formato de citação destacada.
Repetir o mesmo texto-base em questões diferentes que toquem no mesmo dado reforça a fixação
por repetição — não tratar como redundância a evitar.

Omitir este bloco quando a questão for puramente interpretativa/situacional e não houver
um dado fechado para destacar.

### Bloco "Indo além desta questão" (aprofundamento)

Parágrafo curto que conecta o tema da questão a um conceito vizinho do mesmo bloco de
estudo — algo que não era exigido para acertar, mas que é related e cai em prova. Funciona
como o "parágrafo extra" comum em gabaritos comentados de banca: a questão termina, mas a
revisão continua um passo além. Priorizar conexões que:
- contrastem o conceito cobrado com seu par mais confundível
- liguem a etapa testada à etapa anterior/posterior do mesmo processo
- apontem onde o tema se cruza com outra disciplina (campo "Conexões com Outras
  Disciplinas" do `revisao_VC0X.md`, quando existir)

Omitir quando não houver conexão natural — não forçar uma ligação artificial.

### Distratores

Construir alternativas erradas que sejam, elas mesmas, conceitos reais do material aplicados
no contexto errado, invertidos ou generalizados sem critério — não invenções aleatórias. Um
bom distrator é aquele que, ao ser comentado, ensina algo.

### Linguagem

Formal e objetiva — padrão de prova institucional. Comentários em tom de revisão (explicam o
"porquê"), não de gabarito seco ("está errado porque sim").

---

## Compatibilidade Mac e iPhone

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Fonte mínima: 16px para texto, 18px para alternativas; comentários podem ser 14-15px
- Botões com altura mínima de 44px e padding adequado para toque
- Sem hover-only interactions — tudo deve funcionar com toque
- Testado para Safari iOS — sem APIs não suportadas
- Layout responsivo com max-width para desktop e fluido no mobile
- Painel de revisão deve ser escaneável: hierarquia visual clara entre banner, análise de
  alternativas, referência e aprofundamento (cores e rótulos diferenciados)

---

## Estrutura HTML

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Simulado — [DISCIPLINA] | VC0X</title>
  <!-- CSS inline — sem dependências externas -->
</head>
<body>
  <!-- Todo CSS e JS inline no mesmo arquivo -->
  <!-- Cada questão: opts com {text, correct, comment} + referencia? + aprofundamento? -->
  <!-- Painel de revisão: banner + varredura de alternativas + blocos opcionais -->
  <!-- Sem CDN, sem APIs externas — funciona offline -->
</body>
</html>
```

Estrutura de dados de cada questão (`QUESTIONS_RAW`):

```js
{
  q: "enunciado",
  opts: [
    { text: "...", correct: true|false, comment: "Certa/Errada. ..." },
    // 5 alternativas, cada uma com seu comentário
  ],
  referencia: "trecho técnico destacado (opcional)",
  aprofundamento: "parágrafo de conexão com assunto vizinho (opcional)"
}
```

---

## Regras críticas

- Arquivo deve funcionar offline — sem dependências de CDN ou APIs externas
- Todo CSS e JS inline no mesmo arquivo HTML
- Depende do arquivo `revisao_VC0X.md` — não gerar sem ele
- Nunca sobrescrever simulado existente da mesma VC — alertar o usuário
- Não inventar dados técnicos para preencher o bloco "Para fixar" — se o material não tiver
  um dado fechado para aquela questão, omitir o bloco
