#!/usr/bin/env python

import argparse
import datetime
import os

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


def aggregate_logs(args):
    output("Searching for log files...")

    log_files = find_log_files(args.log_paths, args.log_extensions)

    output(str(len(log_files)) + " log files found")

    output("Combining log files...")

    write_aggregate_log(log_files, args.output_file)


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


def write_aggregate_log(log_files, output_file_name):
    with open(output_file_name, "w") as out_file:
        out_file.write(HTML_PAGE_HEADERS)
        out_file.write(HTML_PAGE_STYLE)
        out_file.write(HTML_PAGE_BODY)
        out_file.write(HTML_PAGE_SCRIPT_HEADERS)

        out_file.write("lines = [\n'")
        for file_name in log_files:
            add_log_to_output_file(file_name, out_file)
        out_file.write("'\n];\n")

        out_file.write(HTML_PAGE_SCRIPT_FOOTERS)
        out_file.write(HTML_PAGE_FOOTERS)


def add_log_to_output_file(log_file_name, out_file):
    with open(log_file_name, "r") as f:
        log_contents = f.read().decode("utf-8", "ignore")
        out_file.write(format_log_output(log_contents))


def format_log_output(log_contents):
    log_contents = log_contents.encode('ascii', 'xmlcharrefreplace')
    log_contents = log_contents.replace("'", "&#39;")
    log_contents = log_contents.replace("\\", "&#92;")
    log_contents = log_contents.replace("<", "&lt;")
    log_contents = log_contents.replace(">", "&gt;")
    log_contents = log_contents.replace("\r", "")
    return "',\n'".join(log_contents.split("\n"))


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

    aggregate_logs(args)


if __name__ == '__main__':
    main()
