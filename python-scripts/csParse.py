import re
import json
import time
import datetime

"""
Parses a log file and returns the parsed data.
:param filename: filename of the log.
:param ownAddress: (optional) address of the recording device if its measurements should be included.
:return:
data["scans"]
	scans["node address"] = [entry, entry, ...]
		entry["time"] = timestamp
		entry["address"] = address of scanned device
		entry["rssi"] = rssi
		entry["occurances"] = occurances (optional)
data["startTimestamp"] = first seen timestamp
data["endTimestamp"] = last seen timestamp
"""


def parseMinicom(filename, ownAddress=None):
	scanning = False
	logfile = open(filename, "r")

	# Search for something like:
	# [2015-12-24 11:23:16] [cs_MeshControl.cpp             : 68   ] Device D0 E8 42 71 C2 5D scanned these devices:
	startPattern = re.compile("\\[([0-9 \\-:]+)\\] .* Device ([0-9A-F ]+) scanned these devices:")

	# Search for something like:
	# [2015-12-24 11:23:16] [cs_MeshControl.cpp             : 79   ] 2: [C4 D0 90 6F 53 4B]   rssi:  -51    occ:  10
	scanPattern = re.compile("\\[([0-9 \\-:]+)\\] .* [0-9]+: \\[([0-9A-F ]+)\\]\\s+rssi:\\s+(-?[0-9]+)\\s+occ:\\s+([0-9]+)")

	# Search for something like:
	# [2016-02-24 10:50:35] Advertisement from: [EF 36 60 78 1F 1D], rssi: -74
	ownPattern = re.compile("\\[([0-9 \\-:]+)\\] .* Advertisement from:\\s+\\[([0-9A-F ]+)\\],\\s+rssi:\\s+(-?[0-9]+)")

	# scans: map with:
	#	scans["node address"] = [entry, entry, ...]
	#		entry["time"] = timestamp
	#		entry["address"] = address
	#		entry["rssi"] = rssi
	#		entry["occurances"] = occurances
	#	scans["startTimestamp"] = first seen timestamp
	#	scans["endTimestamp"] = last seen timestamp

	nodes = []
	scans = {}
	data = {"scans" : scans}

	if (ownAddress is not None):
		nodes.append(ownAddress)
#		print ownAddress

	startFound = False
	startTimestamp = -1
	endTimestamp = -1
	address = ""
	for line in logfile:
		matches = startPattern.findall(line)
		if len(matches):
			timestamp = time.mktime(datetime.datetime.strptime(matches[0][0], "%Y-%m-%d %H:%M:%S").timetuple())
			if (startTimestamp < 0):
				startTimestamp = timestamp
			address = matches[0][1].replace(" ", ":")
			if (address not in nodes):
				nodes.append(address)

			startFound = True
#			print matches

		if (startFound):
			matches = scanPattern.findall(line)
			if len(matches):
#				startFound = False
				timestamp = time.mktime(datetime.datetime.strptime(matches[0][0], "%Y-%m-%d %H:%M:%S").timetuple())
				endTimestamp = timestamp
				entry = {"time":timestamp, "address":(matches[0][1]).replace(" ", ":"), "rssi":matches[0][2], "occurances":matches[0][3]}
				if (address not in scans):
					scans[address] = [entry]
				else:
					scans[address].append(entry)
#				print matches

		if(ownAddress is not None):
			matches = ownPattern.findall(line)
			if len(matches):
				try:
					timestamp = time.mktime(datetime.datetime.strptime(matches[0][0], "%Y-%m-%d %H:%M:%S").timetuple())
				except:
					print "Error parsing timestamp '{}'!".format(line)
					continue
				if (startTimestamp < 0):
					startTimestamp = timestamp
				endTimestamp = timestamp
				entry = {"time":timestamp, "address":(matches[0][1]).replace(" ", ":"), "rssi":matches[0][2], "occurances":"1"}
				if (ownAddress not in scans):
					scans[ownAddress] = [entry]
				else:
					scans[ownAddress].append(entry)

	logfile.close()

	data["startTimestamp"] = startTimestamp
	data["endTimestamp"] = endTimestamp
	return data




def parseHubData(filename):
	logfile = open(filename, "r")
	scans = {}
	data = {"scans" : scans}
	startTimestamp = -1
	endTimestamp = -1
	for line in logfile:
		try:
			jscan = json.loads(line)
		except:
			print "json error at line:"
			print line
			exit()

		timestamp = time.mktime(datetime.datetime.strptime(jscan["timestamp"], "%Y-%m-%dT%H:%M:%S").timetuple())
		if (startTimestamp < 0):
			startTimestamp = timestamp
		endTimestamp = timestamp
		scannedDevices = jscan["scannedDevices"]
#		nodeAddress = "00:00:00:00:00:00"
		nodeAddress = jscan["source_address"]

		for dev in scannedDevices:

			scannedAddress = dev["address"]
			rssi = dev["rssi"]
			entry = {"time":timestamp, "address":scannedAddress, "rssi":rssi}
			if (nodeAddress not in data["scans"]):
				data["scans"][nodeAddress] = [entry]
			else:
				data["scans"][nodeAddress].append(entry)
	logfile.close()
	data["startTimestamp"] = startTimestamp
	data["endTimestamp"] = endTimestamp
	for node in scans.keys():
		print node

	return data


def parseRssiTest(filename):
	logfile = open(filename, "r")
	scans = {}
	data = {"scans" : scans}
	startTimestamp = -1
	endTimestamp = -1

	nodeAddress = "00:00:00:00:00:00"
	scans[nodeAddress] = []

	for line in logfile:
		items = line.rstrip().split(",")
		if (len(items) is not 3):
			continue

		timestamp = time.mktime(datetime.datetime.strptime(items[0], "%Y-%m-%dT%H:%M:%S").timetuple())
		address = items[1]
		rssi = items[2]
		entry = {"time":timestamp, "address":address, "rssi":rssi}
		scans[nodeAddress].append(entry)

		if (startTimestamp < 0):
			startTimestamp = timestamp
		endTimestamp = timestamp
	logfile.close()
	data["startTimestamp"] = startTimestamp
	data["endTimestamp"] = endTimestamp
	return data


if __name__ == '__main__':
	print "File not intended as main."