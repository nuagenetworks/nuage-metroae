#!/usr/bin/env python

import json
import os
import yaml


SCHEMAS_DIRECTORY = "schemas"
TABLE_MARGIN_LEFT = 1
TABLE_MARGIN_TOP = 1

FORMAT = """

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

- ""
- For vCenter deployments only

- schema: common
  no_title: true
  fields:
    - vcenter_datacenter
    - vcenter_cluster
    - vcenter_datastore
  headers: [Common, Values, "", Descriptions]

- ""
- For upgrade only

- schema: upgrade
  fields:
    - upgrade_from_version
    - upgrade_to_version
  headers: [Upgrade, Values, "", Descriptions]

- schema: vsds
  headers: [VSDs, VSD 1 (SA), VSD 2 (HA), VSD 3 (HA),
            VSD 4 (Geo-Red), VSD 5 (Geo-Red), VSD 6 (Geo-Red),
            "", Descriptions]
  extra:
    - vmname

- schema: vscs
  headers: [VSCs, VSC 1 (SA), VSC 2 (HA), "", Descriptions]
  extra:
    - vmname
    - ctrl_ip
    - ctrl_ip_prefix

- schema: vstats
  headers: [VSTATs, VSTAT 1 (SA), VSTAT 2 (HA), VSTAT 3 (HA),
            VSTAT 4 (Geo-Red), VSTAT 5 (Geo-Red), VSTAT 6 (Geo-Red),
            "", Descriptions]
  extra:
    - vmname

- schema: nuhs
  headers: [NUHs, NUH 1 (SA), NUH 2 (HA), "", Descriptions]

- ""
- Configuration for VNS setups

- schema: vnsutils
  headers: [VNSUtils, VNSUTIL 1 , "", Descriptions]
  extra:
    - vmname
    - data_ip
    - data_netmask
    - data_subnet
    - nsgv_gateway

- schema: nsgvs
  headers: [NSGvs, NSGv 1, NSGv 2, more..., "", Descriptions]
  extra:
    - bootstrap_method
    - nsgv_ip
    - nsgv_mac
    - nsg_name
    - match_type
    - match_value
    - network_port_name
    - access_port_name
    - access_port_vlan_range
    - access_port_vlan_number

- ""
- When using MetroAE for zero-factor bootstrap of NSGvs

- schema: nsgv_bootstrap
  headers: [NSGv Bootstrap, Values, "", Descriptions]
  no_title: true
  fields:
    - nsgv_organization
    - proxy_user_first_name
    - proxy_user_last_name
    - proxy_user_email
    - nsg_infra_profile_name
    - nsg_template_name
    - proxy_dns_name
    - vsc_infra_profile_name
    - first_controller_address
    - second_controller_address

- ""
- ""
- Advanced instructions
- This spreadsheet can be used to populate deployment files for any of the
- schemas in the schemas directory.  The case-insenstive name of the schema
- must be specified in the upper left corner of the table.  The table can then
- be positioned anywhere in the spreadsheet provided there is at least one row
- and column of empty space around the table.  The case-insenstive names or
- titles of the properties can be either along rows or columns (either position
- is valid).

"""


def read_format(format):
    return yaml.safe_load(format)


def escape_line(line):
    if '"' in line or ',' in line:
        return '"' + line.replace('"', '""') + '"'
    return line


def read_schema(schema_name):
    file_name = schema_name + ".json"
    file_path = os.path.join(SCHEMAS_DIRECTORY, file_name)
    with open(file_path, "r") as f:
        schema_str = f.read().decode("utf-8")

    try:
        return json.loads(schema_str)
    except Exception as e:
        raise Exception("Could not parse schema: %s\n%s" % (
            file_name, str(e)))


def write_fields(lines, schema, table):
    width = len(table["headers"])
    fields = table.get("fields")
    extra = table.get("extra")

    if schema["type"] == "array":
        schema_props = schema["items"]["properties"]
        required = schema["items"].get("required")
    else:
        schema_props = schema["properties"]
        required = schema.get("required")

    if fields is None:
        fields = required

    if extra is not None:
        fields.extend(extra)

    for field_name in fields:
        field = schema_props[field_name]
        description = field.get("description", "")
        lines.append(field["title"] +
                     ("," * (width - 1)) +
                     escape_line(description))


def write_table(table):
    schema_name = table["schema"]
    schema = read_schema(schema_name)

    lines = list()

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
    format = read_format(FORMAT)

    for item in format:
        if type(item) == dict:
            print write_table(item).encode("utf-8")
        else:
            print escape_line(item) + ","


if __name__ == '__main__':
    main()
