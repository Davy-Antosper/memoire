# Tests E2E de l'API FOMI-Stock (smoke tests sur une instance locale).
# Usage : powershell -ExecutionPolicy Bypass -File scripts\e2e_api.ps1
$ErrorActionPreference = 'Stop'
$Base = if ($env:FOMI_API_URL) { $env:FOMI_API_URL.TrimEnd('/') } else { 'http://localhost:8080' }

$script:Pass = 0
$script:Fail = 0
$script:Failures = @()

function Invoke-Api {
    param(
        [string]$Method,
        [string]$Path,
        [string]$Body = $null,
        [string]$Token = $null,
        [string]$Accept = 'application/json'
    )
    $curlArgs = @('-s', '--max-time', '20', '-X', $Method, "$Base$Path",
                  '-H', "Accept: $Accept", '-w', "`n%{http_code}")
    if ($Token) { $curlArgs += @('-H', "Authorization: Bearer $Token") }
    $tmp = $null
    if ($Body) {
        # PowerShell 5.1 abime les guillemets dans les arguments natifs : on
        # passe le corps JSON par un fichier temporaire en UTF-8 sans BOM.
        $tmp = [System.IO.Path]::GetTempFileName()
        [System.IO.File]::WriteAllText($tmp, $Body, (New-Object System.Text.UTF8Encoding($false)))
        $curlArgs += @('-H', 'Content-Type: application/json', '--data-binary', "@$tmp")
    }
    try {
        $raw = & curl.exe @curlArgs
        if ($LASTEXITCODE -ne 0) { throw "curl a echoue pour $Method $Path" }
    } finally {
        if ($tmp) { Remove-Item $tmp -Force -ErrorAction SilentlyContinue }
    }
    $lines = @($raw -split "`n")
    $code = [int]$lines[-1].Trim()
    $content = ''
    if ($lines.Count -gt 1) {
        $content = ($lines[0..($lines.Count - 2)] -join "`n")
    }
    return [pscustomobject]@{ Code = $code; Body = $content }
}

function Check {
    param([string]$Name, [bool]$Condition, [string]$Detail = '')
    if ($Condition) {
        $script:Pass++
        Write-Host ("PASS  " + $Name)
    } else {
        $script:Fail++
        $script:Failures += $Name
        Write-Host ("FAIL  " + $Name + "  " + $Detail)
    }
}

function Login {
    param([string]$Username, [string]$Password)
    $r = Invoke-Api -Method POST -Path '/api/auth/login' -Body (@{
        username = $Username; password = $Password
    } | ConvertTo-Json -Compress)
    if ($r.Code -ne 200) { throw "Login $Username a echoue (HTTP $($r.Code)) : $($r.Body)" }
    return ($r.Body | ConvertFrom-Json)
}

Write-Host "== FOMI-Stock API E2E : $Base =="

# 1. Sante et authentification
$health = Invoke-Api -Method GET -Path '/actuator/health'
Check 'health UP' ($health.Code -eq 200 -and $health.Body -match '"status"\s*:\s*"UP"') "HTTP $($health.Code)"

$admin = Login 'admin' 'password'
Check 'login admin + token' ([bool]$admin.token -and $admin.role -eq 'ADMIN')
$zone = Login 'agent.zone' 'password'
$colline = Login 'agent.colline' 'password'

$unauth = Invoke-Api -Method GET -Path '/api/depots'
Check '401 sans token' ($unauth.Code -eq 401) "HTTP $($unauth.Code)"

$tok = $admin.token

# 2. Referentiel geographique Province -> Commune -> Zone -> Colline
$provinces = Invoke-Api -Method GET -Path '/api/provinces' -Token $tok
$provincesJson = $provinces.Body | ConvertFrom-Json
Check 'GET /api/provinces (3)' ($provinces.Code -eq 200 -and @($provincesJson).Count -eq 3) "HTTP $($provinces.Code)"

$communes = Invoke-Api -Method GET -Path '/api/communes' -Token $tok
$communesJson = $communes.Body | ConvertFrom-Json
Check 'GET /api/communes (5)' ($communes.Code -eq 200 -and @($communesJson).Count -eq 5) "HTTP $($communes.Code)"

$comPro = Invoke-Api -Method GET -Path '/api/provinces/1/communes' -Token $tok
$comProJson = $comPro.Body | ConvertFrom-Json
Check 'GET /api/provinces/1/communes (2)' ($comPro.Code -eq 200 -and @($comProJson).Count -eq 2) "HTTP $($comPro.Code)"

$communeId = @($comProJson)[0].id
$zonesCommune = Invoke-Api -Method GET -Path "/api/communes/$communeId/zones" -Token $tok
$zonesCommuneJson = $zonesCommune.Body | ConvertFrom-Json
Check 'GET /api/communes/{id}/zones' ($zonesCommune.Code -eq 200 -and @($zonesCommuneJson).Count -ge 1) "HTTP $($zonesCommune.Code)"

