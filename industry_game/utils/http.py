from functools import partial

from aiohttp.web_response import json_response

from industry_game.utils.json import dumps

fast_json_response = partial(json_response, dumps=dumps)
