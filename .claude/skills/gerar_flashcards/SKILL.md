---
name: gerar_flashcards
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera flashcards interativos em HTML
  para memorização de termos técnicos e conceitos. Acionada pela skill REVISAO_PROVA
  ou diretamente quando o usuário pedir "gerar flashcards", "cartões de memorização",
  "flashcard da VC0X". Carta vira ao clicar — frente com termo, verso com definição
  e contexto. Funciona no Mac e iPhone via navegador. Formato a ser iterado.
---

# GERAR_FLASHCARDS

Sub-skill geradora de flashcards interativos em HTML.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/flashcard_VC0X.html`

---

## Fonte de dados

- Arquivos de `pontos_chave/` relevantes ao escopo da avaliação
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica

---

## Especificações dos flashcards

- **Conteúdo:** termos técnicos, conceitos de memorização pura, definições legais, siglas
- **Frente do cartão:** termo ou pergunta curta
- **Verso do cartão:** definição + contexto de aplicação no CBMPA quando relevante
- **Quantidade:** todos os termos relevantes identificados nos pontos-chave

---

## Comportamento interativo

- Clique/toque no cartão: vira mostrando o verso com animação flip 3D
- Clique/toque novamente: volta para a frente
- Botões: "Sei" e "Revisar depois" — separa cartões dominados dos pendentes
- Ao final do baralho: mostra quantos foram para "Revisar depois" e oferece refazer apenas esses
- Botão "Embaralhar" para reiniciar em ordem aleatória

---

## Compatibilidade Mac e iPhone

- `<meta name="viewport" content="width=device-width, initial-scale=1.0">`
- Fonte mínima: 16px para texto dos cartões
- Cartão com tamanho adequado para leitura mobile (min-height: 200px)
- Botões "Sei" e "Revisar depois" com altura mínima de 44px
- Animação flip em CSS puro — sem bibliotecas externas
- Sem hover-only interactions — tudo funciona com toque
- Testado para Safari iOS — sem APIs não suportadas

---

## Estrutura HTML

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Flashcards — [DISCIPLINA] | VC0X</title>
  <!-- CSS inline com animação flip 3D -->
</head>
<body>
  <!-- Todo CSS e JS inline — sem dependências externas -->
  <!-- Funciona offline -->
</body>
</html>
```

---

## Observação de iteração

Formato inicial a ser testado e refinado após os primeiros usos reais.

---

## Regras críticas

- Arquivo deve funcionar offline — sem dependências externas
- Todo CSS e JS inline no mesmo arquivo HTML
- Animação de flip implementada em CSS puro
- Nunca sobrescrever flashcard existente da mesma VC — alertar o usuário
