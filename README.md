# pdml2flow-elasticsearch [![PyPI version](https://badge.fury.io/py/pdml2flow-elasticsearch.svg)](https://badge.fury.io/py/pdml2flow-elasticsearch) 
_Saves [pdml2flow] output in Elasticsearch_

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop) |

## Prerequisites

* [pdml2flow]

* [pip](https://pypi.python.org/pypi/pip)

## Installation

```shell
    $ sudo pip install pdml2flow-elasticsearch
```

## Usage

```shell
$ pdml2flow +elasticsearch -h
usage: Elasticsearch output [-h] [--host ES_HOST] [--port ES_PORT]
                            [--flowindex ES_FLOW_INDEX]
                            [--flowtype ES_FLOW_TYPE] [--no-frames]
                            [--frameindex ES_FRAME_INDEX]
                            [--frametype ES_FRAME_TYPE]

optional arguments:
  -h, --help            show this help message and exit
  --host ES_HOST        Elasticsearch api host [default: localhost]
  --port ES_PORT        Elasticsearch api port [default: 9200]
  --flowindex ES_FLOW_INDEX
                        Index name [default: pdml2flow]
  --flowtype ES_FLOW_TYPE
                        Type [default: flow]
  --no-frames           Do not store frames [default: False]
  --frameindex ES_FRAME_INDEX
                        Index name [default: pdml2frame]
  --frametype ES_FRAME_TYPE
                        Type [default: frame]
```

## Example

## Test environment

```shell
$ sysctl -w vm.max_map_count=262144
$ docker-compose up
```

* Elasticsearch: http://localhost:9000
* Kibana: http://localhost:5601

[pdml2flow]: https://github.com/Enteee/pdml2flow
[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
