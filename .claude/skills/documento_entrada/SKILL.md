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
- Detecta o formato do arquivo (`.pdf` ou `.pptx`)
- Para `.pdf`: lê título, subtítulos, primeiros e últimos parágrafos
- Para `.pptx`: usa a skill `pptx` para extrair títulos dos slides e texto dos primeiros e últimos slides
- Objetivo único: identificar a disciplina e o período correspondente
- Consulta `indice_geral.md` para verificar as disciplinas disponíveis por período
- Age com autonomia — não requer confirmação do usuário para prosseguir

### Passo 2 — Direcionamento autônomo
Após identificação:

1. Verifica o período da disciplina identificada
2. Verifica se a pasta `Nexus_Materiais/Periodo0N/` existe — cria se necessário (local e no Drive)
3. Verifica se a pasta da disciplina existe em `Nexus_Materiais/Periodo0N/`
4. Se não existe: cria com o próximo prefixo numérico disponível dentro do período (`0N_[SIGLA]/`) — local e no Drive (`create_file` com `mimeType: application/vnd.google-apps.folder`)
5. **Arquivo vindo do Drive `_entradas/`:** usar `copy_file` para copiar para a pasta correta em `Nexus_Materiais/` no Drive; baixar e salvar localmente também. Informar ao usuário que o arquivo original em `_entradas/` pode ser deletado manualmente.
6. **Arquivo já local:** mover para `Nexus_Materiais/Periodo0N/0N_[SIGLA]/` e fazer upload para o Drive via `create_file` com base64 ou texto conforme o formato.
7. Atualiza `MOC_CFO.md` / `indice_geral.md` com as informações básicas do documento e sincroniza com Drive

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
