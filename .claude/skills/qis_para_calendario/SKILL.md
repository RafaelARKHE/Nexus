---
name: qis_para_calendario
description: >
  Skill do sistema Nexus que converte um Quadro de Instrução Semanal (QIS) em eventos
  no Google Calendar. Acionada automaticamente pela skill documento_entrada quando um
  QIS é detectado, ou manualmente com "qis calendário", "criar eventos do QIS",
  "colocar QIS no calendário". Suporta JPEG, PNG e PDF.
---

# QIS_PARA_CALENDARIO

Converte o Quadro de Instrução Semanal da Turma 16 em eventos no Google Calendar.
Lê a grade horária, agrupa slots consecutivos da mesma disciplina, aplica cores por
disciplina e cria todos os eventos em paralelo.

---

## Gatilhos

| Origem | Forma |
|--------|-------|
| Automático | Acionada por `documento_entrada` após arquivar um QIS |
| Manual | "qis calendário", "criar eventos do QIS", "colocar QIS no calendário" |

**Entrada esperada:** caminho do arquivo QIS (já arquivado em `Quadros_Instrucao/`).
Se acionada manualmente sem caminho, buscar o arquivo mais recente em
`Nexus_Materiais/Administrativo/Quadros_Instrucao/`.

---

## Configuração do calendário

| Parâmetro   | Valor                        |
|-------------|------------------------------|
| calendarId  | `rafaelras.94@gmail.com`     |
| timeZone    | `America/Belem`              |
| MCP         | Google Calendar (create_event / update_event) |

---

## Estrutura padrão de horários do QIS

### Atividade inicial
| Atividade                | Início | Fim   |
|--------------------------|--------|-------|
| Apresentação dos Cadetes | 06h50  | 07h30 |

### Slots de aula
| Slot | Início | Fim   |
|------|--------|-------|
| 1°   | 07h30  | 08h20 |
| 2°   | 08h20  | 09h10 |
| 3°   | 09h10  | 10h00 |
| —    | 10h00  | 10h20 | ← INTERVALO — não criar evento
| 4°   | 10h20  | 11h10 |
| 5°   | 11h10  | 12h00 |
| 6°   | 12h00  | 12h50 |
| —    | 12h50  | 14h00 | ← ALMOÇO — não criar evento
| 7°   | 14h00  | 14h50 |
| 8°   | 14h50  | 15h40 |
| 9°   | 15h40  | 16h30 |
| —    | 16h30  | 16h50 | ← INTERVALO — não criar evento
| 10°  | 16h50  | 17h40 |
| 11°  | 17h40  | 18h20 |
| 12°  | 18h20  | 19h10 |

**Os intervalos interrompem o agrupamento de slots.** Nunca criar um evento que
atravesse INTERVALO ou ALMOÇO — sempre dividir em dois eventos separados.

---

## Mapeamento de abreviações

### Disciplinas acadêmicas
| Sigla QIS  | SIGLA Nexus | Nome completo                            | colorId     |
|------------|-------------|------------------------------------------|-------------|
| EC         | ETICA       | Ética e Cidadania                        | 5 (Banana)  |
| ANFI       | ANFI        | Anatomia e Fisiologia                    | 2 (Sage)    |
| DA I       | DA          | Direito Administrativo I                 | 7 (Peacock) |
| DC         | DC          | Direito Constitucional                   | 9 (Blueberry) |
| TFM I      | TFM         | TFM I                                    | 11 (Tomato) |
| IM I       | IM          | Instrução Militar I                      | 6 (Tangerine) |
| FSV        | FSV         | Fundamentos de Salvamento Veicular       | 3 (Grape)   |
| FSAT       | FSAT        | Fundamentos de Salvamento Terrestre      | 4 (Flamingo)|
| FSAL       | FSAL        | Fundamentos de Salvamento em Altura      | 4 (Flamingo)|
| FSAQ       | FSAQ        | Fundamentos de Salvamento Aquático       | 4 (Flamingo)|
| APHR       | APHR        | APH e Resgate I                          | 2 (Sage)    |
| FCIU       | FCIU        | Fundamentos do Combate ao Incêndio Urbano| 10 (Basil)  |
| LBI        | LBI         | Legislação Básica Institucional          | 9 (Blueberry)|
| DH         | DH          | Direitos Humanos                         | 9 (Blueberry)|
| NAT        | NAT         | Natação Utilitária                       | 1 (Lavender)|
| TLTI       | TLTI        | Telecomunicações e TI                    | 5 (Banana)  |
| DPIBM      | DPIBM       | DPIBM                                    | 8 (Graphite)|
| HCBMPA     | HCBMPA      | História do CBMPA                        | 8 (Graphite)|
| OAC        | OAC         | OAC                                      | 8 (Graphite)|

