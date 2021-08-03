import ahapi
import typing
""" Generic endpoint reachable at http://localhost:8080/example"""


async def process(state: typing.Any, request, formdata: dict) -> dict:
    if formdata.get("format") == "text":
        return "This is an example string"
    else:
        return {
            "some": "json_response"
        }


def register(state: typing.Any):
    return ahapi.endpoint(process)
