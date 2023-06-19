#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import requests

from client import SSEClient
from config import config


app = Flask(__name__)


def update_url(request: requests.Request) -> str:
    url = request.url.replace(request.host_url, config['OPENAI_API_HOST'])
    return url


def update_stream_param(request: requests.Request) -> bool:
    stream = False
    try:
        stream = request.get_json().get('stream', False)
    except:
        pass
    return stream


def get_request_headers(request: requests.Request) -> dict:
    headers = {key: value for (key, value) in request.headers if key != 'Host'}
    return headers


def update_authorization_headers(headers: dict) -> dict:
    headers.update({'Authorization': f'Bearer {config["OPENAI_API_KEY"]}'})
    headers.update({'OpenAI-Organization': config["OPENAI_ORGANIZATION"]})
    return headers


def get_response_headers(response: Response) -> dict:
    excluded_headers = ['content-encoding',
                        'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in response.raw.headers.items(
    ) if name.lower() not in excluded_headers]
    return headers


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = update_url(request)
    stream = update_stream_param(request)
    headers = get_request_headers(request)
    update_authorization_headers(headers)
    resp = requests.request(
        method=request.method,
        url=url,
        stream=stream,
        headers=headers,
        data=request.get_data(),
        allow_redirects=False)
    if not stream:
        headers = get_response_headers(resp)
        response = app.make_response((resp.content, resp.status_code, headers))
        return response

    def stream_generate():
        client = SSEClient(resp)
        for event in client.events():
            yield ('data: ' + event.data + '\n\n')
    return Response(stream_generate(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000, debug=True)
