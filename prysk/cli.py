"""Main module (invoked by "python3 -m prysk")"""

import sys

import prysk


def main():
    try:
        sys.exit(prysk.main(sys.argv[1:]))
    except (BrokenPipeError, KeyboardInterrupt):  # pragma: nocover
        pass


if __name__ == '__main__':
    main()
