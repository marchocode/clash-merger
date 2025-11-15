#!/bin/sh
set -e

TOKEN_FILE="/tmp/token"

if [ -z "$TOKEN" ]; then
    echo "TOKEN not found, generate token..."
    TOKEN=$(uuidgen)
fi

echo "yes. token is ready! TOKEN=$TOKEN"
echo $TOKEN > $TOKEN_FILE

export TOKEN

exec $@
