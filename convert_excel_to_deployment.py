#!/usr/bin/env python

import json
from jsonschema import validate, ValidationError
from openpyxl import load_workbook
import os
import sys

DEPLOYMENTS_DIRECTORY = "deployments"
SCHEMAS_DIRECTORY = "schemas"
COLUMN_OFFSET = 1
ROW_OFFSET = 4

schemas = dict()
errors = list()


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
    properties = schema["items"]["properties"]
    title_field_map = generate_title_field_map(properties)

    labels = read_labels(worksheet, title_field_map, fields_by_col=True)

    data = list()
    entry_offset = 0
    while True:
        entry = read_data_entry(worksheet, labels, entry_offset,
                                fields_by_col=True)

        if entry != dict():
            validate_against_schema(worksheet.title, [entry])
            data.append(entry)
            entry_offset += 1
        else:
            break

    return data


def read_worksheet_object(schema, worksheet):
    properties = schema["properties"]
    title_field_map = generate_title_field_map(properties)

    labels = read_labels(worksheet, title_field_map, fields_by_col=False)
    data = read_data_entry(worksheet, labels, 0, fields_by_col=False)
    validate_against_schema(worksheet.title, data)

    return data


def read_labels(worksheet, title_field_map, fields_by_col=False):
    labels = list()

    col = COLUMN_OFFSET
    row = ROW_OFFSET

    while True:
        cell = worksheet.cell(row=row, column=col)
        value = cell.value
        if fields_by_col:
            col += 1
        else:
            row += 1

        if value is not None:
            if value in title_field_map:
                labels.append(title_field_map[value])
            else:
                labels.append(None)
        else:
            break

    return labels


def read_data_entry(worksheet, labels, entry_offset, fields_by_col=False):
    entry = dict()

    col = COLUMN_OFFSET
    row = ROW_OFFSET

    if fields_by_col:
        row += entry_offset + 1
    else:
        col += entry_offset + 1

    for label in labels:
        cell = worksheet.cell(row=row, column=col)
        value = cell.value
        if value is not None:
            if label is not None:
                if label.startswith("list:"):
                    list_name = label[5:]
                    entry[list_name] = [x.strip() for x in value.split(",")]
                else:
                    entry[label] = value
            else:
                record_error(worksheet.title, cell.coordinate,
                             "Data entry for unknown label")
        if fields_by_col:
            col += 1
        else:
            row += 1

    return entry


def validate_against_schema(schema_title, data):
    schema_name = get_schema_name(schema_title)
    schema = schemas[schema_name]

    try:
        validate(data, schema)
    except ValidationError as e:

        field = ""
        if "title" in e.schema:
            field = " for " + e.schema["title"]
        msg = "Invalid data in %s%s: %s" % (schema_title, field, e.message)
        raise Exception(msg)


def get_schema_name(title):
    return title.replace(" ", "_").lower()


def generate_title_field_map(properties):
    title_field_map = dict()
    for name, field in properties.iteritems():
        if field["type"] == "array":
            title_field_map[field["title"]] = "list:" + name
        else:
            title_field_map[field["title"]] = name

    return title_field_map


def get_list_name(schema):
    if "listName" in schema:
        list_name = schema["listName"]
    else:
        if "items" in schema and "title" in schema["items"]:
            list_name = schema["items"]["title"].lower() + "s"
        else:
            list_name = schema["title"].lower()

    return list_name


def record_error(schema_title, position, message):
    errors.append({"schema_title": schema_title,
                   "position": position,
                   "message": message})


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
