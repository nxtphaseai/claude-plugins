#!/usr/bin/env bash
# agent-eval installer.
#
# Usage:
#   bash install.sh                   # install into the current project (./.claude/)
#   bash install.sh --user            # install user-wide (~/.claude/)
#   bash install.sh --uninstall       # remove from the chosen scope
#
# Idempotent. Safe to re-run after upgrades.
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

command -v jq     >/dev/null 2>&1 || { echo "jq is required (brew install jq, apt install jq)." >&2; exit 1; }
command -v claude >/dev/null 2>&1 || echo "warning: claude CLI not on PATH; the eval hook will skip silently until it is." >&2

mkdir -p "$TARGET/commands" "$TARGET/hooks"

settings_merge() {
    local target_settings="$1" snippet="$2"
    local current
    if [[ -f "$target_settings" ]]; then
        current="$(cat "$target_settings")"
    else
        current="{}"
    fi
    # Deep-merge our hooks block into whatever already exists. We append to
    # any existing UserPromptSubmit / Stop arrays rather than replacing them.
    jq --argjson add "$snippet" '
      .hooks = (.hooks // {})
      | reduce ($add.hooks | to_entries[]) as $entry (
          .;
          .hooks[$entry.key] = ((.hooks[$entry.key] // []) + $entry.value)
        )
    ' <(printf '%s' "$current") > "$target_settings.tmp"
    mv "$target_settings.tmp" "$target_settings"
}

settings_unmerge() {
    local target_settings="$1"
    [[ -f "$target_settings" ]] || return 0
    jq '
      def drop_eval_hooks:
        if type == "array" then
          map(select(
            (.hooks // [] | map(.command // "" | test("eval-capture-prompt\\.sh|eval-run\\.sh")) | any) | not
          ))
        else . end;
      .hooks = (.hooks // {})
      | .hooks.UserPromptSubmit = ((.hooks.UserPromptSubmit // []) | drop_eval_hooks)
      | .hooks.Stop             = ((.hooks.Stop             // []) | drop_eval_hooks)
      | (if (.hooks.UserPromptSubmit | length) == 0 then del(.hooks.UserPromptSubmit) else . end)
      | (if (.hooks.Stop             | length) == 0 then del(.hooks.Stop)             else . end)
    ' "$target_settings" > "$target_settings.tmp"
    mv "$target_settings.tmp" "$target_settings"
}

if [[ "$ACTION" == "uninstall" ]]; then
    rm -f "$TARGET/commands/eval.md" "$TARGET/hooks/eval-capture-prompt.sh" "$TARGET/hooks/eval-run.sh"
    settings_unmerge "$TARGET/settings.json"
    echo "agent-eval uninstalled from $TARGET"
    exit 0
fi

cp "$SCRIPT_DIR/commands/eval.md"                  "$TARGET/commands/eval.md"
cp "$SCRIPT_DIR/hooks/eval-capture-prompt.sh"      "$TARGET/hooks/eval-capture-prompt.sh"
cp "$SCRIPT_DIR/hooks/eval-run.sh"                 "$TARGET/hooks/eval-run.sh"
chmod +x "$TARGET/hooks/eval-capture-prompt.sh" "$TARGET/hooks/eval-run.sh"

# The shipped hooks.json template uses ${CLAUDE_PLUGIN_ROOT:-$CLAUDE_PROJECT_DIR/.claude}.
# In a manual install we know the target so we substitute the path explicitly.
substituted="$(jq --arg root "$TARGET" '
  .hooks |= with_entries(.value |= map(
    .hooks |= map(.command |= sub("\\$\\{CLAUDE_PLUGIN_ROOT:-\\$CLAUDE_PROJECT_DIR/\\.claude\\}"; $root))
  ))
' "$SCRIPT_DIR/hooks/hooks.json")"

settings_merge "$TARGET/settings.json" "$substituted"

echo "agent-eval installed into $TARGET"
echo "  - $TARGET/commands/eval.md"
echo "  - $TARGET/hooks/eval-capture-prompt.sh"
echo "  - $TARGET/hooks/eval-run.sh"
echo "  - hooks registered in $TARGET/settings.json"
echo
echo "Restart Claude Code so the new slash command and hooks load."
