"""Functional testing framework for command line applications"""
import sys

import prysk.cli


def main():
    try:
        sys.exit(prysk.cli.main())
    except (BrokenPipeError, KeyboardInterrupt):
        sys.exit(2)


if __name__ == "__main__":
    main()