### Atividades de formação/físicas
| Texto QIS                | Título do evento         | colorId      |
|--------------------------|--------------------------|--------------|
| APRESENTAÇÃO DOS CADETES | Apresentação dos Cadetes | 1 (Lavender) |
| TREINAMENTO ESPADIM      | Treinamento Espadim      | 8 (Graphite) |

### Marcadores especiais (aparecem como sufixo na célula do QIS)
| Marcador  | Significado             | Como usar no título do evento      | Observação de location     |
|-----------|-------------------------|------------------------------------|----------------------------|
| VC        | Verificação Corrente    | Incluir `— VC (Verificação Corrente)` antes do número de aulas | — |
| TAF       | Teste de Aptidão Física | Incluir `— TAF` no título          | — |
| Externo   | Atividade externa       | Incluir `· Externo` no título      | Usar `Externo — local a confirmar` |
| Teórica   | Modalidade teórica de VC | Usar `VC Teórica` no título       | — |

---

## Regras de processamento

### O que ignorar
- Qualquer célula com "À DISPOSIÇÃO DA COORDENAÇÃO"
- Linhas de INTERVALO e ALMOÇO
- Dias inteiramente compostos por "À DISPOSIÇÃO DA COORDENAÇÃO" (ex: domingos livres)

### Agrupamento de slots consecutivos
Slots consecutivos com **mesma disciplina E mesmo marcador** → um único evento.

**Horários finais dos grupos padrão:**
- Slots 1–3 (mesma disciplina): 07h30–10h00
- Slots 4–6: 10h20–12h50
- Slots 7–9: 14h00–16h30
- Slots 10–12: 16h50–19h10

Se o agrupamento for parcial (ex: slots 1–5 da mesma disciplina), usar os horários
exatos do slot inicial e do slot final do grupo (ex: 07h30–12h00).

### Formato do título do evento
```
SIGLA — Nome completo — Aulas XX–YY/ZZ
```
- `XX` = número da primeira aula do bloco
- `YY` = número da última aula (omitir se for aula única; usar `Aula XX/ZZ`)
- `ZZ` = total de aulas da disciplina no semestre
- Se não houver número visível no QIS: omitir numeração (ex: `Treinamento Espadim`)
- Marcadores especiais: inserir entre o nome e a numeração

**Exemplos de títulos corretos:**
- `FSV — Fundamentos de Salvamento Veicular — Aulas 19–21/30 · Externo`
- `DA I — Direito Administrativo I — VC (Verificação Corrente) — Aulas 27–29/30`
- `TFM I — TAF — Aulas 35–37/60`
- `ETICA — Ética e Cidadania — Aulas 07–09/20`
- `Treinamento Espadim`

### Location dos eventos
- Padrão: `ABM — IESP, Marituba/PA`
- Se marcador "Externo": `Externo — local a confirmar`

### Description dos eventos
```
[Nome completo da disciplina] · [N] aulas · Slots [X]–[Y] · CFO T16
```

---

## Fluxo de execução

### Passo 1 — Leitura do QIS
- Ler o arquivo com a ferramenta adequada ao formato:
  - `.jpeg` / `.jpg` / `.png` → ferramenta de leitura de imagem (visão)
  - `.pdf` → skill nativa de PDF
- Extrair: período da semana (datas), colunas por dia, conteúdo de cada slot

### Passo 2 — Mapeamento e agrupamento
Para cada coluna (dia da semana):
1. Percorrer os slots de cima para baixo
2. Mapear cada célula usando a tabela de abreviações acima
3. Agrupar slots consecutivos da mesma disciplina + marcador
4. Registrar ambiguidades: siglas não reconhecidas, células ilegíveis

### Passo 3 — Criação dos eventos em paralelo
- Lançar **todas** as chamadas `create_event` em um único bloco simultâneo
- Cada evento deve ter: `summary`, `startTime`, `endTime`, `colorId`, `location`,
  `description`, `calendarId`, `timeZone`
- Formato de data/hora: ISO 8601 sem offset (ex: `2026-06-08T07:30:00`), com
  `timeZone: America/Belem`

### Passo 4 — Relatório de encerramento
Emitir relatório com:
- Total de eventos criados
- Resumo por dia (dia, disciplinas, horários)
- Ambiguidades encontradas (siglas não reconhecidas, células ilegíveis)
- Sugestão de ação para cada ambiguidade

---

## Regras críticas

- **Nunca** criar evento para "À DISPOSIÇÃO DA COORDENAÇÃO"
- **Nunca** atravessar INTERVALO ou ALMOÇO em um único evento — sempre dois
- **Nunca** inventar número de aula se não estiver visível no QIS — omitir
- **Sempre** usar `VC` como "Verificação Corrente" — nunca "Verificação de Conhecimento"
- **Sempre** criar eventos em paralelo (bloco único de chamadas)
- Sinalizar explicitamente qualquer sigla não reconhecida — não criar evento com dado errado
- Se uma sigla nova aparecer no QIS, perguntar ao usuário o nome completo antes de criar
