"""
Get other data out of the parsed data
"""

from csData import *
import numpy as np
import copy


def switchDeviceAndNode(data):
	"""
	Returns the same data but with node and device switched around. Handy when devices scan nodes.
	:param data:
	:return:
	"""

	data2 = {}
	data2["startTimestamp"] = data["startTimestamp"]
	data2["endTimestamp"] = data["endTimestamp"]
	data2["scans"] = {}
	scans = data["scans"]
	for nodeAddr in scans:
		for scan in scans[nodeAddr]:
			devAddr = scan["address"]
			#entry = copy.deepcopy(scan) # TODO: Do we really need a deep copy?
			entry = scan
			entry["address"] = nodeAddr # Switch devAddr with nodeAddr
			if (devAddr not in data2["scans"]):
				data2["scans"][devAddr] = [entry]
			else:
				data2["scans"][devAddr].append(entry)
	return data2



def getScansPerDevicePerNode(data):
	"""
	Returns data as scans per device per node.
	:param data: Data as returned by the parse functions
	:return: dict with:
		["scansPerDev"]:
			["<device address>"]:
				["<node address>"]:
					["time"]: timestamp
					["rssi"]: rssi
		["minRssi"]: minimal rssi of all scans
		["maxRssi"]: maximal rssi of all scans
	"""
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



def getScansPerNodePerDevice(data):
	"""
	Returns data as scans per node per device.
	:param data: Data as returned by the parse functions
	:return: dict with:
		["scansPerNode"]:
			["<node address>"]:
				["<device address>"]:
					["time"]: timestamp
					["rssi"]: rssi
		["minRssi"]: minimal rssi of all scans
		["maxRssi"]: maximal rssi of all scans
	"""
	scans = data["scans"]
	scansPerNode = {}
	minRssi = 127
	maxRssi = -127
	for nodeAddr in scans:
		for scan in scans[nodeAddr]:
			devAddr = scan["address"]
			timestamp = scan["time"]
			rssi = scan["rssi"]
			entry = {"time":timestamp, "rssi":rssi}
			if (nodeAddr not in scansPerNode):
				scansPerNode[nodeAddr] = {}

			if (devAddr not in scansPerNode[nodeAddr]):
				scansPerNode[nodeAddr][devAddr] = [entry]
			else:
				scansPerNode[nodeAddr][devAddr].append(entry)
			if (rssi > maxRssi):
				maxRssi = rssi
			if (rssi < minRssi):
				minRssi = rssi
	return {"scansPerNode":scansPerNode, "minRssi":minRssi, "maxRssi":maxRssi}



def getFrequencyPerDevicePerNode(data, windowSize, stepSize):
	"""
	Returns the number of time each device was scanned by each node, over time.
	:param data: Data as returned by the parse functions
	:param windowSize: Size of bucket window in seconds
	:param stepSize: Size of each time step in seconds
	:return dict with:
		["startTimes"]: [timestamp, timestamp, ...]
		["numScansPerDev"]:
			["<device address>"]:
				["<node address>"]: [rssi, rssi, ...]
	"""
	startTimestamp = data["startTimestamp"]
	endTimestamp = data["endTimestamp"]
	data2 = getScansPerDevicePerNode(data)
	scansPerDev = data2["scansPerDev"]
	startTimes = range(int(startTimestamp), int(endTimestamp)-windowSize+1, stepSize)
	numScans = {}
	for devAddr in scansPerDev:
		if (devAddr not in numScans):
			numScans[devAddr] = {}
		for tInd in xrange(1,len(startTimes)):
			for nodeAddr in scansPerDev[devAddr]:
				if (nodeAddr not in numScans[devAddr]):
					numScans[devAddr][nodeAddr] = [0.0]
				else:
					numScans[devAddr][nodeAddr].append(0.0)
				for scan in scansPerDev[devAddr][nodeAddr]:
					timestamp = scan["time"]
					if (startTimes[tInd] <= timestamp < startTimes[tInd]+windowSize):
						numScans[devAddr][nodeAddr][-1] += 1.0
				# Beacon 0, 5, 9 scan six times faster atm
				if (nodeAddr in ["E8:00:93:4E:7B:D9", "F5:A7:4B:49:8C:7D", "FE:04:85:F9:8F:E9"]):
					numScans[devAddr][nodeAddr][-1] /= 6.0
	return {"numScansPerDev":numScans, "startTimes": startTimes}



