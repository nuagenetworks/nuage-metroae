#!/usr/bin/env python

import argparse
import datetime
import dateutil.parser
import os
import re
import shutil
import tarfile

MAX_LINE_LENGTH = 2000

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

.slideToggle {
  width: 80px;
  height: 26px;
  background: #333;
  margin: 5px auto;
  position: relative;
  border-radius: 50px;
  box-shadow: inset 0px 1px 1px rgba(0, 0, 0, 0.5), 0px 1px 0px rgba(255, 255, 255, 0.2);
}
.slideToggle:after {
  content: 'OFF';
  color: #000;
  position: absolute;
  right: 10px;
  z-index: 0;
  font: 12px/26px Arial, sans-serif;
  font-weight: bold;
  text-shadow: 1px 1px 0px rgba(255, 255, 255, 0.15);
}
.slideToggle:before {
  content: 'ON';
  color: #27ae60;
  position: absolute;
  left: 10px;
  z-index: 0;
  font: 12px/26px Arial, sans-serif;
  font-weight: bold;
}
.slideToggle label {
  display: block;
  width: 34px;
  height: 20px;
  cursor: pointer;
  position: absolute;
  top: 3px;
  left: 3px;
  z-index: 1;
  background: #fcfff4;
  background: -webkit-gradient(linear, left top, left bottom, from(#fcfff4), color-stop(40%, #dfe5d7), to(#b3bead));
  background: linear-gradient(to bottom, #fcfff4 0%, #dfe5d7 40%, #b3bead 100%);
  border-radius: 50px;
  -webkit-transition: all 0.4s ease;
  transition: all 0.4s ease;
  box-shadow: 0px 2px 5px 0px rgba(0, 0, 0, 0.3);
}
.slideToggle input[type=checkbox] {
  visibility: hidden;
}
.slideToggle input[type=checkbox]:checked + label {
  left: 43px;
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

filesPane {
  width: 20%;
  height: 100%;
  overflow: scroll;
}

#fileList {
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
  order: 1;
  -webkit-order: 1;
}

.logName {
  height: 28px;
  margin: 5px auto;
  margin-left: 5px;
  display: flex;
  align-items: center;
}

pageControls {
    height: 100%;
    width: 55px;
    display: flex;
    flex-direction: column;
    align-content: center;
    justify-content: center;
}

.pageButton {
    width: 50px;
    height: 50px;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-left: 3px;
    margin-right: 3px;
    font-size: 30px;
    cursor: pointer;
    outline: none;
    border-radius: 12px;
    color: #ddd;
    background: #333;
    box-shadow: inset 0px 1px 1px rgba(0, 0, 0, 0.5), 0px 1px 0px rgba(255, 255, 255, 0.2);
}

logPane {
  width: calc(80% - 55px);
  height: 100%;
  display: flex;
  flex-direction: column;
  align-content: center;
  justify-content: center;

}

logControls {
  height: 30px;
  width: 100%;
  overflow: scroll;
}

#status {
    float: right;
}

#logConsole {
  height: calc(100% - 30px);
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
  font-size: 13px;
  white-space: pre;
}

.logLine {
    width: 100%;
    height: 15px;
    border: 0;
    margin: 0;
}

.selected {
    outline-style: solid;
    outline-color: yellow;
    outline-width: 3px;
}

.found {
    outline-style: dotted;
    outline-color: yellow;
    outline-width: 1px;
}

screen {
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: row;
}

</style>

"""

HTML_PAGE_BODY = """
<screen>
    <filesPane>

    <div id="fileList">

    <div class="fileRow">

    <button onclick="handleAllToggle(true)">All ON</button>
    <button onclick="handleAllToggle(false)">All OFF</button>

    </div>

    <div class="fileRow">
        <hr class="style">
    </div>


<div id="loading" class="loader" style="order: 1; -webkit-order: 1;"></div>

    </div>
    </filesPane>

    <pageControls>
        <button class="pageButton" onclick="gotoPage('first')">&#x2912;</button>
        <button class="pageButton" onclick="gotoPage('bigup')">&#x219F;</button>
        <button class="pageButton" onclick="gotoPage('prev')">&#8593;</button>
        <button class="pageButton" onclick="gotoPage('next')">&#8595;</button>
        <button class="pageButton" onclick="gotoPage('bigdown')">&#x21A1;</button>
        <button class="pageButton" onclick="gotoPage('last')">&#x2913;</button>
    </pageControls>

    <logPane>

    <logControls>
        <input id="find" onkeyup="handleFind();" placeholder="Find">
        <button onclick="handleFindNext(-1);">Prev</button>
        <button onclick="handleFindNext(1);">Next</button>
        <input id="filter" onchange="handleFilter();" placeholder="Filter">
        <input id="exclude"  onchange="handleExclude();" placeholder="Exclude">
        <span id="findStatus"></span>
        <span id="status">Loading...</span>
    </logControls>

    <div id="logConsole">

    <div id="logText">Loading logs...
<div id="loading" class="loader"></div>

    </div>
    </div>

    </logPane>
</screen>

"""

HTML_PAGE_SCRIPT_HEADERS = "<script>"

HTML_PAGE_SCRIPT_FOOTERS = """

var filtered = [];

var toggles = [];

var curPage = 0;

var findString = "";
var filterString = "";
var excludeString = "";

var findLineCols = [];
var curFindIndex = -1;
var curWriteFindIndex = 0;

var findAsyncInProgress = false;
var findCurPage = 0;
var findAsyncString = "";
var findNumLines = 0;
var findAsyncStartLine = 0;
var findAsyncLimit = 0;
var findAsyncInsertPos = 0;
var findAsyncWrapped = false;
var linesSearched = 0;

var disableReorder = false;

var fileRowElems = [];

var fileListHeading =
    '<div class="fileRow" style="order: -2; -webkit-order: -2;">\\n' +
    '<button onclick="handleAllToggle(true)">All ON</button>\\n' +
    '<button onclick="handleAllToggle(false)">All OFF</button>\\n' +
    '</div>\\n' +
    '<div class="fileRow" style="order: -1; -webkit-order: -1;">\\n' +
    '    <hr class="style">\\n' +
    '</div>\\n';

var fileListTemplate =
    '<div id="file_row_--index--" class="fileRow highlight_--index--" ' +
    'style="background-color: --color--; order: 1; -webkit-order: 1;" ' +
    'onmouseover="logHighlight(--index--, true)" ' +
    'onmouseout="logHighlight(--index--, false)">\\n' +
    '<div>\\n' +
    '<div class="slideToggle">\\n' +
    '  <input class="toggle" type="checkbox" id="toggle_--index--" ' +
    'onclick="handleToggle()" checked />\\n' +
    '  <label for="toggle_--index--"></label>\\n' +
    '</div>\\n' +
    '</div>\\n' +
    '<div class="logName tooltip">\\n' +
    '--name--\\n' +
    '<span class="tooltiptext">--path--</span>\\n' +
    '</div>\\n' +
    '</div>\\n';

function get(elementId) {
    return document.getElementById(elementId);
}

function getLinesPerPage() {
    var logsElem = get("logConsole");
    return parseInt(logsElem.clientHeight / 15);
}

function getLastPage() {
    var linesPerPage = getLinesPerPage();
    var lastPage = 0;
    if (linesPerPage > 0) {
        lastPage = Math.floor(filtered.length / linesPerPage) - 1;
    }
    return Math.max(lastPage, 0);
}

function getViewingLine() {
    var filteredLine = getLinesPerPage() * curPage;
    if (filtered.length == 0) {
        return 0;
    }
    if (filteredLine >= filtered.length) {
        return filtered[filteredLine.length - 1];
    }
    return filtered[filteredLine];
}

function getLineColor(logNum, highlighted) {
    var hue = 0;
    var sat = 100;
    var lum = 15;
    if (highlighted) {
        lum = 25;
    }

    numLogFiles = files.length;
    if (numLogFiles > 16) {
        hue = Math.floor(720 * logNum / numLogFiles);
        if (hue >= 360) {
            hue = Math.floor(hue / 2);
            sat = 50;
        }
    } else if (numLogFiles > 0) {
        hue = Math.floor(360 * logNum / numLogFiles);
    }

    return "hsl(" + hue + "0, " + sat + "%, " + lum + "%)"
}

function writeLogPage() {
    checkAndResetFind();
    curWriteFindIndex = 0;

    resetFileRowOrder();

    var logsElem = get("logText");

    var numLines = getLinesPerPage();
    var offset = numLines * curPage;
    logsElem.innerHTML = "";
    for (i = offset; i < numLines * 2 + offset; i++) {
        if (i < filtered.length) {
            logsElem.innerHTML += formatLogLine(i);
        } else {
            logsElem.innerHTML += "<div class='logLine'>&nbsp;</div>";
        }
    }
}

function formatLogLine(lineNum) {
    var logIndex = lines[filtered[lineNum]];
    var line = lines[filtered[lineNum] + 1];

    moveUpFileRowOrder(logIndex);

    if (curFindIndex != -1) {
        line = formatSelectLine(line, lineNum);
    }
    return "<div class='logLine highlight_" + logIndex + "' style='background-color: " +
           getLineColor(logIndex, false) +
           "' onmouseover='logHighlight(" + logIndex + ", true)'" +
           " onmouseout='logHighlight(" + logIndex + ", false)'>" + line + "</div>";
}

function formatSelectLine(line, lineNum) {
    var newLine = "";
    var curCol = 0;

    var findIndex = nextWriteFindIndex(lineNum);
    while (findIndex >= 0) {
        var col = findLineCols[findIndex * 2 + 1];
        var prefix = "";
        if (col > 0) {
            prefix = line.substring(curCol, col);
        }
        var selected = line.substr(col, findString.length);
        var cssClass = "found";
        if (findIndex == curFindIndex) {
            cssClass = "selected";
        }

        newLine += prefix + "<span class='" + cssClass + "'>" +
                   selected + "</span>";

        curCol = col + findString.length;
        curWriteFindIndex++;
        findIndex = nextWriteFindIndex(lineNum);
    }

    return newLine + line.substring(curCol);
}

function nextWriteFindIndex(lineNum) {
    while ((curWriteFindIndex * 2) < findLineCols.length &&
           findLineCols[curWriteFindIndex * 2] < lineNum) {
        curWriteFindIndex++;
    }
    if (findLineCols[curWriteFindIndex * 2] == lineNum) {
        return curWriteFindIndex;
    } else {
        return -1;
    }
}

function writeLogFileList() {
    var fileListElem = get("fileList");
    var fileList = fileListHeading

    for (var i = 0; i < files.length; i++) {
        var baseName = files[i].split("/");
        baseName = baseName[baseName.length - 1];
        var fileItem = fileListTemplate.replace(/--name--/g, baseName);
        fileItem = fileItem.replace(/--index--/g, i);
        fileItem = fileItem.replace(/--path--/g, files[i]);
        fileItem = fileItem.replace(/--color--/g, getLineColor(i, false));
        fileList += fileItem;
    }
    fileListElem.innerHTML = fileList;

}

function resetFileRowOrder() {
    if (disableReorder) {
        return;
    }
    for (var i = 0; i < files.length; i++) {
        fileRowElems[i] = get("file_row_" + i);
        fileRowElems[i].style["order"] = 1;
        fileRowElems[i].style["-webkit-order"] = 1;
    }
}

function moveUpFileRowOrder(logIndex) {
    if (disableReorder) {
        return;
    }
    fileRowElems[logIndex].style["order"] = 0;
    fileRowElems[logIndex].style["-webkit-order"] = 0;
}

function handleToggle() {
    for (var i = 0; i < files.length; i++) {
        toggle = get("toggle_" + i);
        toggles[i] = toggle.checked;
    }
    disableReorder = true;
    filterLines();
    disableReorder = false;
}

function filterLines() {
    var viewingLine = getViewingLine();
    var linesPerPage = getLinesPerPage();
    var skipFilters = (filterString == "" && excludeString == "");

    filtered = [];
    var filteredLine = 0;
    curPage = 0;
    for (var i = 0; i < lines.length; i += 2) {
        if (toggles[lines[i]]) {
            if (skipFilters || checkFilters(lines[i + 1])) {
                filtered.push(i);
                filteredLine++;
            }
        }
        if (linesPerPage > 0 && i == viewingLine) {
            curPage = Math.floor(filtered.length / linesPerPage);
        }
    }
    writeLogPage();
    updateStatus();
}

function checkFilters(line) {
    var lowerLine = line.toLowerCase();
    if (filterString != "" && lowerLine.indexOf(filterString) < 0) {
        return false;
    }
    if (excludeString != "" && lowerLine.indexOf(excludeString) >= 0) {
        return false;
    }

    return true;
}

function handleScroll() {
    var logsElem = get("logConsole");
    var linesPerPage = getLinesPerPage();

    var scrollThresh = parseInt(logsElem.clientHeight * 0.95);
    if (logsElem.scrollTop == 0 && curPage > 0) {
        curPage -= 1;
        writeLogPage();
        logsElem.scrollTop = scrollThresh;
        updateStatus();
    } else if (logsElem.scrollTop > scrollThresh && linesPerPage * (curPage + 2) < filtered.length) {
        curPage += 1;
        writeLogPage();
        logsElem.scrollTop = 1
        updateStatus();
    }
}

function updateStatus() {
    var linesPerPage = getLinesPerPage();
    numPages = getLastPage() + 1;

    var status = get("status");
    status.innerHTML = "Page: " + (curPage + 1) + "/" + numPages;
}

function gotoPage(which) {
    switch (which) {
        case "first":
            var logsElem = get("logConsole");
            curPage = 0;
            writeLogPage();
            logsElem.scrollTop = 0;
            updateStatus();
            break;
        case "bigup":
            var lastPage = getLastPage();
            curPage -= Math.max(Math.floor(lastPage / 10), 1);
            curPage = Math.max(curPage, 0);
            var logsElem = get("logConsole");
            writeLogPage();
            updateStatus();
            break;
        case "prev":
            if (curPage > 0) {
                var logsElem = get("logConsole");
                curPage -= 1;
                writeLogPage();
                updateStatus();
            }
            break;
        case "next":
            var linesPerPage = getLinesPerPage();
            var lastPage = getLastPage();
            if (curPage < lastPage) {
                curPage += 1;
                writeLogPage();
                updateStatus();
            }
            break;
        case "bigdown":
            var lastPage = getLastPage();
            curPage += Math.max(Math.floor(lastPage / 10), 1);
            curPage = Math.min(curPage, lastPage);
            var logsElem = get("logConsole");
            writeLogPage();
            updateStatus();
            break;
        case "last":
            curPage = 0;
            var linesPerPage = getLinesPerPage();
            if (linesPerPage > 0) {
                curPage = Math.floor(filtered.length / linesPerPage) - 1;
            }
            curPage = Math.max(curPage, 0);
            var logsElem = get("logConsole");
            writeLogPage();
            logsElem.scrollTop = 0;
            updateStatus();
            break;
        case "find":
            if (curFindIndex >= 0) {
                var oldCurPage = curPage;
                curPage = 0;
                var linesPerPage = getLinesPerPage();

                if (linesPerPage > 0) {
                    curPage = Math.floor(findLineCols[curFindIndex * 2] / linesPerPage);
                }
                curPage = Math.min(curPage, getLastPage());
                if (curPage != oldCurPage) {
                    var logsElem = get("logConsole");
                    logsElem.scrollTop = 0;
                }
                updateStatus();
            }
            writeLogPage();
            break;
    }
}

function handleFind() {
    var findElem = get("find");
    var value = findElem.value.toLowerCase();
    findString = value;
    if (!findAsyncInProgress) {
        findAsyncInProgress = true;
        resetFind();
        window.setTimeout(findAsync, 1);
    }
}

function resetFind() {
    findLineCols = [];
    findAsyncString = findString;
    findNumLines = filtered.length;
    findCurPage = curPage;
    curFindIndex = -1;
    findAsyncStartLine = curPage * getLinesPerPage();
    findAsyncLimit = filtered.length;
    findAsyncWrapped = false;
    findAsyncInsertPos = 0;
    linesSearched = 0;
    updateFindStatus();
}

function checkAndResetFind() {
   if (findString != findAsyncString || filtered.length != findNumLines) {
        resetFind();
    }
}

function updateFindStatus() {
    var status = get("findStatus");

    if (findAsyncInProgress || findLineCols.length > 0) {
        var findStatus = "Found " + (curFindIndex + 1) + "/" + (findLineCols.length / 2);

        if (findAsyncInProgress) {
            var linesPerPage = getLinesPerPage();
            var offset = linesPerPage * findCurPage;
            findStatus += " Finding... " + Math.floor(linesSearched * 100 / filtered.length) + "%";
        }

        status.innerHTML = findStatus;
    } else {
        if (findString == "") {
            status.innerHTML = "";
        } else {
            status.innerHTML = "Found None";
        }
    }
}

function findAsync() {

    checkAndResetFind();

    var linesPerPage = getLinesPerPage();
    var offset = linesPerPage * findCurPage;

    if (findAsyncString == "" || linesPerPage <= 0) {
        findAsyncInProgress = false;
        resetFind();
        writeLogPage();
        return;
    }

    updateFindStatus();

    for (var i = offset; i < offset + linesPerPage; i++) {
        if (i < findAsyncLimit) {
            var line = lines[filtered[i] + 1];
            var col = line.toLowerCase().indexOf(findAsyncString);
            linesSearched++;
            while (col >= 0) {
                if (findAsyncWrapped) {
                    findLineCols.splice(findAsyncInsertPos, 0, i);
                    findAsyncInsertPos++;
                    findLineCols.splice(findAsyncInsertPos, 0, col);
                    findAsyncInsertPos++;
                    if (curFindIndex >= 0) {
                        curFindIndex++;
                    }
                } else {
                    findLineCols.push(i);
                    findLineCols.push(col);
                }
                if (curFindIndex == -1) {
                    curFindIndex = (findLineCols.length / 2) - 1;
                    gotoPage("find");
                }
                col = line.toLowerCase().indexOf(findAsyncString,
                                                 col + findAsyncString.length);
            }
        }
    }
    findCurPage++;

    if (linesPerPage * findCurPage < findAsyncLimit) {
        window.setTimeout(findAsync, 1);
    } else if (findAsyncStartLine > 0) {
        findAsyncLimit = findAsyncStartLine;
        findAsyncStartLine = 0;
        findCurPage = 0;
        findAsyncInsertPos = 0;
        findAsyncWrapped = true;
        window.setTimeout(findAsync, 1);
    } else {
        if (curFindIndex == -1 && findLineCols.length > 0) {
            curFindIndex = 0;
        }
        findAsyncInProgress = false;
        updateFindStatus();
        gotoPage("find");
    }
}

function handleFindNext(inc) {
    var numFound = findLineCols.length / 2;
    if (numFound > 0 && curFindIndex >= 0) {
        curFindIndex += inc;
        if (curFindIndex < 0) {
            curFindIndex = numFound - 1;
        }
        if (curFindIndex >= numFound) {
            curFindIndex = 0;
        }
        updateFindStatus();
        gotoPage("find");
    }
}

function handleFilter() {
    var filterElem = get("filter");
    filterString = filterElem.value.toLowerCase();
    filterLines();
}

function handleExclude() {
    var excludeElem = get("exclude");
    excludeString = excludeElem.value.toLowerCase();
    filterLines();
}

function logHighlight(logIndex, hover) {

    var elements = document.querySelectorAll('.highlight_' + logIndex);
    for (var i = 0; i < elements.length; i++) {
        elements[i].style["background-color"] = getLineColor(logIndex, hover);
    }
}

function handleAllToggle(on) {

    for (var i = 0; i < files.length; i++) {
        toggles[i] = on;
    }

    var elements = document.querySelectorAll('.toggle');
    for (var i = 0; i < elements.length; i++) {
        elements[i].checked = on;
    }

    filterLines();
}

document.body.onload = function() {

    writeLogFileList();

    handleToggle();

    var logsElem = get("logConsole");
    logsElem.onscroll = handleScroll;

    document.body.onresize = writeLogPage;

}
</script>

"""

HTML_PAGE_FOOTERS = """
</body></html>
"""

tar_dirs_to_clean = list()


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

    clean_tar_dirs()

    timestamps = list()
    for i, log in enumerate(log_list):
        output("Detecting timestamps %d/%d ..." % (i + 1, len(log_list)))
        timestamps.append(detect_timestamps(log))

    output("Interleaving logs ...")
    combined = interleave_logs(log_list, timestamps)

    write_aggregate_log(log_files, combined, args.output_file)

    output("\nDone! View in web browser: " + args.output_file)


def find_log_files(paths, extensions):
    log_files = list()
    for path in paths:
        if os.path.isdir(path):
            for file_name in os.listdir(path):
                log_files.extend(find_log_files(
                    [os.path.join(path, file_name)], extensions))
        elif os.path.isfile(path):
            if path.endswith(".tar.gz") or path.endswith(".tgz"):
                log_files.extend(find_log_files_in_archive(path, extensions))
            else:
                for ext in extensions:
                    if path.endswith(ext):
                        log_files.append(path)
        elif os.path.islink(path):
            pass
        else:
            fatal_error("File or path not found: " +
                        path)

    return log_files


def find_log_files_in_archive(archive, extensions):
    output("Untar archive %s ..." % archive)
    tar = tarfile.open(archive)
    tar_dir = os.path.basename(archive).replace(".tgz", "").replace(".tar.gz",
                                                                    "")
    tar.extractall(tar_dir)
    tar_dirs_to_clean.append(tar_dir)
    return find_log_files([tar_dir], extensions)


def clean_tar_dirs():
    for tar_dir in tar_dirs_to_clean:
        output("Clean up archive %s ..." % tar_dir)
        shutil.rmtree(tar_dir)


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
        trimmed_line = line[0:MAX_LINE_LENGTH]
        timestamps.append(find_timestamp_in_line(trimmed_line))

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

        out_file.write("  0, ''];\n")

        out_file.write("files = [\n")
        for i, file_name in enumerate(log_files):
            out_file.write("'%s'" % file_name)
            if (i + 1) == len(log_files):
                out_file.write("\n")
            else:
                out_file.write(",\n")

        out_file.write("];\n")

        out_file.write(HTML_PAGE_SCRIPT_FOOTERS)
        out_file.write(HTML_PAGE_FOOTERS)


def format_log_line(log_line):
    if type(log_line) == int:
        return "%3d, " % log_line
    else:
        log_line = log_line[0:MAX_LINE_LENGTH]
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
