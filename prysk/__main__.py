"""Main module (invoked by "python3 -m prysk")"""
import sys

import prysk.cli

try:
    sys.exit(prysk.cli.main())
except (BrokenPipeError, KeyboardInterrupt):
    sys.exit(2)
