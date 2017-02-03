# pdml2flow-elasticsearch-elasticsearch [![PyPI version](https://badge.fury.io/py/pdml2flow-elasticsearch.svg)](https://badge.fury.io/py/pdml2flow-elasticsearch) 
_Aggregates wireshark pdml to flows_

| Branch  | Build  | Coverage |
| ------- | ------ | -------- |
| master  | [![Build Status master]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status master]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=master) |
| develop  | [![Build Status develop]](https://travis-ci.org/Enteee/pdml2flow-elasticsearch) | [![Coverage Status develop]](https://coveralls.io/github/Enteee/pdml2flow-elasticsearch?branch=develop) |

## Prerequisites
* [python]:
  - 3.4
  - 3.5
  - 3.5-dev
  - nightly
* [pip](https://pypi.python.org/pypi/pip)

## Installation
```shell
    $ sudo pip install pdml2flow-elasticsearch
```

## Configuration

ES_HOST
| Environment variable | Description |
| ------- | ------ |
| ES_HOST | Elasticsearch hostname|
| ES_PORT | Elasticsearch port number |
| ES_INDEX | Elasticsearch index name |
| ES_TYPE | Elasticsearch type name |


## Example

[python]: https://www.python.org/
[wireshark]: https://www.wireshark.org/
[dict2xml]: https://github.com/delfick/python-dict2xml
[jq]: https://stedolan.github.io/jq/
[FluentFlow]: https://github.com/t-moe/FluentFlow

[Build Status master]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=master
[Coverage Status master]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=master
[Build Status develop]: https://travis-ci.org/Enteee/pdml2flow-elasticsearch.svg?branch=develop
[Coverage Status develop]: https://coveralls.io/repos/github/Enteee/pdml2flow-elasticsearch/badge.svg?branch=develop
