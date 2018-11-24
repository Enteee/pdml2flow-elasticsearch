# vim: set fenc=utf8 ts=4 sw=4 et :
import http
import json
import os

from argparse import ArgumentParser

from datetime import *
from dateutil.tz import *

from pdml2flow.logging import *
from pdml2flow.plugin import Plugin2

HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

argparser = ArgumentParser('Elasticsearch output')

ES_HOST_DEFAULT = os.environ.get('ES_HOST', 'localhost')
argparser.add_argument(
    '--host',
    dest = 'ES_HOST',
    type = str,
    default = ES_HOST_DEFAULT,
    help = 'Elasticsearch api host [default: {}]'.format(
        ES_HOST_DEFAULT
    ),
)


ES_PORT_DEFAULT = os.environ.get('ES_PORT', '9200')
argparser.add_argument(
    '--port',
    dest = 'ES_PORT',
    type = int,
    default = ES_PORT_DEFAULT,
    help = 'Elasticsearch api port [default: {}]'.format(
        ES_PORT_DEFAULT
    ),
)

ES_FLOW_INDEX_DEFAULT = os.environ.get('ES_FLOW_INDEX', 'pdml2flow')
argparser.add_argument(
    '--flowindex',
    dest = 'ES_FLOW_INDEX',
    type = str,
    default = ES_FLOW_INDEX_DEFAULT,
    help = 'Index name [default: {}]'.format(
        ES_FLOW_INDEX_DEFAULT
    ),
)

ES_FLOW_TYPE_DEFAULT = os.environ.get('ES_FLOW_TYPE', 'flow')
argparser.add_argument(
    '--flowtype',
    dest = 'ES_FLOW_TYPE',
    type = str,
    default = ES_FLOW_TYPE_DEFAULT,
    help = 'Type [default: {}]'.format(
        ES_FLOW_TYPE_DEFAULT
    ),
)

ES_NO_FRAMES = os.environ.get('ES_NO_FRAMES', False)
argparser.add_argument(
    '--no-frames',
    action = 'store_true',
    dest = 'ES_NO_FRAMES',
    default = ES_NO_FRAMES,
    help = 'Do not store frames [default: {}]'.format(
        ES_NO_FRAMES
    ),
)

ES_FRAME_INDEX_DEFAULT = os.environ.get('ES_FRAME_INDEX', 'pdml2frame')
argparser.add_argument(
    '--frameindex',
    dest = 'ES_FRAME_INDEX',
    type = str,
    default = ES_FRAME_INDEX_DEFAULT,
    help = 'Index name [default: {}]'.format(
        ES_FRAME_INDEX_DEFAULT
    ),
)

ES_FRAME_TYPE_DEFAULT = os.environ.get('ES_FRAME_TYPE', 'frame')
argparser.add_argument(
    '--frametype',
    dest = 'ES_FRAME_TYPE',
    type = str,
    default = ES_FRAME_TYPE_DEFAULT,
    help = 'Type [default: {}]'.format(
        ES_FRAME_TYPE_DEFAULT
    ),
)

class Elasticsearch(Plugin2):

    @staticmethod
    def help():
        return argparser.format_help()

    def __init__(self, *args):
        self.conf = argparser.parse_args(args)
        debug(
            '{}: {}'.format(
                self.__class__.__name__,
                self.conf
            )
        )

    def _save(self, obj, es_index, es_type):
        """Save object in Elasticsearch."""
        conn = http.client.HTTPConnection(self.conf.ES_HOST, self.conf.ES_PORT)
        conn.request('POST', '/{}-{}/{}/'.format(
            es_index,
            datetime.now().strftime('%F'),
            es_type
        ), json.dumps(obj), HEADERS)
        response = conn.getresponse()
        (debug if response.status in (http.client.OK, http.client.CREATED) else warning)('{} ({}): {}, {}'.format(
            http.client.responses[response.status],
            response.status,
            response.reason,
            json.dumps(
                json.loads(response.read()),
                sort_keys=True,
                indent=4,
                separators=(',', ': ')
            )
        ))
        conn.close()

    def flow_end(self, flow):
        frames = flow.frames
        frames['timestamp'] = datetime.now(
            tzlocal()
        ).strftime('%Y-%m-%dT%H:%M:%S%z')
        self._save(
            frames,
            self.conf.ES_FLOW_INDEX,
            self.conf.ES_FLOW_TYPE
        )

    def frame_new(self, frame, flow):
        if self.conf.ES_NO_FRAMES:
            return

        frame['timestamp'] = datetime.now(
            tzlocal()
        ).strftime('%Y-%m-%dT%H:%M:%S%z')
        self._save(
            frame,
            self.conf.ES_FRAME_INDEX,
            self.conf.ES_FRAME_TYPE
        )


if __name__ == '__main__':
    print(Plugin.help())
