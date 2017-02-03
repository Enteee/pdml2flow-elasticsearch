# vim: set fenc=utf8 ts=4 sw=4 et :
import http, json, os

from datetime import *
from dateutil.tz import *
from base64 import b64encode

from pdml2flow.logging import *
from pdml2flow.plugin import *


ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')
ES_INDEX = os.environ.get('ES_INDEX', 'pdml2flow')
ES_TYPE = os.environ.get('ES_TYPE', 'flow')
ES_USER = os.environ.get('ES_USER', '')
ES_PASSWORD = os.environ.get('ES_PASSWORD', '')

HEADER = { 
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

class Elasticsearch(Plugin1):
    """Stores flows in elasticsearch."""

    def flow_expired(self, flow):
        frames = flow.get_frames()
        frames['timestamp'] = datetime.now(
            tzlocal()
        ).strftime('%Y-%m-%dT%H:%M:%S%z')

        # Send flow to elasticsearch
        conn = http.client.HTTPConnection(ES_HOST, ES_PORT)
        if ES_USER:
            HEADER['Authorization'] = 'Basic {}'.format(
                b64encode('{}:{}'.format(ES_USER, ES_PASSWORD).encode()).decode("ascii")
            )
        conn.request('POST', '/{}-{}/{}/'.format(
            ES_INDEX,
            datetime.now().strftime('%F'),
            ES_TYPE
        ), json.dumps(frames), HEADER)

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
