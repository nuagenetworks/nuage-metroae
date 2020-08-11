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
    return yaml.safe_load(open(join(deployment_folder, deployment +'.yml')))


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


def write_fields(lines, schema, table):
    width = len(table["headers"])
    data = table['data']

    if schema["type"] == "array":
        schema_props = schema["items"]["properties"]
        required = schema["items"].get("required")
    else:
        schema_props = schema["properties"]
        required = schema.get("required")

    dataDict = {}
    dataDictList = []
    if type(data) == list:
        dataDictList = data
    else:
        dataDict = data
    fields = required
    for k in dataDict.keys():
        if k not in fields:
            fields.append(k)

    for field_name in fields:
        fieldValList = []
        if dataDictList:
            for item in dataDictList:
                fieldVal = item[field_name]
                if type(fieldVal) == list:
                    fieldVal = ','.join(fieldVal)
                fieldValList.append(fieldVal)
        else:
            fieldVal = dataDict[field_name]
            if type(fieldVal) == list:
                fieldVal = ','.join(fieldVal)
            fieldValList.append(fieldVal)
        fieldValuesString = ''
        for val in fieldValList:
            fieldValuesString += "," + "\"" + str(val) + "\""
        field = schema_props[field_name]
        description = field.get("description", "")
        lines.append(field["title"] + fieldValuesString +
                     ("," * 2) +
                     escape_line(description))


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


def main():

    if len(sys.argv) != 3:
        usage()
        exit(1)

    deployment_folder = sys.argv[1]
    csv_file = sys.argv[2]
    content = []
    content.append('MetroAE deployment template CSV')
    content.append('This Spreadsheet can be used for KVM SDWan install')
    deployments = getAllDeployments(deployment_folder)
    for deployment in deployments:
        deploymentData = getValuesFromDeployment(deployment_folder, deployment)
        headerList = [deployment]
        if type(deploymentData) == list:
            for i in range(len(deploymentData)):
                headerList.append(deployment + str(i + 1))
        else:
            headerList.append('Values')
        headerList.append('')
        headerList.append('Descriptions')
        schemaDict = {
            'schema': deployment,
            'headers': headerList,
            'data': deploymentData
        }
        content.append('')
        content.append(schemaDict)
    contentToWrite = addContent(content)
    writeCsvFile(csv_file, contentToWrite)


if __name__ == '__main__':
    main()
