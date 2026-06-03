---
name: leitura_aprofundada
description: >
  Skill de processamento profundo do sistema Nexus. Use sempre que o usuário quiser
  processar um documento já classificado em Nexus_Materiais/, ou quando for acionada
  automaticamente pela skill documento_entrada. Gatilhos: "leitura aprofundada",
  "processar documento", "estudar material", ou acionamento automático pós-classificação.
  Esta skill orquestra a geração do RESUMO e dos PONTOS_CHAVE — acione sempre
  que houver necessidade de transformar um PDF bruto em material de estudo estruturado.
---

# LEITURA_APROFUNDADA

Skill orquestradora de processamento. Lê um documento já classificado e aciona
as skills RESUMO_GERAL e PONTOS_CHAVE em sequência.

---

## Caminhos do sistema

- Materiais originais: `Nexus/Nexus_Materiais/Periodo0N/0N_[SIGLA]/`
- Saída dos arquivos gerados: `Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/`
- MOC da disciplina: `Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/MOC_[SIGLA].md`

---

## Gatilhos

### Acionamento automático
Chamada pela skill DOCUMENTO_ENTRADA ao final da Modalidade 2.
Recebe: caminho do arquivo + disciplina + período confirmados.

### Acionamento manual
Usuário informa: "leitura aprofundada [nome do arquivo ou disciplina]"
Claude busca o arquivo em `Nexus_Materiais/Periodo0N/` e processa.

---

## Fluxo de execução

### Passo 1 — Carregamento do contexto
- Lê o arquivo PDF indicado integralmente
- Lê o `MOC_[SIGLA].md` da disciplina (se existir) para ter contexto do que já foi estudado
- Lê o `resumo_[SIGLA].md` da disciplina (se existir) para não duplicar conteúdo

### Passo 2 — Verificação da pasta de destino
- Verifica se a pasta do período existe em `Nexus_Obsidian/` — cria se necessário
- Verifica se a pasta da disciplina existe em `Nexus_Obsidian/Periodo0N/`
- Se não existe: cria `Nexus_Obsidian/Periodo0N/0N_[SIGLA]/`
- O prefixo numérico deve ser idêntico ao da pasta correspondente em `Nexus_Materiais/`

### Passo 3 — Orquestração
Aciona em sequência:
1. Skill **RESUMO_GERAL** — cria ou atualiza o resumo da disciplina
2. Skill **PONTOS_CHAVE** — cria arquivos de pontos-chave do conteúdo processado

### Passo 4 — Atualização dos MOCs
Após geração dos arquivos:
- Atualiza `MOC_[SIGLA].md` com os novos arquivos gerados
- Atualiza `MOC_CFO.md` com o novo status da disciplina

---

## Relatório de encerramento

Ao final, emitir relatório com:
- Documento processado
- Arquivos gerados (resumo e pontos-chave)
- Conexões identificadas com outras disciplinas
- Sugestões de melhoria para retenção daquele conteúdo específico

---

## Regras críticas

- O PDF original é lido apenas uma vez nesta skill — todo o fluxo de prova trabalha sobre os arquivos gerados
- Nunca sobrescrever conteúdo existente — sempre acrescentar
- Sempre verificar o MOC da disciplina antes de processar para evitar duplicação
