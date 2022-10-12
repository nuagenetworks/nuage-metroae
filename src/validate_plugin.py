#!/usr/bin/env python

import os
from jsonschema import validate, ValidationError
import sys
import yaml

PLUGIN_CONFIG_NAME = "plugin-cfg.yml"
PLUGIN_CONFIG_SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "urn:nuage-metroae:plugin",
    "title": "Plugin",
    "description": "Plugin configuration schema",
    "type": "object",
    "additionalProperties": False,
    "properties": {
        "plugin_name": {
            "type": "string",
            "title": "Name",
            "description": ("The name of the plugin.  This will be used as the"
                            " the plugin directory name.  No special "
                            "characters allowed."),
            "pattern": "[0-9a-zA-Z_-]+"
        },
        "description": {
            "type": "string",
            "title": "Description",
            "description": "A suitable description of the plugin"
        },
        "version": {
            "type": "string",
            "title": "Version",
            "description": "Version of the plugin itself",
            "pattern": "[0-9]+[.][0-9]+[.][0-9]+"
        },
        "required_metro_version": {
            "type": "string",
            "title": "Required Metro Version",
            "description": ("Minimum required version of MetroAE to support "
                            "the plugin"),
            "pattern": "[0-9]+[.][0-9]+[.][0-9]+"
        },
        "schemas": {
            "type": "array",
            "title": "Schemas",
            "description": ("Set of schemas provided by plugin for "
                            "configuration"),
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "name": {
                        "type": "string",
                        "title": "Schema Name",
                        "description": "Name of schema file without extension",
                        "pattern": "[0-9a-zA-Z_-]+"
                    },
                    "is_list": {
                        "title": "Schema is_list",
                        "type": "boolean",
                        "description": "Does schema contain a list of items"
                    },
                    "required": {
                        "title": "Schema Required",
                        "type": "boolean",
                        "description": "Is schema required in deployment"
                    },
                    "encrypted": {
                        "title": "Schema Encrypted",
                        "type": "boolean",
                        "description": "Does schema contain a encrypted data"
                    }
                },
                "required": ["name", "is_list", "required", "encrypted"]
            }
        },
        "hooks": {
            "type": "array",
            "title": "Hooks",
            "description": "Set of hooks to execute within MetroAE workflow",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "location": {
                        "title": "Hook Location",
                        "type": "string",
                        "description": "Hook location in MetroAE workflow"
                    },
                    "role": {
                        "title": "Hook Role",
                        "type": "string",
                        "description": "Plugin Ansible role to execute at hook"
                    },
                    "tasks": {
                        "title": "Hook Tasks",
                        "type": "string",
                        "description": ("Plugin Ansible tasks to execute at "
                                        "hook")
                    }
                },
                "required": ["location", "role", "tasks"]
            }
        }

    },
    "required": ["plugin_name", "version", "required_metro_version"]
}

PLUGIN_SCHEMA_PROPERTIES_SCHEMA = {
    "type": "object",
    "title": "Properties",
    "description": "Set of properties",
    "patternProperties": {
        "^.*$": {
            "type": "object",
            "title": "Property",
            "description": "Allowed schema property",
            "properties": {
                "type": {
                    "type": "string",
                    "title": "Property type",
                    "description": ("Type for property field. Cannot support "
                                    "objects of objects"),
                    "enum": ["string", "integer", "number", "boolean", "array"]
                },
                "title": {
                    "type": "string",
                    "title": "Property title",
                    "description": "Title for schema property"
                },
                "description": {
                    "type": "string",
                    "title": "Property description",
                    "description": "description for schema property"
                },
                "propertyOrder": {
                    "type": "integer",
                    "title": "Property order",
                    "description": "Defines the ordering of properties"
                },
                "items": {
                    "type": "object",
                    "title": "Property Items",
                    "description": "Allowed array properties",
                    "properties": {
                        "type": {
                            "type": "string",
                            "title": "Property array type",
                            "description": ("Type for property array items. "
                                            "Cannot support arrays of objects "
                                            "or arrays"),
                            "enum": ["string", "integer", "number", "boolean"]
                        }
                    },
                    "required": ["type"]
                }
            },
            "required": ["type", "title", "propertyOrder"]
        }
    },
}

