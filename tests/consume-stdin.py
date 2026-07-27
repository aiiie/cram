#!/usr/bin/env python

import os
import sys

fd = sys.stdin.fileno()
os.set_blocking(fd, False)
try:
    data = os.read(fd, 512)
except BlockingIOError:
    pass
