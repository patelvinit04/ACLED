import acled

import logging
import argparse
import sys

parser = argparse.ArgumentParser(description='For running GDELT v1 and v2 ETL processes')

parser.add_argument('--log-level', type=str, help='The logging level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', dest='logLevel')

def setup_logger(log_level):
    logFormatter = logging.Formatter(
        "%(asctime)s [%(filename)s:%(lineno)s - %(funcName)20s()] [%(levelname)-4.7s]  %(message)s"
    )

    log = logging.getLogger("acled")
    log.setLevel(log_level)
    log.propagate = False

    if len(log.handlers) < 1:
        streamHandler = logging.StreamHandler(sys.stdout)
        streamHandler.setFormatter(logFormatter)
        log.addHandler(streamHandler)
    else:
        streamHandler = log.handlers[0]
        streamHandler.setFormatter(logFormatter)


if __name__ == "__main__":
    args = parser.parse_args()
    setup_logger(args.logLevel)
    acled.exec()