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
ES_TIMESTAMP_FIELD = os.environ.get('ES_TIMESTAMP_FIELD', '@timestamp')
ES_TIMESTAMP_FMT = os.environ.get('ES_TIMESTAMP_FMT', '%Y-%m-%dT%H:%M:%S%z')
ES_UPDATE_INTERVAL__s = int(os.environ.get('ES_UPDATE_INTERVAL', '60'))

HEADER = { 
    'Content-type': 'application/json',
    'Accept': 'application/json',
}

def connect_to_es():
    if ES_USER:
        HEADER['Authorization'] = 'Basic {}'.format(
            b64encode('{}:{}'.format(ES_USER, ES_PASSWORD).encode()).decode("ascii")
        )
    return http.client.HTTPConnection(ES_HOST, ES_PORT)

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

def update_flow(flow):
    frames = flow.get_frames()
    frames[ES_TIMESTAMP_FIELD] = datetime.now(
        tzlocal()
    ).strftime(ES_TIMESTAMP_FMT)

    conn = connect_to_es()
    conn.request('PUT', '/{}-{}/{}/{}'.format(
        ES_INDEX,
        datetime.now().strftime('%F'),
        ES_TYPE,
        frames['ES_ID']
    ), json.dumps(frames), HEADER)
    response = parse_response(conn.getresponse())
    frames['ES_ID'] = response['_id']
    conn.close()

class Elasticsearch(Plugin1):
    """Stores flows in elasticsearch."""

    def flow_new(self, flow, frame):
        frames = flow.get_frames()
        frames[ES_TIMESTAMP_FIELD] = datetime.now(
            tzlocal()
        ).strftime(ES_TIMESTAMP_FMT)

        conn = connect_to_es()
        conn.request('POST', '/{}-{}/{}/'.format(
            ES_INDEX,
            datetime.now().strftime('%F'),
            ES_TYPE
        ), json.dumps(frames), HEADER)
        response = parse_response(conn.getresponse())
        frames['ES_ID'] = response['_id']
        conn.close()

    def frame_new(self, frame, flow):
        frames = flow.get_frames()
        if (datetime.now(
            tzlocal()
        ) - datetime.strptime(
            frames[ES_TIMESTAMP_FIELD], 
            ES_TIMESTAMP_FMT
        )).seconds >= ES_UPDATE_INTERVAL__s:
            update_flow(flow)

    def flow_expired(self, flow):
        update_flow(flow)
