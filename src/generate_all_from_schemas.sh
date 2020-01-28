#!/bin/bash

BASE_DIRECTORY=..
SCHEMA_DIRECTORY=schemas
DEFAULT_DEPLOY_DIRECTORY=deployments/default
TEMPLATE_DIRECTORY=src/deployment_templates
EXAMPLE_DIR=examples
EXAMPLE_DATA_DIR=src/raw_example_data
BLANK_DEPLOYMENT_DIR=$EXAMPLE_DIR/blank_deployment
MIN_BLANK_DEPLOYMENT_DIR=$EXAMPLE_DIR/minimum_required_blank_deployment

if [[ -d schemas/  ]]; then
    BASE_DIRECTORY=.
fi

pushd $BASE_DIRECTORY

directories_to_clean="$TEMPLATE_DIRECTORY $DEFAULT_DEPLOY_DIRECTORY $EXAMPLE_DIR $BLANK_DEPLOYMENT_DIR $MIN_BLANK_DEPLOYMENT_DIR"
for item in $directories_to_clean; do
    if [ -d "$item" ]; then
        rm -rf $item
    fi
    mkdir $item
done

for fullpath in $SCHEMA_DIRECTORY/*.json; do
    filename=$(basename -- "$fullpath")
    filename="${filename%.*}"

    echo "Generating resources for schema $filename"

    # Generate template
    python generate_example_from_schema.py --schema $filename --as-template > $TEMPLATE_DIRECTORY/$filename.j2

    # Generate blank deployment file
    python generate_example_from_schema.py --schema $filename > $BLANK_DEPLOYMENT_DIR/$filename.yml

    if [[ $filename != "upgrade" ]]; then
        # Generate deployment file
        python generate_example_from_schema.py --schema $filename --no-comments > $EXAMPLE_DIR/minimum_required_blank_deployment/$filename.yml
    fi

done

echo "Generating examples from example data"
for dir in $EXAMPLE_DATA_DIR/*/; do
    example_name=$(basename -- "$dir")
    echo "Generating example $example_name"
    if [ -d "$EXAMPLE_DIR/$example_name" ]; then
        rm -rf $EXAMPLE_DIR/$example_name
    fi

    mkdir $EXAMPLE_DIR/$example_name
    for fullpath in $EXAMPLE_DATA_DIR/$example_name/*.yml; do
        filename=$(basename -- "$fullpath")
        filename="${filename%.*}"

        python generate_example_from_schema.py --schema $filename --as-example --example_data_folder $EXAMPLE_DATA_DIR/$example_name > "$EXAMPLE_DIR/$example_name/$filename.yml"
    done
done

echo "Generate deployment spreadsheet template CSV"
python src/generate_deployment_spreadsheet_template.py > deployment_spreadsheet_template.csv

# Add specific files to default deployment
add_to_default_deployment="common credentials upgrade vscs vsds vstats"
for item in $add_to_default_deployment; do
    cp $BLANK_DEPLOYMENT_DIR/$item.yml $DEFAULT_DEPLOY_DIRECTORY/.
done

popd
