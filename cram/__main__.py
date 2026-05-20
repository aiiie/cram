"""Main module (invoked by "python3 -m cram")"""

import sys

import cram

__all__ = ['main']

def main() -> int:
    """Run cram"""
    try:
        return cram.main(sys.argv[1:])
    except (BrokenPipeError, KeyboardInterrupt): # pragma: nocover
        return 0

if __name__ == '__main__':
    sys.exit(main())
