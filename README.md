# Sudo Code 2024 Setup

## Start database
    cd mariadb
    rename env to .env and config the environments
    docker compose up -d

## Start chatbot backend
    cd chatbot
    rename env to .env and config the environments
    docker compose up -d --build

## Start chatbot UI
    cd chatbot-ui
    docker compose up -d --build
