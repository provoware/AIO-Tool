#!/usr/bin/env bash
set -Eeuo pipefail
ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PY="$ROOT/.venv/bin/python"
[[ -x "$PY" ]] || PY="$(command -v python3 || true)"
if [[ -z "$PY" ]]; then
  echo "🔴 Python 3 wurde nicht gefunden. Bitte zuerst AIO-Tool normal starten."
  exit 1
fi
echo "AIO-Tool · Native Acceptance Runner"
echo "🟢 Toolbasis: $ROOT"
echo "🟢 Modus: reale L4-Prüfung mit manueller PASS/FAIL/SKIP-Bestätigung"
exec "$PY" scripts/native_acceptance_runner.py
