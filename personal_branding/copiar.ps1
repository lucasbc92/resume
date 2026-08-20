# Copia um bloco do arquivo de post direto para a area de transferencia,
# sem passar pelo terminal (que quebra linhas ao renderizar).
#
# Uso:
#   .\copiar.ps1              -> bloco [2], o corpo do post
#   .\copiar.ps1 4            -> bloco [4], o primeiro comentario
#   .\copiar.ps1 3 -Ver       -> mostra o bloco [3] em vez de copiar
#   .\copiar.ps1 -Arquivo outro_post.txt

[CmdletBinding()]
param(
    [Parameter(Position = 0)]
    [int]$Bloco = 2,

    [string]$Arquivo = 'linkedin_post_wame_link.txt',

    [switch]$Ver
)

$ErrorActionPreference = 'Stop'

$caminho = Join-Path $PSScriptRoot $Arquivo
if (-not (Test-Path $caminho)) {
    throw "Arquivo nao encontrado: $caminho"
}

$raw = Get-Content $caminho -Raw

# Blocos sao delimitados por:
#   ----- (linha de tracos)
#   [N] TITULO
#   ----- (linha de tracos)
#   conteudo
#   ----- (linha de tracos)
$padrao = "(?s)\[$Bloco\][^\r\n]*\r?\n-{40,}\r?\n(.*?)\r?\n-{40,}"
$m = [regex]::Match($raw, $padrao)

if (-not $m.Success) {
    throw "Bloco [$Bloco] nao encontrado em $Arquivo."
}

$texto = $m.Groups[1].Value.Trim()

if ($Ver) {
    $texto
    return
}

Set-Clipboard -Value $texto

$n = $texto.Length
Write-Host "Bloco [$Bloco] copiado: $n caracteres." -ForegroundColor Green

if ($Bloco -eq 2) {
    if ($n -gt 3000) {
        Write-Host "ESTOUROU o limite de 3.000 do LinkedIn em $($n - 3000)." -ForegroundColor Red
    }
    else {
        Write-Host "Folga ate o limite de 3.000: $(3000 - $n)." -ForegroundColor DarkGray
    }
    if ($texto -match 'https?://') {
        Write-Host "AVISO: ha 'https://' no corpo. O LinkedIn vai transformar em link." -ForegroundColor Yellow
    }
}

if ($texto -match 'X{6,}') {
    Write-Host "AVISO: ainda ha placeholder (XXXX...) neste bloco. Gere o link curto antes de publicar." -ForegroundColor Yellow
}