def getAverageRssiPerDevicePerNode(data, windowSize, stepSize):
	"""
	Returns the average rssi of each device with each node, over time.
	:param data: Data as returned by the parse functions
	:param windowSize: Size of averaging window in seconds
	:param stepSize: Size of each time step in seconds
	:return dict with:
		["startTimes"]: [timestamp, timestamp, ...]
		["avgRssiPerDev"]:
			["<device address>"]:
				["<node address>"]: [rssi, rssi, ...]
	"""
	startTimestamp = data["startTimestamp"]
	endTimestamp = data["endTimestamp"]
	data2 = getScansPerDevicePerNode(data)
	scansPerDev = data2["scansPerDev"]
	startTimes = range(int(startTimestamp), int(endTimestamp)-windowSize+1, stepSize)
	avgRssi = {}

	# TODO: this algorithm needs some performance improvements
	# Use cumulative sum to speed up the averaging
	for devAddr in scansPerDev:
		avgRssi[devAddr] = {}
		for nodeAddr in scansPerDev[devAddr]:
			avgRssi[devAddr][nodeAddr] = [-105.0]*(len(startTimes))


		# Assumes increasing timestamps!
		for nodeAddr in scansPerDev[devAddr]:
			startScanInd = 0
			for tInd in xrange(0,len(startTimes)):
				rssiSum = 0.0
				numScans = 0
				for scanInd in xrange(startScanInd, len(scansPerDev[devAddr][nodeAddr])):
					scan = scansPerDev[devAddr][nodeAddr][scanInd]
					timestamp = scan["time"]
					rssi = scan["rssi"]
					if (startTimes[tInd] <= timestamp < startTimes[tInd]+windowSize):
						rssiSum += rssi
						numScans += 1
					if (timestamp < startTimes[tInd]):
						startScanInd = scanInd
					if (timestamp > startTimes[tInd]+windowSize):
						break
				if (numScans > 0):
					avgRssi[devAddr][nodeAddr][tInd] = rssiSum / numScans

		# for tInd in xrange(0,len(startTimes)):
		# 	for nodeAddr in scansPerDev[devAddr]:
		# 		rssiSum = 0.0
		# 		numScans = 0
		# 		for scan in scansPerDev[devAddr][nodeAddr]:
		# 			timestamp = scan["time"]
		# 			rssi = scan["rssi"]
		# 			if (startTimes[tInd] <= timestamp < startTimes[tInd]+windowSize):
		# 				rssiSum += rssi
		# 				numScans += 1
		# 		if (numScans > 0):
		# 			avgRssi[devAddr][nodeAddr][tInd] = rssiSum / numScans
	return {"avgRssiPerDev":avgRssi, "startTimes": startTimes}



def getPathPerDevice2D(data, windowSize, stepSize, nodeLocations):
	"""
	Returns the estimated positions of each device, over time.
	:param data: Data as returned by the parse functions
	:param windowSize: Size of averaging window in seconds
	:param nodeLocations: position of each scanning node
	:return dict with:
		["startTimes"]: [timestamp, timestamp, ...]
		["pathPerDevice"]:
			["<device address>"]:
				["x"]: [float, float, float, ...]
				["y"]: [float, float, float, ...]
	"""
#	data2 = getFrequencyPerDevicePerNode(data, windowSize, stepSize)
#	numScans = data2["numScansPerDev"]
#	startTimes = data2["startTimes"]
	data3 = getAverageRssiPerDevicePerNode(data, windowSize, stepSize)
	avgRssi = data3["avgRssiPerDev"]
	startTimes = data3["startTimes"]

	paths = {}
	for dev in avgRssi:
		pathX = [0.0]*len(startTimes)
		pathY = [0.0]*len(startTimes)
		paths[dev] = {"x":pathX, "y":pathY}

		for tInd in xrange(0, len(startTimes)):
			weightSum = 0
			weights = {}
			for nodeAddr in avgRssi[dev]:
#				weights[nodeAddr] = numScans[dev][nodeAddr][tInd] - 0.0
				weights[nodeAddr] = (avgRssi[dev][nodeAddr][tInd] + 105.0)**2
				weightSum += weights[nodeAddr]

#			# If almost no node scanned the device, assume it stayed on the same location?
#			if (weightSum < 1.0 and tInd > 0):
#				pathX[tInd] = pathX[tInd-1]
#				pathY[tInd] = pathY[tInd-1]
			# If almost no node scanned the device, assume it's not here
			if (weightSum < 1.0):
				pathX[tInd] = float("NaN")
				pathY[tInd] = float("NaN")
				continue

			for nodeAddr in avgRssi[dev]:
				weight = weights[nodeAddr] / weightSum
				pathX[tInd] += weight * nodeLocations[nodeAddr]["x"]
				pathY[tInd] += weight * nodeLocations[nodeAddr]["y"]
	return {"pathPerDevice":paths, "startTimes":startTimes}


