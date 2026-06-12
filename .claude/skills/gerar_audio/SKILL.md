---
name: gerar_audio
description: >
  Sub-skill do fluxo de prova do sistema Nexus. Gera roteiro de áudio para
  escuta passiva no deslocamento. Acionada pela skill REVISAO_PROVA ou diretamente
  quando o usuário pedir "gerar áudio da prova", "áudio para dirigir", "versão
  para ouvir". Transforma o documento de revisão em texto corrido com linguagem
  fluida, redundância planejada e 8.000 a 10.000 palavras (32 a 40 minutos de escuta).
---

# GERAR_AUDIO

Sub-skill geradora do roteiro de áudio para escuta passiva.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/audio_VC0X.txt`

---

## Fonte de dados

- `revisao_VC0X.md` da mesma avaliação
- PDF original em `Nexus_Materiais/` apenas se necessário confirmar informação específica

---

## Cabeçalho padrão Nexus

```yaml
---
sistema: Nexus
tipo: audio_prova
disciplina: [NOME_COMPLETO]
sigla: [SIGLA]
periodo: Periodo0N
avaliacao: VC0X
duracao_estimada: 35min
palavras_alvo: 9000
criado_em: [DATA DD/MM/AAAA]
versao: 1.0
---
```

---

## Especificações técnicas

- **Extensão alvo: 8.000 a 10.000 palavras** — abaixo de 8.000 o áudio fica curto demais
- **Velocidade de referência:** ~250 palavras/minuto — taxa REAL medida de reprodução TTS
  (calibrada em 12/06/2026 com o áudio de DA VC01: 4.000 palavras renderam apenas ~16
  minutos, não os 30 estimados pela referência antiga de 133 wpm)
- **Duração estimada:** 32 a 40 minutos
- **Formato:** texto corrido em `.txt` — sem listas, sem marcadores, sem headers
- **Como chegar à extensão sem encher linguiça:** além do `revisao_VC0X.md`, puxar os
  `pontos_chave/*.md` da disciplina — detalhamentos, exemplos práticos, súmulas, tabelas
  comparativas e "Pontos de Atenção" viram parágrafos explicados com calma. A redundância
  planejada (retomadas, recapitulações por bloco) também é parte legítima da extensão

---

## Diretrizes de linguagem

### Tom
- Linguagem falada, não acadêmica
- Como se um colega estivesse explicando o conteúdo em voz alta
- Sem jargões desnecessários — quando usar termo técnico, explicar brevemente

### Estrutura narrativa
- Começar com uma introdução curta do que será coberto
- Progredir do mais simples para o mais complexo
- Encerrar com recapitulação dos pontos críticos

### Redundância planejada
- Estratégia central: dar um passo atrás antes de avançar
- Retomar conceitos anteriores ao introduzir novos
- Usar frases de transição explícitas:
  - "Voltando ao que vimos antes..."
  - "Isso se conecta com o conceito de..."
  - "Para consolidar: [recapitulação breve]"
  - "Seguindo essa linha de raciocínio..."

### Recuperação de atenção
- O ouvinte pode se distrair enquanto dirige — o texto deve permitir reentrada
- A cada novo bloco de conteúdo, retomar brevemente o que veio antes
- Nunca assumir que o ouvinte lembrou do que foi dito 5 minutos atrás

---

## Regras críticas

- Nenhuma lista ou marcador — tudo em texto corrido
- Nenhum símbolo Markdown — o arquivo será lido por TTS ou pelo próprio usuário em voz alta
- Manter contagem de palavras **entre 8.000 e 10.000** — verificar com `wc -w` após gerar
- Números, artigos de lei e siglas por extenso quando a leitura TTS exigir (ex: "artigo
  trinta e sete", "Lei número nove mil duzentos e trinta e quatro")
- Depende do arquivo `revisao_VC0X.md` — não gerar sem ele
