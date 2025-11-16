"""Main module (invoked by "python3 -m cram")"""

import sys

import cram

def main():
    try:
        return cram.main(sys.argv[1:])
    except (BrokenPipeError, KeyboardInterrupt):
        pass

if __name__ == '__main__':
    sys.exit(main())
