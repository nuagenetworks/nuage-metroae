import sys
import os.path
import argparse
import yaml
from datetime import datetime


def verify_dockermon_result(content):
    result = ""
    error = ""
    if ("docker start/running, process "
        +content["docker_pid"] not in content["docker_status"]):
        error += "Error! Docker service is not running!"

    if ("Service nuage-docker-monitor is running" not in content["dockermon_status"]):
        error += "| Error! Dockermon service is not running!"

    if ("nuage-docker-monitor: monitoring pid "
        +content["dockermon_pid"]+" healthy" not in content["process_docker_status"]):
        error += "| Error! Dockermon is not monitoring!"

    # Check the logs only if dockermon and docker have started
    if (error == ''):
        # Split most recent logs into a list
        docker_logs_list = content["docker_logs"].split("||")
        # Check if logs are generated after the dockermon process started
        process_status_list = content["process_docker_status"].split("||")
        for process_status in process_status_list:
            if ("nuage-docker-monitor: monitoring pid" in process_status):
                dockermon_start_time =  process_status.split("nuage-docker-monitor")[0].strip()

        date_dockermon = datetime.strptime(dockermon_start_time, '%a %b %d %H:%M:%S %Y')

        for index in range(len(docker_logs_list)):
            log_time = docker_logs_list[index].split("|")[0]
            date_log = datetime.strptime(log_time, '%b %d %H:%M:%S')
            # Setting the year of the logs to current year
            date_log = date_log.replace(year=datetime.now().year)

            if (date_log >= date_dockermon):
                # The log should have been generated after the start of dockermon
                if ((index == 0) and 
                    ("Nuage Docker Monitor started successfully" not in docker_logs_list[index])):
                    error += "| Error! Log for successful start of dockermon not received."
                elif (index == 1 and 
                    ("Nuage Docker Monitor is now monitoring container lifecycle events" not in docker_logs_list[index])):
                    error += "| Error! Log for dockermon monitoring life cycle events not received."
                elif (index == 2 and
                    ("Initial Sync, Resending all the containers..." not in docker_logs_list[index])):
                    error += "| Error! Log for initial sync not received."
            else:
                error += "| Error! Log:"+str(index)+" was generated before current instance of dockermon started."

    if (error == ''):
        result = "Dockermon is OK!"
    else:
        result = error

    return result


# Main
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("dockermon_output_file", type=str,
                        help="File for output of commands for verification of dockermon deployment.")
    parser.add_argument("playbook_dir", type=str,
                        help="Path of playbook directory.")
    args = parser.parse_args()
    dockermon_output_file = args.dockermon_output_file
    playbook_dir = args.playbook_dir

    if (not playbook_dir):
        print ("Error! Invalid input: playbook_dir.")
        sys.exit(1)

    if (not dockermon_output_file):
        print ("Error! Invalid input: ovs_output_file.")
        sys.exit(1)

    dockermon_file_path = playbook_dir+"/scripts/tmp/"+dockermon_output_file
    if (not os.path.exists(dockermon_file_path)):
        print ("ERROR! Temporary file {0} not found." .format(dockermon_file_path))
        sys.exit(1)

    try:
        with open(dockermon_file_path, "r") as stream:
             file_content = yaml.safe_load(stream)
    except:
        print("Error processing dockermon results output file {0}:{1}" .format(dockermon_file_path, sys.exc_info()[0]))
        sys.exit(1)

    result = verify_dockermon_result(file_content)
    print result
