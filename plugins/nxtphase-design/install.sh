#!/usr/bin/env bash
# nxtphase-design installer.
#
# Usage:
#   bash install.sh                   # install into the current project (./.claude/)
#   bash install.sh --user            # install user-wide (~/.claude/)
#   bash install.sh --uninstall       # remove from the chosen scope
#
# Idempotent. Skill-only plugin — no hook merging required. Copies the
# full skill bundle (SKILL.md + assets, fonts, slides, UI kit, CSS) into
# `<scope>/skills/nxt-phase-ai-design/`.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SRC="$SCRIPT_DIR/skills/nxt-phase-ai-design"
SKILL_NAME="nxt-phase-ai-design"

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

SKILL_DST="$TARGET/skills/$SKILL_NAME"

if [[ "$ACTION" == "uninstall" ]]; then
    rm -rf "$SKILL_DST"
    echo "nxtphase-design uninstalled from $SKILL_DST"
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

echo "nxtphase-design installed into $SKILL_DST"
echo "  SKILL.md, README.md, colors_and_type.css, fonts/, assets/, preview/, slides/, ui_kits/"
echo
echo "Restart Claude Code so the skill is picked up."
