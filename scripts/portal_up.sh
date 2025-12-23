#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_portal_compose.sh"

dc up -d
dc ps
echo ""
echo "OK: портал поднят. Открывать: http://localhost:8080"