#!/bin/bash

if [ -z "$1" ]; then
   echo "BUNDLEVERSION not provided"
   exit 255
fi

URL_PREFIX=${ODLNEXUSPROXY:-https://nexus.opendaylight.org}
NEXUSPATH="${URL_PREFIX}/content/repositories/opendaylight.snapshot/org/opendaylight/integration/distribution-karaf"
BUNDLEVERSION=$1
shift

# Acquire the timestamp information from maven-metadata.xml
TFILE="/tmp/$(basename $0).$$.tmp"
trap "rm -f '$TFILE'" exit
wget --quiet -O ${TFILE}  ${NEXUSPATH}/${BUNDLEVERSION}/maven-metadata.xml

if [ $? -ne 0 ]; then
    echo "unable to find maven-metadata.xml in ${NEXUSPATH}/${BUNDLEVERSION}: $?"
    exit 254
fi

BUNDLE_TIMESTAMP=$(xpath $TFILE "//snapshotVersion[extension='zip'][1]/value/text()" 2>/dev/null)
ODL_NAME="distribution-karaf-${BUNDLEVERSION}"
ODL_PKG="distribution-karaf-${BUNDLE_TIMESTAMP}.zip"
ODL_URL="${NEXUSPATH}/${BUNDLEVERSION}"

if [ "$1" == "-v" ]; then
    echo "Nexus timestamp is ${BUNDLE_TIMESTAMP}"
    echo "ODL_NAME=\"$ODL_NAME\""
    echo "ODL_PKG=\"$ODL_PKG\""
    echo "ODL_URL=\"$ODL_URL\""
    echo ""
fi

echo "${NEXUSPATH}/${BUNDLEVERSION}/${ODL_PKG}"

