#!/usr/bin/env python

import argparse
import datetime
import dateutil.parser
import os
import re

RE_MONTH_NAME = "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)"
RE_MONTH_NUM = "((1[0-2])|(0?[1-9]))"
RE_DAY = "(([1-2][0-9])|(3[0-1]|(0?[1-9])))"
RE_YEAR = "(20[0-9][0-9])"
RE_HOUR = "((1[0-9])|(2[0-3])|(0?[0-9]))"
RE_MIN = "([0-5][0-9])"
RE_SEC = "([0-5][0-9])"
RE_MSEC = "([0-9][0-9][[0-9])"

DATE_PATTERNS = [
    "({day}[ /-]{month_name}([ /-]{year})?)".format(year=RE_YEAR,
                                                    month_name=RE_MONTH_NAME,
                                                    day=RE_DAY),
    "({month_name}([ ]+){day}([ ]+{year})?)".format(year=RE_YEAR,
                                                    month_name=RE_MONTH_NAME,
                                                    day=RE_DAY),
    "({month}[/-]{day}[/-]{year})".format(year=RE_YEAR,
                                          month=RE_MONTH_NUM,
                                          day=RE_DAY),
    "({year}[/-]{month}[/-]{day})".format(year=RE_YEAR,
                                          month=RE_MONTH_NUM,
                                          day=RE_DAY),
    "({year}[/-]{month_name}[/-]{day})".format(year=RE_YEAR,
                                               month_name=RE_MONTH_NAME,
                                               day=RE_DAY)
]

date_patterns = list()

TIME_PATTERNS = [
    "({hour}:{min}:{sec}([,.]{msec})?)".format(hour=RE_HOUR,
                                               min=RE_MIN,
                                               sec=RE_SEC,
                                               msec=RE_MSEC)
]

time_patterns = list()

HTML_PAGE_HEADERS = """
<html><head><title>Aggregated logs - %s</title></head><body>
""" % datetime.datetime.now()

HTML_PAGE_STYLE = """
<style>

body {
    background-color: #202020;
    color: #e0e0e0;
}

.loader {
  top: 30%;
  font-size: 10px;
  margin: 50px auto;
  text-indent: -9999em;
  width: 11em;
  height: 11em;
  border-radius: 50%;
  background: #ffffff;
  background: -moz-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
  background: -webkit-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
  background: -o-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
  background: -ms-linear-gradient(left, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
  background: linear-gradient(to right, #ffffff 10%, rgba(255, 255, 255, 0) 42%);
  position: relative;
  -webkit-animation: load3 1.4s infinite linear;
  animation: load3 1.4s infinite linear;
  -webkit-transform: translateZ(0);
  -ms-transform: translateZ(0);
  transform: translateZ(0);
}
.loader:before {
  width: 50%;
  height: 50%;
  background: #ffffff;
  border-radius: 100% 0 0 0;
  position: absolute;
  top: 0;
  left: 0;
  content: '';
}
.loader:after {
  background: #202020;
  width: 75%;
  height: 75%;
  border-radius: 50%;
  content: '';
  margin: auto;
  position: absolute;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
}
@-webkit-keyframes load3 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}
@keyframes load3 {
  0% {
    -webkit-transform: rotate(0deg);
    transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
    transform: rotate(360deg);
  }
}

/* .roundedCheck */
.roundedCheck {
  width: 28px;
  height: 28px;
  position: relative;
  margin: 5px auto;
  background: #fcfff4;
  background: -webkit-gradient(linear, left top, left bottom, from(#fcfff4), color-stop(40%, #dfe5d7), to(#b3bead));
  background: linear-gradient(to bottom, #fcfff4 0%, #dfe5d7 40%, #b3bead 100%);
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px white, 0px 1px 3px rgba(0, 0, 0, 0.5);
}
.roundedCheck label {
  width: 20px;
  height: 20px;
  cursor: pointer;
  position: absolute;
  left: 4px;
  top: 4px;
  background: -webkit-gradient(linear, left top, left bottom, from(#222222), to(#45484d));
  background: linear-gradient(to bottom, #222222 0%, #45484d 100%);
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px rgba(0, 0, 0, 0.5), 0px 1px 0px white;
}
.roundedCheck label:after {
  content: '';
  width: 16px;
  height: 16px;
  position: absolute;
  top: 2px;
  left: 2px;
  background: #27ae60;
  background: -webkit-gradient(linear, left top, left bottom, from(#27fe60), to(#145b32));
  background: linear-gradient(to bottom, #27fe60 0%, #145b32 100%);
  opacity: 0;
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px white, 0px 1px 3px rgba(0, 0, 0, 0.5);
}
.roundedCheck label:hover::after {
  opacity: 0.3;
}
.roundedCheck input[type=checkbox] {
  visibility: hidden;
}
.roundedCheck input[type=checkbox]:checked + label:after {
  opacity: 1;
}

/* Tooltip container */
.tooltip {
  position: relative;
  display: inline-block;
  border-bottom: 1px dotted black; /* If you want dots under the hoverable text */
}

/* Tooltip text */
.tooltip .tooltiptext {
  visibility: hidden;
  /*width: 120px;*/
  background-color: #555;
  color: #fff;
  text-align: center;
  padding: 5px 5px;
  border-radius: 6px;
  white-space: nowrap;

  /* Position the tooltip text - see examples below! */
  position: absolute;
  z-index: 1;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  transition-delay:1s;
}

hr {
  border: 0;
  height: 1px;
  width: 100%;
  background-image: -webkit-linear-gradient(left, #202020, #e0e0e0, #202020);
  background-image: -moz-linear-gradient(left, #202020, #e0e0e0, #202020);
  background-image: -ms-linear-gradient(left, #202020, #e0e0e0, #202020);
  background-image: -o-linear-gradient(left, #202020, #e0e0e0, #202020);
}

#filesPane {
  width: 30%;
  height: 100%;
}

.fileList {
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;
}

.fileRow {
  width: 100%;
  min-width: 200px;
  display: flex;
  flex-direction: row;
  align-content: baseline;
  justify-content: flex-start;
}

.logName {
  height: 28px;
  margin: 5px auto;
  margin-left: 5px;
  display: flex;
  /*justify-content: center;*/
  align-items: center;
}

#logPane {
  width: 100%;
  height: 100%;
}

#logConsole {
  border: 2px solid #606060;
  border-radius: 15px;
  overflow: scroll;
  scroll-behavior: auto;
}

#logText {
  width: 100%;
  height: 100%;
  padding: 4px;
  font-family: monospace;
  white-space: pre;
}

#screen {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: row;
}

</style>

"""

