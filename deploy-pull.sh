#!/bin/bash
set -e

cd /root/swarm-demo

git fetch origin main

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "New version found. Pulling..."
  git pull origin main

  APP_TAG=$(git rev-parse --short HEAD)

  echo "Deploying tag: $APP_TAG"
  APP_TAG=$APP_TAG docker stack deploy -c stack.yml demo
else
  echo "No changes."
fi
