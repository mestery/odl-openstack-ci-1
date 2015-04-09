#!/usr/bin/env python

# ref
# https://jenkins.opendaylight.org/releng/view/ovsdb/job/ovsdb-daily-openstack-master/api/

## https://jenkins.opendaylight.org/releng/view/ovsdb/job/ovsdb-daily-openstack-master/api/json?pretty=true

import urllib2, json, sys, re

urlPrefix = 'https://jenkins.opendaylight.org/releng/view/'
urlJob = 'ovsdb/job/ovsdb-daily-openstack-master'
urlPostfix = '/api/json'
testResultPath = '/artifact/logs/testr_results.html'

# ======================================================================

buildsDict = {}
buildResultsDict = {}
debug = 1

def grabJson():
    global buildsDict

    response = urllib2.urlopen(urlPrefix + urlJob + urlPostfix)
    data = json.load(response)
    for build in data["builds"]:
        buildsDict[ build["number"] ] = build["url"]

# --

def grabTestResults():
    global buildsDict, buildResultsDict

    if debug > 0: print "Grabbing results from builds", 
    for build, url in buildsDict.items():
        if debug > 0: 
            print build,
            sys.stdout.flush()

        try:
            grabTestResult(build, url + testResultPath)
        except urllib2.HTTPError, err:
            if err.code == 404:
                if debug > 1: print "\nNote: build", build, "has no results artifact"
            else:
                raise
    if debug > 0: print "done."
        
# --

def grabTestResult(build, url):
    global buildResultsDict

    foundResult = False
    response = urllib2.urlopen(url)
    for lineBuffer in response:
        if debug > 9: print line
        lineMatch = re.search("Status.*(Pass (\d+) Failure (\d+) Skip (\d+))", lineBuffer)
        if lineMatch:
            if debug > 8: print build, lineMatch.group(1).rstrip()
            buildResultsDict[build] = lineMatch.group(1).rstrip()
            foundResult = True
            break
    if not foundResult:
        print "Trouble: could not find status line in build", url

# --

def showResults():
    global buildResultsDict

    for build in sorted(buildResultsDict.keys()):
        print "build %d:" % (build), buildResultsDict[build]

# --

if __name__ == '__main__':
    grabJson()
    grabTestResults()
    showResults()
    sys.exit(0)
    
