#!/usr/bin/env python

import json
from openpyxl import load_workbook
import os
import sys

DEPLOYMENTS_DIRECTORY = "deployments"
SCHEMAS_DIRECTORY = "schemas"

schemas = dict()


def usage():
    print "Converts a XLSX file (Excel spreadsheet) into a deployment "
    print "configuration under the %s/ directory.  A template for the " % (
        DEPLOYMENTS_DIRECTORY)
    print "spreadsheet is provided as sample_deployment.xlsx"
    print ""
    print "Usage:"
    print "    " + " ".join([sys.argv[0],
                             "<xlsx_file>",
                             "<deployment_name>"])
    print ""


def read_and_parse_schemas():
    for file_name in os.listdir(SCHEMAS_DIRECTORY):
        if (file_name.endswith(".json")):
            file_path = os.path.join(SCHEMAS_DIRECTORY, file_name)
            with open(file_path, "r") as f:
                schema_str = f.read().decode("utf-8")

            try:
                schemas[file_name[0:-5]] = json.loads(schema_str)
            except Exception as e:
                raise Exception("Could not parse schema: %s\n%s" % (
                    file_name, str(e)))


def read_xlsx(xlsx_file):
    data = dict()
    workbook = load_workbook(xlsx_file)
    for worksheet in workbook:
        schema_name = get_schema_name(worksheet.title)
        schema = schemas[schema_name]
        data[schema_name] = read_worksheet(schema, worksheet)

    return data


def read_worksheet(schema, worksheet):
    if schema["type"] == "array":
        data = read_worksheet_list(schema, worksheet)
    else:
        data = read_worksheet_object(schema, worksheet)

    return data


def read_worksheet_list(schema, worksheet):
    pass


def read_worksheet_object(schema, worksheet):
    pass


def get_schema_name(title):
    return title.replace(" ", "_").lower()


def get_list_name(schema):
    if "listName" in schema:
        list_name = schema["listName"]
    else:
        if "items" in schema and "title" in schema["items"]:
            list_name = schema["items"]["title"].lower() + "s"
        else:
            list_name = schema["title"].lower()

    return list_name


def main():
    if len(sys.argv) != 3:
        usage()
        exit(1)

    xlsx_file = sys.argv[1]
    deployment_name = sys.argv[2]

    read_and_parse_schemas()
    data = read_xlsx(xlsx_file)

    print json.dumps(data)


if __name__ == '__main__':
    main()
