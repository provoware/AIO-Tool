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
echo "AIO-Tool · SAFE-FILE Simulation"
echo "🟡 SIMULATION ONLY · keine Datei wird kopiert, verschoben, umbenannt oder gelöscht."
exec "$PY" scripts/safe_file_simulator.py
