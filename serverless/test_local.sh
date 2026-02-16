#!/usr/bin/env bash
set -euo pipefail

# Démarre serverless-offline, puis teste /health et /chat.
# Usage: bash test_local.sh

( npx serverless offline --stage local ) &
PID=$!

sleep 2
echo "GET /health"
curl -s http://localhost:3000/health | cat
echo
echo "POST /chat"
curl -s http://localhost:3000/chat -H "Content-Type: application/json" -d '{"question":"Explique cet exemple."}' | cat
echo

kill $PID
