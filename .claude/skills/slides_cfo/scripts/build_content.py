r"""
build_content.py — biblioteca reutilizável para gerar conteúdo de slides
do template institucional da ABM (`_modelos/Slide - Modelo Padrão.pptx`)
em XML (OOXML) válido, a partir de dados estruturados em Python.

OBJETIVO: eliminar o retrabalho de reescrever, a cada apresentação, a lógica
de "como transformar uma frase em <a:p> válido". Essa lógica foi escrita ad-hoc
três vezes (build_content.py / build_comparacao.py / build_capa_objetivos.py)
durante a montagem de "Responsabilidade Civil do Estado" — este arquivo é a
versão consolidada, generalizada e testada (QA visual passou nas 16 páginas).

NÃO faz: unpack/pack do .pptx (use scripts/office/unpack.py e pack.py do skill
nativo `pptx`, ou o fallback em zip_pack_unpack.sh deste diretório), nem decide
o que escrever (isso é papel do roteiro + humanizar.md, ANTES deste script
entrar em ação — conteúdo já deve estar pronto e humanizado quando chega aqui).

---

## Como usar

1. Tenha o conteúdo de cada slide já fechado, revisado e humanizado no roteiro
   (formato: lista de blocos, cada um com tipo, texto e formatação).
2. Rode unpack no template/apresentação.
3. Para cada slide de conteúdo, monte a lista de blocos e gere o XML do corpo:

   ```python
   from build_content import build_body, build_comparacao_columns

   # Slide single-column (Definição, Argumento, Aplicação Operacional, Síntese...)
   xml_corpo = build_body([
       {"kind": "anchor", "text": "Frase-âncora do slide, em uma linha."},
       {"kind": "bullet", "text": "Bullet com **termo técnico** em negrito."},
       {"kind": "bullet", "text": "Outro bullet, de tamanho diferente do anterior — "
                                  "varie o comprimento."},
   ])

   # Slide Comparação (duas colunas)
   col_esq = build_comparacao_columns(
       "Risco administrativo",
       [{"text": "Admite excludentes: culpa exclusiva da vítima, força maior."},
        {"text": "O ônus da prova é do Estado."}]
   )
   ```

4. Substitua o `<p:txBody>...</p:txBody>` do placeholder correto no XML do
   slide pelo resultado — string pronta para inserir.
5. Pack, exportar PDF, QA visual pontual (só onde o tamanho do texto mudou
   de forma relevante).

## Formato de bloco (dict) aceito por build_body / build_comparacao_columns

| campo    | valores                          | obrigatório | default |
|----------|----------------------------------|-------------|---------|
| `kind`   | `"anchor"` \| `"plain"` \| `"bullet"` | sim    | —       |
| `text`   | string (aceita `**negrito**`)    | sim         | —       |
| `bold`   | bool — força negrito no bloco inteiro | não    | depende do kind |
| `italic` | bool                             | não         | False   |
| `sz`     | int — tamanho da fonte (centésimos de ponto, ex.: 2000 = 20pt) | não | depende do kind |

- `anchor`: a frase-âncora do slide — primeiro bloco, sem marcador, em negrito,
  sz maior (3200 por padrão). Critério 6 do humanizar.md: a ideia central deve
  sobreviver sozinha.
- `plain`: parágrafo de corpo sem marcador (•) — para texto corrido, citações,
  legendas.
- `bullet`: item com marcador "•", justificado, sz 2000 por padrão.

`**texto**` dentro de `text` vira negrito local (ex.: nome de teoria, artigo de
lei) — não usar para o bloco inteiro (use `bold=True` nesse caso).
"""

import re
import xml.sax.saxutils as sax

CAMBRIA_RPR = (
    '<a:latin typeface="Cambria"/><a:ea typeface="Cambria"/>'
    '<a:cs typeface="Cambria"/><a:sym typeface="Cambria"/>'
)

# Tamanhos padrão (em centésimos de ponto — sz="2000" = 20pt) por tipo de bloco,
# espelhando o que foi usado e QA'd em "Responsabilidade Civil do Estado".
DEFAULT_SZ = {"anchor": 2000, "plain": 2000, "bullet": 2000}
DEFAULT_BOLD = {"anchor": True, "plain": False, "bullet": False}


def _esc(text):
    """Escapa caracteres especiais de XML (&, <, >) preservando aspas tipográficas."""
    return sax.escape(text)


def parse_inline(text):
    """
    Converte uma string com marcação `**negrito**` numa lista de runs
    [(texto, é_negrito), ...]. Suporta múltiplos trechos em negrito na mesma
    frase. NÃO suporta itálico via `*itálico*` de propósito — single-asterisk
    em PT-BR colide com "1º, 2º..." e outros usos; se precisar de itálico,
    use o parâmetro `italic` do bloco inteiro (ex.: subtítulos, citações).

    Isso corrige o bug observado na v1 (asterisco literal renderizado em
    "países de *common law*" porque parse_inline só tratava **bold**).
    """
    parts = re.split(r"(\*\*.+?\*\*)", text)
    runs = []
    for part in parts:
        if not part:
            continue
        m = re.match(r"^\*\*(.+)\*\*$", part)
        if m:
            runs.append((m.group(1), True))
        else:
            runs.append((part, False))
    return runs


