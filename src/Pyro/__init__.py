# Pyro package.
# Contains some generic init stuff.

import logging

if len(logging.root.handlers)==0:
    # configure the logging with some sensible defaults.
    logging.basicConfig(
        level=logging.DEBUG,
        filename="pyro.log",
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d,%(name)s,%(levelname)s] %(message)s"
        )
    log=logging.getLogger("Pyro")
    log.info("Pyro log configured using built-in defaults")

