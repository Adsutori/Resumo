#!/usr/bin/env bash
set -o errexit

curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
export PATH="$HOME/.cargo/bin:$PATH"

pip install -r requirements.txt
python manage.py collectstatic --no-input
