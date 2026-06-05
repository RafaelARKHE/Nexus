---
name: consulta_nexus
description: >
  Skill de consulta inteligente do sistema Nexus. Acionar quando o usuário fizer
  qualquer pergunta sobre conteúdo do CFO/CBMPA. Gatilhos: "nexus, [pergunta]",
  "tenho uma dúvida sobre [tema]", "consulta nexus [assunto]", "me explica [conceito]",
  "o que o nexus sabe sobre [tema]". Busca nos arquivos do sistema em 3 camadas
  progressivas para não sobrecarregar o contexto. Projetada para consultas iterativas:
  várias trocas até a dúvida ser completamente sanada. Complementa com IA quando o
  Nexus não tem cobertura, sinalizando a fonte claramente.
---

# CONSULTA_NEXUS

Skill de consulta inteligente. Responde dúvidas sobre conteúdo do CFO/CBMPA buscando
progressivamente nos arquivos do Nexus sem sobrecarregar o contexto.

---

## Caminhos do sistema

- MOC geral: `Nexus/Nexus_Obsidian/MOC_CFO.md`
- MOC das disciplinas: `Nexus/Nexus_Obsidian/Periodo0N/0N_[SIGLA]/MOC_[SIGLA].md`
- Pensamentos: `Nexus/Nexus_Obsidian/Pensamento/MOC_Pensamentos.md`

---

## Gatilhos

- `nexus, [pergunta]` — chamada direta
- `tenho uma dúvida sobre [tema]`
- `consulta nexus [assunto]`
- `me explica [conceito]`
- `o que o nexus sabe sobre [tema]`
- Qualquer pergunta aberta sobre conteúdo do CFO/CBMPA

---

## Fluxo de execução — 3 Camadas Progressivas

### Camada 1 — Orientação (sempre executada)

Lê apenas `MOC_CFO.md`.
- Identifica quais disciplinas são relevantes para a dúvida
- Verifica quais têm material processado (status ✅)
- Decide se prossegue para Camada 2 ou sinaliza falta de cobertura imediatamente

### Camada 2 — Mapeamento

Para cada disciplina relevante com material processado:
- Lê `MOC_[SIGLA].md` da disciplina
- Mapeia quais arquivos de resumo e pontos-chave cobrem o tema

Lê `MOC_Pensamentos.md` em paralelo:
- Verifica se existe raciocínio consolidado relacionado ao tema
- Anota os arquivos de Pensamento relevantes para carregar na Camada 3

### Camada 3 — Carregamento seletivo

Carrega **apenas** os arquivos identificados como necessários:
- Máximo de 5 arquivos por consulta para preservar contexto
- Se necessário mais, priorizar por grau de relevância e informar ao usuário
- Ordem de prioridade: `pontos_chave` > `resumo` > `Pensamento` > PDF original

Após carregar: identifica lacunas de cobertura (conteúdo ausente no Nexus).

---

## Geração da resposta

### Estrutura

Texto único integrado — não lista de tópicos desconexos.
- Conecta ao contexto do bombeiro militar e do CBMPA quando relevante
- Prioriza o ângulo prático e operacional (como isso se aplica no serviço?)
- Referencia explicitamente o que veio do Nexus e o que é complemento de IA

### Sinalização de fontes

- **(Nexus)** — informação encontrada em arquivo do sistema
- **(IA)** — complemento gerado sem cobertura no Nexus
- **(Nexus + IA)** — informação parcialmente coberta

### Bloco de referências (ao final de cada resposta)

```
---
**Referências consultadas**
- [SIGLA] `pontos_chave/XX_nome-do-arquivo.md`
- [Pensamento] `Pensamento/AAAA-MM-DD_nome-tema.md`
```

---

## Modo iterativo

Esta skill é projetada para múltiplas trocas na mesma sessão.

- Após cada resposta, permanece disponível para perguntas de acompanhamento
- Não recarrega Camadas 1 e 2 para perguntas de seguimento sobre o mesmo tema
- Recarrega as camadas se o tema mudar significativamente
- Ao perceber que a sessão foi profunda e gerou conexões relevantes, sinaliza:
  > "Percorremos bastante conteúdo sobre [tema]. Quer consolidar esse raciocínio com a skill CONSOLIDAR?"

---

## Quando o Nexus não tem cobertura

Se a disciplina relevante não tiver material processado (status 🔲 no MOC_CFO):
- Informar claramente: *"Nexus não tem material processado para [DISCIPLINA]. A resposta a seguir é baseada em IA."*
- Responder usando conhecimento geral, sinalizando **(IA)** ao longo do texto
- Sugerir processar o material quando disponível

---

## Regras críticas

- Nunca alucinar — se não tiver certeza, sinalizar **(IA)** e indicar grau de confiança
- Não carregar mais de 5 arquivos por consulta
- Nunca gerar ou modificar arquivos — esta skill é somente leitura
- Sempre conectar ao contexto do CBMPA quando possível
