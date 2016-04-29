"""
Filter data
Set remove to False to keep only matching items
Set remove to True to remove all matching items
"""


def filterDevAddresses(data, addresses, remove=False):
	scans = data["scans"]
	for addr in scans:
		for i in xrange(len(scans[addr])-1, -1,-1):
			scan = scans[addr][i]
			dev = scan["address"]
			if (dev in addresses and remove):
				scans[addr].pop(i)
			if (dev not in addresses and not remove):
				scans[addr].pop(i)
	return data

def filterMostScannedDevices(data, minNumTimesScanned, remove=False):
	numTimesScanned = {}
	scans = data["scans"]
	for addr in scans:
		for scan in scans[addr]:
			dev = scan["address"]
			if (dev not in numTimesScanned):
				numTimesScanned[dev] = 1
			else:
				numTimesScanned[dev] += 1

#	numTimesScannedList = []
#	for dev in numTimesScanned:
#		numTimesScannedList.append({"address": dev, "num": numTimesScanned[dev]})
#	sortedList = sorted(numTimesScannedList, key=lambda dev: dev["num"], reverse=True)
#	sortedList = sorted(numTimesScannedList, key=operator.attrgetter("num"), reverse=True)

	for addr in scans:
		for i in xrange(len(scans[addr])-1, -1,-1):
			scan = scans[addr][i]
			dev = scan["address"]
			if (numTimesScanned[dev] < minNumTimesScanned and not remove):
				scans[addr].pop(i)
			if (numTimesScanned[dev] >= minNumTimesScanned and remove):
				scans[addr].pop(i)
	return data


def filterTime(data, start=None, end=None):
	startTimestamp = -1
	endTimestamp = -1
	filteredData = {
		"scans": {},
		"startTimestamp": startTimestamp,
		"endTimestamp": endTimestamp
	}
	for node in data["scans"]:
		for entry in data["scans"][node]:
			if start and entry["time"] < start:
				continue
			if end and entry["time"] > end:
				continue
			if entry["time"] < startTimestamp or startTimestamp == -1:
				startTimestamp = entry["time"]
			if entry["time"] > endTimestamp or endTimestamp == -1:
				endTimestamp = entry["time"]
			if node not in filteredData["scans"]:
				filteredData["scans"][node] = []
			filteredData["scans"][node].append(entry)
	filteredData["startTimestamp"] = startTimestamp
	filteredData["endTimestamp"] = endTimestamp
	return filteredData


def mergeData(*data):
	mergedData = {
		"scans": {},
		"startTimestamp": None,
		"endTimestamp": None,
	}
	for thisData in data:
		if not mergedData["startTimestamp"] or thisData["startTimestamp"] < mergedData["startTimestamp"]:
			mergedData["startTimestamp"] = thisData["startTimestamp"]
		if not mergedData["endTimestamp"] or thisData["endTimestamp"] > mergedData["endTimestamp"]:
			mergedData["endTimestamp"] = thisData["endTimestamp"]
		for node_address in thisData["scans"]:
			entries = thisData["scans"][node_address]
			if node_address not in mergedData["scans"]:
				mergedData["scans"][node_address] = []
			for entry in entries:
				mergedData["scans"][node_address].append(entry)
	return mergedData



if __name__ == '__main__':
	print "File not intended as main."