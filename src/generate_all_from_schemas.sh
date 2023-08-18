#!/bin/bash

BASE_DIRECTORY=..
SCHEMA_DIRECTORY=schemas
DEFAULT_DEPLOY_DIRECTORY=deployments/default
TEMPLATE_DIRECTORY=src/deployment_templates
EXAMPLE_DIR=examples
EXAMPLE_DATA_DIR=src/raw_example_data
BLANK_DEPLOYMENT_DIR=$EXAMPLE_DIR/blank_deployment
CSV_DEPLOYMENT_DIR=$EXAMPLE_DIR/csv_deployment
MIN_BLANK_DEPLOYMENT_DIR=$EXAMPLE_DIR/minimum_required_blank_deployment

if [[ -d schemas/  ]]; then
    BASE_DIRECTORY=.
fi

pushd $BASE_DIRECTORY

for fullpath in $EXAMPLE_DIR/*; do
    dir_name=$(basename -- "$fullpath")
    dir_name="${dir_name%.*}"
    if [[ -d $fullpath && $dir_name != "plugins" ]]; then
        rm -rf $fullpath
    fi
done

directories_to_clean="$TEMPLATE_DIRECTORY $DEFAULT_DEPLOY_DIRECTORY $BLANK_DEPLOYMENT_DIR $MIN_BLANK_DEPLOYMENT_DIR"
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

    # Run the schema property ordering script
    python src/renumber_schema_ordering.py ${filename}.json

    # Checking the schema sections
    python src/validate_schema_section.py ${filename}.json

    if [ $? -ne 0 ]; then
        exit 1
    fi

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

    mkdir -p $EXAMPLE_DIR/excel
    python3 src/convert_schemas_to_excel.py $EXAMPLE_DIR/excel/${example_name}.xlsx $dir
done

echo "Generate deployment spreadsheet template CSV"
python src/generate_deployment_spreadsheet_template.py > deployment_spreadsheet_template.csv


echo "Generate deployment excel spreadsheet template"
python3 src/convert_schemas_to_excel.py sample_deployment.xlsx
python3 src/convert_schemas_to_excel.py $EXAMPLE_DIR/excel/blank_deployment.xlsx

echo "Generate deployment spreadsheet example"
mkdir $CSV_DEPLOYMENT_DIR
python convert_deployment_to_csv.py examples/kvm_sdwan_install/ $CSV_DEPLOYMENT_DIR/sample_deployment.csv

# Add specific files to default deployment
add_to_default_deployment="common credentials upgrade vscs vsds vstats"
for item in $add_to_default_deployment; do
    cp $BLANK_DEPLOYMENT_DIR/$item.yml $DEFAULT_DEPLOY_DIRECTORY/.
done

popd
