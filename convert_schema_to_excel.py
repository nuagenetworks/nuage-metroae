#!/usr/bin/env python

import json
from openpyxl import Workbook
from openpyxl.comments import Comment
from openpyxl.styles import Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation
import os
import sys
import yaml


WORKBOOK_FILE = "sample_deployment.xlsx"
SCHEMAS_DIRECTORY = "schemas"
SCHEMAS = ["common", "vsds", "vscs", "vstats", "credentials"]
COLUMN_OFFSET = 1
ROW_OFFSET = 4
OBJECT_WIDTH = 70
COLUMN_WIDTH = 25
COMMENT_WIDTH = 300
COMMENT_HEIGHT = 100
REQUIRED_COLOR = "FFFFDD"
NORMAL_COLOR = "FFFFFF"
ADVANCED_COLOR = "EEEEEE"
ADVANCED_TEXT_COLOR = "888888"
BORDER_COLOR = "AAAAAA"
NUM_LIST_ENTRIES = 6


def write_workbook(schemas, output_file, example_dir=None):
    workbook = Workbook()

    workbook.remove_sheet(workbook.active)

    for schema_name in schemas:
        generate_worksheet(workbook, schema_name, example_dir)

    # workbook.template = True
    workbook.save(output_file)


def generate_worksheet(workbook, schema_name, example_dir=None):
    schema = read_schema(schema_name)
    example = None
    if example_dir is not None:
        example = read_example(example_dir, schema_name)

    worksheet = workbook.create_sheet(capitalize(schema_name))

    generate_title(worksheet, schema)

    if schema["type"] == "array":
        generate_schema_list(worksheet, schema, example)
    else:
        generate_schema_object(worksheet, schema, example)

    return worksheet


def generate_title(worksheet, schema):
    worksheet["A1"] = schema["title"]
    worksheet["A1"].style = "Title"
    worksheet["A2"] = schema["description"]
    worksheet["A2"].style = "Headline 3"


def generate_schema_object(worksheet, schema, example=None):
    i = 0
    for name, field in sorted(schema["properties"].iteritems(),
                              key=lambda (k, v): (v["propertyOrder"], k)):
        field["name"] = name
        field["required"] = "required" in schema and name in schema["required"]

        value = None
        if example is not None and name in example:
            value = example[name]

        write_label_cell(worksheet, field, i + ROW_OFFSET,
                         COLUMN_OFFSET)
        write_field_cell(worksheet, field, i + ROW_OFFSET,
                         COLUMN_OFFSET + 1, value)
        add_data_validation(worksheet, field, i + ROW_OFFSET,
                            COLUMN_OFFSET + 1)
        i += 1

    col = worksheet.column_dimensions['A']
    col.width = OBJECT_WIDTH
    col = worksheet.column_dimensions['B']
    col.width = OBJECT_WIDTH


def generate_schema_list(worksheet, schema, example=None):
    i = 0
    for name, field in sorted(schema["items"]["properties"].iteritems(),
                              key=lambda (k, v): (v["propertyOrder"], k)):
        field["name"] = name
        field["required"] = ("required" in schema["items"] and
                             name in schema["items"]["required"])

        write_label_cell(worksheet, field, ROW_OFFSET,
                         i + COLUMN_OFFSET)
        cell = worksheet.cell(row=ROW_OFFSET, column=i + COLUMN_OFFSET)
        col = worksheet.column_dimensions[cell.column_letter]
        col.width = COLUMN_WIDTH

        num_rows = NUM_LIST_ENTRIES
        list_name = get_list_name(schema)
        value = None
        if example is not None and list_name in example:
            num_rows = len(example[list_name])

        for j in range(num_rows):
            if example is not None and list_name in example:
                example_row = example[list_name][j]
                if name in example_row:
                    value = example_row[name]
            write_field_cell(worksheet, field, ROW_OFFSET + j + 1,
                             i + COLUMN_OFFSET, value)
            add_data_validation(worksheet, field, ROW_OFFSET + j + 1,
                                i + COLUMN_OFFSET)
        i += 1


