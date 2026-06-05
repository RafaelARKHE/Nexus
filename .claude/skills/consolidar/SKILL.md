---
name: consolidar
description: >
  Skill de consolidação de raciocínio do sistema Nexus. Acionar quando o usuário
  indicar que uma dúvida foi sanada após sessão de consultas: "consolidar", "salvar
  raciocínio", "dúvida sanada", "quero registrar esse raciocínio". Sintetiza o
  pensamento percorrido (não transcreve a conversa) em arquivo permanente no Nexus.
  Atualiza MOC_Pensamentos.md ao final.
---

# CONSOLIDAR

Skill de síntese e registro permanente do raciocínio percorrido em uma sessão de consulta.

---

## Arquivo gerado

`Nexus/Nexus_Obsidian/Pensamento/[AAAA-MM-DD]_[tema-kebab-case].md`

---

## Caminho do MOC de referência

`Nexus/Nexus_Obsidian/Pensamento/MOC_Pensamentos.md`

---

## Gatilhos

- `consolidar`
- `salvar raciocínio`
- `dúvida sanada`
- `quero registrar esse raciocínio`

---

## Cabeçalho padrão Nexus

```yaml
---
sistema: Nexus
tipo: pensamento
tema: [NOME_DO_TEMA]
disciplinas: [SIGLA1, SIGLA2]
periodo: Periodo0N
criado_em: [DATA DD/MM/AAAA]
versao: 1.0
---
```

---

## Estrutura do arquivo gerado

```markdown
# [Tema do Raciocínio]
> Criado em: [DATA] | Disciplinas: [SIGLAS]

---

## Dúvida Original
A pergunta ou dúvida que deu início à sessão de consulta.
Uma ou duas frases — o ponto de partida.

## Caminho do Raciocínio
Síntese do percurso intelectual — não transcrição da conversa.
O que foi explorado, como cada conceito se conectou ao próximo,
quais desvios de raciocínio foram corrigidos ao longo do caminho.

## Conexões Identificadas
Links para arquivos do Nexus relacionados ao raciocínio.
Formato: [[Periodo0N/0N_SIGLA/nome-do-arquivo]]
**Apenas para arquivos que JÁ EXISTEM no sistema.**
Para arquivos inexistentes: `Periodo0N/??_SIGLA/arquivo` *(pendente)*

## Conclusão
Em primeira pessoa — é o meu raciocínio, não uma definição do livro.
O que entendi, como isso se encaixa no que já sabia, qual insight emergiu.

## Aplicação Prática ao CBMPA
Como esse entendimento se aplica ao contexto real do bombeiro militar.
Situações operacionais, institucionais ou de comando onde isso é relevante.

## Questões Abertas
Dúvidas que surgiram durante o processo e ficaram pendentes.
Cada item vira potencial nova sessão de consulta futura.
- [ ] [dúvida pendente 1]
- [ ] [dúvida pendente 2]
```

---

## Fluxo de execução

### Passo 1 — Extração do raciocínio
- Revisa a conversa da sessão atual
- Identifica: dúvida original, percurso, conexões, conclusão
- **Não transcreve** — sintetiza em linguagem própria, como se explicando a um colega

### Passo 2 — Geração do arquivo
- Cria o arquivo com nomenclatura `[AAAA-MM-DD]_[tema-kebab-case].md`
- Preenche todas as seções da estrutura
- Para a seção Conexões: verifica se cada arquivo existe antes de criar o link
  - Se existir: usa link Obsidian `[[Periodo0N/0N_SIGLA/arquivo]]`
  - Se não existir: texto simples `` `Periodo0N/??_SIGLA/arquivo` *(pendente)* ``

### Passo 3 — Atualização do MOC_Pensamentos.md
- Lê o arquivo atual
- Adiciona nova linha na tabela de Registro de Raciocínio:

  `| DD/MM/AAAA | [TEMA] | [SIGLAS] | [[Pensamento/AAAA-MM-DD_tema]] |`

- Atualiza o campo `atualizado_em` no frontmatter

### Passo 4 — Verificação de Temas Recorrentes (opcional)
Conta arquivos de Pensamento que abordam as mesmas disciplinas ou tema.
Se 3 ou mais arquivos convergem:
> "Identifiquei [X] arquivos de Pensamento que abordam [TEMA/DISCIPLINA]. Quer adicionar esse tema à seção 'Temas Recorrentes' do MOC_Pensamentos.md?"
Aguarda confirmação — não atualiza automaticamente.

---

## Regras críticas

- Sintetizar, nunca transcrever — o arquivo deve ser legível sem ver a conversa original
- A síntese deve estar em primeira pessoa — é o raciocínio do CAD BM Rafael
- Links `[[...]]` apenas para arquivos que JÁ EXISTEM no sistema
- Nunca sobrescrever arquivo existente — se o nome colidir, incrementar sufixo `_v2`
- Sempre atualizar MOC_Pensamentos.md ao final — nunca deixar arquivo de Pensamento sem registro no MOC
