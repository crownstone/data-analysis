#!/usr/bin/python

import os
import sys
import pickle
from csParse import *
from csFilter import *
from csPlot import *

if __name__ == '__main__':
	fileName = sys.argv[1]
	fileBaseName, fileExtension = os.path.splitext(fileName)
	if (fileExtension == ".p"):
		with open(fileName, "r") as fp:
			logData = pickle.load(fp)
	else:
		logData = parseMinicom(fileName)
#		logData = parseHubData(fileName)
#		logData = parseRssiTest(fileName)
		with open(fileBaseName + ".p", "wb") as fp:
			pickle.dump(logData, fp, pickle.HIGHEST_PROTOCOL)

	# Filter out scanned beacons
	logData = filterDevAddresses(logData, beaconNames.keys(), False)

	# Only show devices that got scanned often
	logData = filterMostScannedDevices(logData, 10)

	plotScansAsDots(logData)

	plt.show()