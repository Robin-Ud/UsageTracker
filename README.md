# UsageTracker

Rastreador de uso do terminal e dos keybinds do Hyprland. Puro Python, zero deps.

## O que ele faz

Dois hooks silenciosos gravam TSV em `~/.local/share/usage-tracker/`:

- **Comandos**: um hook no `.bashrc` (`_usage_tracker_log`) registra a primeira
  palavra de cada comando digitado no terminal, em `cmd_log.tsv`.
- **Keybinds do Hyprland**: `track_bind.sh` é chamado por todo `bind =` do
  `hyprland.conf` — ele registra o atalho em `bind_log.tsv` e executa o comando de
  verdade na sequência (`exec env "$@"`). Se esse arquivo sumir, **todos os
  atalhos do Hyprland param de funcionar**.

`usage_tracker.py` lê os dois logs e imprime um relatório: comandos e binds mais
usados, e quais binds estão parados (sem uso há `stale_days` dias).

## Rodar

```bash
usage-report   # alias/symlink pra usage_tracker.sh em ~/.local/bin
```

## Estrutura

```
track_bind.sh          ← chamado pelo hyprland.conf, registra bind + roda o comando
usage_tracker.py        ← lê os TSV e imprime o relatório
usage_tracker.sh         ← wrapper (alvo do symlink usage-report)
configs.json              ← log_dir, top_n, stale_days
```

`DATA_DIR` dos logs é `~/.local/share/usage-tracker/` (fora do repo, configurável
em `configs.json`), não a pasta do projeto — os dados sobrevivem mesmo que o
projeto seja apagado de novo.
