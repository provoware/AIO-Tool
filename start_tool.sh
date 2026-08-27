#!/usr/bin/env bash
set -Eeuo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT"
PORT="${AIO_PORT:-8765}"
URL="http://127.0.0.1:${PORT}"
VENV="$ROOT/.venv"
RUNTIME="$ROOT/runtime"
SESSION_ID="$(date '+%Y%m%d-%H%M%S')-$$"
SESSION_START="$(date +%s)"
VERSION="$(cat "$ROOT/VERSION" 2>/dev/null || printf 'unbekannt')"
CONSOLE_LOG="$RUNTIME/launcher-console.log"
BACKEND_LOG="$RUNTIME/launcher-backend.log"
EVENT_LOG="$RUNTIME/launcher-events.jsonl"
REPORT="$RUNTIME/launcher-report.txt"
SERVER_PID_FILE="$RUNTIME/server.pid"
TOTAL=9
CURRENT=0
FAILED_EVENT=""
FAILED_TEXT=""
MAX_LOG_BYTES=$((2 * 1024 * 1024))

mkdir -p "$RUNTIME"
rotate_log(){
  local file="$1"
  if [[ -f "$file" ]] && (( $(wc -c < "$file") > MAX_LOG_BYTES )); then
    mv -f "$file" "$file.1"
  fi
}
rotate_log "$CONSOLE_LOG"
rotate_log "$BACKEND_LOG"
rotate_log "$EVENT_LOG"
touch "$CONSOLE_LOG" "$BACKEND_LOG" "$EVENT_LOG"
exec > >(tee -a "$CONSOLE_LOG") 2>&1

supports_color(){ [[ -t 1 && "${NO_COLOR:-}" == "" ]]; }
if supports_color; then
  C_GREEN=$'\033[32m'; C_YELLOW=$'\033[33m'; C_RED=$'\033[31m'; C_BLUE=$'\033[36m'; C_BOLD=$'\033[1m'; C_RESET=$'\033[0m'
else
  C_GREEN=""; C_YELLOW=""; C_RED=""; C_BLUE=""; C_BOLD=""; C_RESET=""
fi

line(){ printf '%s\n' "────────────────────────────────────────────────────────────"; }
percent(){ printf '%d' $(( CURRENT * 100 / TOTAL )); }
json_escape(){ python3 -c 'import json,sys; print(json.dumps(sys.argv[1], ensure_ascii=False)[1:-1])' "$1" 2>/dev/null || printf '%s' "$1"; }
event(){
  local id="$1" level="$2" phase="$3" message="$4" detail="${5:-}"
  printf '{"time":"%s","session":"%s","event":"%s","level":"%s","phase":"%s","message":"%s","detail":"%s"}\n' \
    "$(date -Is)" "$SESSION_ID" "$id" "$level" "$(json_escape "$phase")" "$(json_escape "$message")" "$(json_escape "$detail")" >> "$EVENT_LOG"
}
checkpoint(){
  local id="$1" status="$2" title="$3" detail="${4:-}"
  CURRENT=$((CURRENT + 1))
  local color="$C_BLUE" icon="🔵"
  case "$status" in
    PASS) color="$C_GREEN"; icon="🟢";;
    WARN) color="$C_YELLOW"; icon="🟡";;
    FAIL) color="$C_RED"; icon="🔴";;
    INFO) color="$C_BLUE"; icon="🔵";;
  esac
  printf '%s[%02d/%02d · %3d%%]%s %s %-5s  %s\n' "$C_BOLD" "$CURRENT" "$TOTAL" "$(percent)" "$C_RESET" "$icon" "$status" "$title"
  [[ -n "$detail" ]] && printf '                 %s↳ %s%s\n' "$color" "$detail" "$C_RESET"
  event "$id" "${status,,}" "$title" "$detail"
}
info(){ printf '%sℹ %s%s\n' "$C_BLUE" "$*" "$C_RESET"; }
next_hint(){ printf '%s→ Nächster Schritt: %s%s\n' "$C_YELLOW" "$*" "$C_RESET"; }

