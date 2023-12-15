import re
from loguru import logger
from collections import defaultdict

from string import Template
from app import sio


STORE = {}
LISTENERS = defaultdict(list)


async def update_store(key: str, value: str):
    stripped_key = key.split(":")[-1]
    STORE[stripped_key] = value
    logger.info(f"UPDATE: {key} = {value}")
    await sio.emit("update", {"key": key, "value": value})


@sio.event
def connect(sid, environ, __):
    logger.info(f"{environ['REMOTE_ADDR']} connected")


@sio.event
def disconnect(sid):
    logger.info(f"{sid} disconnected")


@sio.event
def get_store(sid):
    return STORE

@sio.event
def clear_store(sid):
    STORE.clear()

def extract_placeholders(input_string):
    pattern = r'\$(?:(?P<escaped>\$)|(?P<braced>\{[^}]+\})|(?P<unbraced>[a-zA-Z_][a-zA-Z0-9_]*))'
    matches = re.finditer(pattern, input_string)

    placeholders = []
    for match in matches:
        if match.group('braced'):
            # Remove the curly braces
            placeholders.append(match.group('braced')[1:-1])
        elif match.group('unbraced'):
            placeholders.append(match.group('unbraced'))

    return placeholders


def update_template(ltnr: dict):
    key, template_str = ltnr["key"], ltnr["placeholder"]
    print(key, template_str)
    temp = Template(template_str)
    return key, temp.safe_substitute(STORE)


async def update_listeners_for(key: str):
    for ltnr in LISTENERS[key]:
        n_key, value = update_template(ltnr)
        await update_store(n_key, value)


async def check_for_placeholders(key: str, value: str) -> bool:
    placeholders = extract_placeholders(value)
    for place in placeholders:
        new_ltnr = {"key": key, "placeholder": value}
        LISTENERS[place].append(new_ltnr)
        key, value = update_template(new_ltnr)
        await update_store(key, value)
   

@sio.event
async def send_signal(sid, payload):
    signal_key = payload["signal"]
    await sio.emit("signal", {"key": signal_key})


@sio.event
async def do_update(sid, payload):
    key, value = payload["key"], payload["value"]
    """
    if await check_for_placeholders(key, value):
        logger.info(f"ADDED PLACEHOLDER: {key} = {value}")
    else:
        await update_store(key, value)
    
    if key in LISTENERS:
        await update_listeners_for(key)
    """
    await update_store(key, value)
