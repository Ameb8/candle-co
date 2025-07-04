#!/bin/bash

# Load environment variables from .env
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
fi

# Set DJANGO_SETTINGS_MODULE to production settings
export DJANGO_SETTINGS_MODULE=candle_co.settings.production

gunicorn candle_co.wsgi:application --bind 0.0.0.0:8000 --timeout 120 --log-level debug
