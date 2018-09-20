import re
import sys


# Verify stats collector info on vrs
def verify_vrs_stats(stats_str):
    result = ''

    # Remove special chars added by ansible
    stats_info = stats_str.strip()
    stats_re = re.sub('\t', '', stats_info)

    # Extract all the stats servers
    stats = re.search(r'stats_collectors:(.*)\s+(\w+.*)', stats_re)
    stats_server = stats.group(1)
    if stats_server == ' ':
        error = "ERROR: Did not find any stats collectors info"
        return error
    else:
        lst_stats_server = stats_server.split(',')
        result = result + "Found %s stats collectors for vrs \n" \
            % (len(lst_stats_server))

    # Find the stat server that is actively connected to VSD
    stats_conn = stats.group(2)
    if "ACTIVE" in stats_conn:
        active_server = re.search(r'tcp:(\d+.\d+.\d+.\d+:\d+)', stats_conn)
        result = result + "Connection to stats collector is active and \
                 connected to %s\n" % active_server.group(1)
    else:
        error = "ERROR: Connection to stat server is not active\n"
        return result + error

    return result


if __name__ == "__main__":
    stats_str = sys.argv[1]
    if not stats_str:
        print "ERROR: No ouput from 'ovs-appctl ofproto/show alubr0' command"
        sys.exit(1)

    result = verify_vrs_stats(stats_str)

    # Display final result
    print ("{0}" .format(result))
