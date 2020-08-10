import sys
from os import listdir
from os.path import isfile, join, splitext
import yaml
import json


SCHEMAS_DIRECTORY = "schemas"
TABLE_MARGIN_TOP = 1
TABLE_MARGIN_LEFT = 1


def usage():
    print "Converts a deployment configuration folder into a CSV file (spreadsheet)"
    print ""
    print "Usage:"
    print "    " + " ".join([sys.argv[0],
                             "<deployment_folder>",
                             "<csv_file>"])
    print ""


def getAllDeployments(deployment_folder):
    schemas = [splitext(f)[0] for f in listdir(deployment_folder)
               if isfile(join(deployment_folder, f))]
    print schemas
    return schemas


def getValuesFromDeployment(deployment_folder, deployment):
    print yaml.safe_load(open(join(deployment_folder, deployment +'.yml')))


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


def writeCsvFile(filename, content):
    f = open(filename, "w")
    f.write(content)


def escape_line(line):
    if '"' in line or ',' in line:
        return '"' + line.replace('"', '""') + '"'
    return line


def addContent(content):
    csvContent = ''
    for item in content:
        if type(item) == dict:
            csvContent += (write_table(item).encode("utf-8")) + '\n'
        else:
            csvContent += escape_line(item) + "," + '\n'
    return csvContent


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

    # write_fields(lines, schema, table)

    lines = [("," * TABLE_MARGIN_LEFT) + x for x in lines]

    return ",\n".join(lines)


def main():

    if len(sys.argv) != 3:
        usage()
        exit(1)

    deployment_folder = sys.argv[1]
    csv_file = sys.argv[2]
    deployments = getAllDeployments(deployment_folder)
    for deployment in deployments:
        getValuesFromDeployment(deployment_folder, deployment)
    print csv_file
    print read_schema('vsds')
    content = """

    - MetroAE deployment template CSV
    - ""
    - This spreadsheet can be converted to a set of MetroAE deployment files for
    - use in an install or upgrade.
    - ""
    - Fill out the fields of this spreadsheet, save as CSV and then issue "metroae
    - wizard" or "convert_csv_to_deployment.py <csv_file> <deployment_name>"

    - schema: common
      headers: [Common, Values, "", Descriptions]
      extra:
        - access_bridge
        - vsd_license_file
    """
    contentToWrite = addContent(yaml.safe_load(content))
    print contentToWrite
    writeCsvFile(csv_file, contentToWrite)


if __name__ == '__main__':
    main()
