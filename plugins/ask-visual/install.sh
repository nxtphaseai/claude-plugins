#!/usr/bin/env bash
# ask-visual installer.
#
# Usage:
#   bash install.sh                   # install into the current project (./.claude/)
#   bash install.sh --user            # install user-wide (~/.claude/)
#   bash install.sh --uninstall       # remove from the chosen scope
#
# Idempotent. No hook merging needed — this plugin only ships a slash
# command and a helper script.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

SCOPE="project"
ACTION="install"
for arg in "$@"; do
    case "$arg" in
        --user)      SCOPE="user" ;;
        --project)   SCOPE="project" ;;
        --uninstall) ACTION="uninstall" ;;
        -h|--help)
            sed -n '2,9p' "$0" | sed 's/^# //; s/^#//'
            exit 0
            ;;
        *)
            echo "unknown arg: $arg" >&2
            exit 2
            ;;
    esac
done

if [[ "$SCOPE" == "user" ]]; then
    TARGET="$HOME/.claude"
else
    if ! git rev-parse --show-toplevel >/dev/null 2>&1; then
        echo "Run this from inside a git repo, or use --user to install user-wide." >&2
        exit 1
    fi
    TARGET="$(git rev-parse --show-toplevel)/.claude"
fi

command -v python3 >/dev/null 2>&1 || echo "warning: python3 not on PATH; ask-visual needs it." >&2

mkdir -p "$TARGET/commands" "$TARGET/bin"

if [[ "$ACTION" == "uninstall" ]]; then
    rm -f "$TARGET/commands/ask-visual.md" "$TARGET/bin/ask-visual.py"
    echo "ask-visual uninstalled from $TARGET"
    exit 0
fi

cp "$SCRIPT_DIR/commands/ask-visual.md" "$TARGET/commands/ask-visual.md"
cp "$SCRIPT_DIR/bin/ask-visual.py"      "$TARGET/bin/ask-visual.py"
chmod +x "$TARGET/bin/ask-visual.py"

echo "ask-visual installed into $TARGET"
echo "  - $TARGET/commands/ask-visual.md"
echo "  - $TARGET/bin/ask-visual.py"
echo
echo "Restart Claude Code so the slash command loads."
