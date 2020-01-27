#!/usr/bin/env python

import os
import re
import sys

SECTION_BEGIN_FIELD = "sectionBegin"
SECTION_END_FIELD = "sectionEnd"
SCHEMA_DIRECTORY = "schemas"

def validate_sections(schema_contents, file_name):
    pattern = re.compile('"' + '(' + SECTION_BEGIN_FIELD + '|' + SECTION_END_FIELD + ')' + '":\\s*"(.*)"')
    it = pattern.finditer(schema_contents)
    stack = []
    for match in it:
      if match.group(1) == SECTION_BEGIN_FIELD:
        if len(stack) > 0:
          # Two sectionBegin
          print("Error in " + file_name + "! There are two overlap " + SECTION_BEGIN_FIELD + ': "' + stack.pop() + '" and "' + match.group(2) + '"')
          exit(1)
        stack.append(match.group(2))
      elif match.group(1) == SECTION_END_FIELD:
        if len(stack) == 0:
          # No previous match
          print("Error in " + file_name + "! There is no " + SECTION_BEGIN_FIELD + ' correspond to "' + SECTION_END_FIELD + '": ' + match.group(2))
          exit(1)
        pre_section = stack.pop()
        if pre_section != match.group(2):
          # Previous match is not the same as current section
          print("Error in " + file_name + '! The previous ' + SECTION_BEGIN_FIELD + ': "' + pre_section + '" is not the same as "' + SECTION_END_FIELD + '": "' + match.group(2) + '"')
          exit(1)

def main():

    if len(sys.argv) < 2:
        print "Usage: " + sys.argv[0] + " <schema_file>"
        exit(1)

    schema_file = os.path.join(SCHEMA_DIRECTORY, sys.argv[1])

    with open(schema_file, "r") as f:
        schema_contents = f.read().decode("utf-8")

    validate_sections(schema_contents, sys.argv[1])


if __name__ == '__main__':
    main()
