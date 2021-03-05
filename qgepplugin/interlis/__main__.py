import sys
import logging

from . import main
from .utils.various import logger

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s\t%(message)s')
    main(sys.argv[1:])