def write_label_cell(worksheet, field, row, col):
    cell = worksheet.cell(row=row, column=col)
    cell.value = field["title"]
    default = ""
    if "default" in field:
        default = " [default: %s]" % field["default"]

    cell.comment = Comment(field["description"] + default, field["name"])
    cell.comment.width = COMMENT_WIDTH
    cell.comment.height = COMMENT_HEIGHT
    # thin = Side(border_style="thin", color="000000")
    # cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
    if "required" in field and field["required"]:
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=REQUIRED_COLOR)
    elif "advanced" in field and field["advanced"]:
        cell.font = Font(color=ADVANCED_TEXT_COLOR)
        cell.fill = PatternFill("solid", fgColor=ADVANCED_COLOR)
    else:
        cell.fill = PatternFill("solid", fgColor=NORMAL_COLOR)


def write_field_cell(worksheet, field, row, col, value=None):
    cell = worksheet.cell(row=row, column=col)
    if value is not None:
        if type(value) == list:
            cell.value = ", ".join(value)
        else:
            cell.value = value
    # if "default" in field:
    #     cell.comment = Comment("%s, default: %s" % (field["name"],
    #                                                 field["default"]),
    #                            field["name"])
    # else:
    #     cell.comment = Comment(field["name"], field["name"])
    # cell.comment.width = COMMENT_WIDTH
    # cell.comment.height = COMMENT_HEIGHT
    thin = Side(border_style="thin", color=BORDER_COLOR)
    cell.border = Border(top=thin, left=thin, right=thin, bottom=thin)
    if "required" in field and field["required"]:
        cell.fill = PatternFill("solid", fgColor=REQUIRED_COLOR)
    elif "advanced" in field and field["advanced"]:
        cell.fill = PatternFill("solid", fgColor=ADVANCED_COLOR)
    else:
        cell.fill = PatternFill("solid", fgColor=NORMAL_COLOR)


def add_data_validation(worksheet, field, row, col):
    if "enum" in field:
        dv = DataValidation(type="list",
                            formula1='"%s"' % ",".join(field["enum"]),
                            allow_blank=True, errorStyle='warning')
        dv.error = "Your entry is not in the list, Change anyway?"
        dv.errorTitle = "Invalid Entry"
        dv.prompt = "Please select from the list"
        dv.promptTitle = "List Selection"
    elif field["type"] == "boolean":
        dv = DataValidation(type="list",
                            formula1='"true,false"',
                            allow_blank=True, errorStyle='warning')
        dv.error = "Your entry is not true or false, change anyway?"
        dv.errorTitle = "Invalid Entry"
        dv.prompt = "Please select true or false"
        dv.promptTitle = "True or False Selection"
    elif field["type"] == "integer":
        dv = DataValidation(type="whole",
                            allow_blank=True, errorStyle="warning")
        dv.error = "Your entry is not an integer, change anyway?"
        dv.errorTitle = "Invalid Entry"
        dv.prompt = "Please provide integer"
        dv.promptTitle = "Integer Selection"
    else:
        return

    worksheet.add_data_validation(dv)
    c = worksheet.cell(row=row, column=col)
    dv.add(c)


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


def capitalize(name):
    return name[0].upper() + name[1:]


def read_example(example_dir, schema_name):
    file_name = os.path.join(example_dir, schema_name + ".yml")
    try:
        with open(file_name, "r") as f:
            return yaml.safe_load(f.read().decode("utf-8"))
    except Exception as e:
        raise Exception("Could not parse example: %s\n%s" % (
            file_name, str(e)))


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
    if len(sys.argv) > 1:
        write_workbook(SCHEMAS, WORKBOOK_FILE, sys.argv[1])
    else:
        write_workbook(SCHEMAS, WORKBOOK_FILE)


if __name__ == '__main__':
    main()
