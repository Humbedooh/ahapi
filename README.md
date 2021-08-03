# ahapi
Asynchronous HTTP API Server for Python


Main server example:
~~~python3
import ahapi.server

httpserver = ahapi.simple(api_dir="/foo/bar/scripts", bind_ip="127.0.0.1", bind_port="8080", state={"something": "stateful"})

loop = asyncio.get_event_loop()
loop.run_until_complete(httpserver.loop())
~~~

`/foo/bar/scripts/example.py`:
~~~python3
import ahapi.server
import typing
""" Generic endpoint reachable at http://localhost:8080/example"""

async def process(state: typing.Any, request, formdata: dict) -> dict:
    # do_stuff_here()
    return {
        "some": "json_response"
    }


def register(server: ahapi.server.Server):
    return ahapi.server.Endpoint(process)

~~~
