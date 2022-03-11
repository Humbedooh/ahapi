# ahapi
Asynchronous HTTP API Server for Python 3.5+

Allows you to spin up a simple JSON/formdata capable API server where each 
file in the `api_dir` is an endpoint. formdata or JSON payloads to the API 
endpoints are automatically converted into dictionaries/lists by the server,
and a global state object can be passed to each request.

Main server example:
~~~python3
import ahapi
import asyncio

httpserver = ahapi.simple(
    api_dir="/foo/bar/scripts", 
    bind_ip="127.0.0.1", 
    bind_port="8080", 
    state={"something": "stateful"}
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(httpserver.loop())
~~~

`/foo/bar/scripts/example.py`:
~~~python3
import ahapi
import typing
""" Generic endpoint reachable at http://localhost:8080/example"""

async def process(state: typing.Any, request, formdata: dict) -> dict:
    # do_stuff_here()
    return {
        "some": "json_response",
        "global_state": state,
    }


def register(state: typing.Any):
    return ahapi.endpoint(process)

~~~

## Installing
Use pip to install it, either via `requirements.txt` or via the CLI:
~~~bash
pip install ahapi
~~~

## Serving static content
You can also serve static content from a separate directory, which will mix in with the api handlers:
~~~python3
import ahapi
import asyncio

httpserver = ahapi.simple(
    api_dir="/foo/bar/scripts",    # serve api end points from here
    static_dir="/foo/bar/htdocs",  # serve stuff like html and images from here
    bind_ip="127.0.0.1", 
    bind_port="8080", 
    state={"something": "stateful"}
    )

loop = asyncio.get_event_loop()
loop.run_until_complete(httpserver.loop())
~~~

Static content supports caching via eTag or Last-Modified.


## Using cookies and session objects
You may use persistent session objects tied to HTTP cookies by utilizing the CookieFactory class:

~~~python3
import ahapi
import ahapi.session
import asyncio

my_state = {}
httpserver = ahapi.simple(
    api_dir="/foo/bar/scripts",    # serve api end points from here
    static_dir="/foo/bar/htdocs",  # serve stuff like html and images from here
    bind_ip="127.0.0.1", 
    bind_port="8080", 
    state=my_state
    )

cookie_factory = ahapi.session.CookieFactory(httpserver, cookie_name="mycookie")
my_state["cookies"] = cookie_factory

loop = asyncio.get_event_loop()
loop.run_until_complete(httpserver.loop())
~~~

As the global state is passed on to every request, you can get or set sessions thusly:


`/foo/bar/scripts/example.py`:
~~~python3
import ahapi
import typing
""" Generic endpoint reachable at http://localhost:8080/example"""

async def process(state: typing.Any, request, formdata: dict) -> dict:
    cookie = state["cookies"].get(request)  # Fetches a valid session or None if not found
    if not cookie:
        cookie = state["cookies"].make(request, state)  # generate a new cookie, will automatically be sent to client
        cookie.state = f"Hi, person with cookie ID {cookie.cookie}"  # cookie.state can be any type of object
    return {
        "some": "json_response",
        "cookie_state": cookie.state
    }


def register(state: typing.Any):
    return ahapi.endpoint(process)
~~~

## Error logging
Upon encountering errors, by default, stack traces will be provided to the client.
Traces can be set to either output to the client, stdout (for internal logging), both, or no tracing:

~~~python3
httpserver = ahapi.simple(
    api_dir="/foo/bar/scripts",    # serve api end points from here
    static_dir="/foo/bar/htdocs",  # serve stuff like html and images from here
    bind_ip="127.0.0.1", 
    bind_port="8080", 
    log_stdout=True,  # Send stack traces to stdout
    log_web=False,    # Do not log stacks to client. Since stdout is True, this will log an error id matching the stdout traces
    )
~~~

If web logging is disabled but stdout is enabled, an error ID will be shown to the client that matches the stdout trace.
This error ID can then be used to locate the stack trace from stdout.