HTML_PAGE_BODY = """
<div id="screen">
    <div id="filesPane">

    <div id="fileList">

    <div class="fileRow">
    <div>
    <div class="roundedCheck">
      <input type="checkbox" value="None" id="all" name="all" checked />
      <label for="all"></label>
    </div>
    </div>
    <div class="logName">
    Show all
    </div>
    </div>

    <div class="fileRow">
        <hr class="style">
    </div>

    <div class="fileRow">
    <div>
    <div class="roundedCheck">
      <input type="checkbox" value="None" id="metroae.log" name="metroae.log" checked />
      <label for="metroae.log"></label>
    </div>
    </div>
    <div class="logName tooltip">
    metroae.log
    <span class="tooltiptext">/nuage-metroae/metroae.log</span>
    </div>
    </div>

    <div class="fileRow">
    <div>
    <div class="roundedCheck">
      <input type="checkbox" value="None" id="output.log" name="output.log" checked />
      <label for="output.log"></label>
    </div>
    </div>
    <div class="logName tooltip">
    output.log
    <span class="tooltiptext">/nuage-metroae/output.log</span>
    </div>
    </div>

    <div class="fileRow">
    <div>
    <div class="roundedCheck">
      <input type="checkbox" value="None" id="aud.log" name="aud.log" checked />
      <label for="aud.log"></label>
    </div>
    </div>
    <div class="logName tooltip">
    aud.log
    <span class="tooltiptext">/nuage-metroae/aud.log</span>
    </div>
    </div>

Loading files...
<div id="loading" class="loader"></div>

    </div>
    </div>

    <div id="logPane">

    <div id="logConsole">
    <div id="logText">Loading logs...
<div id="loading" class="loader"></div>

    </div>
    </div>

    </div>
</div>
"""

HTML_PAGE_SCRIPT_HEADERS = "<script>"

