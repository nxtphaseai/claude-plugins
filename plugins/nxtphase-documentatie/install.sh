#!/usr/bin/env bash
# nxtphase-documentatie installer.
#
# Usage:
#   bash install.sh                   # install into the current project (./.claude/)
#   bash install.sh --user            # install user-wide (~/.claude/)
#   bash install.sh --uninstall       # remove from the chosen scope
#
# Idempotent. Skill-only plugin, no hook merging required. Copies the full
# skill bundle (SKILL.md, reference/, assets/) into
# `<scope>/skills/nxtphase-documentatie/`.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills/nxtphase-documentatie"
SKILL_NAME="nxtphase-documentatie"

SCOPE="project"
ACTION="install"
for arg in "$@"; do
    case "$arg" in
        --user)      SCOPE="user" ;;
        --project)   SCOPE="project" ;;
        --uninstall) ACTION="uninstall" ;;
        -h|--help)
            sed -n '2,8p' "$0" | sed 's/^# //; s/^#//'
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

SKILL_DST="$TARGET/skills/$SKILL_NAME"

if [[ "$ACTION" == "uninstall" ]]; then
    rm -rf "$SKILL_DST"
    echo "nxtphase-documentatie uninstalled from $SKILL_DST"
    exit 0
fi

if [[ ! -d "$SKILL_SRC" ]]; then
    echo "skill source missing: $SKILL_SRC" >&2
    exit 1
fi

mkdir -p "$TARGET/skills"

if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete "$SKILL_SRC/" "$SKILL_DST/"
else
    rm -rf "$SKILL_DST"
    mkdir -p "$SKILL_DST"
    cp -R "$SKILL_SRC/." "$SKILL_DST/"
fi

echo "nxtphase-documentatie installed into $SKILL_DST"
echo "  SKILL.md, reference/, assets/"
echo

if command -v python3 >/dev/null 2>&1; then
    PY=python3
elif command -v python >/dev/null 2>&1; then
    PY=python
else
    PY=""
fi

if [[ -z "$PY" ]]; then
    echo "Warning: no python found on PATH. assets/build_docx.py needs Python 3.8 or newer" >&2
    echo "to turn the Markdown sources into .docx." >&2
else
    if ! "$PY" -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'; then
        echo "Warning: $PY is older than 3.8; assets/build_docx.py needs 3.8 or newer." >&2
    fi
fi

if ! command -v az >/dev/null 2>&1; then
    echo "Warning: the Azure CLI (az) is not on PATH. The skill uses read-only az commands" >&2
    echo "to verify what is actually deployed; without it you can only document the code." >&2
fi

echo
echo "Restart Claude Code so the skill is picked up."
