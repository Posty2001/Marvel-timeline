# Calcola gli hash SRI (sha384) degli SDK Firebase 10.13.0 come serviti da gstatic (Windows PowerShell 5+/7). Richiede rete.
# Uso:  powershell -ExecutionPolicy Bypass -File tools\sri_firebase.ps1 > sri_firebase.json
$ErrorActionPreference = 'Stop'
$V = '10.13.0'; $B = "https://www.gstatic.com/firebasejs/$V"; $out = [ordered]@{}
foreach ($f in 'firebase-app-compat.js','firebase-database-compat.js','firebase-auth-compat.js') {
  $tmp = [System.IO.Path]::GetTempFileName()
  Invoke-WebRequest -UseBasicParsing -Uri "$B/$f" -OutFile $tmp
  $bytes = [System.IO.File]::ReadAllBytes($tmp)
  $h384 = [Convert]::ToBase64String([System.Security.Cryptography.SHA384]::Create().ComputeHash($bytes))
  $h256 = ([System.Security.Cryptography.SHA256]::Create().ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
  $out[$f] = [ordered]@{ integrity = "sha384-$h384"; sha256_hex = $h256; bytes = $bytes.Length }
  Remove-Item $tmp
}
$out | ConvertTo-Json
