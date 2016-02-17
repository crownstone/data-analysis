"""
Get other data out of the parsed data
"""

def getScansPerDevicePerNode(data):
	scans = data["scans"]
	scansPerDev = {}
	minRssi = 127
	maxRssi = -127
	for nodeAddr in scans:
		for scan in scans[nodeAddr]:
			devAddr = scan["address"]
			timestamp = scan["time"]
			rssi = scan["rssi"]
			entry = {"time":timestamp, "rssi":rssi}
			if (devAddr not in scansPerDev):
				scansPerDev[devAddr] = {}

			if (nodeAddr not in scansPerDev[devAddr]):
				scansPerDev[devAddr][nodeAddr] = [entry]
			else:
				scansPerDev[devAddr][nodeAddr].append(entry)
			if (rssi > maxRssi):
				maxRssi = rssi
			if (rssi < minRssi):
				minRssi = rssi
	return {"scansPerDev":scansPerDev, "minRssi":minRssi, "maxRssi":maxRssi}


def getFrequencyPerDevicePerNode(data, windowSize):
	startTimestamp = data["startTimestamp"]
	endTimestamp = data["endTimestamp"]
	data2 = getScansPerDevicePerNode(data)
	scansPerDev = data2["scansPerDev"]
	startTimes = range(int(startTimestamp), int(endTimestamp)+1, windowSize)
	numScans = {}
	for devAddr in scansPerDev:
		if (devAddr not in numScans):
			numScans[devAddr] = {}
		for tInd in range(1,len(startTimes)):
			for nodeAddr in scansPerDev[devAddr]:
				if (nodeAddr not in numScans[devAddr]):
					numScans[devAddr][nodeAddr] = [0.0]
				else:
					numScans[devAddr][nodeAddr].append(0.0)
				for scan in scansPerDev[devAddr][nodeAddr]:
					timestamp = scan["time"]
					rssi = scan["rssi"]
					if (startTimes[tInd-1] <= timestamp < startTimes[tInd]):
						numScans[devAddr][nodeAddr][-1] += 1.0
				# Beacon 0, 5, 9 scan six times faster atm
				if (nodeAddr in ["E8:00:93:4E:7B:D9", "F5:A7:4B:49:8C:7D", "FE:04:85:F9:8F:E9"]):
					numScans[devAddr][nodeAddr][-1] /= 6.0
	return {"numScansPerDev":numScans, "startTimes": startTimes}


def getAverageRssiPerDevicePerNode(data, windowSize):
	startTimestamp = data["startTimestamp"]
	endTimestamp = data["endTimestamp"]
	data2 = getScansPerDevicePerNode(data)
	scansPerDev = data2["scansPerDev"]
	startTimes = range(int(startTimestamp), int(endTimestamp)+1, windowSize)
	avgRssi = {}
	for devAddr in scansPerDev:
		avgRssi[devAddr] = {}
		for nodeAddr in scansPerDev[devAddr]:
			avgRssi[devAddr][nodeAddr] = [-105.0]*(len(startTimes)-1)
		for tInd in range(1,len(startTimes)):
			for nodeAddr in scansPerDev[devAddr]:
				rssiSum = 0.0
				numScans = 0
				for scan in scansPerDev[devAddr][nodeAddr]:
					timestamp = scan["time"]
					rssi = scan["rssi"]
					if (startTimes[tInd-1] <= timestamp < startTimes[tInd]):
						rssiSum += rssi
						numScans += 1
				if (numScans > 0):
					avgRssi[devAddr][nodeAddr][tInd-1] = rssiSum / numScans
	return {"avgRssiPerDev":avgRssi, "startTimes": startTimes}


if __name__ == '__main__':
	print "File not intended as main."