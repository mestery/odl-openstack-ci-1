#!/usr/bin/env python

import sys
import re

# Initialize defaults
debug = 1

class State(object):
    testsFailedCount = 0
    testsOkCount = 0
    testsFailed = set()
    testsOk = set()
    
    def __init__(self):
        pass
    def __repr__(self):
        return "testsFailedCount", self.testsFailedCount, \
            "testsOkCount", self.testsOkCount, \
            "testsFailed", self.testsFailed, \
            "testsOk", self.testsOk

state = State()

# ======================================================================

def printError(msg):
    sys.stderr.write(msg)

# ======================================================================

def parseInput(inputFile):
    global debug, state

    currTestPrefix = ''
    ignoringLines = False
    lookingForCloseParen = False
    lineCount = 0

    while 1:
        lineBuffer = inputFile.readline()
        if not lineBuffer: break
        lineCount += 1

        # look for marker that turns off ignore lines
        if ignoringLines:
            # Ran 258 tests in 296.899s
            lineMatch = re.search("^\s*[Rr]an\s+(\d+)\s+tests", lineBuffer)
            if lineMatch:
                ignoringLines = False
                if debug > 0: print "Stop ignoring lines at", lineCount
            else:
                continue
        else:
            # ======================
            lineMatch = re.search("^===========================", lineBuffer)
            if lineMatch:
                ignoringLines = True
                if debug > 0: print "Start ignoring lines at", lineCount
                continue

        # setUpClass (tempest.api.network.admin.test_lbaas_agent_scheduler
        # LBaaSAgentSchedulerTestJSON)                                      FAIL
        lineMatch = re.search("^([^\s]+)\s*\(([^\)]+)$", lineBuffer)
        if lineMatch:
            currTestPrefix = lineMatch.group(2).rstrip()
            lookingForCloseParen = True
            if debug > 0: 
                print "Found open parenthesis on", lineCount, "at", lineMatch.group(1), lineMatch.group(2).rstrip()
                ## print lineBuffer
            continue
        if lookingForCloseParen:
            lineMatch = re.search("^\s*(.+)\)\s*[fF][Aa][Ii][Ll]", lineBuffer)
            if lineMatch:
                testName = currTestPrefix + "." + lineMatch.group(1)
                # print "full testname", testName
                if testName not in state.testsFailed:
                    state.testsFailed.add(testName)
                    state.testsFailedCount += 1
                    if debug > 0: print "Added failed test", testName
            else:
                printError("Did not find expected match for parenthesis on %d %s" % (lineCount, currTestPrefix))
                print lineBuffer
            currTestPrefix = ''
            lookingForCloseParen = False
        
        lineMatch = re.search("^\s*(.+)\)\s*[fF][Aa][Ii][Ll]", lineBuffer)



        
# ======================================================================

def parseInput2(inputFile):
    global debug, fileNames

    while 1:
        lineBuffer = inputFile.readline()
        if not lineBuffer: break
        # print lineBuffer,
        lineMatch = re.search("^\s*---\s+([^\s@]+)[\s@]+", lineBuffer)
        if not lineMatch:
            lineMatch = re.search("^\s*\+\+\+\s+([^\s@]+)[\s@]+", lineBuffer)
        if lineMatch:
            currFileName = lineMatch.group(1)

            # trim off 'a/' and 'b/' that you will normally see in git output
            #
            if len(currFileName) > 2 and currFileName[1] == '/' and \
                    (currFileName[0] == 'a' or currFileName[0] == 'b'):
                currFileName = currFileName[2:]

            # ignore funny files that git can produce
            #
            if currFileName == '/dev/null':
                continue

            if not currFileName in fileNames:
                # print currFileName
                fileNames[currFileName] = 1
            else:
                fileNames[currFileName] += 1

# ======================================================================

if __name__ == '__main__':

    if len(sys.argv) == 1:
        parseInput(sys.stdin)
    else:
        for currInputName in sys.argv[1:]:
            try:
                # print currInputName
                currInputFile = open(currInputName, 'r')
                parseInput(currInputFile)
                currInputFile.close()
            except IOError, eStr:
                printError("Cannot open %s: %s\n" % (currInputName, eStr))
                sys.exit(255)

    

    sys.exit(0)