write_report(){
  local outcome="$1" reason="${2:-keine}"
  local now elapsed
  now="$(date +%s)"; elapsed=$((now - SESSION_START))
  cat > "$REPORT" <<EOF
AIO-Tool Startauswertung
=======================
Zeit:        $(date -Is)
Sitzung:     $SESSION_ID
Version:     $VERSION
Ergebnis:    $outcome
Checkpoint:  $CURRENT/$TOTAL
Dauer:       ${elapsed}s
Port:        $PORT
Adresse:     $URL
Grund:       $reason

Debug-Dateien
-------------
Konsolenlog: $CONSOLE_LOG
Backendlog:  $BACKEND_LOG
Ereignisse:  $EVENT_LOG
PID-Datei:   $SERVER_PID_FILE

Weiterführende Prüfung
----------------------
1. Letzte Launcher-Ereignisse: tail -n 30 "$EVENT_LOG"
2. Letzte Backendmeldungen:    tail -n 50 "$BACKEND_LOG"
3. Backendstatus prüfen:        curl -fsS "$URL/api/status"
4. Runtime-Vorprüfung:          "$VENV/bin/python" scripts/runtime_preflight.py
5. Repo-Vollprüfung (falls vorhanden): python3 scripts/validate.py
EOF
}

debug_summary(){
  local reason="$1"
  line
  printf '%sSTARTAUSWERTUNG · FEHLER%s\n' "$C_RED$C_BOLD" "$C_RESET"
  printf 'Sitzung: %s | Version: %s | Checkpoint: %d/%d\n' "$SESSION_ID" "$VERSION" "$CURRENT" "$TOTAL"
  printf 'Ursache: %s\n' "$reason"
  printf 'Konsolenlog: %s\nBackendlog:  %s\nEreignisse:  %s\n' "$CONSOLE_LOG" "$BACKEND_LOG" "$EVENT_LOG"
  if [[ -s "$BACKEND_LOG" ]]; then
    printf '\n%sLetzte Backend-Ereignisse:%s\n' "$C_BOLD" "$C_RESET"
    tail -n 12 "$BACKEND_LOG" | sed 's/^/  │ /'
  fi
  printf '\n%sDebug-Befehle:%s\n' "$C_BOLD" "$C_RESET"
  printf '  tail -n 30 "%s"\n' "$EVENT_LOG"
  printf '  tail -n 50 "%s"\n' "$BACKEND_LOG"
  printf '  curl -fsS "%s/api/status"\n' "$URL"
  printf '  "%s/bin/python" scripts/runtime_preflight.py\n' "$VENV"
  if [[ -f "$ROOT/scripts/validate.py" ]]; then
    printf '  python3 scripts/validate.py  # Repository-Vollprüfung\n'
  fi
  line
}

fail(){
  local event_id="$1" message="$2" hint="${3:-Details in der Startauswertung prüfen.}"
  FAILED_EVENT="$event_id"; FAILED_TEXT="$message"
  checkpoint "$event_id" FAIL "$message" "$hint"
  event "$event_id" "error" "Abbruch" "$message" "$hint"
  write_report "FEHLER" "$event_id · $message"
  debug_summary "$event_id · $message"
  next_hint "$hint"
  exit 1
}

on_unexpected_error(){
  local code=$? line_no="${BASH_LINENO[0]:-?}" cmd="${BASH_COMMAND:-?}"
  [[ -n "$FAILED_EVENT" ]] && exit "$code"
  FAILED_EVENT="LAUNCH-E900"
  FAILED_TEXT="Unerwarteter Fehler in der Startroutine"
  event "LAUNCH-E900" "error" "Shell" "$FAILED_TEXT" "Zeile $line_no · Exit $code · $cmd"
  write_report "FEHLER" "LAUNCH-E900 · Zeile $line_no · Exit $code"
  debug_summary "LAUNCH-E900 · Zeile $line_no · Exit $code · $cmd"
  exit "$code"
}
trap on_unexpected_error ERR

probe_instance(){
  local output
  mapfile -t output < <(python3 scripts/launcher_probe.py inspect --port "$PORT")
  PROBE_STATE="${output[0]:-error}"
  PROBE_DETAIL="${output[1]:-Statusprüfung lieferte kein verwertbares Ergebnis.}"
}
is_own_ready(){
  probe_instance
  [[ "$PROBE_STATE" == "own-ready" ]]
}

