#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/_portal_compose.sh"

dc down --remove-orphans
dc ps || true