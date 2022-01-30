""" Cli tool to calculate the md5 checksum for one or multiple files """
import argparse
import sys
from hashlib import md5


def _create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "files", metavar="FILE", type=argparse.FileType("rb"), nargs="+"
    )
    return parser


def main(argv=None):
    parser = _create_parser()
    args = parser.parse_args(argv)
    for file in args.files:
        hasher = md5()
        hasher.update(file.read())
        print(hasher.hexdigest())


if __name__ == "__main__":
    sys.exit(main())
