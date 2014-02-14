#!/usr/bin/env python3
"""Sum values for each key."""

import sys
from mr import values_by_key, emit

for key, value_iterator in values_by_key(sys.stdin):
    emit(key, sum(value_iterator))
