#!/bin/bash

BRANCH="main"

git pull origin "$BRANCH"

# Rebuild Docker Compose images
docker compose build

# Restart/Start all Docker Compose services
docker compose up -d
