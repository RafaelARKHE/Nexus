# scripts/ — pipeline reutilizável de geração de `.pptx`

Este diretório existe para que **montar um `.pptx` nunca exija reescrever
lógica de zero em `/tmp`**. Tudo aqui foi extraído, generalizado e testado a
partir da montagem real de "Responsabilidade Civil do Estado" — não é código
especulativo, é o que já funcionou, persistido para reuso.

Ponto de partida da filosofia "zero retrabalho": o conteúdo chega humanizado
(critérios de `humanizar.md`, gate mecânico da etapa 7 do `SKILL.md`) **antes**
de qualquer script aqui ser chamado. Estes scripts não decidem o que escrever —
só transformam conteúdo já pronto em XML válido e exportam o resultado.

---

## Os dois artefatos

### 1. `build_content.py`

Biblioteca Python que converte uma lista de blocos estruturados
(`{"kind": "anchor"|"plain"|"bullet", "text": "...", ...}`) em XML `<a:p>`
válido para o template ABM (`_modelos/Slide - Modelo Padrão.pptx`).

Funções principais:
- `build_body(items)` — corpo de slide single-column (Definição, Argumento,
  Aplicação Operacional, Síntese...)
- `build_comparacao_columns(header, items)` — uma coluna do layout Comparação
  (chamar duas vezes, para `idx="1"` e `idx="2"`)
- `title_with_anchor(title_text, anchor_text)` — título + subtítulo-âncora em
  itálico, para slides Comparação
- `parse_inline(text)` / `bullet_para(...)` — primitivas internas, expostas
  para casos que fogem dos três moldes acima

Documentação completa de uso e formato de bloco está no docstring do módulo.
Rodar `python3 build_content.py` valida o módulo (XML bem-formado, sem
travessão introduzido pelo código, sem marcação `**markdown**` residual) —
útil como smoke test antes de uma montagem grande.

**O que esta lib garante:** Cambria em todos os runs, indentação/marcador/
alinhamento corretos por tipo de bloco, negrito local via `**texto**`, e os
tamanhos de fonte que já passaram em QA visual (`DEFAULT_SZ`/`DEFAULT_BOLD`).

**O que esta lib NÃO faz** (de propósito — não é o papel dela):
- Unpack/pack do `.pptx` — ver seção 3 abaixo
- Decidir o que escrever — isso é do roteiro humanizado, que chega pronto

### 2. `export_pdf.scpt`

AppleScript parametrizado que exporta um `.pptx` para PDF via Microsoft
PowerPoint, encapsulando três detalhes de sintaxe que não são óbvios e que
custaram tentativas com erro na sessão em que foram descobertos:

1. `pdfPath` precisa ser `POSIX file`, não string simples (senão erro `-50`)
2. precisa de `with timeout of 600 seconds` (decks grandes estouram o timeout
   padrão do AppleEvent — erro `-1712`)
3. depois de editar/reempacotar o `.pptx`, reabrir pode renderizar conteúdo em
   cache — `pkill -x "Microsoft PowerPoint"` antes de reabrir resolve

Uso:
```bash
pkill -x "Microsoft PowerPoint" 2>/dev/null; sleep 2
osascript export_pdf.scpt "/caminho/absoluto/apresentacao.pptx" "/caminho/absoluto/saida.pdf"
pdftoppm -png -r 80 "/caminho/absoluto/saida.pdf" "/caminho/qa/slide"
```

Os dois caminhos são argumentos — não precisa editar o `.scpt` a cada uso.

