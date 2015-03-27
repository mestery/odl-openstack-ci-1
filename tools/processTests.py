#!/usr/bin/env python

import sys
import re

# Initialize defaults
# debug = 10
debug = 0

class State(object):
    testsFailedCount = 0
    testsOkCount = 0
    testsFailed = {}
    testsOk = {}
    def __init__(self):
        pass
    def __repr__(self):
        return "[State testsFailedCount: %d" % (self.testsFailedCount) \
            + " testsOkCount: %d" % (self.testsOkCount) \
            + " testsFailed: %s" %  (self.testsFailed) \
            + " testsOk: %s" % (self.testsOk) \
            + "]"

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
                if debug > 8: print "Stop ignoring lines at", lineCount
            else:
                continue
        else:
            # ======================
            lineMatch = re.search("^===========================", lineBuffer)
            if lineMatch:
                ignoringLines = True
                if debug > 8: print "Start ignoring lines at", lineCount
                continue

        # setUpClass (tempest.api.network.admin.test_lbaas_agent_scheduler
        # LBaaSAgentSchedulerTestJSON)                                      FAIL
        lineMatch = re.search("^([^\s]+)\s*\(([^\)]+)$", lineBuffer)
        if lineMatch:
            currTestPrefix = lineMatch.group(2).rstrip()
            lookingForCloseParen = True
            if debug > 6: 
                print "Found open parenthesis on", lineCount, "at", lineMatch.group(1), lineMatch.group(2).rstrip()
                ## print lineBuffer
            continue
        if lookingForCloseParen:
            lineMatch = re.search("^\s*(.+)\)\s*[fF][Aa][Ii][Ll]", lineBuffer)
            if lineMatch:
                testName = currTestPrefix + "." + lineMatch.group(1)
                # print "full testname", testName
                currFailureCount = state.testsFailed.get(testName, 0)
                state.testsFailed[testName] = currFailureCount + 1
                state.testsFailedCount += 1
                if debug > 4: print "Added failed test", testName, "count", currFailureCount + 1
            else:
                printError("Did not find expected match for parenthesis on %d %s" % (lineCount, currTestPrefix))
                print lineBuffer
            currTestPrefix = ''
            lookingForCloseParen = False
        
        # tempest.api.network.admin.test_agent_management.AgentManagementTestJSON
        #      test_list_agent[gate,id-9c80f04d-11f3-44a4-8738-ed2f879b0ff4,smoke]OK  0.01
        #      test_update_port_with_security_group_and_extra_attributes[gate,id-58091b66-4ff4-4cc1-a549-05d60c7acd1a,smoke]  5.96
        lineMatch = re.search("^(tempest\..+)$", lineBuffer)
        if lineMatch:
            currTestPrefix = lineMatch.group(1)
            if debug > 5: print "Current test prefix is", currTestPrefix, "at line", lineCount
            continue
        lineMatch = re.search("^\s+(.+)\[.+\]\s*(OK\s)?\d+", lineBuffer)
        if lineMatch:
            testName = currTestPrefix + "." + lineMatch.group(1)
            currOkCount = state.testsOk.get(testName, 0)
            state.testsOk[testName] = currOkCount + 1
            state.testsOkCount += 1
            if debug > 4: print "Added passed test", testName, "count", currOkCount + 1, "at line", lineCount
            continue
        #    test_dhcp_stateful[id-4ab211a0-276f-4552-9070-51e27f58fecf]       FAIL
        lineMatch = re.search("^\s+(.+)\[.+\]\s*FAIL", lineBuffer)
        if lineMatch:
            testName = currTestPrefix + "." + lineMatch.group(1)
            currFailedCount = state.testsFailed.get(testName, 0)
            state.testsFailed[testName] = currFailedCount + 1
            state.testsFailedCount += 1
            if debug > 4: print "Added failed test", testName, "count", currFailedCount + 1, "at line", lineCount
            continue
        
# ======================================================================

def showReport():
    global debug, state

    allKeys = set(state.testsFailed.keys() + state.testsOk.keys())
    for currKey in sorted(allKeys):
        print currKey, "pass:%d" % state.testsOk.get(currKey, 0), "fail:%d" % state.testsFailed.get(currKey, 0)
    # print "%s" % state

# ======================================================================

if __name__ == '__main__':
    if len(sys.argv) == 1:
        ## parseInput(sys.stdin)
        printError("Usage: %s tempestRun.log [tempestRun2.log ... tempestRunN.log]\n" % (sys.argv[0]))
        sys.exit(1)
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
    showReport()
    sys.exit(0)

