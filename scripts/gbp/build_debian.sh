#!/usr/bin/env bash

set -euo pipefail

SOURCE=$(realpath "${BASH_SOURCE[0]}")
CURRENT_DIR=$(dirname "$SOURCE")
PROJECT_DIR=$(dirname "$(dirname "$CURRENT_DIR")")

# GnuPG
docker run -it --rm \
  -v ~/.gitconfig:/root/.gitconfig \
  -v ~/.gnupg:/root/.gnupg \
  -v ~/.ssh:/root/.ssh \
  -v /private/var/folders/bz/_4yfstb957l_3r72k3vr58wc0000gp/T/secrets.d/55/id_ed25519:/root/.ssh/id_ed25519 \
  -v /run/host-services/ssh-auth.sock:/run/host-services/ssh-auth.sock \
  -v "${PROJECT_DIR}:/opt/picamzero" \
  -w "/opt/picamzero" \
  -e SSH_AUTH_SOCK="/run/host-services/ssh-auth.sock" \
  -e TERM=xterm-256color \
  -e PS1='\e[92m\u\e[0m@\e[94m\h\e[0m:\e[35m\w\e[0m# ' \
  gbp
