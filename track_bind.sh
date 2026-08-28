#!/bin/bash
# Registra o uso de um keybind do Hyprland e executa o comando associado.
#
# Uso:  track_bind.sh 'SUPER+1' <comando> [args...]
#
# O primeiro argumento é o rótulo do bind; o resto é o comando a executar.
# Nada é escrito em stdout: alguns binds fazem pipe da saída do comando
# (ex: `track_bind.sh 'none+Print' grim - | wl-copy`).

LOG="${XDG_DATA_HOME:-$HOME/.local/share}/usage-tracker/bind_log.tsv"

bind=$1
shift

mkdir -p "$(dirname "$LOG")"
printf '%s\t%s\n' "$(date +%s)" "$bind" >> "$LOG" 2>/dev/null

[ $# -eq 0 ] && exit 0

# `env` permite prefixos VAR=valor no comando (ex: QT_QPA_PLATFORM=xcb qgis).
exec env "$@"
