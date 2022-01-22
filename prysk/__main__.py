"""Main module (invoked by "python3 -m prysk")"""

import sys

import prysk

try:
    sys.exit(prysk.main(sys.argv[1:]))
except (BrokenPipeError, KeyboardInterrupt):
    pass
