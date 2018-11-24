# pdml2flow-elasticsearch [![PyPI version](https://badge.fury.io/py/pdml2flow-elasticsearch.svg)](https://badge.fury.io/py/pdml2flow-elasticsearch) 
_Saves [pdml2flow] output in Elasticsearch_

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop) |

## Prerequisites


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
                            [--frametype ES_FRAME_TYPE] [--user ES_USER]
                            [--password ES_PASSWORD]
                            [--timestamp-field ES_TIMESTAMP_FIELD]
                            [--timestamp-fmt ES_TIMESTAMP_FMT]
                            [--update-flows]
                            [--update-interval ES_UPDATE_FLOWS_INTERVAL__S]
                            [--use-time-now]

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
  --user ES_USER        Elasticsearch user [default: None]
  --password ES_PASSWORD
                        Elasticsearch password [default: None]
  --timestamp-field ES_TIMESTAMP_FIELD
                        Elasticsearch timestamp_field [default: @timestamp]
  --timestamp-fmt ES_TIMESTAMP_FMT
                        Elasticsearch timestamp format [default:
                        %Y-%m-%dT%H:%M:%S%z]
  --update-flows        Wirte flows to elastic search early and keep them up
                        to date [default: False]
  --update-interval ES_UPDATE_FLOWS_INTERVAL__S
                        Elasticsearch update interval [default: 60]
  --use-time-now        Do not store frames [default: False]
```

## Example

## Test environment

```shell
$ sysctl -w vm.max_map_count=262144
$ docker-compose up
```

* Elasticsearch: http://localhost:9000
* Kibana: http://localhost:5601

```yaml
version: '2.2'
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:6.5.1
    container_name: elasticsearch
    environment:
      - cluster.name=docker-cluster
      - bootstrap.memory_lock=true
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"
    ulimits:
      memlock:
        soft: -1
        hard: -1
    volumes:
      - esdata1:/usr/share/elasticsearch/data
    ports:
      - 9200:9200
  kibana:
    image: docker.elastic.co/kibana/kibana:6.5.1
    environment:
      SERVER_NAME: localhost
      ELASTICSEARCH_URL: http://elasticsearch:9200
    ports:
      - 5601:5601

volumes:
  esdata1:
    driver: local
```

[pdml2flow]: https://github.com/Enteee/pdml2flow
[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
