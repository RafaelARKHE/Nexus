---
name: documento_entrada
description: >
  Skill de entrada do sistema Nexus. Use sempre que o usuário disser "documento novo",
  "chegou material", "novo PDF", "novo arquivo", ou qualquer variação indicando que há
  um arquivo novo em _entradas/ para ser processado. Também acionar quando o usuário
  quiser apenas classificar um documento sem processar ("só direcionar"). Esta skill é
  o portão de entrada de todo o fluxo de estudo do Nexus — acione-a sempre que houver
  qualquer menção a novo material de estudo chegando ao sistema. Aceita PDF e PPTX.
---

# DOCUMENTO_ENTRADA

Skill de entrada do sistema Nexus. Classifica, direciona e opcionalmente processa
novos documentos recebidos.

---

## Formatos suportados

| Extensão | Ferramenta de leitura       |
|----------|-----------------------------|
| `.pdf`   | Skill nativa de leitura PDF |
| `.pptx`  | Skill `pptx` do sistema     |

Para qualquer outro formato encontrado em `_entradas/`, alertar o usuário e encerrar
sem mover o arquivo. Informar os formatos suportados.

---

## Caminhos do sistema

- Entrada: `Nexus/_entradas/`
- Materiais de estudo: `Nexus/Nexus_Materiais/Periodo0N/0N_[SIGLA]/`
- Documentos administrativos: `Nexus/Nexus_Materiais/Administrativo/`
- MOC geral: `Nexus/Nexus_Obsidian/MOC_CFO.md`
- MOC administrativo: `Nexus/Nexus_Materiais/Administrativo/MOC_Adm.md`
- Skills: `Nexus/.claude/skills/`

---

## Passo 0 — Classificação do tipo de documento

**Antes de qualquer outra etapa**, identificar se o documento é:

### Tipo A — Material de estudo
Conteúdo pedagógico de uma disciplina específica do CFO.
Exemplos: apostilas, slides de aula, notas de aula, roteiros de prática.
→ Segue para as **Modalidades 1, 2 ou 3** abaixo.

### Tipo B — Documento administrativo/institucional
Conteúdo institucional que não pertence a uma disciplina específica.
Exemplos: relações de docentes, calendários acadêmicos, portarias, boletins,
matrizes curriculares, resultados de avaliação, regulamentos.
→ Segue para a **Modalidade 4** abaixo.

**Como decidir:** se o documento serve para estudar uma disciplina → Tipo A.
Se serve como referência institucional ou registro do curso → Tipo B.

---

## Modalidades de execução

### Modalidade 1 — Só classificar (Tipo A)
**Gatilho:** "documento novo, só direcionar" ou "só classificar"

Executa apenas os Passos 1 e 2 abaixo. Encerra com relatório.

### Modalidade 2 — Classificar e processar (Tipo A, padrão)
**Gatilho:** "documento novo" sem especificação adicional

Executa todos os passos (1 a 3). Aciona LEITURA_APROFUNDADA automaticamente ao final.

### Modalidade 3 — Usuário informa a disciplina (Tipo A)
**Gatilho:** "documento novo — [nome da disciplina]"

Usa a disciplina informada diretamente, sem etapa de identificação automática.

### Modalidade 4 — Documento administrativo (Tipo B)
**Gatilho:** detecção automática no Passo 0, ou "documento novo, é administrativo"

Executa os Passos A1 e A2 abaixo. Não aciona LEITURA_APROFUNDADA.

---

## Fluxo Tipo A — Material de estudo

### Passo 1 — Leitura superficial
Para cada arquivo em `_entradas/`:
- Detecta o formato do arquivo (`.pdf` ou `.pptx`)
- Para `.pdf`: lê título, subtítulos, primeiros e últimos parágrafos
- Para `.pptx`: usa a skill `pptx` para extrair títulos dos slides e texto dos primeiros e últimos slides
- Objetivo único: identificar a disciplina e o período correspondente
- Consulta `MOC_CFO.md` para verificar as disciplinas disponíveis por período
- Age com autonomia — não requer confirmação do usuário para prosseguir

### Passo 2 — Direcionamento autônomo
Após identificação:

1. Verifica o período da disciplina identificada
2. Verifica se a pasta `Nexus_Materiais/Periodo0N/` existe — cria se necessário
3. Verifica se a pasta da disciplina existe em `Nexus_Materiais/Periodo0N/`
4. Se não existe: cria com o próximo prefixo numérico disponível dentro do período (`0N_[SIGLA]/`)
5. Move o arquivo para `Nexus_Materiais/Periodo0N/0N_[SIGLA]/`
6. Atualiza `MOC_CFO.md` com as informações básicas do documento

### Passo 3 — Processamento (Modalidade 2 apenas)
Aciona automaticamente a skill **LEITURA_APROFUNDADA** passando:
- Caminho do arquivo recém-direcionado
- Disciplina e período identificados

---

## Fluxo Tipo B — Documento administrativo

### Passo A1 — Identificação da categoria
1. Lê `MOC_Adm.md` para ver as categorias existentes em `Administrativo/`
2. Lê o documento superficialmente para entender sua natureza
3. Decide se ele se encaixa em alguma categoria existente
   - Se sim → usa essa categoria
   - Se não → define um nome descritivo para a nova categoria (substantivo no plural, ex: `Calendarios/`, `Normas/`, `Avaliacoes/`)

### Passo A2 — Direcionamento e registro
1. Se a pasta da categoria não existe → cria em `Nexus_Materiais/Administrativo/`
2. Move o arquivo para `Nexus_Materiais/Administrativo/[Categoria]/`
3. Atualiza `MOC_Adm.md`:
   - Se categoria nova: cria nova seção com descrição e registra o arquivo
   - Se categoria existente: adiciona o arquivo na tabela da categoria
4. Se o documento revelar informação estrutural (ex: lista de disciplinas de um período)
   → atualiza também `MOC_CFO.md` com as informações relevantes

---

## Relatório de encerramento

Ao final de qualquer modalidade, emitir relatório com:
- Tipo do documento identificado (A — estudo ou B — administrativo)
- Arquivos processados e disciplina/categoria identificada
- Período ou categoria atribuída
- Pastas criadas (se houver)
- MOCs atualizados
- Próxima ação (leitura aprofundada pendente, já acionada, ou nenhuma)

---

## Regras críticas

- Nunca sobrescrever arquivo existente na pasta destino
- Sempre usar prefixo numérico sequencial dentro do período correto (Tipo A)
- Nunca criar pastas administrativas vazias pré-definidas — só criar quando um arquivo chegar
- Se `_entradas/` estiver vazia, informar o usuário e encerrar
- Sempre informar no relatório o que foi feito — o usuário não acompanha em tempo real