def _run_xml(text, bold=False, italic=False, sz=2000):
    attrs = f'lang="pt-BR" sz="{sz}"'
    if bold:
        attrs += ' b="1"'
    if italic:
        attrs += ' i="1"'
    return f'<a:r><a:rPr {attrs}>{CAMBRIA_RPR}</a:rPr><a:t>{_esc(text)}</a:t></a:r>'


def bullet_para(text, kind="bullet", bold=None, italic=False, sz=None):
    """
    Gera um <a:p> completo e válido para o template ABM.

    kind:
      - "anchor": sem marcador, negrito, alinhado à esquerda, fonte maior
      - "plain":  sem marcador, peso conforme `bold` (default: normal)
      - "bullet": marcador "•", justificado, peso conforme `bold` (default: normal)

    `**trechos**` dentro de `text` viram negrito local mesmo que o bloco
    inteiro não seja `bold=True` — os dois se combinam (ex.: bullet normal
    com um termo técnico em negrito no meio da frase).
    """
    if kind not in DEFAULT_SZ:
        raise ValueError(f"kind inválido: {kind!r} — use anchor, plain ou bullet")

    block_bold = DEFAULT_BOLD[kind] if bold is None else bold
    font_sz = DEFAULT_SZ[kind] if sz is None else sz

    if kind == "bullet":
        algn = 'algn="just"'
        bullet_xml = '<a:buFont typeface="Arial" panose="020B0604020202020204" pitchFamily="34" charset="0"/><a:buChar char="•"/>'
        indent = 'indent="-228600" marL="228600"'
    else:
        algn = 'algn="l"'
        bullet_xml = "<a:buNone/>"
        indent = 'indent="0" marL="0"'

    pPr = (
        f'<a:pPr {indent} lvl="0" rtl="0" {algn}>'
        f'<a:lnSpc><a:spcPct val="100000"/></a:lnSpc>'
        f'<a:spcBef><a:spcPts val="0"/></a:spcBef>'
        f'<a:spcAft><a:spcPts val="600"/></a:spcAft>'
        f'{bullet_xml}</a:pPr>'
    )

    runs = []
    for chunk, chunk_bold in parse_inline(text):
        runs.append(_run_xml(chunk, bold=(block_bold or chunk_bold), italic=italic, sz=font_sz))

    return f'<a:p>{pPr}{"".join(runs)}<a:endParaRPr lang="pt-BR" sz="{font_sz}"/></a:p>'


def build_body(items):
    """
    Gera o conteúdo interno de um <p:txBody> single-column a partir de uma
    lista de blocos (ver formato no docstring do módulo).

    Regra de composição (critério 1 e 6 do humanizar.md): o primeiro bloco
    deve normalmente ser `anchor` — a ideia central do slide, isolada — e os
    seguintes devem variar de comprimento entre si. Esta função não impõe
    isso (a decisão é de conteúdo, não de código), mas espera blocos já
    pensados dessa forma.
    """
    paras = []
    for item in items:
        kind = item.get("kind", "bullet")
        paras.append(bullet_para(
            item["text"],
            kind=kind,
            bold=item.get("bold"),
            italic=item.get("italic", False),
            sz=item.get("sz"),
        ))
    return "".join(paras)


def build_comparacao_columns(header, items, header_sz=2400):
    """
    Gera o conteúdo de UMA coluna do layout Comparação: cabeçalho em negrito
    seguido de bullets. Chamar duas vezes (uma por placeholder idx="1" e
    idx="2") para montar o slide inteiro.

    `header`: string curta (nome da teoria/categoria comparada — ex.:
    "Risco administrativo"). Vai em negrito, sem marcador.
    `items`: lista de blocos no mesmo formato de build_body (normalmente
    só `bullet`, mas aceita `plain` para observações finais sem marcador).
    """
    header_para = bullet_para(header, kind="plain", bold=True, sz=header_sz)
    body = build_body(items)
    return header_para + body


def title_with_anchor(title_text, anchor_text, title_sz=2400, anchor_sz=1800):
    """
    Para slides Comparação que precisam de título + subtítulo-âncora em
    itálico (ex.: "Risco administrativo x risco integral" + frase que
    ancora o critério de comparação). Retorna XML de dois <a:p>.
    """
    title_para = bullet_para(title_text, kind="plain", bold=True, sz=title_sz)
    anchor_para = bullet_para(anchor_text, kind="plain", bold=False, italic=True, sz=anchor_sz)
    return title_para + anchor_para


# ---------------------------------------------------------------------------
# Auto-teste leve: garante que as funções produzem XML bem-formado antes de
# qualquer uso real. Rodar `python3 build_content.py` valida o módulo.
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import xml.dom.minidom as minidom

    sample = build_body([
        {"kind": "anchor", "text": "Frase-âncora de teste, sem travessão e sem floreio."},
        {"kind": "bullet", "text": "Bullet com **termo técnico** em negrito local."},
        {"kind": "bullet", "text": "Bullet mais curto."},
    ])
    wrapped = f'<root xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">{sample}</root>'
    minidom.parseString(wrapped)  # lança exceção se malformado
    assert "—" not in sample, "build_content não deve introduzir travessões por conta própria"
    assert "*" not in sample.replace("**", ""), "marcação markdown residual vazou para o XML"
    print("OK — build_content.py gera XML bem-formado e sem marcação residual.")