PLUGIN_SCHEMA_SCHEMA = {
    "$schema": "http://json-schema.org/draft-06/schema#",
    "$id": "urn:nuage-metroae:plugin-schema",
    "title": "Plugin Schema",
    "description": "Schema for plugin schema",
    "type": "object",
    "properties": {
        "type": {
            "type": "string",
            "title": "Type",
            "description": "Allowed top-level schema types",
            "enum": ["object", "array"]
        },
        "title": {
            "type": "string",
            "title": "Title",
            "description": "Schema title"
        },
        "description": {
            "type": "string",
            "title": "Description",
            "description": "Schema description"
        },
        "properties": PLUGIN_SCHEMA_PROPERTIES_SCHEMA,
        "items": {
            "type": "object",
            "title": "Schema items",
            "description": "Items in schema",
            "properties": {
                "type": {
                    "type": "string",
                    "title": "Item type",
                    "description": "Array items must be objects",
                    "enum": ["object"]
                },
                "title": {
                    "type": "string",
                    "title": "Item title",
                    "description": "Title for each item"
                },
                "properties": PLUGIN_SCHEMA_PROPERTIES_SCHEMA
            },
            "required": ["type", "title", "properties"]
        }
    },
    "required": ["type", "title", "description"]
}


def validate_plugin(plugin_directory):

    plugin_config_file = os.path.join(plugin_directory, PLUGIN_CONFIG_NAME)

    if not os.path.isfile(plugin_config_file):
        print(plugin_directory + " is missing config file " +
                                           PLUGIN_CONFIG_NAME)
        sys.exit(1)

    plugin_config = parse_plugin_config(plugin_config_file)

    validate_schemas(plugin_directory, plugin_config["schemas"])
    validate_hooks(plugin_directory, plugin_config["hooks"])


def parse_plugin_config(plugin_config_file):
    return parse_yaml(plugin_config_file, PLUGIN_CONFIG_SCHEMA)


def parse_yaml(yaml_file, schema):
    with open(yaml_file, 'r') as file:
        try:
            parsed_yaml = yaml.safe_load(file.read())
        except Exception as e:
            msg = "Could not parse plugin file %s: %s" % (
                yaml_file, str(e))
            print(msg)
            sys.exit(1)

    try:
        validate(parsed_yaml, schema)
    except ValidationError as e:

        field = ""
        if "title" in e.schema:
            field = " for " + e.schema["title"]
        msg = "Invalid data in %s%s: %s" % (yaml_file, field, e.message)
        print(msg)
        sys.exit(1)

    return parsed_yaml


def validate_schemas(plugin_directory, schemas):
    for schema in schemas:
        schema_file = os.path.join(plugin_directory, "schemas",
                                   schema["name"] + ".json")

        if not os.path.isfile(schema_file):
            print(plugin_directory + " is missing schema file " +
                   schema_file)
            sys.exit(1)

        parse_yaml(schema_file, PLUGIN_SCHEMA_SCHEMA)


def validate_hooks(plugin_directory, hooks):
    for hook in hooks:
        role_file = os.path.join(plugin_directory, "roles", hook["role"],
                                 "tasks", hook["tasks"] + ".yml")

        if not os.path.isfile(role_file):
            print(plugin_directory + " is missing role file " +
                   role_file)
            sys.exit(1)


def main():
    if len(sys.argv) != 2:
        print("Validates the format of a MetroAE plugin")
        print("Usage:")
        print("  " + sys.argv[0] + " <plugin-directory>")
        sys.exit(1)

    plugin_directory = sys.argv[1]

    if not os.path.isdir(plugin_directory):
        print(plugin_directory + " is not a plugin directory")
        sys.exit(1)

    validate_plugin(plugin_directory)

    print("Plugin OK!")


if __name__ == '__main__':
    main()
