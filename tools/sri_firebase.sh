#!/usr/bin/env bash
# Calcola gli hash SRI (sha384) degli SDK Firebase 10.13.0 ESATTAMENTE come serviti da gstatic (stessi URL usati da index.html).
# Va eseguito su una macchina CON rete (il sandbox di sviluppo non raggiunge gstatic). Richiede: curl, openssl.
# Uso: bash tools/sri_firebase.sh > sri_firebase.json     (poi: python3 tools/apply_sri.py sri_firebase.json <index.html>)
set -euo pipefail
V=10.13.0; B=https://www.gstatic.com/firebasejs/$V; T=$(mktemp -d); trap 'rm -rf "$T"' EXIT
printf '{\n'; first=1
for f in firebase-app-compat.js firebase-database-compat.js firebase-auth-compat.js; do
  curl -fsS --proto '=https' --tlsv1.2 -o "$T/$f" "$B/$f"
  h=$(openssl dgst -sha384 -binary "$T/$f" | openssl base64 -A)
  s=$(openssl dgst -sha256 "$T/$f" | awk '{print $NF}'); n=$(wc -c < "$T/$f" | tr -d ' ')
  [ $first = 1 ] || printf ',\n'; first=0
  printf '  "%s": {"integrity": "sha384-%s", "sha256_hex": "%s", "bytes": %s}' "$f" "$h" "$s" "$n"
done
printf '\n}\n'
