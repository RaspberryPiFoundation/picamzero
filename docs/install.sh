#!/usr/bin/env bash

set -euo pipefail

if [ "$(whoami)" = "root" ]; then
  echo "WARNING: user is root"
  SUDO=
else
  SUDO=sudo
fi
VENV_NAME='picamzero-venv'

DEPENDENCIES=(
  python3-pip
  python3-venv
  libcap-dev
  python3-libcamera
  python3-opencv
  python3-picamera2
  python3-numpy
  python3-opencv
)
echo "***************************"
echo "Picamera Zero (picamzero)"
echo "***************************"
echo "I will need to use sudo to install some dependencies"
echo "-------------------------------------------------------------"
$SUDO apt-get update
$SUDO apt-get install -y "${DEPENDENCIES[@]}"
(cd "$HOME" && python3 -m venv --system-site-packages "$VENV_NAME")
source "${HOME}/${VENV_NAME}/bin/activate"
pip install picamzero

echo "-------------------------------------------------------------"
echo "All done!"
echo "Created virtual environment \"${VENV_NAME}\""
echo "To use picamzero with Thonny, follow the instructions here:"
echo "https://rpf.io/thonny-install"