def getPosMultiLateration(rssiPerNode, rssiAtOneMeter, nodeList, signalLossParameter=4.0, weightGradient=0.1, dimensions=3):
	"""
	Use multi lateration to calculate a position.
	Multi lateration estimases the distance based on the RSSI and then uses weighted linear least squares to estimate the position.
	:param rssiPerNode: dict with RSSI per node address. rssiPerNode["<nodeAddress>"] = rssi
	:param rssiAtOneMeter: float
	:param nodeList: List of nodes with the position of each node.
	:param signalLossParameter: higher value means the signal drops faster per meter.
	:param weightGradient: higher value means that high RSSI values get an even larger weight. Set to 0.0 to give all RSSI values the same weight.
	:param dimensions:
	:return:
	"""

	# Make a list of node addresses that are both in rssiPerNode and nodeLocations
	nodeAddresses = rssiPerNode.keys()
	for nodeAddr in reversed(nodeAddresses):
		if nodeAddr not in nodeList:
			nodeAddresses.remove(nodeAddr)


	# Calculate distances and weight matrix
	distances = [0.0]*len(nodeAddresses)
	weights = np.eye(len(nodeAddresses)-1)
	for i in xrange(0, len(nodeAddresses)):
		nodeAddr = nodeAddresses[i]

		rssi = rssiPerNode[nodeAddr]

		# rssi = RSSI_0 - 10 * n * log_10(d / d_0) - X_g
		# rssi = RSSI_0 + 10 * n * log_10(d / d_0) + X_g

		# d = d_0 * 10^( (RSSI_0 - RSSI - Xg) / (10 * n) )

		# RSSI_0 is RSSI at d_0
		# n is multipath parameter:
		#    2: free space
		#    2.7-3.5: urban area
		#    1.6-1.8: line of sight
		#    4-6: obstruced in building
		#    2-3: office
		# X_g is fading parameter

		distances[i] = np.exp((rssiAtOneMeter - rssi) / signalLossParameter)
		# Weight increases exponentially with higher RSSI
		weights[i-1][i-1] = 2**((rssi+70.0) * weightGradient)

	# Calculate A and b such that: Ax=b
	A = np.empty([len(nodeAddresses)-1, dimensions])
	b = np.empty([len(nodeAddresses)-1, 1])

	firstNodeLocation = np.array(getLocation(nodeAddresses[0], nodeList)[0:dimensions])
	firstNodeLocTranspose = np.transpose(firstNodeLocation)
	for i in xrange(1,len(nodeAddresses)):
		nodeLoc = np.array(getLocation(nodeAddresses[i], nodeList)[0:dimensions])
		A[i-1] = (nodeLoc - firstNodeLocation)*2
		b[i-1] = np.dot(np.transpose(nodeLoc), nodeLoc) - np.dot(firstNodeLocTranspose, firstNodeLocation)
		b[i-1] += distances[0] - distances[i]

	# Use weighted linear least squares to solve
	Atranspose = np.transpose(A)
	AtWA = np.dot(np.dot(Atranspose, weights), A)
	AtWAInv = np.linalg.inv(AtWA)

	# pos = inv(At * W * A) * Xt * W * b
	pos = np.dot(np.dot(np.dot(AtWAInv, Atranspose), weights), b)

	return pos.reshape(dimensions)



def multiLateration(data, nodeLocations, windowSize, stepSize, rssiAtOneMeter, signalLossParameter, weightGradient, dimensions=3):
	"""

	:param data:
	:param nodeLocations:
	:param windowSize:
	:param stepSize:
	:param rssiAtOneMeter:
	:param signalLossParameter:
	:param weightGradient:
	:param dimensions:
	:return: dict with:
		["startTimes"]: [timestamp, timestamp, ...]
		["pathPerDevice"]:
			["<device address>"]:
				["x"]: [float, float, float, ...]
				["y"]: [float, float, float, ...]
				["z"]: [float, float, float, ...]
	"""

	startTimestamp = data["startTimestamp"]
	endTimestamp = data["endTimestamp"]
	data2 = getAverageRssiPerDevicePerNode(data, windowSize, stepSize)
	avgRssi = data2["avgRssiPerDev"]
	startTimes = data2["startTimes"]

	paths = {}

	for devAddr in avgRssi:
		pathX = [0.0]*len(startTimes)
		pathY = [0.0]*len(startTimes)
		pathZ = [0.0]*len(startTimes)
		paths[devAddr] = {"x":pathX, "y":pathY, "z":pathZ}
		for tInd in xrange(0, len(startTimes)):
			rssiPerNode = {}
			for nodeAddr in avgRssi[devAddr]:
				rssiPerNode[nodeAddr] = avgRssi[devAddr][nodeAddr][tInd]
			pos = getPosMultiLateration(rssiPerNode, rssiAtOneMeter, nodeLocations, signalLossParameter, weightGradient, dimensions)
			pathX[tInd] = pos[0]
			pathY[tInd] = pos[1]
			if (dimensions > 2):
				pathZ[tInd] = pos[2]
			else:
				pathZ[tInd] = 0.0

	return {"pathPerDevice":paths, "startTimes":startTimes}


if __name__ == '__main__':
	print "File not intended as main."