---
name: pontos_chave
description: >
  Skill de geração de arquivos de pontos-chave por assunto no sistema Nexus.
  Acionada automaticamente pela skill LEITURA_APROFUNDADA. Também acionar quando
  o usuário pedir "pontos-chave de [assunto]", "criar pontos-chave", "destacar
  pontos importantes". Gera um arquivo .md separado para cada assunto autônomo
  identificado no material, com prefixo numérico definindo a ordem lógica de estudo.
---

# PONTOS_CHAVE

Skill de geração de arquivos de pontos-chave por assunto de uma disciplina.

---

## Caminho dos arquivos gerados

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/pontos_chave/0N_[NOME_ASSUNTO].md`

---

## Critério de criação de arquivos

Um assunto vira arquivo próprio quando for um **conceito autônomo** — pode ser
estudado de forma independente sem depender de outro para fazer sentido.

Assuntos com forte interdependência são **agrupados no mesmo arquivo**.

Exemplos:
- Hierarquia e Disciplina → mesmo arquivo (interdependentes)
- Sistema Circulatório e Sistema Respiratório → arquivos separados (autônomos)

---

## Prefixo numérico — ordem lógica de estudo

Cada arquivo recebe um prefixo que define a sequência ideal de estudo:
- `01_[ASSUNTO].md` — deve ser estudado primeiro
- `02_[ASSUNTO].md` — depende do anterior para fazer sentido pleno
- E assim por diante...

O Claude Code define a ordem com base na dependência conceitual entre os assuntos.

---

## Cabeçalho padrão Nexus (YAML frontmatter)

```yaml
---
sistema: Nexus
tipo: pontos_chave
disciplina: [NOME_COMPLETO_DA_DISCIPLINA]
sigla: [SIGLA]
periodo: Periodo0N
assunto: [NOME_DO_ASSUNTO]
prefixo: [01, 02, 03...]
arquivo_origem: [NOME_DO_PDF]
criado_em: [DATA DD/MM/AAAA]
atualizado_em: [DATA DD/MM/AAAA]
versao: 1.0
moc_cfo: sim
moc_materia: sim
---
```

---

## Estrutura do arquivo

```markdown
# [Nome do Assunto]
> Disciplina: [SIGLA] | Período: Periodo0N | Origem: [NOME_DO_PDF] | Criado em: [DATA]

---

## Conceitos Fundamentais
Os conceitos base sem os quais o assunto não se sustenta.
Direto ao ponto — sem introdução.

## Detalhamento
Aprofundamento dos conceitos fundamentais.
Inclui exceções, casos especiais e nuances relevantes.

## Aplicação Prática
Como esse assunto aparece na realidade do CBMPA.
Exemplos operacionais e institucionais quando possível.

## Conexões
Links para outros arquivos do Obsidian relacionados.
Formato: [[Periodo0N/0N_SIGLA/nome-do-arquivo]]

## Pontos de Atenção
O que o Nexus identificou como crítico para prova ou aplicação prática.
```

---

## Diretrizes de conteúdo

- Filtro de relevância: incluir apenas o que é essencial para o CFO/CBMPA
- Agrupamento por afinidade conceitual — não por ordem de aparição no PDF
- Linguagem direta — sem rodeios
- Imagens: incluir quando for insubstituível (diagrama anatômico, mapa cartográfico)
  Formato: `![descrição](caminho/relativo/imagem.png)`

---

## Sincronização com o Drive

Após criar cada arquivo local de pontos-chave, fazer upload para o Google Drive:
- `parentId`: ID Drive da pasta `pontos_chave/` da disciplina (consultar `CLAUDE.md → IDs do Google Drive`)
- Se a pasta `pontos_chave/` ainda não existir no Drive: criar com `create_file` (`mimeType: application/vnd.google-apps.folder`, `parentId` da pasta da disciplina)
- Para cada arquivo:
  - `title`: nome exato do arquivo (ex: `05_choque-fisiopatologia.md`)
  - `contentMimeType`: `text/markdown`
  - `disableConversionToGoogleType`: `true`
- Pontos-chave são sempre arquivos NOVOS — não há duplicatas esperadas

---

## Regras críticas

- Nunca criar arquivo sem prefixo numérico
- Nunca sobrescrever arquivo existente — se assunto já existe, acrescentar nova seção com marcação de data e origem
- **Links `[[...]]` do Obsidian apenas para arquivos que JÁ EXISTEM no sistema** — o Obsidian cria arquivos vazios automaticamente ao detectar links não resolvidos, violando a regra de não criar arquivos vazios
- Para conexões com disciplinas ainda sem material processado, usar texto simples: `` `Periodo0N/??_SIGLA/arquivo` *(pendente — sem material processado)* ``
- Nomear arquivos em kebab-case: `01_sistema-circulatorio.md`
