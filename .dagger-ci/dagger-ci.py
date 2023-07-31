#!/usr/bin/python


# Logging
# https://docs.python.org/3/howto/logging.html
# DEBUG, INFO, WARNING, ERROR, CRITICAL
import logging

import os
import sys
import datetime
import anyio
import dagger

# Global variables
LOG_LEVEL = logging.INFO


async def main():
    '''
    The main function, duh
    '''
    async with dagger.Connection(dagger.Config(log_output=sys.stderr)) as client:
        # invalidate cache to force execution
        # of second with_exec() operation
        output = await (
            client.pipeline(name="test", description="whatever")
            .container()
            .from_("alpine")
            .with_exec(["apk", "add", "curl"])
            .with_env_variable("CACHEBUSTER", str(datetime.datetime.now()))
            .with_exec(["apk", "add", "zip"])
            .stdout()
        )
    print(output)


if __name__ == '__main__':
    #####
    # Mandatory guard
    # Detailed explanation: https://stackoverflow.com/a/419185
    #####
    # Setup nice logging
    logging.basicConfig(format='%(levelname)s: %(message)s', level=LOG_LEVEL)

    # LET'S DO IT !!!
    sys.exit(anyio.run(main))

