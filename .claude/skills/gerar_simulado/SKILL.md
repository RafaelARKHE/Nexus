---
name: gerar_simulado
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera simulado interativo em HTML
  com 30 questões de múltipla escolha. Acionada pela skill REVISAO_PROVA ou
  diretamente quando o usuário pedir "gerar simulado", "criar questões para prova",
  "simulado da VC0X". Feedback imediato ao selecionar alternativa — verde para
  acerto, vermelho para erro, com justificativa pedagógica. Funciona no Mac e iPhone
  via navegador. Formato a ser iterado com base nos primeiros testes reais.
---

# GERAR_SIMULADO

Sub-skill geradora do simulado interativo em HTML.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/simulado_VC0X.html`

---

## Fonte de dados

- `revisao_VC0X.md` da mesma avaliação
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica

---

## Especificações do simulado

- **Quantidade:** 30 questões de múltipla escolha
- **Alternativas:** 5 por questão (A, B, C, D, E)
- **Nível:** integrado — questões que testam conexões entre conceitos, não memorização isolada
- **Distribuição:** cobrir todos os tópicos do escopo proporcionalmente

---

## Comportamento interativo

- Ao clicar em uma alternativa:
  - **Acerto:** alternativa fica verde + justificativa do porquê está correta
  - **Erro:** alternativa fica vermelha + justificativa do porquê está errada + indica a correta
- Após responder, mostrar botão "Próxima questão"
- Ao final: placar com total de acertos e percentual
- Botão "Refazer simulado" embaralha as questões e reinicia

---

## Compatibilidade Mac e iPhone

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Fonte mínima: 16px para texto, 18px para alternativas
- Botões com altura mínima de 44px e padding adequado para toque
- Sem hover-only interactions — tudo deve funcionar com toque
- Testado para Safari iOS — sem APIs não suportadas
- Layout responsivo com max-width para desktop e fluido no mobile

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
  <!-- Sem CDN, sem APIs externas — funciona offline -->
</body>
</html>
```

---

## Diretrizes para as questões

- Baseadas no conteúdo de `revisao_VC0X.md` — não inventar conteúdo externo
- Questões que testam compreensão e aplicação — não apenas definição
- Distratores plausíveis — alternativas erradas que fazem sentido superficialmente
- Justificativas pedagógicas claras — explicar o conceito, não apenas confirmar a resposta
- Linguagem formal e objetiva — padrão de prova institucional

---

## Observação de iteração

Formato inicial a ser testado e refinado com base nos primeiros usos reais.

---

## Regras críticas

- Arquivo deve funcionar offline — sem dependências de CDN ou APIs externas
- Todo CSS e JS inline no mesmo arquivo HTML
- Depende do arquivo `revisao_VC0X.md` — não gerar sem ele
- Nunca sobrescrever simulado existente da mesma VC — alertar o usuário