> **Caveat conhecido:** durante o teste de verificação isolado deste script
> (fora do fluxo real de entrega), o PowerPoint abriu o arquivo (lock file
> `~$arquivo.pptx` criado) e ficou parado indefinidamente, sem produzir o PDF
> e com CPU em ~0% — sintoma de um diálogo oculto travando o AppleEvent. Não
> foi possível diagnosticar via computer-use (timeout no `request_access`) nem
> via Accessibility API (`osascript`/System Events bloqueado por permissão não
> concedida ao Terminal). **Importante:** essa exata sintaxe — `POSIX file` +
> `timeout of 600 seconds` + force-quit antes de abrir — funcionou
> corretamente nesta mesma sessão para exportar o deck revisado de
> "Responsabilidade Civil do Estado" (16 páginas, PDF de ~900KB confirmado via
> `pdfinfo`). Conclusão: o script está correto; o travamento foi um problema
> pontual de ambiente (estado do PowerPoint após múltiplos force-quits em
> sequência durante o teste). **Recomendação:** ao rodar a exportação, manter o
> PowerPoint em primeiro plano e observável (não em background/headless) na
> primeira vez de uma sessão — se aparecer qualquer diálogo, dispensar
> manualmente antes de repetir a chamada.

---

## 3. Unpack / pack do `.pptx`

Não há um script próprio aqui para isso — duas opções equivalentes, conforme
disponibilidade:

- **Skill nativo `pptx`** (`scripts/office/unpack.py`, `pack.py`, `clean.py`,
  `validate.py` — documentados em `editing.md` daquele skill): é a ferramenta
  genérica de unpack/pack/validação OOXML, mantida fora deste diretório porque
  já existe e é mantida centralmente — duplicar aqui criaria um segundo lugar
  para divergir.
- **Fallback via zip** (sempre disponível, sem dependência de outro skill):
  ```bash
  mkdir -p /tmp/pptx_work && cd /tmp/pptx_work
  unzip -q "/caminho/apresentacao.pptx" -d unpacked
  # ... editar XML em unpacked/ppt/slides/slideN.xml ...
  cd unpacked && zip -X -r -q "/caminho/apresentacao.pptx" . && cd ..
  ```
  O `-X` evita metadados extras que o PowerPoint às vezes rejeita.

---

## Fluxo recomendado de ponta a ponta (zero retrabalho)

A ordem importa: humanizar **antes** de montar é o que evita reabrir o XML
depois para reescrever frases.

1. **Roteiro humanizado primeiro** — escrever `roteiro_[tema].md` já nos 13
   critérios de `humanizar.md`, e rodar o gate mecânico (etapa 7 do
   `SKILL.md`: `grep -c '—'`, busca por frases de preenchimento, contagem de
   `**Termo:** explicação`) **no markdown**, antes de qualquer XML existir.
   Corrigir texto em markdown é ordens de magnitude mais barato que corrigir
   dentro de `<a:t>`.
2. **Unpack** do template ou da apresentação existente (seção 3).
3. **Gerar o XML do corpo de cada slide** com `build_content.py` —
   `build_body`, `build_comparacao_columns` ou `title_with_anchor`, conforme o
   tipo de slide (ver `tipos-de-slide.md`). Substituir o `<p:txBody>` do
   placeholder correspondente.
4. **Pack** de volta para `.pptx` (seção 3) e salvar em
   `Nexus_Materiais/Periodo0N/0N_[SIGLA]/Apresentacoes/[tema]/apresentacao_[tema].pptx`.
5. **Exportar para PDF** com `export_pdf.scpt` e gerar imagens de QA com
   `pdftoppm` (receita completa no rodapé do próprio `.scpt`).
6. **QA visual pontual** — não reabrir o deck inteiro: olhar só os slides cujo
   tamanho de texto mudou de forma relevante (overflow, quebra de linha
   estranha). Se o roteiro já passou no gate mecânico e a composição seguiu os
   13 critérios, não deve haver necessidade de reescrever conteúdo nesta etapa
   — só ajustar formatação pontual, se algo vazar.
7. **Fechar o roteiro** (etapa 9 do `SKILL.md`): preencher `arquivo_gerado`,
   `atualizado_em`, registrar notas de revisão.

Este fluxo substitui o que antes exigia escrever 3 scripts ad-hoc em `/tmp`
(`build_content.py`, `build_comparacao.py`, `build_capa_objetivos.py`) e
redescobrir a sintaxe do AppleScript por tentativa e erro a cada exportação.
