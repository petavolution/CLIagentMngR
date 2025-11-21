#!/bin/bash
# Run the EATS CLI supervisor

set -e

cd "$(dirname "$0")"

echo "==================================="
echo "EATS - CLI Supervisor"
echo "==================================="
echo ""

python -m eats.cli_supervisor "$@"
