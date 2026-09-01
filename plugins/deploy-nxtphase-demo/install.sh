#!/usr/bin/env bash
# deploy-nxtphase-demo installer.
#
# Usage:
#   bash install.sh                   # install into the current project (./.claude/)
#   bash install.sh --user            # install user-wide (~/.claude/)
#   bash install.sh --uninstall       # remove from the chosen scope
#
# Idempotent. Skill-only plugin, no hook merging required. Copies the full
# skill bundle (SKILL.md, references/, assets/) into
# `<scope>/skills/deploy-nxtphase-demo/`.
#
# Installs no credentials. The skill reads RAILWAY_API_TOKEN and CLOUDFLARE_TOKEN
# from a .env file in the app you deploy; see skills/deploy-nxtphase-demo/
# references/tokens.md.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="deploy-nxtphase-demo"
SKILL_SRC="$SCRIPT_DIR/skills/$SKILL_NAME"

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
    echo "deploy-nxtphase-demo uninstalled from $SKILL_DST"
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

echo "deploy-nxtphase-demo installed into $SKILL_DST"
echo "  SKILL.md, references/, assets/"
echo

if ! command -v railway >/dev/null 2>&1; then
    echo "Warning: the Railway CLI is not on PATH. The skill needs it to upload source" >&2
    echo "and read logs. Install with one of:" >&2
    echo "  macOS:   brew install railway" >&2
    echo "  Windows: npm i -g @railway/cli" >&2
    echo "  any:     bash <(curl -fsSL cli.new)" >&2
    echo >&2
fi

if ! command -v curl >/dev/null 2>&1; then
    echo "Warning: curl is not on PATH; the skill calls the Railway and Cloudflare APIs with it." >&2
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "Note: jq is not on PATH. The skill can read the deploy token out of" >&2
    echo ".railway-deploy.json with sed instead, so this is not fatal." >&2
fi

if ! command -v dig >/dev/null 2>&1 && ! command -v nslookup >/dev/null 2>&1; then
    echo "Warning: neither dig nor nslookup is on PATH; the skill uses one of them to" >&2
    echo "confirm DNS propagated before testing the URL." >&2
fi

cat <<'NEXT'

Next: the skill ships with no tokens. In the app you want to deploy, create a
.env file with:

    RAILWAY_API_TOKEN=<railway account token>
    CLOUDFLARE_TOKEN=<cloudflare api token>

Ask a developer on the team for both values; they belong to the shared
"Nxtphase AI demos" Railway workspace and the nxtphase.ai Cloudflare zone. Have
them sent through a password manager, not through chat or a Notion page.

A template lives at assets/env.example inside the installed skill, and
references/tokens.md documents the exact permissions if you mint your own.

Add .env and .railway-deploy.json to that app's .gitignore before you deploy.

Restart Claude Code so the skill is picked up.
NEXT
