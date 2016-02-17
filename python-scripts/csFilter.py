"""
Filter data
Set remove to False to keep only matching items
Set remove to True to remove all matching items
"""


def filterDevAddresses(data, addresses, remove=False):
	scans = data["scans"]
	for addr in scans:
		for i in range(len(scans[addr])-1, -1,-1):
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
		for i in range(len(scans[addr])-1, -1,-1):
			scan = scans[addr][i]
			dev = scan["address"]
			if (numTimesScanned[dev] < minNumTimesScanned and not remove):
				scans[addr].pop(i)
			if (numTimesScanned[dev] >= minNumTimesScanned and remove):
				scans[addr].pop(i)
	return data


if __name__ == '__main__':
	print "File not intended as main."