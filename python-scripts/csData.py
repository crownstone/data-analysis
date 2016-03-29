def getName(address, nodeList=None):
	name = address
	if (nodeList):
		if (address in nodeList):
			name = nodeList[address]["name"]
	for devList in devLists:
		if (address in devList):
			name = devList[address]["name"]
			break
	return name


def getLocation(address, nodeList=None):
	location = [0.0, 0.0, 0.0]
	if (nodeList):
		if (address in nodeList):
			location[0] = nodeList[address]["x"]
			location[1] = nodeList[address]["y"]
			location[2] = nodeList[address]["z"]
	else:
		for devList in devLists:
			if (address in devList):
				location[0] = devList[address]["x"]
				location[1] = devList[address]["y"]
				location[2] = devList[address]["z"]
				break
	return location

jawBones = {
	"C5:4F:A0:00:20:A6":{"name":"jawbone 1"},
	"D6:49:EB:45:48:9B":{"name":"jawbone 2"},
	"D3:41:EE:0F:5F:DC":{"name":"jawbone 3"},
	"EE:E4:04:45:35:1C":{"name":"jawbone 4"},
	"D9:30:DD:8B:08:07":{"name":"jawbone 5"},
	"EF:5B:87:42:7A:A8":{"name":"jawbone 6"},
	"EC:9B:F8:75:5E:BA":{"name":"jawbone 7"},
	"F6:1F:00:EE:76:F2":{"name":"jawbone 8"},
	"D8:81:E2:53:8A:7A":{"name":"jawbone 9"},
	"C7:3D:B1:AB:43:8D":{"name":"jawbone 10"},
	"C9:B1:1F:DD:9F:FF":{"name":"jawbone 11"},
	"CB:18:6F:55:04:4C":{"name":"jawbone 12"},
	"DE:3F:87:54:32:EF":{"name":"jawbone 13"},
	"E7:6E:56:4D:B0:12":{"name":"jawbone 14"},
	"F2:E4:3A:F3:EB:63":{"name":"jawbone 15"},
	"F4:A9:86:17:16:81":{"name":"jawbone 16"},
	"EE:F9:B5:A5:26:6F":{"name":"jawbone 17"},
	"D2:40:6A:F8:ED:1B":{"name":"jawbone 18"},
	"ED:EC:18:BF:BB:22":{"name":"jawbone 19"},
	"D6:F4:3D:F9:41:7E":{"name":"jawbone 20"},
	"F8:D8:C1:27:DE:A0":{"name":"jawbone 21"},
	"EC:5C:CC:F6:CF:B6":{"name":"jawbone 22"},
	"DD:87:41:12:D2:61":{"name":"jawbone 23"},
	"E9:7A:E6:D7:60:12":{"name":"jawbone 24"},
	"FE:AD:80:17:81:32":{"name":"jawbone 25"},
	"C3:A2:18:F9:FC:D9":{"name":"jawbone 26"},
	"F1:F2:5A:C5:B3:86":{"name":"jawbone 27"},
	"D1:29:15:DF:17:CD":{"name":"jawbone 28"},
	"F6:5F:FC:B5:AC:4A":{"name":"jawbone 29"},
	"D4:56:1C:38:30:D5":{"name":"jawbone 30"},
	"DF:17:E6:41:65:83":{"name":"jawbone 31"},
	"E5:A9:B2:CA:7B:7F":{"name":"jawbone 32"},
	"D8:07:BC:E7:75:03":{"name":"jawbone 33"},
	"DA:BD:B2:3A:CF:A8":{"name":"jawbone 34"},
	"D2:E3:0B:F6:F1:21":{"name":"jawbone 35"},
	"E5:8A:16:7D:83:B3":{"name":"jawbone 36"},
	"ED:8B:F9:3B:0E:B6":{"name":"jawbone 37"},
	"D8:9D:6E:77:2D:A8":{"name":"jawbone 38"},
	"CE:F1:97:31:DB:51":{"name":"jawbone 39"},
	"EF:59:29:1B:D3:91":{"name":"jawbone 40"},
	"CC:C5:87:95:5B:18":{"name":"jawbone 41"},
	"CB:44:67:84:81:F2":{"name":"jawbone 42"},
	"D7:86:64:1E:EE:9D":{"name":"jawbone 43"},
	"CD:A0:F7:6A:D2:82":{"name":"jawbone 44"},
	"D6:85:E3:9E:C5:1A":{"name":"jawbone 45"},
	"D6:20:51:29:D8:69":{"name":"jawbone 46"},
	"C1:97:6F:DC:EE:24":{"name":"jawbone X 1"},
	"C9:D5:C2:7D:D8:19":{"name":"jawbone X 2"},
	"CD:0E:C0:35:37:55":{"name":"jawbone X 3"},
}