HTML_PAGE_SCRIPT_FOOTERS = """
var files = [
'nuage-metro/metroae.log',
'nuage-metro/audit.log',
'nuage-metro/ansible.log',
];

var fileListHeading =
    '<div class="fileRow">\\n' +
    '<div>\\n' +
    '<div class="roundedCheck">\\n' +
    '  <input type="checkbox" value="None" id="all" name="all" checked />\\n' +
    '  <label for="all"></label>\\n' +
    '</div>\\n' +
    '</div>\\n' +
    '<div class="logName">\\n' +
    'Show all\\n' +
    '</div>\\n' +
    '</div>\\n' +
    '<div class="fileRow">\\n' +
    '    <hr class="style">\\n' +
    '</div>\\n';

var fileListTemplate =
    '<div class="fileRow">\\n' +
    '<div>\\n' +
    '<div class="roundedCheck">\\n' +
    '  <input type="checkbox" value="None" id="--name--" name="--name--" checked />\\n' +
    '  <label for="--name--"></label>\\n' +
    '</div>\\n' +
    '</div>\\n' +
    '<div class="logName tooltip">\\n' +
    '--name--\\n' +
    '<span class="tooltiptext">--path--</span>\\n' +
    '</div>\\n' +
    '</div>\\n';

var curPage = 0;

function get(elementId) {
    return document.getElementById(elementId);
}

function getNumPageLines() {
    var logsElem = get("logConsole");
    return parseInt(logsElem.clientHeight / 15);
}

function showLogPage() {
    var logsElem = get("logText");

    var numLines = getNumPageLines();
    var offset = numLines * curPage;
    // logsElem.style.height = lines.length * 15;
    logsElem.innerHTML = "";
    for (i = offset; i < numLines * 2 + offset; i++) {
        logsElem.innerHTML += lines[i] + "\\n";
    }
}

function handleScroll() {
    var logsElem = get("logConsole");
    console.log(logsElem.scrollTop);
    console.log(logsElem.clientHeight);
    console.log(logsElem.scrollHeight);

    var scrollThresh = parseInt(logsElem.clientHeight * 0.95);
    if (logsElem.scrollTop == 0 && curPage > 0) {
        curPage -= 1;
        showLogPage();
        logsElem.scrollTop = scrollThresh;
    } else if (logsElem.scrollTop > scrollThresh) {
        curPage += 1;
        showLogPage();
        logsElem.scrollTop = 1
    }

}

document.body.onload = function() {
    var fileListElem = get("fileList");
    var fileList = fileListHeading

    for (var i = 0; i < files.length; i++) {
        var baseName = files[i].split("/");
        baseName = baseName[baseName.length - 1];
        var fileItem = fileListTemplate.replace(/--name--/g, baseName);
        fileItem = fileItem.replace(/--path--/g, files[i]);
        fileList += fileItem;
    }
    fileListElem.innerHTML = fileList;

    showLogPage();

    var logsElem = get("logConsole");
    logsElem.onscroll = handleScroll;

    document.body.onresize = showLogPage;

    // var logsElem = get("logText");
    // logsElem.innerHTML = lines.join("\\n");

    // for (i = 0; i < 1000; i++) {
    //     document.write(lines[i] + '<br>');
    // }
}
</script>

"""

HTML_PAGE_FOOTERS = """
</body></html>
"""


def output(msg):
    print(msg)


def fatal_error(msg):
    print(msg)
    exit(1)


def complile_re_patterns():
    for pattern in DATE_PATTERNS:
        date_patterns.append(re.compile(pattern, re.IGNORECASE))

    for pattern in TIME_PATTERNS:
        time_patterns.append(re.compile(pattern, re.IGNORECASE))


def aggregate_logs(args):
    output("Searching for log files ...")

    log_files = find_log_files(args.log_paths, args.log_extensions)

    output(str(len(log_files)) + " log files found")

    log_list = read_log_files(log_files)
    timestamps = list()
    for i, log in enumerate(log_list):
        # output("%d - %s" % (detect_prefix(log), log_files[i]))
        # output(log[0].strip())
        # output(" " * detect_prefix(log) + "^")
        output("Detecting timestamps %d/%d ..." % (i + 1, len(log_list)))
        timestamps.append(detect_timestamps(log))
        # output(str(timestamps[i][0]))

    output("Interleaving logs ...")
    combined = interleave_logs(log_list, timestamps)

    write_aggregate_log(log_files, combined, args.output_file)

    output("\nDone! View in web browser: " + args.output_file)


def find_log_files(paths, extensions):
    log_files = list()
    for path in paths:
        if (os.path.isdir(path)):
            for file_name in os.listdir(path):
                log_files.extend(find_log_files(
                    [os.path.join(path, file_name)], extensions))
        elif os.path.isfile(path):
            for ext in extensions:
                if (path.endswith(ext)):
                    log_files.append(path)
        elif os.path.islink(path):
            pass
        else:
            fatal_error("File or path not found: " +
                        path)

    return log_files


def read_log_files(log_files):
    log_list = list()
    for file_name in log_files:
        output("Reading %s ..." % file_name)
        with open(file_name, "r") as f:
            log_contents = f.read().decode("utf-8", "ignore")
            log_list.append(log_contents.split("\n"))

    return log_list


def detect_prefix(log):
    position_count = dict()

    for line in log:
        position = -1
        words = line.strip().split(" ")
        for word in words:
            position += len(word) + 1
            if position in position_count:
                position_count[position] += 1
            else:
                position_count[position] = 1

    threshold = int(len(log) * 0.75)

    best_position = 0
    for position, count in position_count.iteritems():
        if count > threshold and position > best_position:
            best_position = position

    return best_position


