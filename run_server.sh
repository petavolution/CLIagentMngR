#!/bin/bash
# Run the EATS web server

set -e

cd "$(dirname "$0")"

echo "==================================="
echo "EATS - Evolutionary Agent Tree System"
echo "==================================="
echo ""
echo "Starting server at http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

python -m uvicorn eats.api:app --reload --host 0.0.0.0 --port 8000
