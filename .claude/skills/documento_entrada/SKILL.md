---
name: documento_entrada
description: >
  Skill de entrada do sistema Nexus. Use sempre que o usuário disser "documento novo",
  "chegou material", "novo PDF", ou qualquer variação indicando que há um arquivo novo
  em _entradas/ para ser processado. Também acionar quando o usuário quiser apenas
  classificar um documento sem processar ("só direcionar"). Esta skill é o portão
  de entrada de todo o fluxo de estudo do Nexus — acione-a sempre que houver
  qualquer menção a novo material de estudo chegando ao sistema.
---

# DOCUMENTO_ENTRADA

Skill de entrada do sistema Nexus. Classifica, direciona e opcionalmente processa
novos documentos recebidos.

---

## Caminhos do sistema

- Entrada: `Nexus/_entradas/`
- Materiais originais: `Nexus/Nexus_Materiais/Periodo0N/0N_[SIGLA]/`
- MOC geral: `Nexus/Nexus_Obsidian/MOC_CFO.md`
- Skills: `Nexus/.claude/skills/`

---

## Modalidades de execução

### Modalidade 1 — Só classificar
**Gatilho:** "documento novo, só direcionar" ou "só classificar"

Executa apenas os Passos 1 e 2 abaixo. Encerra com relatório.

### Modalidade 2 — Classificar e processar (padrão)
**Gatilho:** "documento novo" sem especificação adicional

Executa todos os passos (1 a 3). Aciona LEITURA_APROFUNDADA automaticamente ao final.

### Modalidade 3 — Usuário informa a disciplina
**Gatilho:** "documento novo — [nome da disciplina]"

Usa a disciplina informada diretamente, sem etapa de identificação automática.

---

## Fluxo de execução

### Passo 1 — Leitura superficial
Para cada arquivo em `_entradas/`:
- Lê título, subtítulos, primeiros e últimos parágrafos apenas
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

## Relatório de encerramento

Ao final de qualquer modalidade, emitir relatório com:
- Arquivos processados e disciplinas identificadas
- Período atribuído a cada documento
- Pastas criadas (se houver)
- MOC atualizado
- Próxima ação (leitura aprofundada pendente ou já acionada)

---

## Regras críticas

- Nunca sobrescrever arquivo existente na pasta destino
- Sempre usar prefixo numérico sequencial dentro do período correto
- Se `_entradas/` estiver vazia, informar o usuário e encerrar
- Sempre informar no relatório o que foi feito — o usuário não acompanha em tempo real
