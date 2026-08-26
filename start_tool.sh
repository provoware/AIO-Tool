#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PORT="${AIO_PORT:-8765}"
URL="http://127.0.0.1:${PORT}"
VENV="$ROOT/.venv"
RUNTIME="$ROOT/runtime"
mkdir -p "$RUNTIME"

say(){ printf '[AIO-Tool] %s\n' "$*"; }
fail(){ printf '[AIO-Tool] FEHLER: %s\n' "$*" >&2; exit 1; }

command -v python3 >/dev/null 2>&1 || fail "Python 3 fehlt. Bitte über die Paketverwaltung installieren."

is_ready(){
  python3 - "$PORT" <<'PY' >/dev/null 2>&1
import http.client, sys
port=int(sys.argv[1])
try:
    c=http.client.HTTPConnection('127.0.0.1',port,timeout=.35)
    c.request('GET','/api/status',headers={'Host':f'127.0.0.1:{port}'})
    r=c.getresponse(); ok=r.status==200; r.read(); c.close()
    raise SystemExit(0 if ok else 1)
except Exception:
    raise SystemExit(1)
PY
}

open_ui(){
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 || true
  elif command -v firefox >/dev/null 2>&1; then
    firefox "$URL" >/dev/null 2>&1 &
  elif command -v google-chrome >/dev/null 2>&1; then
    google-chrome "$URL" >/dev/null 2>&1 &
  else
    say "Browser konnte nicht automatisch geöffnet werden: $URL"
  fi
}

if is_ready; then
  say "Tool läuft bereits. Vorhandene Instanz wird geöffnet."
  open_ui
  exit 0
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  say "Lokale Python-Umgebung wird einmalig vorbereitet …"
  rm -rf "$VENV"
  if ! python3 -m venv --without-pip "$VENV"; then
    fail "Virtuelle Umgebung konnte nicht erstellt werden. Auf Ubuntu/Kubuntu fehlt meist das Paket python3-venv."
  fi
fi

say "Vorprüfung läuft …"
"$VENV/bin/python" scripts/validate.py --quick || fail "Vorprüfung fehlgeschlagen. Details stehen oben."

say "Lokales Backend wird gestartet …"
nohup "$VENV/bin/python" -m app.server --port "$PORT" >>"$RUNTIME/launcher.log" 2>&1 &
echo $! > "$RUNTIME/server.pid"

for _ in $(seq 1 50); do
  if is_ready; then
    say "Bereit. Oberfläche wird geöffnet."
    open_ui
    exit 0
  fi
  sleep .1
done

fail "Backend wurde nicht rechtzeitig bereit. Siehe runtime/launcher.log."