def detect_timestamps(log):
    timestamps = list()

    for line in log:
        timestamps.append(find_timestamp_in_line(line))

    return timestamps


def find_timestamp_in_line(line):
    date_string = find_pattern_match(date_patterns, line)
    time_string = find_pattern_match(time_patterns, line)

    if time_string is None:
        return None

    if date_string is None:
        timestamp_str = time_string
    else:
        timestamp_str = " ".join([date_string, time_string])

    try:
        # return dateutil.parser.parse(timestamp_str)
        return (dateutil.parser.parse(timestamp_str) -
                datetime.datetime(1970, 1, 1)).total_seconds()
    except Exception:
        return None


def find_pattern_match(patterns, line):
    best_match = None
    best_position = 999999999
    for pattern in patterns:
        match = pattern.search(line)
        if match is not None and match.pos < best_position:
            best_match = match.groups()[0]
            best_position = match.pos

    return best_match


def interleave_logs(log_list, timestamps):
    combined = list()
    positions = initialize_positions(timestamps)

    log_index = 0

    # Interleave log lines with timestamps
    while log_index is not None:
        log_index = find_next_log_index(positions)
        if log_index is not None:
            add_log_lines(combined,
                          positions[log_index],
                          log_list[log_index],
                          timestamps[log_index],
                          log_index)

    # Flush remaining lines
    for log_index, log in enumerate(log_list):
        add_log_lines(combined,
                      positions[log_index],
                      log,
                      timestamps[log_index],
                      log_index)

    return combined


def initialize_positions(timestamps):
    positions = list()
    for timestamp_set in timestamps:
        first_timestamp = None
        for timestamp in timestamp_set:
            if timestamp is not None:
                first_timestamp = timestamp
                break

        positions.append([first_timestamp, 0])

    return positions


def find_next_log_index(positions):
    best_index = None
    best_position = 999999999999.0
    for i, position in enumerate(positions):
        if position[0] is not None and position[0] < best_position:
            best_index = i
            best_position = position[0]

    return best_index


def add_log_lines(combined, position, log, timestamp_set, log_index):
    first = True
    while position[1] < len(log) and (
            first or timestamp_set[position[1]] is None):
        first = False
        combined.append(log_index)
        combined.append(log[position[1]])
        position[1] += 1

    if position[1] < len(timestamp_set):
        position[0] = timestamp_set[position[1]]
    else:
        position[0] = None


def write_aggregate_log(log_files, combined, output_file_name):
    with open(output_file_name, "w") as out_file:
        out_file.write(HTML_PAGE_HEADERS)
        out_file.write(HTML_PAGE_STYLE)
        out_file.write(HTML_PAGE_BODY)
        out_file.write(HTML_PAGE_SCRIPT_HEADERS)

        out_file.write("lines = [\n")

        for line in combined:
            out_file.write(format_log_line(line))
        # for file_name in log_files:
        #     output("Adding %s ..." % file_name)
        #     add_log_to_output_file(file_name, out_file)

        out_file.write("''];\n")

        out_file.write(HTML_PAGE_SCRIPT_FOOTERS)
        out_file.write(HTML_PAGE_FOOTERS)


# def add_log_to_output_file(log_file_name, out_file):
#     with open(log_file_name, "r") as f:
#         log_contents = f.read().decode("utf-8", "ignore")
#         out_file.write(format_log_output(log_contents))


def format_log_line(log_line):
    if type(log_line) == int:
        return "%3d, " % log_line
    else:
        log_line = log_line.encode('ascii', 'xmlcharrefreplace')
        log_line = log_line.replace("'", "&#39;")
        log_line = log_line.replace("\\", "&#92;")
        log_line = log_line.replace("<", "&lt;")
        log_line = log_line.replace(">", "&gt;")
        log_line = log_line.replace("\r", "")
        return "".join(["'", log_line, "',\n"])


def main():
    parser = argparse.ArgumentParser(
        description='Aggregate a set of logs into a single viewable file')
    parser.add_argument("log_paths", help="Log paths or files to aggregate",
                        nargs="*")
    parser.add_argument("-x", "--log_extensions",
                        help="File extension for log files",
                        nargs="*", default=[".log"])
    parser.add_argument("-o", "--output_file",
                        help="Path to file to output aggregated logs",
                        action="store",
                        default="aggregated_logs.html")

    args = parser.parse_args()

    complile_re_patterns()

    aggregate_logs(args)


if __name__ == '__main__':
    main()
