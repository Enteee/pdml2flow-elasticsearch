#!/usr/bin/env bash
set -exuo pipefail

TOPLEVEL="$( cd "$(dirname "$0")" ; pwd -P )/../"

# Install plugin
sudo pip install --upgrade -e "${TOPLEVEL}"

cat <<EOF > "${TOPLEVEL}/README.md"
# pdml2flow-elasticsearch [![PyPI version](https://badge.fury.io/py/pdml2flow-elasticsearch.svg)](https://badge.fury.io/py/pdml2flow-elasticsearch) 
_Saves [pdml2flow] output in Elasticsearch_

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop) |

## Prerequisites

$( cat "${TOPLEVEL}/.travis.yml" | 
    sed -n -e '/# VERSION START/,/# VERSION END/ p' |
    sed -e '1d;$d' |
    tr -d \'\"  |
    sed -e 's/\s*-\(.*\)/  -\1/g' |
    sed -e 's/python/\* [python\]/g'
)
* [pip](https://pypi.python.org/pypi/pip)

## Installation

\`\`\`shell
$ sudo pip install pdml2flow-elasticsearch
\`\`\`

## Usage

\`\`\`shell
$ pdml2flow +elasticsearch -h
$(pdml2flow +elasticsearch -h)
\`\`\`

## Example

## Test environment

\`docker-compose.yml\`:

\`\`\`yaml
$(cat "${TOPLEVEL}/docker-compose.yml")
\`\`\`

Start the environment:

\`\`\`shell
$ sysctl -w vm.max_map_count=262144
$ docker-compose up
\`\`\`

* Elasticsearch: http://localhost:9000
* Kibana: http://localhost:5601

[pdml2flow]: https://github.com/Enteee/pdml2flow
[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
EOF
