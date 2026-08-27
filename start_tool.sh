#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"

# Portable releases ship a bundled interpreter. Prefer it so a normal user
# never needs Python, pip, venv, sudo or package-manager interaction.
if [[ -x "$ROOT/AIO-Tool-Start" ]]; then
  exec "$ROOT/AIO-Tool-Start" "$@"
fi

# Source/runtime packages intentionally need only the Python standard library.
# A virtual environment would add another failure point without isolation value.
for candidate in python3 python; do
  if command -v "$candidate" >/dev/null 2>&1 \
     && "$candidate" -c 'import sys; raise SystemExit(0 if sys.version_info >= (3,10) else 1)' >/dev/null 2>&1; then
    exec "$candidate" -m app.autostart "$@"
  fi
done

printf '🔴 AIO-Tool kann nicht starten: kein kompatibles Python >= 3.10 vorhanden.\n' >&2
printf 'Nutze das PORTABLE-LINUX-Paket; es enthält den Interpreter bereits.\n' >&2
exit 102
