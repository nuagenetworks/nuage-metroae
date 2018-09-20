#!/bin/bash

BASE_DIRECTORY=..
SCHEMA_DIRECTORY=schemas
DEFAULT_DEPLOY_DIRECTORY=deployments/default
TEMPLATE_DIRECTORY=src/deployment_templates
SKIPPED_SCHEMA_IN_DEPLOY_NAME=deployment

if [[ -d schemas/  ]]; then
    BASE_DIRECTORY=.
fi

pushd $BASE_DIRECTORY

for fullpath in $SCHEMA_DIRECTORY/*.json; do
    filename=$(basename -- "$fullpath")
    filename="${filename%.*}"

    echo "Generating resources for schema $filename"

    # Generate template
    python generate_example_from_schema.py $filename --as-template > $TEMPLATE_DIRECTORY/$filename.j2

    # Generate deployment file
    if [[ $filename != $SKIPPED_SCHEMA_IN_DEPLOY_NAME ]]; then
        python generate_example_from_schema.py $filename > $DEFAULT_DEPLOY_DIRECTORY/$filename.yml
    fi
done

popd
