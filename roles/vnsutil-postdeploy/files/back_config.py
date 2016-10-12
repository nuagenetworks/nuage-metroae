import sha
#license

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
