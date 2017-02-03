#!/bin/bash
TOPLEVEL=$(git rev-parse --show-toplevel)

cat <<EOF > "${TOPLEVEL}/README.md"
# pdml2flow-elasticsearch-elasticsearch [![PyPI version](https://badge.fury.io/py/pdml2flow-elasticsearch.svg)](https://badge.fury.io/py/pdml2flow-elasticsearch) 
_Writes [pdml2flow] output to Elasticsearch _

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop) |

## Prerequisites

* [pdml2flow]
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

## Configuration

| Environment variable | Description |
| ------- | ------ |
| ES_HOST | Elasticsearch hostname|
| ES_PORT | Elasticsearch port number |
| ES_INDEX | Elasticsearch index name |
| ES_TYPE | Elasticsearch type name |


## Example

[pdml2flow]: https://github.com/Enteee/pdml2flow
[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
EOF
