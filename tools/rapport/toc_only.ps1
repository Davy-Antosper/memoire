param([string]$Docx = 'Rapport_stage_FOMI_canevas.docx')
$ErrorActionPreference = 'Stop'
$src = (Resolve-Path $Docx).Path

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
try {
    $doc = $word.Documents.Open($src, $false, $false, $false)
    Write-Host ("ouvert, pages=" + $doc.ComputeStatistics(2))
    Write-Host ("TOC count=" + $doc.TablesOfContents.Count)
    if ($doc.TablesOfContents.Count -gt 0) {
        foreach ($t in $doc.TablesOfContents) { $t.Update() }
        Write-Host "TOC updated"
    }
    $doc.Repaginate()
    Write-Host ("pages apres=" + $doc.ComputeStatistics(2))
    $doc.Save()
    Write-Host "saved"
    $doc.Close(0)
} catch {
    Write-Host ("ERREUR: " + $_.Exception.Message)
    try { $doc.Close(0) } catch {}
} finally {
    $word.Quit()
    Start-Sleep -Seconds 2
}
"FINI"