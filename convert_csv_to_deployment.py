#!/usr/bin/env python

from generate_example_from_schema import ExampleFileGenerator
import jinja2
import json
from jsonschema import validate, ValidationError
import os
import sys
from builtins import str


DEBUG = False
SCHEMAS_DIRECTORY = "schemas"
DEPLOYMENTS_DIRECTORY = "deployments"
CONTAINER_MOUNT_DIRECTORY = "/metroae_data/deployments"


def usage():
    print("Converts a CSV file (spreadsheet) into a deployment configuration")
    print("under the %s/ directory.  A template for the spreadsheet is " % (
          DEPLOYMENTS_DIRECTORY))
    print("provided as deployment_spreadsheet_template.csv")
    print("")
    print("Usage:")
    print("    " + " ".join([sys.argv[0],
                             "<csv_file>",
                             "<deployment_name>"]))
    print("")


class CsvDeploymentConverter(object):

    def __init__(self):
        self.data = dict()
        self.has_output = False
        self.has_debug = False

    def set_output(self, output=True):
        self.has_output = output

    def set_debug(self, debug=True):
        self.has_debug = debug

    def convert(self, csv_file, deployment_name):
        self._read_and_parse_csv(csv_file)
        self._read_and_parse_schemas()
        self._find_schema_tables()
        self._parse_tables()
        self._validate_data()
        self._generate_deployment_files(deployment_name)

    def get_data(self):
        return self.data

    def _read_and_parse_csv(self, csv_file):
        self.rows = list()

        with open(csv_file, 'r') as f:
            lines = f.read().encode("utf-8").decode("utf-8")

        for row in lines.split("\n"):
            self._parse_row(row)

    def _parse_row(self, row):
        cols = list()

        in_quote = False
        is_first_quote = False
        col = ""
        for char in row:
            if char == "\r":
                pass
            elif in_quote:
                if char == '"':
                    if is_first_quote:
                        col += char
                        is_first_quote = False
                    else:
                        in_quote = False
                        is_first_quote = True
                else:
                    col += char
                    is_first_quote = False
            else:
                if char == '"':
                    in_quote = True
                    if is_first_quote:
                        col += char
                        is_first_quote = False
                    else:
                        is_first_quote = True
                elif char == ",":
                    cols.append(col)
                    col = ""
                else:
                    col += char

        cols.append(col)
        self.rows.append(cols)

    def _read_and_parse_schemas(self):
        self.schemas = dict()

        for file_name in os.listdir(SCHEMAS_DIRECTORY):
            if (file_name.endswith(".json")):
                file_path = os.path.join(SCHEMAS_DIRECTORY, file_name)
                self._debug("Reading schema %s", file_path)
                with open(file_path, "r") as f:
                    schema_str = f.read().encode("utf-8").decode("utf-8")

                try:
                    self.schemas[file_name[0:-5]] = json.loads(schema_str)
                except Exception as e:
                    raise Exception("Could not parse schema: %s\n%s" % (
                        file_name, str(e)))

    def _find_schema_tables(self):

        self.tables = list()

        for r, row in enumerate(self.rows):
            for c, col in enumerate(row):
                schema_name = self._normalize_name(col)
                if schema_name in self.schemas:
                    self._debug("Found table %s at %s", schema_name,
                                self._get_cell_id(r, c))
                    self.tables.append({"schema": self._normalize_name(
                                        schema_name),
                                        "r": r,
                                        "c": c})

    def _normalize_name(self, table_name):
        return table_name.lower().replace(" ", "_")

    def _parse_tables(self):
        self.data = dict()
        self.validation_errors = list()

        for table in self.tables:
            self._output("Reading table %s at %s", table["schema"],
                         self._get_cell_id(table["r"], table["c"]))
            self._parse_table(table)

        if len(self.validation_errors) > 0:
            error_msg = self._collect_validation_errors()
            raise Exception("Validation Errors:\n" + error_msg)

    def _parse_table(self, table):

        is_transposed = self._check_for_transposed(table)
        self._debug("transposed: %s", str(is_transposed))
        self._read_table(table, is_transposed)

    def _check_for_transposed(self, table):
        r = table["r"]
        c = table["c"]
        schema_name = table["schema"]

        cell_value = self._get_cell_value(r + 1, c)
        row_name = None
        if cell_value is not None:
            row_name = self._lookup_schema_field(schema_name, cell_value)

        cell_value = self._get_cell_value(r, c + 1)
        col_name = None
        if cell_value is not None:
            col_name = self._lookup_schema_field(schema_name, cell_value)

        if row_name is None:
            if col_name is None:
                raise Exception("Table %s at %s has invalid fields" % (
                    schema_name, self._get_cell_id(r, c)))
            else:
                return True
        else:
            if col_name is None:
                return False
            else:
                raise Exception("Table %s at %s has fields on both axes" % (
                    schema_name, self._get_cell_id(r, c)))

    def _lookup_schema_field(self, schema_name, field_name):
        schema = self.schemas[schema_name]
        if self._is_schema_a_list(schema_name):
            fields = schema["items"]["properties"]
        else:
            fields = schema["properties"]

        normal_field_name = self._normalize_name(field_name)

        for field in fields:
            if self._normalize_name(field) == normal_field_name:
                return field
            elif (self._normalize_name(fields[field]["title"]) ==
                  normal_field_name):
                return field

        return None

    def _is_schema_a_list(self, schema_name):
        schema = self.schemas[schema_name]
        return schema["type"] == "array"

    def _get_field_datatype(self, schema_name, field_name):
        schema = self.schemas[schema_name]
        if self._is_schema_a_list(schema_name):
            fields = schema["items"]["properties"]
        else:
            fields = schema["properties"]

        if field_name in fields:
            if "type" in fields[field_name]:
                return fields[field_name]["type"]
            else:
                return "string"
        else:
            raise Exception("No field %s in schema %s" % (field_name,
                                                          schema_name))

    def _read_table(self, table, is_transposed=False):
        field_names = self._get_field_names(table, is_transposed)
        self._debug("Fields: %s", ", ".join(field_names))
        self._get_data(table, field_names, is_transposed)

    def _get_field_names(self, table, is_transposed=False):
        r = table["r"]
        c = table["c"]
        schema_name = table["schema"]

        field_names = list()

        r, c = self._next_field(r, c, is_transposed)
        cell_value = ""
        while cell_value is not None:
            cell_value = self._get_cell_value(r, c)
            field_name = None
            if cell_value is not None:
                field_name = self._lookup_schema_field(schema_name, cell_value)

                if field_name is not None:
                    field_names.append(field_name)
                else:
                    raise Exception("Invalid field %s in table %s at %s" % (
                        cell_value, schema_name, self._get_cell_id(r, c)))

                r, c = self._next_field(r, c, is_transposed)

        return field_names

    def _get_data(self, table, field_names, is_transposed=False):
        r = table["r"]
        c = table["c"]
        schema_name = table["schema"]

        data = list()

        r, c = self._next_item(r, c, is_transposed)
        item_values = list()
        while item_values is not None:
            item_values = self._get_item_values(field_names, schema_name, r, c,
                                                is_transposed)
            if item_values is not None:
                data.append(item_values)
                r, c = self._next_item(r, c, is_transposed)

        self._update_data(schema_name, data)

    def _update_data(self, schema_name, new_data):

        if len(new_data) > 0:
            is_list = self._is_schema_a_list(schema_name)
            if schema_name not in self.data:
                if is_list:
                    self.data[schema_name] = list()
                else:
                    self.data[schema_name] = dict()

            for item in new_data:
                self._debug("Data: %s", str(item))

                if is_list:
                    self.data[schema_name].append(item)
                else:
                    self.data[schema_name].update(item)

    def _get_item_values(self, field_names, schema_name, r, c,
                         is_transposed=False):
        values = dict()
        has_data = False

        r, c = self._next_field(r, c, is_transposed)
        for field_name in field_names:

            cell_value = self._get_cell_value(r, c)
            if cell_value is not None:
                values[field_name] = self._format_value(schema_name,
                                                        r, c,
                                                        field_name,
                                                        cell_value)
                has_data = True

            r, c = self._next_field(r, c, is_transposed)

        if has_data:
            return values
        else:
            return None

    def _get_cell_value(self, r, c):
        if r < len(self.rows):
            row = self.rows[r]
            if c < len(row):
                if row[c] == "":
                    return None
                else:
                    return row[c]
            else:
                return None
        else:
            return None

    def _format_value(self, schema_name, r, c, field_name, cell_value):
        datatype = self._get_field_datatype(schema_name, field_name)

        if datatype == "string":
            return str(cell_value)
        elif datatype == "integer":
            try:
                return int(cell_value)
            except ValueError:
                self.validation_errors.append({
                    "msg": "Invalid integer",
                    "r": r,
                    "c": c,
                    "field_name": field_name,
                    "schema_name": schema_name,
                    "value": cell_value})
        elif datatype == "boolean":
            if cell_value.lower() in ['true', 'yes']:
                return True
            elif cell_value.lower() in ['false', 'no']:
                return False
            else:
                self.validation_errors.append({
                    "msg": "Invalid Boolean",
                    "r": r,
                    "c": c,
                    "field_name": field_name,
                    "schema_name": schema_name,
                    "value": cell_value})
        elif datatype == "array":
            return [x.strip() for x in cell_value.split(",")]
        else:
            self.validation_errors.append({
                "msg": "Unsupported datatype",
                "r": r,
                "c": c,
                "field_name": field_name,
                "schema_name": schema_name,
                "value": cell_value})

        return None

    def _collect_validation_errors(self):
        errors = list()

        for error in self.validation_errors:
            errors.append("At %s: Table %s field %s value %s: %s" % (
                self._get_cell_id(error["r"], error["c"]),
                error["schema_name"],
                error["field_name"],
                error["value"],
                error["msg"]))

        return "\n".join(errors)

    def _validate_data(self):
        for schema_name in self.data:
            self._validate_against_schema(schema_name, self.data[schema_name])

    def _validate_against_schema(self, schema_name, data):
        self._debug("Schema validating: %s" % schema_name)
        try:
            validate(data, self.schemas[schema_name])
        except ValidationError as e:

            field = ""
            if "title" in e.schema:
                field = " for " + e.schema["title"]
            msg = "Invalid data in %s%s: %s" % (schema_name, field, e.message)
            raise Exception(msg)

    def _generate_deployment_files(self, deployment_name):
        if "/" in deployment_name:
            dir_name = os.path.dirname(deployment_name)
            if not os.path.isdir(dir_name):
                raise Exception("Parent directory %s does not exist" %
                                (dir_name))
            deployment_dir = deployment_name
        else:
            if os.path.isdir(CONTAINER_MOUNT_DIRECTORY):
                deployment_dir = os.path.join(CONTAINER_MOUNT_DIRECTORY,
                                              deployment_name)
            else:
                deployment_dir = os.path.join(DEPLOYMENTS_DIRECTORY,
                                              deployment_name)

        if not os.path.isdir(deployment_dir):
            self._output("Creating deployment directory: %s", deployment_dir)
            os.mkdir(deployment_dir)

        for schema_name in self.data:
            file_name = os.path.join(deployment_dir, schema_name + ".yml")
            self._generate_deployment_file(schema_name, file_name,
                                           self.data[schema_name])

    def _generate_deployment_file(self, schema_name, file_name, data):
        self._output("Writing %s", file_name)

        if type(data) == list:
            data = {schema_name: data}
        data["generator_script"] = "CSV spreadsheet"
        gen_example = ExampleFileGenerator(False, True)
        example_lines = gen_example.generate_example_from_schema(
            os.path.join("schemas", schema_name + ".json"))
        template = jinja2.Template(example_lines)
        rendered = template.render(**data)
        with open(file_name, 'w') as file:
            file.write(rendered.encode("utf-8"))

    def _next_field(self, r, c, is_transposed=False):
        if is_transposed:
            return r, c + 1
        else:
            return r + 1, c

    def _next_item(self, r, c, is_transposed=False):
        if is_transposed:
            return r + 1, c
        else:
            return r, c + 1

    def _get_cell_id(self, r, c):
        return chr(ord('A') + c) + str(r + 1)

    def _output(self, msg, *args):
        if self.has_output:
            print(msg % args)

    def _debug(self, msg, *args):
        if self.has_debug:
            print(msg % args)


def main():

    if len(sys.argv) != 3:
        usage()
        exit(1)

    csv_file = sys.argv[1]
    deployment_name = sys.argv[2]

    converter = CsvDeploymentConverter()
    converter.set_output()
    if DEBUG:
        converter.set_debug()
        converter.convert(csv_file, deployment_name)
    else:
        try:
            converter.convert(csv_file, deployment_name)
        except Exception as e:
            print(str(e))
            exit(2)


if __name__ == '__main__':
    main()
