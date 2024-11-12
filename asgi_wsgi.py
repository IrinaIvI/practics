import json
import requests
import httpx
from wsgiref.simple_server import make_server

API_URL = "https://api.exchangerate-api.com/v4/latest/USD"

def wsgi_func(environ, start_response):
    if environ['REQUEST_METHOD'] == 'GET':
        try:
            response = requests.get(API_URL)
            data = response.json()
            start_response('200 OK', [("Content-Type", "application/json")])
            return [json.dumps(data).encode('utf-8')]

        except Exception as e:
            start_response('500 Internal Server Error', [("Content-Type", "text/plain")])
            return [f"Internal server error: {str(e)}".encode('utf-8')]
    else:
        start_response('405 Method Not Allowed', [("Content-Type", "text/plain")])
        return ["Method Not Allowed"]
    

async def asgi_func(scope, receive, send):
    if scope["type"] == "http" and scope["method"] == "GET":
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(API_URL)
                response.raise_for_status()
                data = response.json()

                await send({
                    "type": "http.response.start",
                    "status": 200,
                    "headers": [("Content-type", "application/json")],
                })
                await send({
                    "type": "http.response.body",
                    "body": json.dumps(data).encode("utf-8"),
                })

            except Exception as e:
                error_response = {"error": "Internal server error"}
                await send({
                    "type": "http.response.start",
                    "status": 500,
                    "headers": [("Content-type", "application/json")],
                })
                await send({
                    "type": "http.response.body",
                    "body": json.dumps(error_response).encode("utf-8"),
                })

    else:
        error_response = {"error": "Method Not Allowed"}
        await send({
            "type": "http.response.start",
            "status": 405,
            "headers": [("Content-type", "application/json")],
        })
        await send({
            "type": "http.response.body",
            "body": json.dumps(error_response).encode("utf-8"),
        })



if __name__ == '__main__':
    with make_server('', 8000, wsgi_func) as httpd:
        httpd.serve_forever()
