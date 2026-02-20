#!/bin/bash

set -eao pipefail

ROOT_DIR=$(pwd)
TRADING_BOT_DIR=$ROOT_DIR"/trading-bot"
MARKET_MATCHING_DIR=$ROOT_DIR"/market-matching"
DOCKER_DIR=$ROOT_DIR"/docker"
SECRETS_DIR=$ROOT_DIR/"secrets"

POSTGRES_ENV="postgres.env"
DOCKER_ENV="docker.env"

# Init
mkdir -p $SECRETS_DIR

# Setting up python
read -rp $'Setup Python virtual environment? [Y/n] ' -n 1
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
    echo "Setting up python virtual environment..."
    cd $MARKET_MATCHING_DIR

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    deactivate

    cd $ROOT
    echo "Done!"
    echo ""
fi

# Setting up Postgres
read -rp $'Setup Postgres? [Y/n] ' -n 1
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
    echo "Setting up Postgres..."
    cd $SECRETS_DIR

    read -rep $'Postgres Password:\n > ' -i "password123" postgres_password
    read -rep $'Postgres Database:\n > ' -i "spellbookdb" postgres_database

    rm $POSTGRES_ENV 2>/dev/null || true
    echo "POSTGRES_PASSWORD="$postgres_password >> $POSTGRES_ENV
    echo "POSTGRES_DB="$postgres_database >> $POSTGRES_ENV

    cd $ROOT
    echo "Done!"
    echo ""
fi

# Setting up Docker
read -rp $'Setup Docker? [Y/n] ' -n 1
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
    echo "Setting up Docker..."
    cd $SECRETS_DIR

    read -rep $'Timezone:\n > ' -i "America/New_York" timezone

    rm $DOCKER_ENV 2>/dev/null || true
    echo "TIMEZONE="$timezone >> $DOCKER_ENV

    cd $DOCKER_DIR
    sudo docker compose pull

    cd $ROOT
    echo "Done!"
    echo ""
fi

# Setting up trading bot + dashboard
read -rp $'Setup Trading Bot and Dashboard? [Y/n] ' -n 1
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]
then
    echo "Setting up Trading Bot + Dashboard"
    cd $TRADING_BOT_DIR"/client"
    npm install

    cd $TRADING_BOT_DIR"/server"
    npm install

    cd $ROOT
    echo "Done!"
    echo ""
fi