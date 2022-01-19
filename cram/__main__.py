"""Main module (invoked by "python3 -m cram")"""

import sys

import cram

try:
    sys.exit(cram.main(sys.argv[1:]))
except (BrokenPipeError, KeyboardInterrupt):
    pass
