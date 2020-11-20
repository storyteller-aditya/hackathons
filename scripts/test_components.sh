#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


__scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root_dir="$(cd "$(dirname "${__scripts_dir}")" && pwd)"


source ${__scripts_dir}/activate_venv.sh
cd ${__root_dir}
python -m unittest discover
