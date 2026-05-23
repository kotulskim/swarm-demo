#!/bin/bash
set -e

cd /root/swarm-demo

git fetch origin main

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" != "$REMOTE" ]; then
  echo "New git version found. Pulling..."
  git pull origin main
fi

APP_TAG=$(git rev-parse --short HEAD)
CURRENT_IMAGE=$(docker service inspect demo_web --format '{{.Spec.TaskTemplate.ContainerSpec.Image}}' 2>/dev/null || echo "")

echo "Current image: $CURRENT_IMAGE"
echo "Expected tag: $APP_TAG"

if echo "$CURRENT_IMAGE" | grep -q ":$APP_TAG"; then
  echo "Service already uses current tag. No deploy needed."
else
  echo "Deploying tag: $APP_TAG"
  APP_TAG=$APP_TAG docker stack deploy -c stack.yml demo
fi
