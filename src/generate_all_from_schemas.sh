#!/bin/bash

BASE_DIRECTORY=..
SCHEMA_DIRECTORY=schemas
DEFAULT_DEPLOY_DIRECTORY=deployments/default
TEMPLATE_DIRECTORY=src/deployment_templates
SKIPPED_SCHEMA_IN_DEPLOY_NAME=deployment
EXAMPLE_DIR=examples
EXAMPLE_DATA_DIR=src/raw_example_data

if [[ -d schemas/  ]]; then
    BASE_DIRECTORY=.
fi

pushd $BASE_DIRECTORY

for fullpath in $SCHEMA_DIRECTORY/*.json; do
    filename=$(basename -- "$fullpath")
    filename="${filename%.*}"

    echo "Generating resources for schema $filename"

    # Generate template
    python generate_example_from_schema.py --schema $filename --as-template > $TEMPLATE_DIRECTORY/$filename.j2

    # Generate deployment file
    if [[ $filename != $SKIPPED_SCHEMA_IN_DEPLOY_NAME ]]; then
        python generate_example_from_schema.py --schema $filename > $DEFAULT_DEPLOY_DIRECTORY/$filename.yml
    fi
done

echo "Generating examples from example data"
for dir in $EXAMPLE_DATA_DIR/*/; do
    example_name=$(basename -- "$dir")
    echo "Generating example $example_name"
    for fullpath in $EXAMPLE_DATA_DIR/$example_name/*.yml; do
        filename=$(basename -- "$fullpath")
        filename="${filename%.*}"

        if [ ! -d "$EXAMPLE_DIR/$example_name" ]; then
            mkdir $EXAMPLE_DIR/$example_name
        fi

        python generate_example_from_schema.py --schema $filename --as-example --example_data_folder $EXAMPLE_DATA_DIR/$example_name > "$EXAMPLE_DIR/$example_name/$filename.yml"
    done
done
# Copy empty deployment as example
if [ ! -d "$EXAMPLE_DIR/blank_deployment" ]; then
    mkdir $EXAMPLE_DIR/blank_deployment
fi
mv $DEFAULT_DEPLOY_DIRECTORY/* $EXAMPLE_DIR/blank_deployment/.

# Add specific files to default deployment 
add_to_default_deployment="common credentials upgrade vscs vsds vstats"
for item in $add_to_default_deployment; do
    cp $EXAMPLE_DIR/blank_deployment/$item.yml $DEFAULT_DEPLOY_DIRECTORY/.
done

popd
