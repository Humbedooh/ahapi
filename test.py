import ahapi
import asyncio

httpserver = ahapi.simple(
    api_dir="./example_scripts/",
    bind_ip="127.0.0.1",
    bind_port="8080",
    state={"something": "stateful"}
)

loop = asyncio.get_event_loop()
loop.run_until_complete(httpserver.loop(forever=True))

