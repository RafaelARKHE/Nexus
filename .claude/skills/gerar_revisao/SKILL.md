---
name: gerar_revisao
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera o documento de revisão
  unificado para uma avaliação específica. Acionada pela skill REVISAO_PROVA
  ou diretamente quando o usuário pedir "gerar revisão da prova", "documento
  de revisão para VC0X". Funde conteúdos de múltiplas unidades em um bloco
  uníssono de conhecimento integrado direcionado ao escopo da avaliação.
---

# GERAR_REVISAO

Sub-skill geradora do documento de revisão para avaliação.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/revisao_VC0X.md`

---

## Fonte de dados

- `resumo_[SIGLA].md` da disciplina
- Arquivos de `pontos_chave/` relevantes ao escopo informado
- Arquivos de `Pensamento/` relacionados ao escopo (passados pela REVISAO_PROVA quando encontrados)
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica

---

## Cabeçalho padrão Nexus

```yaml
---
sistema: Nexus
tipo: revisao_prova
disciplina: [NOME_COMPLETO]
sigla: [SIGLA]
periodo: Periodo0N
avaliacao: VC0X
escopo: [tópicos informados pelo usuário]
criado_em: [DATA DD/MM/AAAA]
versao: 1.0
---
```

---

## Estrutura do documento

```markdown
# Revisão — [Nome da Disciplina] | VC0X

---

## Base Conceitual
Fundamentos necessários para entender o escopo da prova.
Conceitos que sustentam tudo que vem a seguir.

## Conteúdo Integrado
Todos os tópicos do escopo unidos em bloco uníssono.
Sem separação por lei, unidade ou origem — conhecimento integrado.
Conexões entre tópicos explicitadas ao longo do texto.

## Pontos Críticos
O que o Nexus identificou como mais provável de ser cobrado.
Baseado na análise do material + escopo informado pelo usuário.

## Conexões com Outras Disciplinas
Apenas quando diretamente relevante para a prova.
Se REVISAO_PROVA identificou arquivos de Pensamento relacionados, incorporá-los aqui:
referencias explícitas ao raciocínio já construído sobre o tema.
Formato: [[Pensamento/AAAA-MM-DD_tema]] (apenas para arquivos que já existem)
```

---

## Diretrizes de conteúdo

- Linguagem direta e objetiva — sem introduções longas
- Integrar os tópicos — não listar um após o outro como blocos separados
- Explicitar as conexões entre conceitos ao longo do texto
- Priorizar o que o instrutor sinalizou + o que o Nexus identificar como crítico
- Adaptar a densidade ao tipo de matéria (legislação vs. técnico vs. doutrinário)

---

## Regras críticas

- Este arquivo é a base para GERAR_AUDIO e GERAR_SIMULADO — deve ser gerado primeiro
- Nunca substituir revisão existente da mesma VC — alertar o usuário se já existir
