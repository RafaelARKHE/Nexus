(*
export_pdf.scpt — exporta um .pptx para PDF via Microsoft PowerPoint (AppleScript).

USO:
    osascript export_pdf.scpt /caminho/absoluto/para/apresentacao.pptx /caminho/absoluto/para/saida.pdf

POR QUE ESTE ARQUIVO EXISTE:
A sintaxe que de fato funciona não é óbvia e custou duas tentativas com erro
na sessão em que foi descoberta:
  - "save theDoc in pdfPath as save as PDF" com `pdfPath` como string simples
    falha com "Erro de parâmetro (-50)" — PowerPoint exige um alias/POSIX file,
    não uma string de caminho.
  - sem "with timeout of 600 seconds", export de decks grandes estoura o
    timeout padrão do AppleEvent com erro -1712.
  - depois de editar e reempacotar o .pptx, reabrir no PowerPoint às vezes
    renderiza conteúdo em cache (versão antiga) — force-quit completo
    (`pkill -x "Microsoft PowerPoint"`) antes de reabrir resolve.

Este script já encapsula as três correções. Recebe os caminhos como
argumentos — não precisa editar o arquivo a cada uso.
*)

on run argv
    if (count of argv) < 2 then
        error "Uso: osascript export_pdf.scpt <entrada.pptx> <saida.pdf> — ambos caminhos absolutos"
    end if

    set pptxPath to POSIX file (item 1 of argv)
    set pdfPath to POSIX file (item 2 of argv)

    tell application "Microsoft PowerPoint"
        activate
        with timeout of 600 seconds
            open pptxPath
            delay 3
            set theDoc to active presentation
            save theDoc in pdfPath as save as PDF
            delay 2
            close theDoc saving no
        end timeout
    end tell
end run

(*
RECEITA COMPLETA DE EXPORTAÇÃO (rodar antes de chamar este script):

    pkill -x "Microsoft PowerPoint" 2>/dev/null; sleep 2
    osascript export_pdf.scpt "/caminho/apresentacao.pptx" "/caminho/saida.pdf"
    pdftoppm -png -r 80 "/caminho/saida.pdf" "/caminho/qa/slide"

O force-quit + sleep antes de abrir é o que evita o problema de cache de
conteúdo antigo quando o mesmo nome de arquivo já foi aberto antes.
*)
