import sys
from os import listdir
from os.path import isfile, join, splitext
import yaml


def usage():
    print "Converts a deployment configuration folder into a CSV file (spreadsheet)"
    print ""
    print "Usage:"
    print "    " + " ".join([sys.argv[0],
                             "<deployment_folder>",
                             "<csv_file>"])
    print ""


def getAllSchemas(deployment_folder):
    schemas = [splitext(f)[0] for f in listdir(deployment_folder)
               if isfile(join(deployment_folder, f))]
    print schemas
    return schemas


def getValuesFromDeployment(deployment_folder, deployment_name):
    print yaml.safe_load(open(join(deployment_folder, deployment_name +'.yml')))


def main():

    if len(sys.argv) != 3:
        usage()
        exit(1)

    deployment_folder = sys.argv[1]
    csv_file = sys.argv[2]
    schemas = getAllSchemas(deployment_folder)
    for schema in schemas:
        getValuesFromDeployment(deployment_folder, schema)
    print csv_file


if __name__ == '__main__':
    main()
