#!/usr/bin/env bash

chall=$(basename "$(pwd)")

if ! echo "${chall}" | grep -qP 'chall-\d\d'; then
    echo 'Not inside challenge directory' >&2
    exit 1
fi

CHALL_BIN="./bin-${chall}"

echo "[+] Downloading challenge binary file"
docker cp "intro2rop-${chall}-1":/srv/app/run "${CHALL_BIN}"
echo "[+] File downloaded: ${CHALL_BIN}"

if ! [ -f ./solve.py ]; then
    echo
    echo "[+] Generating base solve script"
    sed "s/<CHALL_PLACEHOLDER>/${chall}/" ../template.py > ./solve.py
    chmod +x ./solve.py
    echo "[+] Solve script generated: ./solve.py"
fi
