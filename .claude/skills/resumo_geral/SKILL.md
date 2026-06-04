---
name: resumo_geral
description: >
  Skill de geração e atualização do resumo de uma disciplina no sistema Nexus.
  Acionada automaticamente pela skill LEITURA_APROFUNDADA. Também acionar quando
  o usuário pedir explicitamente "atualizar resumo", "gerar resumo de [disciplina]"
  ou "resumo geral". Cria um documento evolutivo que cresce a cada novo material
  adicionado à disciplina — nunca substitui, sempre acrescenta.
---

# RESUMO_GERAL

Skill de geração do documento de resumo evolutivo de uma disciplina.

---

## Caminho do arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/resumo_[SIGLA].md`

---

## Comportamento

- Se o arquivo **não existe**: cria do zero
- Se o arquivo **já existe**: acrescenta novo conteúdo ao final, sem apagar o anterior
- O documento evolui a cada novo PDF adicionado à disciplina

---

## Cabeçalho padrão Nexus (YAML frontmatter)

Todo arquivo gerado deve começar com:

```yaml
---
sistema: Nexus
tipo: resumo
disciplina: [NOME_COMPLETO_DA_DISCIPLINA]
sigla: [SIGLA]
periodo: Periodo0N
arquivo_origem: [NOME_DO_PDF]
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
moc_cfo: sim
moc_materia: sim
---
```

---

## Estrutura do documento

```markdown
# Resumo — [Nome da Disciplina]

---

## [Título do Conteúdo Processado]
> Adicionado em: [DATA] | Origem: [NOME_DO_PDF]

### Pré-requisitos
O que preciso saber antes de estudar esse assunto.

### Termos Técnicos
Glossário dos termos essenciais — definição direta e objetiva.

### Resumo
Corpo dinâmico adaptado ao tipo de matéria:
- Legislação: estrutura por artigos e dispositivos principais
- Anatomia/Fisiologia: estrutura por sistemas e funções
- Operacional/Técnico: estrutura por procedimentos e critérios
- Doutrinário: estrutura por conceitos e princípios

### Conexões
Links para outros arquivos do Obsidian relacionados.
Formato: [[Periodo0N/0N_SIGLA/nome-do-arquivo]]

### Pontos de Atenção
O que o Nexus identificou como crítico para retenção.

---
```

---

## Diretrizes de conteúdo

- Objetivo: extrair o essencial para um cadete do CFO/CBMPA com tempo limitado
- Linguagem clara e direta — sem rodeios acadêmicos
- Foco no que é relevante para o contexto operacional e institucional do CBMPA
- Sempre que possível, conectar o conteúdo à realidade prática do bombeiro militar

---

## Regras críticas

- Nunca substituir conteúdo anterior — sempre acrescentar com marcação de data e origem
- Manter o cabeçalho YAML atualizado a cada nova versão (campos `atualizado_em` e `versao`)
- **Links `[[...]]` do Obsidian apenas para arquivos que JÁ EXISTEM no sistema** — o Obsidian cria arquivos vazios automaticamente ao detectar links não resolvidos, violando a regra de não criar arquivos vazios
- Para conexões com disciplinas ainda sem material processado, usar texto simples: `` `Periodo0N/??_SIGLA/arquivo` *(pendente — sem material processado)* ``
