import sys
import os.path
import argparse
import yaml
from datetime import datetime


def verify_dockermon_result(content):
    result = ""
    error = ""
    if ("docker start/running, process " not in content["docker_status"] and "Active:" not in content["docker_status"]):
        error += "Error! Docker service is not running!"

    if ("Service nuage-docker-monitor is running" not in content["dockermon_status"]):
        error += "| Error! Dockermon service is not running!"

    if (("/usr/bin/python /usr/bin/nuage-docker-monitor" not in content["process_docker_status"])
            and ("nuage-docker-monitor: monitoring" not in content["process_docker_status"])):
        error += "| Error! Dockermon process is not running!"

    # Check the logs only if dockermon and docker have started
    if (error == ''):
        # Split most recent logs into a list
        docker_logs_list = content["docker_logs"].split("||")
        # Check if logs are generated after the dockermon process started
        process_status_list = content["process_docker_status"].split("||")
        for process_status in process_status_list:
            if ("/usr/bin/python /usr/bin/nuage-docker-monitor" in process_status):
                dockermon_start_time = process_status.split("/usr/bin/python /usr/bin/nuage-docker-monitor")[0].strip()
                break
            elif ("nuage-docker-monitor: monitoring" in process_status):
                dockermon_start_time = process_status.split("nuage-docker-monitor: monitoring")[0].strip()
                break

        date_dockermon = datetime.strptime(dockermon_start_time, '%a %b %d %H:%M:%S %Y')

        # Check the log time of the first log
        log_time = docker_logs_list[0].split("|")[0]
        date_log = datetime.strptime(log_time, '%b %d %H:%M:%S')
        # Setting the year of the logs to current year
        date_log = date_log.replace(year=datetime.now().year)

        # The first log should have been generated after dockermon started
        if (date_log >= date_dockermon):
            if (not(("Nuage Docker Monitor started successfully" in content["docker_logs"]) or
                ("Nuage Docker Monitor is now monitoring container lifecycle events" in content["docker_logs"]) or
                    ("Initial Sync, Resending all the containers" in content["docker_logs"]))):
                error += "| Error! Nuage Docker Monitor did not start successfully."
        else:
            error += "| Error! Current Nuage Docker Monitor events not found."

    if (error == ''):
        result = "Dockermon is OK!"
    else:
        result = error

    return result


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dockermon_data_file", type=str,
                        help="Name of the input file that contains dockermon data to be verified.")
    parser.add_argument("dockermon_file_path", type=str,
                        help="Path to location of dockermon data file.")
    args = parser.parse_args()
    dockermon_data_file = args.dockermon_data_file

    dockermon_file_path = args.dockermon_file_path + dockermon_data_file
    if (not os.path.exists(dockermon_file_path)):
        print ("ERROR! Nuage Docker Monitor data file not found.")
        sys.exit(1)

    try:
        with open(dockermon_file_path, "r") as stream:
            file_content = yaml.safe_load(stream)
    except:
        print("Error processing dockermon results output file {0}:{1}" .format(dockermon_file_path, sys.exc_info()[0]))
        sys.exit(1)

    result = verify_dockermon_result(file_content)
    print result
