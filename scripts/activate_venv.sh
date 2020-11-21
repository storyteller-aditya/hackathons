#!/usr/bin/env bash

set -o errexit
set -o pipefail
set -o nounset


__scripts_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
__root_dir="$(cd "$(dirname "${__scripts_dir}")" && pwd)"


[ -z "${VIRTUAL_ENV_DIR-}" ] && VIRTUAL_ENV_DIR=${__root_dir}/env
echo "Virtual Env Directory: ${VIRTUAL_ENV_DIR}"


if [ ! -d ${VIRTUAL_ENV_DIR} ]
then
	python3 -m venv ${VIRTUAL_ENV_DIR}
	source ${VIRTUAL_ENV_DIR}/bin/activate
	pip install -r ${__root_dir}/requirements.txt
else
	source ${VIRTUAL_ENV_DIR}/bin/activate
fi
export PYTHONPATH=${__root_dir}:${PYTHONPATH-}
