import sys
from os import listdir
from os.path import isfile, join, splitext
import yaml
import json


SCHEMAS_DIRECTORY = "schemas"


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


if __name__ == '__main__':
    main()
