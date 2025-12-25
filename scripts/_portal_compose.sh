#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_DIR="${ROOT_DIR}/portal/frappe_docker"
COMPOSE_FILE="${COMPOSE_DIR}/pwd.yml"
COMPOSE_OVERRIDE_FILE="${ROOT_DIR}/portal/pwd.override.yml"

# важно: фиксируем имя compose-проекта, чтобы up/down попадали в один и тот же стек
PROJECT_NAME="frappe_docker"

dc() {
  docker compose \
    --project-directory "${COMPOSE_DIR}" \
    -p "${PROJECT_NAME}" \
    -f "${COMPOSE_FILE}" \
    -f "${COMPOSE_OVERRIDE_FILE}" \
    "$@"
}