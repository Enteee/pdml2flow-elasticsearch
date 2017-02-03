# vim: set fenc=utf8 ts=4 sw=4 et :
import http, json, os

from datetime import *
from dateutil.tz import *

from pdml2flow.logging import *
from pdml2flow.plugin import *

HEADERS = {'Content-type': 'application/json', 'Accept': 'application/json'}

ES_HOST = os.environ.get('ES_HOST', 'localhost')
ES_PORT = os.environ.get('ES_PORT', '9200')
ES_INDEX = os.environ.get('ES_INDEX', 'pdml2flow')
ES_TYPE = os.environ.get('ES_TYPE', 'flow')

class Elasticsearch(Plugin1):
    """Stores flows in elasticsearch."""

    def flow_expired(self, flow):
        frames = flow.get_frames()
        frames['timestamp'] = datetime.now(
            tzlocal()
        ).strftime('%Y-%m-%dT%H:%M:%S%z')

        # Send flow to elasticsearch
        conn = http.client.HTTPConnection(ES_HOST, ES_PORT)
        conn.request('POST', '/{}-{}/{}/'.format(
            ES_INDEX,
            datetime.now().strftime('%F'),
            ES_TYPE
        ), json.dumps(frames), HEADERS)
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
