#!/usr/bin/env python

import os
import re
import sys

ORDERING_FIELD = "propertyOrder"
SCHEMA_DIRECTORY = "schemas"


class OrderingGenerator(object):
    def __init__(self, field, start=0, incr=10):
        self.field = field
        self.count = start
        self.incr = incr

    def __call__(self, match):
        self.count += self.incr
        return '"%s": %d' % (self.field, self.count)


def renumber_schema(schema_contents):
    pattern = re.compile('"' + ORDERING_FIELD + '": (\\d+)')

    return re.sub(pattern, OrderingGenerator(ORDERING_FIELD), schema_contents)


def main():

    if len(sys.argv) < 2:
        print("Usage: " + sys.argv[0] + " <schema_file>")
        exit(1)

    schema_file = os.path.join(SCHEMA_DIRECTORY, sys.argv[1])

    with open(schema_file, "rb") as f:
        schema_contents = f.read().decode("utf-8")

    new_contents = renumber_schema(schema_contents)

    with open(schema_file, "wb") as f:
        schema_contents = f.write(new_contents.encode("utf-8"))


if __name__ == '__main__':
    main()