$zones = Invoke-Api -Method GET -Path '/api/zones' -Token $tok
$zonesJson = $zones.Body | ConvertFrom-Json
$zoneOk = $zones.Code -eq 200 -and @($zonesJson).Count -eq 4 `
    -and @($zonesJson)[0].communeNom -and @($zonesJson)[0].provinceNom
Check 'GET /api/zones (commune + province)' $zoneOk "HTTP $($zones.Code)"

$zonesPro = Invoke-Api -Method GET -Path '/api/provinces/1/zones' -Token $tok
$zonesProJson = $zonesPro.Body | ConvertFrom-Json
Check 'GET /api/provinces/1/zones (2)' ($zonesPro.Code -eq 200 -and @($zonesProJson).Count -eq 2) "HTTP $($zonesPro.Code)"

$collines = Invoke-Api -Method GET -Path '/api/collines' -Token $tok
$collinesJson = $collines.Body | ConvertFrom-Json
Check 'GET /api/collines' ($collines.Code -eq 200 -and @($collinesJson).Count -ge 6) "HTTP $($collines.Code)"

$collinesZone = Invoke-Api -Method GET -Path '/api/zones/1/collines' -Token $tok
$collinesZoneJson = $collinesZone.Body | ConvertFrom-Json
Check 'GET /api/zones/1/collines (2)' ($collinesZone.Code -eq 200 -and @($collinesZoneJson).Count -eq 2) "HTTP $($collinesZone.Code)"

# 3. Depots : uniquement PROVINCE et ZONE
$depots = Invoke-Api -Method GET -Path '/api/depots' -Token $tok
$depotsJson = $depots.Body | ConvertFrom-Json
Check 'GET /api/depots (9)' ($depots.Code -eq 200 -and @($depotsJson).Count -eq 9) "HTTP $($depots.Code)"
Check 'aucun depot COLLINE' (-not ($depots.Body -match '"niveau"\s*:\s*"COLLINE"'))
Check 'depots exposes communeNom' ($depots.Body -match '"communeNom"')

$depotZone = Invoke-Api -Method GET -Path '/api/depots/6' -Token $tok
$depotZoneJson = $depotZone.Body | ConvertFrom-Json
Check 'depot 6 converti en ZONE' ($depotZone.Code -eq 200 -and $depotZoneJson.niveau -eq 'ZONE' -and $depotZoneJson.zoneId) "HTTP $($depotZone.Code) / $($depotZoneJson.niveau)"

$depot404 = Invoke-Api -Method GET -Path '/api/depots/99999' -Token $tok
Check '404 depot inconnu' ($depot404.Code -eq 404) "HTTP $($depot404.Code)"

$method405 = Invoke-Api -Method DELETE -Path '/api/depots/1' -Token $tok
Check '405 methode non supportee' ($method405.Code -eq 405) "HTTP $($method405.Code)"

$collineRefusee = Invoke-Api -Method POST -Path '/api/depots' -Token $tok -Body '{"code":"DEP-E2E-C","nom":"Depot colline","niveau":"COLLINE","collineId":1}'
Check '400 depot COLLINE refuse' ($collineRefusee.Code -eq 400) "HTTP $($collineRefusee.Code)"

$rbac = Invoke-Api -Method POST -Path '/api/depots' -Token $zone.token -Body '{"code":"DEP-E2E-R","nom":"Interdit","niveau":"PROVINCE","provinceId":1}'
Check '403 agent.zone ne cree pas de depot' ($rbac.Code -eq 403) "HTTP $($rbac.Code)"

# 4. Tickets, saison, export et suivi public
$tickets = Invoke-Api -Method GET -Path '/api/tickets?page=0&size=5' -Token $tok
$ticketsJson = $tickets.Body | ConvertFrom-Json
Check 'GET /api/tickets pagine' ($tickets.Code -eq 200 -and $ticketsJson.content) "HTTP $($tickets.Code)"

$ticketsSaison = Invoke-Api -Method GET -Path '/api/tickets?saison=2026A&page=0&size=5' -Token $tok
Check 'GET /api/tickets?saison=2026A' ($ticketsSaison.Code -eq 200) "HTTP $($ticketsSaison.Code)"

$ticketsVide = Invoke-Api -Method GET -Path '/api/tickets?saison=1900Z&page=0&size=5' -Token $tok
$ticketsVideJson = $ticketsVide.Body | ConvertFrom-Json
Check 'filtre saison sans resultat' ($ticketsVide.Code -eq 200 -and [int]$ticketsVideJson.totalElements -eq 0) "HTTP $($ticketsVide.Code) total=$($ticketsVideJson.totalElements)"

$csv = Invoke-Api -Method GET -Path '/api/export/tickets.csv?saison=2026A' -Token $tok -Accept 'text/csv'
Check 'export CSV filtre par saison' ($csv.Code -eq 200 -and $csv.Body -match 'Saison') "HTTP $($csv.Code)"

$csvRefuse = Invoke-Api -Method GET -Path '/api/export/tickets.csv' -Token $tok -Accept 'application/json'
Check '406 export CSV avec Accept JSON' ($csvRefuse.Code -eq 406) "HTTP $($csvRefuse.Code)"

if (@($ticketsJson.content).Count -gt 0) {
    $numero = @($ticketsJson.content)[0].numeroTicket
    $public = Invoke-Api -Method GET -Path "/api/public/tickets/$numero"
    Check 'suivi public sans token' ($public.Code -eq 200 -and $public.Body -match [regex]::Escape($numero)) "HTTP $($public.Code)"
} else {
    Check 'suivi public sans token' $false 'aucun ticket pour le test'
}

$ticketInvalide = Invoke-Api -Method POST -Path '/api/tickets' -Token $colline.token -Body '{"agriculteurId":1,"engraisTypeId":1,"quantiteCommandee":10,"depotRetraitId":1}'
Check '400 ticket sans saison' ($ticketInvalide.Code -eq 400) "HTTP $($ticketInvalide.Code)"

# 5. Statistiques
foreach ($path in '/api/statistiques/ruptures', '/api/statistiques/stocks-par-province', '/api/statistiques/taux-service') {
    $r = Invoke-Api -Method GET -Path $path -Token $tok
    Check ("GET " + $path) ($r.Code -eq 200) "HTTP $($r.Code)"
}

Write-Host ""
Write-Host "== Resultat : $script:Pass reussis, $script:Fail echoues =="
if ($script:Fail -gt 0) {
    Write-Host ("Echecs : " + ($script:Failures -join ', '))
    exit 1
}
exit 0