beacons = {
	"F8:27:73:28:DA:FE":{"name":"hans",                         "x":407, "y":1240, "z":733+15},
	"F1:C1:B8:AC:03:CD":{"name":"chloe",                        "x":252, "y":253,  "z":1108+222},
	"E1:89:95:C1:06:04":{"name":"meeting",                      "x":0,   "y":955,  "z":733+15},
	"DB:26:1F:D9:FA:5E":{"name":"old office chloe",             "x":0,   "y":1123, "z":1108+10},
	"F0:20:A1:2C:57:D4":{"name":"hallway 0",                    "x":0,   "y":690,  "z":733+15},
	"C9:92:1A:78:F4:81":{"name":"trash room", "x":0, "y":0, "z":0},
	"CF:5E:84:EF:00:91":{"name":"lunch room", "x":0, "y":0, "z":0},
	"ED:F5:F8:E3:6A:F6":{"name":"kitchen",                      "x":820, "y":1098, "z":330+10},
	"EB:4D:30:14:6D:C1":{"name":"server room", "x":0, "y":0, "z":0},
	"F4:A2:89:23:53:92":{"name":"basement",                     "x":820, "y":898,  "z":330+10},
	"EB:82:34:DA:EE:0B":{"name":"balcony",                      "x":0,   "y":532,  "z":1108+10},
	"ED:AF:F3:7E:E1:47":{"name":"jan geert",                    "x":820, "y":816,  "z":1108+10},
	"C6:27:A8:D7:D4:C7":{"name":"allert",                       "x":482, "y":250,  "z":1108+149},
	"E0:31:D7:C5:CA:FF":{"name":"hallway 1",                    "x":820, "y":64,   "z":733+15},
	"D7:59:D6:BD:2A:5A":{"name":"dobots software", "x":0, "y":0, "z":0},
	"DE:41:8E:2F:58:85":{"name":"interns",                      "x":420, "y":573,  "z":330+148},
	"D7:D5:51:82:49:43":{"name":"peet",                         "x":575, "y":300,  "z":733+131},
	"FD:CB:99:58:0B:88":{"name":"hallway 2",                    "x":0,   "y":267,  "z":330+10},
	"EF:36:60:78:1F:1D":{"name":"dobots hardware", "x":0, "y":0, "z":0},
	"E8:B7:37:29:F4:77":{"name":"hallway 3", "x":0, "y":0, "z":0},
	"C5:25:3F:5E:92:6F":{"name":"small multi purpose room", "x":0, "y":0, "z":0},
	"EA:A6:ED:8A:13:8E":{"name":"billiard table", "x":0, "y":0, "z":0},
	"C5:71:64:3A:15:74":{"name":"proto table",                  "x":0,   "y":1002, "z":330+10},
	"D5:6B:B8:B4:39:C0":{"name":"LowBeacon 6",                  "x":0,   "y":618,  "z":330+10},

	"DC:1A:5A:AF:1A:44":{"name":"32k hans",                     "x":383, "y":1240, "z":330+10},
	"C6:A0:0C:5A:C8:C6":{"name":"32k chloe",                    "x":400, "y":141,  "z":330+142},
	"D4:0B:9E:30:B2:73":{"name":"32k meeting", "x":0, "y":0, "z":0},
	"CC:02:60:7A:83:46":{"name":"32k old office chloe",         "x":820, "y":1148, "z":1108+10},
	"D5:A7:34:EC:72:90":{"name":"32k hallway 0",                "x":420, "y":626,  "z":733+143},
	"DB:E3:E7:9B:60:81":{"name":"32k trash room", "x":0, "y":0, "z":0},
	"C0:82:3E:B9:F5:91":{"name":"32k server room",              "x":0,   "y":266,  "z":733+15},
	"D7:BE:C6:21:71:F2":{"name":"32k basement", "x":0, "y":0, "z":0},
	"EB:C9:C2:58:52:C4":{"name":"32k balcony",                  "x":416, "y":522,  "z":1108+145},
	"C2:92:09:5F:04:78":{"name":"32k jan geert",                "x":619, "y":1240, "z":733+15},
	"EF:79:08:EF:50:AC":{"name":"32k dobots hardware", "x":0, "y":0, "z":0},
	"E8:C5:AE:A7:6B:A9":{"name":"32k small multi purpose room", "x":0,   "y":822,  "z":1108+10},

	"EC:9C:70:56:9F:90":{"name":"32k", "x":0, "y":0, "z":0},
}

beaconsCbre = {
	"E8:00:93:4E:7B:D9":{"name":"32k beacon 0",  "x":439.0, "y":255.0, "z":0.0},
	"C6:B1:9A:0A:25:E0":{"name":"32k beacon 1",  "x":439.0, "y":334.0, "z":0.0},
	"EA:64:68:47:B8:EE":{"name":"32k beacon 2",  "x":439.0, "y":465.0, "z":0.0},
	"E8:DF:9A:90:54:6C":{"name":"32k beacon 3",  "x":439.0, "y":596.0, "z":0.0},
	"C4:D9:1C:34:16:09":{"name":"32k beacon 4",  "x":439.0, "y":752.0, "z":0.0},
	"F5:A7:4B:49:8C:7D":{"name":"32k beacon 5",  "x":861.0, "y":727.0, "z":0.0},
	"C0:6E:12:A4:6B:06":{"name":"32k beacon 6",  "x":861.0, "y":607.0, "z":0.0},
	"FA:23:55:F1:04:0E":{"name":"32k beacon 7",  "x":861.0, "y":490.0, "z":0.0},
	"F8:AC:E5:C4:E0:3E":{"name":"32k beacon 8",  "x":861.0, "y":401.0, "z":0.0},
	"FE:04:85:F9:8F:E9":{"name":"32k beacon 9",  "x":861.0, "y":308.0, "z":0.0},
	"F8:85:28:C1:4D:D2":{"name":"32k beacon 10", "x":861.0, "y":176.0, "z":0.0},
}

kontakts = {
	"E3:BF:7F:5F:59:0C":{"name":"kontakt 1"},
	"DF:8F:3F:A7:A0:BE":{"name":"kontakt 2"},
	"C0:B7:12:98:FD:7C":{"name":"kontakt 3"},
}

usbDongles = {
	"E6:EF:B4:98:25:4B":{"name":"usb14"},
	"E5:6F:56:1F:97:83":{"name":"usb54"},
	"C4:D0:90:6F:53:4B":{"name":"usb56"},
	"D0:E8:42:71:C2:5D":{"name":"usb76"},
	"D0:6D:AA:45:54:55":{"name":"usb91"},
}

devLists = [jawBones, beacons, beaconsCbre, kontakts, usbDongles]

if __name__ == '__main__':
	print "File not intended as main."