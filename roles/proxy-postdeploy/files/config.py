import sha
#license
vsd_license = "MDEyOHHM97ypxoABRnJlkfEukp74dsjj599F9ot/xPA/s+EYjB+z86DgVpeqs+DPeE4mgft8jtv27diccsTeSY4L5ZifuZR0ewn3DrPXwd7iE0/cnLG8EHm1wFfrXJwv2V+msaW3AAKBTH1E+xV2Upc1GoE9T089k4PNBDoCKgFRW+6qMDE2MjCBnzANBgkqhkiG9w0BAQEFAAOBjQAwgYkCgYEAkOyl181q5j2UHPUCD5nzBE5Gz0g3N1n8KAs6aEcNO7ueXvPUeiuNQ//ui0vE9otuo4AnLJkLKuxoIJmVjIKzxXlMEqsAK5zwOJpECOTEMxjZkyWcAujQg/ajVRcUAW+91UPz2nkzs1WkPhKs5ZjJTrksoEvmMt5fhNFXgLY2jCcCAwEAATA1OTh7InByb3ZpZGVyIjoiTnVhZ2UgTmV0d29ya3MgLSBBbGNhdGVsLUx1Y2VudCBJbmMiLCJwcm9kdWN0VmVyc2lvbiI6IjQuMCIsImxpY2Vuc2VJZCI6MSwibWFqb3JSZWxlYXNlIjoxLCJtaW5vclJlbGVhc2UiOjAsInVzZXJOYW1lIjoiYWRtaW4iLCJlbWFpbCI6ImFkbWluQGFsdS5jb20iLCJjb21wYW55IjoiQWxjYXRlbCBMdWNlbnQiLCJwaG9uZSI6Ijk5OS05OTktOTk5OSIsInN0cmVldCI6IjgwNSBFIE1pZGRsZWZpZWxkIFJkIiwiY2l0eSI6Ik1vdW50YWluIFZpZXciLCJzdGF0ZSI6IkNBIiwiemlwIjoiOTQwNDMiLCJjb3VudHJ5IjoiVVNBIiwiY3VzdG9tZXJLZXkiOiJmZWZlZmVmZS1mZWZlLWZlZmUtZmVmZSIsImFsbG93ZWRWTXNDb3VudCI6LTEsImFsbG93ZWROSUNzQ291bnQiOi0xLCJhbGxvd2VkVlJTc0NvdW50IjotMSwiYWxsb3dlZFZSU0dzQ291bnQiOi0xLCJhbGxvd2VkQ1BFc0NvdW50IjotMSwiaXNDbHVzdGVyTGljZW5zZSI6ZmFsc2UsImV4cGlyYXRpb25EYXRlIjoiMDMvMTYvMjAxNyIsImVuY3J5cHRpb25Nb2RlIjpmYWxzZSwibGljZW5zZUVudGl0aWVzIjpudWxsLCJhZGRpdGlvbmFsU3VwcG9ydGVkVmVyc2lvbnMiOm51bGx9"

#proxy user
pwd = sha.new('test').hexdigest()
user_params = {
                "firstName": "test",
		"lastName":  "test",
		"userName":  "proxy",
		"email":     "test@caso.com",
		"passowrd": pwd,
	      }

#nsg infra profile
vns_nsg = {
           "proxyDNSName": "proxy.example.com",
	   "useTwoFactor": False,
	   "upgradeAction": "NONE",
	   "name": "metro_vns"
	  }

#vsc infra profile
vns_vsc = {
           "name": "metro_vsc",
	   "firstController": "10.0.1.97",
	   "secondController": "10.0.1.98"
	  }

#NSGV ports
nsg_port = {
	    "ntwrk_port": {
			   "name": "port1_ntwrk",
			   "physicalName": "port1",
			   "portType": "NETWORK",
			  },
	    "access_port": {
			    "name": "port2_access",
			    "physicalName": "port2",
		            "portType": "ACCESS",
			    "VLANRange": "0-100"
			    }
	   }

#ISO parameters
iso_params = {
              "mediaType": "ISO",
              "associatedEntityType": "nsgatewaytemplate",
	      "NSGType": "ANY",
	      "associatedEntityID": "update"
	     }