open_ui(){
  if command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$URL" >/dev/null 2>&1 || return 1
  elif command -v firefox >/dev/null 2>&1; then
    firefox "$URL" >/dev/null 2>&1 &
  elif command -v google-chrome >/dev/null 2>&1; then
    google-chrome "$URL" >/dev/null 2>&1 &
  else
    return 2
  fi
}

clear 2>/dev/null || true
line
printf '%sAIO-TOOL · SICHERE STARTRUTINE%s\n' "$C_BOLD" "$C_RESET"
printf 'Version %s | Sitzung %s | lokal/offline-first\n' "$VERSION" "$SESSION_ID"
printf 'Ziel: %s\n' "$URL"
line
info "Jeder Startschritt wird geprüft. Grün = bestanden, Gelb = Hinweis, Rot = Abbruch mit Diagnose."

checkpoint "LAUNCH-CP01" PASS "Projektordner erkannt" "$ROOT"

if command -v python3 >/dev/null 2>&1; then
  PYVER="$(python3 --version 2>&1)"
  checkpoint "LAUNCH-CP02" PASS "Python-Basis verfügbar" "$PYVER"
else
  fail "LAUNCH-E102" "Python 3 fehlt" "Python 3 über die Paketverwaltung installieren und erneut starten."
fi

if [[ ! "$PORT" =~ ^[0-9]+$ ]] || (( PORT < 1024 || PORT > 65535 )); then
  fail "LAUNCH-E103" "Ungültiger lokaler Port" "AIO_PORT muss eine Zahl zwischen 1024 und 65535 sein."
fi
URL="http://127.0.0.1:${PORT}"

if python3 scripts/launcher_probe.py ensure-marker >/dev/null; then
  checkpoint "LAUNCH-CP03" PASS "Diagnose und Instanzkennung vorbereitet" "runtime/ getrennt von der lokalen Installationskennung"
else
  fail "LAUNCH-E303" "Lokale Instanzkennung konnte nicht vorbereitet werden" "Schreibrechte im Toolordner prüfen."
fi

probe_instance
case "$PROBE_STATE" in
  own-ready|occupied|free) ;;
  *) fail "LAUNCH-E304" "Instanzprüfung lieferte keinen sicheren Zustand" "Probe-Ausgabe prüfen; bei unbekanntem Zustand wird nicht gestartet.";;
esac
if [[ "$PROBE_STATE" == "own-ready" ]]; then
  checkpoint "LAUNCH-CP04" PASS "Passende vorhandene Instanz erkannt" "$PROBE_DETAIL"
  checkpoint "LAUNCH-CP05" PASS "Lokale Python-Umgebung" "Für die laufende Instanz ist keine Neuinitialisierung nötig."
  checkpoint "LAUNCH-CP06" PASS "Runtime-Vertrag" "Version und Installationskennung der laufenden Instanz stimmen überein."
  checkpoint "LAUNCH-CP07" PASS "Backendprozess" "Bestehende passende Instanz bleibt unverändert aktiv."
  checkpoint "LAUNCH-CP08" PASS "Bereitschaft bestätigt" "$URL/api/status und Instanzmarker stimmen."
  if open_ui; then
    checkpoint "LAUNCH-CP09" PASS "Oberfläche geöffnet" "$URL"
  else
    checkpoint "LAUNCH-CP09" WARN "Browser nicht automatisch geöffnet" "Adresse manuell öffnen: $URL"
  fi
  write_report "ERFOLG" "Passende vorhandene Instanz wiederverwendet"
  line
  printf '%s✓ START ERFOLGREICH%s · 9/9 Checkpoints bewertet · Bericht: %s\n' "$C_GREEN$C_BOLD" "$C_RESET" "$REPORT"
  line
  exit 0
fi

if [[ "$PROBE_STATE" == "occupied" ]]; then
  OLD_PORT="$PORT"
  if PORT="$(python3 scripts/launcher_probe.py find-free --start $((OLD_PORT + 1)) --span 30)"; then
    URL="http://127.0.0.1:${PORT}"
    checkpoint "LAUNCH-CP04" WARN "Standardport anderweitig belegt" "Port $OLD_PORT wird nicht übernommen; sicherer Ausweichport $PORT wird verwendet."
    event "LAUNCH-D404" "warning" "Portwahl" "Fremde oder alte lokale Instanz nicht übernommen" "Alt=$OLD_PORT · Neu=$PORT"
  else
    fail "LAUNCH-E404" "Kein freier lokaler Ausweichport gefunden" "Andere lokale Instanzen beenden oder AIO_PORT mit einem freien Port setzen."
  fi
