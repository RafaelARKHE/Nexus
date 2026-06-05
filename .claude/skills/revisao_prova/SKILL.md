---
name: revisao_prova
description: >
  Skill-mãe do fluxo de prova do sistema Nexus. Acionar sempre que o usuário
  mencionar "tenho prova", "prova marcada", "preparar para prova", "vou ter avaliação"
  ou qualquer variação indicando uma avaliação próxima. Lê os arquivos já processados
  da disciplina e orquestra a geração modular dos artefatos de revisão. Trabalha
  prioritariamente sobre resumo_[SIGLA].md e pontos_chave/*.md — pode consultar
  o PDF original apenas para confirmar uma informação específica quando necessário.
---

# REVISAO_PROVA

Skill-mãe do fluxo de prova. Orquestra a geração dos artefatos de revisão
para uma avaliação específica.

---

## Caminhos do sistema

- Fonte: `Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/`
- Saída: `Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/VC0X/`

---

## Gatilho

Usuário informa:
1. Que tem uma prova marcada
2. Nome da disciplina
3. Escopo provável (em texto livre — ex: "vai cair LOB, Lei de Promoções e Código de Ética")

---

## Fluxo de execução

### Passo 1 — Leitura do material disponível
- Lê `resumo_[SIGLA].md` da disciplina
- Lê todos os arquivos em `pontos_chave/` da disciplina
- Mapeia o que está disponível vs. o que foi solicitado no escopo
- Se necessário confirmar alguma informação específica, pode consultar o PDF original em `Nexus_Materiais/Periodo0N/0N_[SIGLA]/`

### Passo 1.5 — Verificação de raciocínio consolidado
- Lê `Nexus/Nexus_Obsidian/Pensamento/MOC_Pensamentos.md`
- Verifica se existe pensamento consolidado relacionado ao escopo da prova (por tema ou disciplina)
- Se sim: carrega os arquivos de Pensamento relevantes identificados no MOC
- Guarda esse contexto para passar ao GERAR_REVISAO na etapa de execução

### Passo 2 — Criação da subpasta
- Verifica o último número de VC usado na disciplina
- Cria subpasta `VC0X/` dentro da pasta da disciplina no Nexus_Obsidian

### Passo 3 — Apresentação das opções
Antes de gerar qualquer arquivo, lista as sub-skills disponíveis:

```
Tenho prova de [DISCIPLINA] preparada. O que deseja gerar?

1. GERAR_REVISAO     — documento unificado focado no escopo da prova
2. GERAR_AUDIO       — roteiro de áudio (~30 min) para escuta no deslocamento
3. GERAR_SIMULADO    — 30 questões interativas em HTML
4. GERAR_FLASHCARDS  — cartões de memorização interativos em HTML
5. Todos

Digite o número ou números separados por vírgula.
```

### Passo 4 — Execução modular
Aciona apenas as sub-skills escolhidas pelo usuário, em sequência:
1. GERAR_REVISAO (sempre primeiro, se selecionado — os demais dependem dele)
2. GERAR_AUDIO
3. GERAR_SIMULADO
4. GERAR_FLASHCARDS

---

## Regras críticas

- Trabalhar prioritariamente sobre arquivos já processados — consultar PDF original apenas quando necessário para confirmar informação específica
- Sempre criar subpasta VC0X antes de gerar qualquer arquivo
- GERAR_REVISAO deve ser gerado antes dos demais (é a base para GERAR_AUDIO e GERAR_SIMULADO)
- Se o escopo informado pelo usuário não estiver coberto pelos arquivos existentes, alertar antes de prosseguir
