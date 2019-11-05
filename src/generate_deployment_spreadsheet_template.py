#!/usr/bin/env python

import json
import os
import sys
import yaml


SCHEMAS_DIRECTORY = "schemas"
TABLE_MARGIN_LEFT = 1
TABLE_MARGIN_TOP = 1

FORMAT = """

- MetroAE deployment template CSV
- ""
- This spreadsheet can be converted to a set of MetroAE deployment files for
- use in an install or upgrade.
- ""
- Fill out the fields of this spreadsheet, save as CSV and then issue "metroae
- wizard" or "convert_csv_to_deployment.py <csv_file> <deployment_name>"
- schema: common
  headers: [Common, Values, "", Descriptions]
- ""
- For vCenter deployments only
- schema: common
  fields:
    - vcenter_datacenter
    - vcenter_cluster
    - vcenter_datastore
  headers: [Common, Values, "", Descriptions]
- ""
- For upgrade only
- schema: upgrade
  fields:
    - upgrade_from_version
    - upgrade_to_version
  headers: [Common, Values, "", Descriptions]
- schema: vsds
  headers: [VSDs, VSD 1 (SA), VSD 2 (HA), VSD 3 (HA),
            VSD 4 (Geo-Red), VSD 5 (Geo-Red), VSD 6 (Geo-Red),
            "", Descriptions]
- schema: vscs
  headers: [VSCs, VSD 1 (SA), VSD 2 (HA), "", Descriptions]


- ""
- Advanced instructions
- This spreadsheet can be used to populate deployment files for any of the
- schemas in the schemas directory.  The case-insenstive name of the schema
- must be specified in the upper left corner of the table.  The table can then
- be positioned anywhere in the spreadsheet provided there is at least one row
- and column of empty space around the table.  The case-insenstive names or
- titles of the properties can be either along rows or columns (either position
- is valid).

"""


def read_format(format):
    return yaml.safe_load(format)


def escape_line(line):
    if '"' in line or ',' in line:
        return '"' + line.replace('"', '""') + '"'
    return line


def read_schema(schema_name):
    file_name = schema_name + ".json"
    file_path = os.path.join(SCHEMAS_DIRECTORY, file_name)
    with open(file_path, "r") as f:
        schema_str = f.read().decode("utf-8")

    try:
        return json.loads(schema_str)
    except Exception as e:
        raise Exception("Could not parse schema: %s\n%s" % (
            file_name, str(e)))


def write_fields():
    pass


def write_table(table):
    schema_name = table["schema"]
    schema = read_schema(schema_name)

    lines = list()

    for i in range(TABLE_MARGIN_TOP):
        lines.append("")

    lines.append(escape_line(schema["title"]))
    lines.append(escape_line(schema["description"]))

    lines.append(",".join(table["headers"]))

    lines = [("," * TABLE_MARGIN_LEFT) + x for x in lines]

    return ",\n".join(lines)


def main():
    format = read_format(FORMAT)

    for item in format:
        if type(item) == dict:
            print write_table(item)
        else:
            print escape_line(item) + ","


if __name__ == '__main__':
    main()