else
  checkpoint "LAUNCH-CP04" INFO "Keine laufende passende Instanz" "Port $PORT ist frei; neue lokale Instanz wird gestartet."
fi

if [[ ! -x "$VENV/bin/python" ]]; then
  info "Die lokale Python-Umgebung fehlt und wird sicher im Projektordner erzeugt."
  rm -rf "$VENV"
  if python3 -m venv --without-pip "$VENV"; then
    checkpoint "LAUNCH-CP05" PASS "Lokale Python-Umgebung erstellt" ".venv/ · keine systemweite Python-Änderung"
  else
    fail "LAUNCH-E205" "Lokale Python-Umgebung konnte nicht erstellt werden" "Unter Ubuntu/Kubuntu meist Paket python3-venv installieren."
  fi
else
  checkpoint "LAUNCH-CP05" PASS "Lokale Python-Umgebung vorhanden" "$VENV"
fi

info "Jetzt wird ausschließlich die transportierte Runtime-Basis geprüft; Repository-Dokumentation ist dafür nicht erforderlich."
if "$VENV/bin/python" scripts/runtime_preflight.py --quick; then
  checkpoint "LAUNCH-CP06" PASS "Runtime-Vorprüfung bestanden" "Version, Runtime-Manifest, Sicherheitsverträge und atomare Speicherung konsistent."
else
  fail "LAUNCH-E306" "Runtime-Vorprüfung fehlgeschlagen" "Die direkt darüber markierte Prüfung beachten; das Backend wurde noch nicht gestartet."
fi

info "Die lokale Serverkomponente wird nur auf 127.0.0.1 gestartet."
: > "$BACKEND_LOG"
nohup "$VENV/bin/python" -m app.server --port "$PORT" >>"$BACKEND_LOG" 2>&1 &
SERVER_PID=$!
printf '%s\n' "$SERVER_PID" > "$SERVER_PID_FILE"
sleep .15
if kill -0 "$SERVER_PID" 2>/dev/null; then
  checkpoint "LAUNCH-CP07" PASS "Backendprozess gestartet" "PID $SERVER_PID · Log: $BACKEND_LOG"
else
  fail "LAUNCH-E407" "Backendprozess wurde direkt beendet" "Backendlog unten prüfen; häufig sind Port-, Datei- oder Konfigurationsfehler die Ursache."
fi

READY=0
for attempt in $(seq 1 50); do
  if is_own_ready; then READY=1; break; fi
  if ! kill -0 "$SERVER_PID" 2>/dev/null; then break; fi
  if (( attempt == 10 || attempt == 25 || attempt == 40 )); then
    event "LAUNCH-D508" "info" "Bereitschaft" "Backend startet noch" "Versuch $attempt/50 · PID $SERVER_PID"
    printf '                 🔵 Backend startet noch … Statusprüfung %d/50\n' "$attempt"
  fi
  sleep .1
done
if [[ "$READY" == "1" ]]; then
  checkpoint "LAUNCH-CP08" PASS "Backend ist verifiziert bereit" "API-Status, Version und Installationskennung stimmen."
else
  fail "LAUNCH-E508" "Backend wurde nicht als passende Instanz bereit" "runtime/launcher-backend.log prüfen; die letzten Meldungen werden unten automatisch angezeigt."
fi

if open_ui; then
  checkpoint "LAUNCH-CP09" PASS "Oberfläche geöffnet" "$URL"
else
  checkpoint "LAUNCH-CP09" WARN "Browser nicht automatisch geöffnet" "Kein Datenfehler: Adresse manuell im Browser öffnen: $URL"
fi

write_report "ERFOLG" "Neuer verifizierter Backendprozess erfolgreich gestartet"
line
printf '%s✓ START ERFOLGREICH%s · %d/%d Checkpoints bewertet · %d%%\n' "$C_GREEN$C_BOLD" "$C_RESET" "$CURRENT" "$TOTAL" "$(percent)"
printf 'Oberfläche: %s\nBericht:    %s\nEreignisse: %s\n' "$URL" "$REPORT" "$EVENT_LOG"
line
