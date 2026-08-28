# CLAUDE.md

Script Python puro para relatório de uso (terminal + keybinds do Hyprland). Sem
dependências externas, sem packaging.

## Rodar

```bash
python usage_tracker.py
# ou via symlink já existente:
usage-report   # -> ~/.local/bin/usage-report -> usage_tracker.sh
```

## Estrutura

```
track_bind.sh        ← chamado por cada `bind =` do hyprland.conf
usage_tracker.py      ← script único, lê os TSV e imprime o relatório
usage_tracker.sh       ← wrapper fino (alvo do symlink usage-report)
configs.json            ← log_dir, top_n, stale_days
```

Logs ficam em `~/.local/share/usage-tracker/` (fora deste diretório, caminho vem
de `configs.json`), gravados por dois pontos independentes:

- `cmd_log.tsv` — hook `_usage_tracker_log` no `~/.bashrc` (não depende deste
  projeto pra funcionar).
- `bind_log.tsv` — `track_bind.sh`, referenciado por path absoluto em ~80 linhas
  de `~/.config/hypr/hyprland.conf`. **Se este arquivo for apagado, todo bind do
  Hyprland para de funcionar** — é o componente crítico do projeto.
- `tracking_started` — epoch do início do tracking, usado só pra contar dias.

## Arquitetura (`usage_tracker.py`)

| Zona | Papel |
|------|-------|
| 1 — Data Engines | `load_configs`, `read_tsv`, `read_tracking_started` — só I/O |
| 2 — Orchestration | `top_counts`, `last_seen`, `stale_entries`, `days_tracked` |
| 3 — Interface | `format_top`, `format_stale`, `print_report` — monta a saída |

## Regras

- Zero dependências externas — só stdlib (`json`, `os`, `collections.Counter`,
  `datetime`)
- Python 3.10+ — usar `X | Y` em vez de `Optional[X]`
- Type hints em todas as assinaturas
- `usage_tracker_test.sh` roda com dados sintéticos em `/tmp`, nunca toca os TSV
  reais do Matheus
