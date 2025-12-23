#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_portal_compose.sh"

# примеры:
# ./scripts/portal_logs.sh
# ./scripts/portal_logs.sh backend
# ./scripts/portal_logs.sh frontend
dc logs --tail=200 "$@"