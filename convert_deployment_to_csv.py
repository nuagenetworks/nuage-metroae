import sys
from os import listdir
from os.path import isfile, join, splitext
import yaml
import json


SCHEMAS_DIRECTORY = "schemas"
TABLE_MARGIN_TOP = 1
TABLE_MARGIN_LEFT = 1


def usage():
    print("Converts a deployment configuration folder into a CSV file (spreadsheet)")
    print("")
    print("Usage:")
    print("    " + " ".join([sys.argv[0],
                             "<deployment_folder>",
                             "<csv_file>"]))
    print("")


def get_all_schemas(deployment_folder):
    schemas = [splitext(f)[0] for f in listdir(deployment_folder)
               if isfile(join(deployment_folder, f))]
    return schemas


def get_values_from_deployment(deployment_folder, deployment):
    return yaml.safe_load(open(join(deployment_folder, deployment + '.yml')))


def read_schema(schema_name):
    file_name = schema_name + ".json"
    file_path = join(SCHEMAS_DIRECTORY, file_name)
    with open(file_path, "r") as f:
        schema_str = f.read().decode("utf-8")
    try:
        return json.loads(schema_str)
    except Exception as e:
        raise Exception("Could not parse schema: %s\n%s" % (
            file_name, str(e)))


def write_csv_file(filename, content):
    f = open(filename, "w")
    f.write(content)


def escape_line(line):
    if '"' in line or ',' in line:
        return '"' + line.replace('"', '""') + '"'
    return line


def add_content(content):
    csv_content = ''
    for item in content:
        if type(item) == dict:
            csv_content += (write_table(item).encode("utf-8")) + '\n'
        else:
            csv_content += escape_line(item) + "," + '\n'
    return csv_content


def add_field_to_list(field_val, field_val_list):
    if type(field_val) == list:
        field_val = ','.join(field_val)
    field_val_list.append(field_val)


def write_fields(lines, schema, table):
    data = table['data']

    if schema["type"] == "array":
        schema_props = schema["items"]["properties"]
        required = schema["items"].get("required")
    else:
        schema_props = schema["properties"]
        required = schema.get("required")

    data_dict = {}
    data_dict_list = []
    if type(data) == list:
        data_dict_list = data
    else:
        data_dict = data
    fields = required

    for name, field in sorted(iter(schema_props.items()), key=lambda v: v[1]["propertyOrder"]):
        if name not in required and name in list(data_dict.keys()):
            fields.append(str(name))

    for field_name in fields:
        field_val_list = []
        if data_dict_list:
            for item in data_dict_list:
                add_field_to_list(item[field_name], field_val_list)
        else:
            add_field_to_list(data_dict[field_name], field_val_list)
        field_values_string = ''
        for val in field_val_list:
            if type(val) == int or val.find(',') == -1:
                field_values_string += "," + str(val)
            else:
                field_values_string += "," + "\"" + str(val) + "\""
        field = schema_props[field_name]
        description = field.get("description", "")
        full_line = field["title"] + field_values_string + ("," * 2) + escape_line(description)
        lines.append(full_line)


def write_table(table):
    schema_name = table["schema"]
    schema = read_schema(schema_name)

    lines = []

    for i in range(TABLE_MARGIN_TOP):
        lines.append("")

    if "no_title" not in table:
        lines.append(escape_line(schema["title"]))
        lines.append(escape_line(schema["description"]))
        lines.append("")

    lines.append(",".join(table["headers"]))
    write_fields(lines, schema, table)
    lines = [("," * TABLE_MARGIN_LEFT) + x for x in lines]

    return ",\n".join(lines)


def create_csv_from_deployment(csv_file, deployment_folder):
    content = []
    content.append('MetroAE deployment template CSV')
    content.append('This Spreadsheet can be used as an Input to MetroAE')
    deployments = get_all_schemas(deployment_folder)
    for deployment in deployments:
        deployment_data = get_values_from_deployment(deployment_folder, deployment)
        header_list = [deployment]
        if type(deployment_data) == list:
            for i in range(len(deployment_data)):
                header_list.append(deployment + str(i + 1))
        else:
            header_list.append('Values')
        header_list.append('')
        header_list.append('Descriptions')
        schemaDict = {
            'schema': deployment,
            'headers': header_list,
            'data': deployment_data
        }
        content.append('')
        content.append(schemaDict)
    content_to_write = add_content(content)
    write_csv_file(csv_file, content_to_write)


def main():

    if len(sys.argv) != 3:
        usage()
        exit(1)

    deployment_folder = sys.argv[1]
    csv_file = sys.argv[2]
    create_csv_from_deployment(csv_file, deployment_folder)


if __name__ == '__main__':
    main()
    pass
