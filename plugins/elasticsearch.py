# vim: set fenc=utf8 ts=4 sw=4 et :
import http
import json
import os

from argparse import ArgumentParser

from datetime import datetime
from dateutil.tz import tzlocal
from base64 import b64encode

from pdml2flow.logging import *
from pdml2flow.utils import make_argparse_help_safe
from pdml2flow.conf import Conf
from pdml2flow.autovivification import getitem_by_path
from pdml2flow.plugin import Plugin2

HEADER = { 
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

argparser = ArgumentParser('Elasticsearch output')

ES_HOST_DEFAULT = os.environ.get('ES_HOST', 'localhost')
argparser.add_argument(
    '--host',
    dest = 'ES_HOST',
    type = str,
    default = ES_HOST_DEFAULT,
    help = 'Elasticsearch api host [default: {}]'.format(
        make_argparse_help_safe(ES_HOST_DEFAULT)
    ),
)

ES_PORT_DEFAULT = int(os.environ.get('ES_PORT', 9200))
argparser.add_argument(
    '--port',
    dest = 'ES_PORT',
    type = int,
    default = ES_PORT_DEFAULT,
    help = 'Elasticsearch api port [default: {}]'.format(
        make_argparse_help_safe(ES_PORT_DEFAULT)
    ),
)

ES_FLOW_INDEX_DEFAULT = os.environ.get('ES_FLOW_INDEX', 'pdml2flow')
argparser.add_argument(
    '--flowindex',
    dest = 'ES_FLOW_INDEX',
    type = str,
    default = ES_FLOW_INDEX_DEFAULT,
    help = 'Index name [default: {}]'.format(
        make_argparse_help_safe(ES_FLOW_INDEX_DEFAULT)
    ),
)

ES_FLOW_TYPE_DEFAULT = os.environ.get('ES_FLOW_TYPE', 'flow')
argparser.add_argument(
    '--flowtype',
    dest = 'ES_FLOW_TYPE',
    type = str,
    default = ES_FLOW_TYPE_DEFAULT,
    help = 'Type [default: {}]'.format(
        make_argparse_help_safe(ES_FLOW_TYPE_DEFAULT)
    ),
)

ES_NO_FRAMES_DEFAULT = bool(os.environ.get('ES_NO_FRAMES', False))
argparser.add_argument(
    '--no-frames',
    action = 'store_true',
    dest = 'ES_NO_FRAMES',
    default = ES_NO_FRAMES_DEFAULT,
    help = 'Do not store frames [default: {}]'.format(
        make_argparse_help_safe(ES_NO_FRAMES_DEFAULT)
    ),
)

ES_FRAME_INDEX_DEFAULT = os.environ.get('ES_FRAME_INDEX', 'pdml2frame')
argparser.add_argument(
    '--frameindex',
    dest = 'ES_FRAME_INDEX',
    type = str,
    default = ES_FRAME_INDEX_DEFAULT,
    help = 'Index name [default: {}]'.format(
        make_argparse_help_safe(ES_FRAME_INDEX_DEFAULT)
    ),
)

ES_FRAME_TYPE_DEFAULT = os.environ.get('ES_FRAME_TYPE', 'frame')
argparser.add_argument(
    '--frametype',
    dest = 'ES_FRAME_TYPE',
    type = str,
    default = ES_FRAME_TYPE_DEFAULT,
    help = 'Type [default: {}]'.format(
        make_argparse_help_safe(ES_FRAME_TYPE_DEFAULT)
    ),
)

ES_USER_DEFAULT = os.environ.get('ES_USER', None)
argparser.add_argument(
    '--user',
    dest = 'ES_USER',
    type = str,
    default = ES_USER_DEFAULT,
    help = 'Elasticsearch user [default: {}]'.format(
        make_argparse_help_safe(ES_USER_DEFAULT)
    ),
)

ES_PASSWORD_DEFAULT = os.environ.get('ES_PASSWORD', None)
argparser.add_argument(
    '--password',
    dest = 'ES_PASSWORD',
    type = str,
    default = ES_PASSWORD_DEFAULT,
    help = 'Elasticsearch password [default: {}]'.format(
        make_argparse_help_safe(ES_PASSWORD_DEFAULT)
    ),
)

ES_TIMESTAMP_FIELD_DEFAULT = os.environ.get('ES_TIMESTAMP_FIELD', '@timestamp')
argparser.add_argument(
    '--timestamp-field',
    dest = 'ES_TIMESTAMP_FIELD',
    type = str,
    default = ES_TIMESTAMP_FIELD_DEFAULT,
    help = 'Elasticsearch timestamp_field [default: {}]'.format(
        make_argparse_help_safe(ES_TIMESTAMP_FIELD_DEFAULT)
    ),
)

ES_TIMESTAMP_FMT_DEFAULT = os.environ.get('ES_TIMESTAMP_FMT', '%Y-%m-%dT%H:%M:%S%z')
argparser.add_argument(
    '--timestamp-fmt',
    dest = 'ES_TIMESTAMP_FMT',
    type = str,
    default = ES_TIMESTAMP_FMT_DEFAULT,
    help = 'Elasticsearch timestamp format [default: {}]'.format(
        make_argparse_help_safe(ES_TIMESTAMP_FMT_DEFAULT)
    ),
)

ES_UPDATE_FLOWS_DEFAULT = bool(os.environ.get('ES_UPDATE_FLOWS', False))
argparser.add_argument(
    '--update-flows',
    action = 'store_true',
    dest = 'ES_UPDATE_FLOWS',
    default = ES_UPDATE_FLOWS_DEFAULT,
    help = 'Wirte flows to elastic search early and keep them up to date [default: {}]'.format(
        make_argparse_help_safe(ES_UPDATE_FLOWS_DEFAULT)
    ),
)

ES_UPDATE_FLOWS_INTERVAL_DEFAULT = int(os.environ.get('ES_UPDATE_FLOWS_INTERVAL', 60))
argparser.add_argument(
    '--update-interval',
    dest = 'ES_UPDATE_FLOWS_INTERVAL__s',
    type = int,
    default = ES_UPDATE_FLOWS_INTERVAL_DEFAULT,
    help = 'Elasticsearch update interval [default: {}]'.format(
        make_argparse_help_safe(ES_UPDATE_FLOWS_INTERVAL_DEFAULT)
    ),
)

ES_USE_TIME_NOW_DEFAULT = bool(os.environ.get('ES_USE_TIME_NOW', False))
argparser.add_argument(
    '--use-time-now',
    action = 'store_true',
    dest = 'ES_USE_TIME_NOW',
    default = ES_USE_TIME_NOW_DEFAULT,
    help = 'Do not store frames [default: {}]'.format(
        make_argparse_help_safe(ES_USE_TIME_NOW_DEFAULT)
    ),
)

def parse_response(response):
    response_json = json.loads(response.read())
    (debug if response.status in (http.client.OK, http.client.CREATED) else warning)('{} ({}): {}, {}'.format(
        http.client.responses[response.status],
        response.status,
        response.reason,
        json.dumps(
            response_json,
            sort_keys=True,
            indent=4,
            separators=(',', ': ')
        )
    ))
    return response_json

class Elasticsearch(Plugin2):

    OBJECT_ID = {}

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

        if self.conf.ES_USER:
            HEADER['Authorization'] = 'Basic {}'.format(
                b64encode('{}:{}'.format(
                    self.conf.ES_USER,
                    self.conf.ES_PASSWORD
                ).encode()).decode("ascii")
            )

    def _save(self, obj, time, es_index, es_type):
        """Save object in Elasticsearch."""

        # update timestamp with time now
        if self.conf.ES_USE_TIME_NOW:
            time = datetime.now()

        obj[self.conf.ES_TIMESTAMP_FIELD] = time.replace(
            tzinfo=tzlocal()
        ).strftime(
            self.conf.ES_TIMESTAMP_FMT
        )

        # store in es
        obj_json = json.dumps(obj)
        conn = http.client.HTTPConnection(
            self.conf.ES_HOST,
            self.conf.ES_PORT
        )
        try:
            es_id = Elasticsearch.OBJECT_ID[obj]
        except (KeyError, TypeError):
            es_id = None

        if not es_id:
            # not in index, add object now
            conn.request(
                'POST', '/{}-{}/{}/'.format(
                    es_index,
                    datetime.now().strftime('%F'),
                    es_type
                ),
                obj_json,
                HEADER
            )
        else:
            # try updating
            conn.request(
                'PUT', '/{}-{}/{}/{}'.format(
                    es_index,
                    datetime.now().strftime('%F'),
                    es_type,
                    es_id,
                ),
                obj_json,
                HEADER
            )

        # update ES_ID
        response = parse_response(conn.getresponse())
        try:
            Elasticsearch.OBJECT_ID[obj] = response['_id']
        except TypeError:
            pass
        conn.close()

    def frame_new(self, frame, flow):
        if not self.conf.ES_NO_FRAMES:
            self._save(
                frame,
                datetime.utcfromtimestamp(
                    getitem_by_path(frame, Conf.FRAME_TIME)
                ),
                self.conf.ES_FRAME_INDEX,
                self.conf.ES_FRAME_TYPE
            )
        if self.conf.ES_UPDATE_FLOWS:
            try:
                frames = flow.frames
            except AttributeError:
                return
            if (datetime.now(
                tzlocal()
            ) - datetime.strptime(
                frames[self.conf.ES_TIMESTAMP_FIELD],
                self.conf.ES_TIMESTAMP_FMT
            )).seconds >= self.conf.ES_UPDATE_FLOWS_INTERVAL__s:
                self._save(
                    flow.frames,
                    datetime.utcfromtimestamp(flow.first_frame_time),
                    self.conf.ES_FLOW_INDEX,
                    self.conf.ES_FLOW_TYPE
                )


    def flow_new(self, flow, frame):
        if self.conf.ES_UPDATE_FLOWS:
            self._save(
                flow.frames,
                datetime.utcfromtimestamp(flow.first_frame_time),
                self.conf.ES_FLOW_INDEX,
                self.conf.ES_FLOW_TYPE
            )

    def flow_end(self, flow):
        self._save(
            flow.frames,
            datetime.utcfromtimestamp(flow.first_frame_time),
            self.conf.ES_FLOW_INDEX,
            self.conf.ES_FLOW_TYPE
        )


if __name__ == '__main__':
    print(Elasticsearch.help())
