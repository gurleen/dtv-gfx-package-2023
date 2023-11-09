from models import *
import msgspec
import os
from loguru import logger


STORE_FILE = "store.hydra"


class Store(msgspec.Struct):
    graphics: list[Graphic]


store: Store = None
if os.path.isfile(STORE_FILE):
    try:
        with open(STORE_FILE, "rb") as storefile:
            logger.info("Store file was found.")
            decoded_store = msgspec.msgpack.decode(storefile.read())
            if type(decoded_store) == Store:
                store = decoded_store
                logger.info("Store file was successfully decoded.")
    except Exception as e:
        logger.error("Error trying to load store file. Creating a new store.")
        logger.trace(e)
        store = Store(graphics=[])
else:
    logger.info("Store file not found. Creating a new store.")
    store = Store(graphics=[])


logger.info("Store initalized.")


def save_store():
    with open(STORE_FILE, "wb") as storefile:
        bin_data = msgspec.msgpack.encode(store)
        storefile.write(bin_data)
    logger.info("Store was saved.")