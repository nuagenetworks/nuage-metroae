# Automatically Generating Deployment Files
If you would like to automatically generate deployment files, MetroÆ provides jinja2 templates for this purpose. The templates are automatically generated from the schemas by the MetroÆ team. They are always up to date. You can find these jinja2 templates in the src/deployment_templates directory in your workspace. You can use one, monolithic YAML file as input to generate all deployment files. You can use multiple input files, one for each deployment file you wish to generate. Or some combination of the two. To generate the files, you can use a Python script to call jinja2 to convert the YAML input file into a deployment file.

### Example code
Below is example code that can be used to create deployment files from a single user input file.

```python
def write_deployment(var_dict, deployment_name, jinja_template_file, deployment_file):

    deployment_dir = os.path.join(DEPLOYMENTS_DIRECTORY, deployment_name)
    if not os.path.exists(deployment_dir):
        os.makedirs(deployment_dir)

    write_deployment_file(jinja_template_file,
                          deployment_file,
                          var_dict)


def write_deployment_file(template_file, to_file, var_dict):
    with open(template_file, "r") as file:
        template_string = file.read().decode("utf-8")

    template = jinja2.Template(template_string,
                               autoescape=False,
                               undefined=jinja2.StrictUndefined)

    var_file_contents = template.render(var_dict)

    with open(to_file, "w") as file:
        file.write(var_file_contents.encode("utf-8"))
```

### Example user data

```yaml
nuage_unzipped_files_dir: "/my/unzipped/filedir"
dns_domain: "company.com"
vsd_fqdn_global: "vsd1.company.com"
mgmt_bridge: "br0"
data_bridge: "br1"
ntp_server_list: [ "5.5.5.5", "2.2.2.2", ]
dns_server_list: [ "10.1.0.2", ]
deployment_name: ""
deployment_description: ""
credentials:
  -
    name: ""
vsds:
  -
    hostname: "vsd1.company.com"
    mgmt_ip: "192.168.110.30"
    mgmt_ip_prefix: 24
    mgmt_gateway: "192.168.110.1"
    target_server_type: "kvm"
    target_server: "10.105.1.102"
```
