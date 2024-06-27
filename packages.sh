apk update
apk add py3-pip cmake curl python3-dev libpq-dev gcc ca-certificates musl-dev libc-dev --no-cache
pip install --no-cache-dir --upgrade pip setuptools wheel --root-user-action=ignore --quiet
pip install --no-cache-dir -r requirements.txt --root-user-action=ignore --quiet