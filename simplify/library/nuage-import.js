#! node

// WANT_JSON

const ansible = require('ansible-node-module');

var msg = "";
var nesting2 = 0;

ansible.main((args) => {

    doImport( args.vsd, args.organization, args.config ) 
    // while (nesting>0);
	
	//while (nesting>0) {
		var waitTill = new Date(new Date().getTime() + 5 * 1000);
		while(waitTill > new Date()){}
	//}
	
    return {
      changed: true,
      failed:  false,
      msg: api.print_stats(),
      str: msg,
      rc: 0
    };
});

/**
	Node.js script to provision Nuage VSP from a JSON template file
	Author: Jeroen van Bemmel ( jeroen.van.bemmel@alcatel-lucent.com ), NPI team
	
	Install:
	  apt-get install node
	  npm install cjson
	  
	Run:
	  node ./import.js <VSD IP> <Organization name> <Nuage Template file (JSON format)>
**/

var doDelete = false;	// TODO implement
var apiErrors = 0;

// Check if Openstack env is setup
var useOS = process.env.OS_AUTH_URL;
// console.log( "Openstack environment configured: " + useOS + "( URL= " + process.env.OS_AUTH_URL + " )" )

// var api = require('./vsd-api.js')

// Remember name-2-id mapping
var name_2_id = {}
var name_2_parentId = {}

// var csp_id;

// Mapping of redirect targets to ESI
var rt_2_esi = {}

// Pending createRecursive calls waiting on resolution, indexed by <setname>.<name>
var to_resolve = {}

// Nuage object key fields, these are used in filter expressions
var key_fields = [ "name", "priority", "type", "actualType", "value", "userName", "nextHopIp", "address", "minAddress" ];

// Determines a unique key for the object. Most objects have 'name', but some are special ( VLANs, users, ACL entries, address ranges, static routes, DHCP options... )
function getKey(obj) {
	for ( var f in key_fields ) {
		var key = obj[ key_fields[f] ]
		if ( typeof key != "undefined" ) return key;
	}
	console.log( "Warning: No key defined for object: " + JSON.stringify(obj) )
	return undefined		// could use 'externalId' and generate a hash
}

function finishResolution(rs) {
  for ( var i=0; i<rs.waiting.length; ++i ) {
	var c = rs.waiting[i];
	// c.dont_postpone = true;		// avoid infinite loop? Can have more than 1 ID to resolve, sequentially
	console.log( "Finish resolving context=" + JSON.stringify(c) );
	if ( c.callback ) {
		c.callback();
	} else {
		console.error( "No callback provided!" );
		process.exit( -11 );
	}
  }
  delete to_resolve[ rs.key ]
}

// Postpone instantiation of domains and l2domains, and VM creation
var domains, l2domains, vms;

// Also postpone NSGateways and NSGRedundancyGroups, else VLAN conflict may arise
var nsgateways, nsgredundancygroups;

var enterprise_id;

function doExit() {
  // Check for pending failed resolutions, can point to config errors
  var exit = true;
  
  if ( nsgateways ) {
	 var gs = nsgateways;
	 nsgateways = null;
	 for ( var t in gs ) {
		createRecursive( createContext(enterprise_id,"nsgateways",gs[t]) );
	 }
  } else if ( nsgredundancygroups ) {
	 var gs = nsgredundancygroups;
	 nsgredundancygroups = null;
	 for ( var t in gs ) {
		createRecursive( createContext(enterprise_id,"nsgredundancygroups",gs[t]) );
	 }
  } else if ( domains || l2domains ) {
	 var d = domains, l2 = l2domains;
	 domains = null;
	 l2domains = null;
	 
	 // Build in some delay to give VSD a chance to finish domain instantiations...
	 if ( d ) {
		console.log( "Instantiating L3 domains..." );
		for ( var t in d ) {
			createRecursive( createContext(enterprise_id,"domains",d[t]) );
		}
	 }
	 if ( l2 ) {
		console.log( "Instantiating L2 domains..." );
		for ( var t in l2 ) {
			createRecursive( createContext(enterprise_id,"l2domains",l2[t]) );
		}
	 }
  } else if ( vms ) {
	 var v = vms;
	 vms = null;
	 createVMs( v );
  } else {
		var exitCode = 0;	// exit with error in case of API error responses
		for ( r in to_resolve ) {
		   msg += ( "Unable to resolve: '" + r + "' (check spelling, case sensitive!) recurse="+to_resolve[r].recurse )
		   ++exitCode;
		}
		
		msg += ( "doExit: exiting nesting=" + nesting + " API errors=" + apiErrors );
		// api.print_stats();
		// process.exit( exitCode );
  }
}

function incRef( rs ) {

  if (!rs) rs = {
	recurse : 0
  }
  ++rs.recurse	// increase counter
  // console.debug( "incRef: " + rs.key + " -> " + rs.recurse )
  return rs
}

function decRef( rs ) {
	if ( rs ) {
	   if (--rs.recurse <= 0) {
	     console.log( "ID for " + rs.key + " now resolvable" )
		 finishResolution(rs)
	   }
	   // console.debug( "decRef: " + rs.key + " -> " + rs.recurse )
	}
}

function putIDs( context, root, ids ) {

   // deal with case where resolution gets postponed
   for ( var t in ids ) {
	  var resolved = resolveStr( ids[t], context, function() { putIDs(context,root,ids); } )
	  if ( !resolved ) {
		 if ( context.dont_postpone ) process.exit(-7)
		 return;
	  }
	  ids[t] = resolved;
   }

   ++nesting;
   api.put( root, ids, function (body) {
	  // decRef(rs)
	  if ( --nesting==0 ) doExit()
   }, onError )
}

function createArrays(context,id)
{
	var template = context.template;
	for ( var p in template ) {
		var t = template[p]
	  
		if ( (t instanceof Array) ) {
			// Samples of Arrays of strings: User IDs, vport tags, hub domains, ...
			var root = '/' + context.set + '/' + id;
			if ( typeof(t[0]) == "string" ) {
				if ( p != "actualValues" ) {	// skip DHCP option values
					putIDs( context, root + '/' + p, t );
				}
			} else {
			  for ( var i in t ) {
			  			  
				var subContext = {
				  root : root,
				  set : p,
				  template : t[i],
				  count : context.count	// Value of '#count' passed down to children
				  // rs : incRef(context.rs)
			    }
				console.info( "createArrays: calling createRecursive root="+root );
		        createRecursive( subContext )
		      }
			}
		}
	}
}

function onResponse( context, obj ) {
	var id = obj.ID
	var key = getKey(obj)
	var template = context.template
	var vlanMapped = false
	console.log( "onResponse -> Object created/obtained in set "+context.set+" key='"+key+"' ID=" + id )

	if (typeof key != "undefined") {
		name_2_id[ context.set + "." + key ] = id;
		console.log( "Added mapping '" + context.set + "." + key + "' => " + id );
		
		// For VLANs, also add mapping for user mnemonic ( VLAN ID not unique for different ports )
		if ( obj.userMnemonic ) {
			console.log( "Adding mapping for VLAN using mnemonic: " + obj.userMnemonic )
			name_2_id[ context.set + "." + obj.userMnemonic ] = id;
			incRef( to_resolve[ context.set + "." + obj.userMnemonic ] );
			vlanMapped = true;
		} else if ( context.set=="vlans" ) {
			console.error( "Unable to map VLAN userMnemonic: " + JSON.stringify(obj) );
		}
	}
	
	// Check if any pending calls are now resolvable
	// Make sure object is fully constructed before resuming
	incRef( to_resolve[ context.set + "." + key ] )
	// incRef( context.rs )
	
	createArrays( context, id );
	
	// For L3 domains or L2 domains, import subnets into Openstack
	if ( useOS ) {
		if (context.set == "domains") {
			// Add some delay, as VSD takes time to instantiate the subnets, especially shared subnets
			++nesting;
			console.log( "Starting delayed creation of Openstack networks...nesting=" + nesting );
			setTimeout( function() { 
				createOpenstackSubnets( id, obj.name );
				if ( --nesting==0 ) doExit();
			}, params.delay ? params.delay : 3000 );
		} else if ( context.set == "l2domains" ) {
			createOpenstackSubnetForL2domain( id, obj.name );
		}
	}
	
	// After recursing, check if any pending createRecursive calls can now be resolved
	// decRef( context.rs )
	
	// Finally, check the parent ( if any )
	decRef( to_resolve[ context.set + "." + key ] );
	if (vlanMapped) decRef( to_resolve[ context.set + "." + obj.userMnemonic ] );
	
	return false;
}

var nesting = 0

// User specified 'parameters' array ( "$name" = "value" }
var params = {}

function resolveStr( val, context, callback )
{
	// Only modify strings
	if ( typeof(val) != "string" ) return val;

	// First resolve any ${param}, then check for ID resolution 
	val = val.replace( /\${[^}]+}/g, function (m) {
	
	   // remove '${...}'
	   var v = m.substring(2,m.length-1)
	
	   // TODO could support nesting
	   if ( v.indexOf("ESI:") === 0 ) {
	      var name = v.substring(4)
		  var lookup = rt_2_esi[ name ]
		  
		  // If not found, return v as "[ESI:....]"
		  v = lookup ? lookup : "[" + v + "]"
		  
	   } else if ( v.indexOf("#count") >= 0 ) {
		  v = eval( v.replace("#count", context.count ) );
	   } else if ( params[v] ) {
		  v = params[v]
	   } else if ( context.template[v] ) {
		  v = context.template[v]
	   } else {
		  console.error( "Parameter in string '" + val + "' undefined: " + m )
		  process.exit(1)
	   }
	   console.log( "Resolved: " + m + " => " + v );
	   return v;
	})

  var len, mapping;
  if ( val.indexOf("ID:") === 0 ) {
     len = 3;
	 mapping = name_2_id;
  } else if ( val.indexOf("[ESI:") >= 0 ) {
     var st = val.indexOf("[ESI:")
	 var en = val.indexOf(']',st)
     val = val.substring(st,en)
     len = 5;
	 mapping = rt_2_esi;
  } else if ( val.indexOf("parentID:") === 0 ) {
     len = 9;
	 mapping = name_2_parentId;
  } else if ( val.indexOf("enterpriseID:") === 0 ) {
     return enterprise_id;
  } else {
     return val; // updated string, may be unmodified
  }
	 
  var dot = val.indexOf('.')
  p_set = val.substring(len,dot)
  p_name = val.substring(dot+1)
   
  // If not found, wait for any parallel API calls
  var obj = p_set + "." + p_name
  var resolved = mapping[ obj ];
  if ( resolved ) { 
	  console.log( "Resolved " + val + " to " + resolved )
  } else if (!context.dont_postpone) {
   
	  // Put this here to distinguish redundancygroups versus single gateways
	  // template["ID.base"] = p_set
   
	  if ( to_resolve[ obj ] == null ) {
		to_resolve[ obj ] = {
		   "key" : obj,
		   "recurse" : 0,
		   "waiting" : []  // Array of context objects
		}
	  }
	  context.callback = callback;
	  to_resolve[ obj ].waiting.push( context )

	  // Support implicit lookups by name; trigger a GET
	  ++nesting;
	  api.get( "/" + p_set, "name == '" + p_name + "'", function (named_obj) {
		if (named_obj[0]) onResponse( { set : p_set }, named_obj[0] );
		if ( --nesting==0 ) doExit();
	  }, onError );
	  
	  console.log( "Resolution postponed for " + val )
  } else {
      console.warn( "Unable to resolve: " + obj + " but dont_postpone flag set!" );
  }
  return resolved	// resolved ID or null if postponed
}



// Resolve names to IDs or parameters where needed
function resolveVars( context, callback ) {
 // e.g. "ID:zonetemplates.web1"
 var instance = {}
 for ( var p in context.template ) {
    var t = context.template[p]
    if ( (t instanceof Array) && (typeof(t[0])==="string") ) {
	   console.warn( "Resolving array of strings ( vPorttags or user IDs )" )
	   var vals = []
	   for ( var i = 0; i < t.length; ++i ) {
	      var resolved = resolveStr( t[i], context, callback ) 
		  if (!resolved) return null
		  vals.push( resolved )
	   }
	   console.info( "Resolved array: " + JSON.stringify(vals) )
	   instance[p] = vals
	} else if ( typeof(t) === "string" && (t.length > 1) ) {
	   var resolved = resolveStr( t, context, callback )
	   if (!resolved) return null	// postpone, restart from scratch next time
	   instance[p] = resolved
	} else if (p[0]!="#") {
		instance[p] = t		// copy unmodified, excluding '#' properties like '#count'
	}
 }
 // instance["#resolved"] = true  // debug
 return instance
}

function zeropad(num, size) {
    var s = "000000000" + num;
    return s.substr(s.length-size);
}

function onError(err) {
	console.error( "Error response from API call: " + JSON.stringify(err) );
	++apiErrors;
	if ( --nesting==0 ) doExit()
}

function createMulti( context, count ) {
	var instance = resolveVars( context, function() { createMulti(context,count) } );
	if (!instance) {
		// More variables to resolve
		return;
	}

	console.log( "createMulti COUNT="+count+" context="+JSON.stringify(context) )
	
	++nesting
	if (context.basename && context.template.name) {
		instance.name = context.basename + count // zeropad(count,4)
	}
	api.post( context.root + '/' + context.set, instance, function (body) {
		  if (body.length>0) {
			var id = body[0].ID
			console.info( "POST: Object created in " + context.set + " ID=" + id )
			// instance["#count"] = count
			var resultContext = {
				root : context.root,
				set  : context.set, 
				template: instance,		// This one has the accurate #count and real name / resolved strings
				count: context.count
			}
			onResponse( resultContext, body[0] )
		  } else {
			console.error( "Empty response for create object at " + context.root + "/" + context.set + ":" + JSON.stringify(context.template) )
		  }
		  // decRef( context.rs )
		  if (count>1) {
		    // Update #count property
			// context.template["#count"] = count-1
			
			// Create new context object!
			var nextContext = {
				root 		: context.root,
				set  		: context.set, 
				template 	: context.template,
				basename 	: context.basename,
				count		: count-1
			}
			createMulti( nextContext, count-1 )
		  }
		  if ( --nesting==0 ) doExit()
	 }, onError )
}

function updateObject( context, id ) {
	var instance = resolveVars( context, function () { updateObject(context,id) } );
	if (instance) {
		var path = "/" + context.set + "/" + id;
		++nesting;
		api.put( path, instance, function (res) {
			console.log( "Updated object: " + path + "=>" + JSON.stringify(res) );
			if (res[0]) {
				// Need to call onResponse e.g. to update VLAN userMnemonic mapping, and create children if any
				var resultContext = {
					root : context.root,
					set  : context.set, 
					template: instance,		// This one has the accurate #count and real name / resolved strings
					count: context.count
				}
				onResponse( resultContext, res[0] )
			}
			
			if ( --nesting==0 ) doExit()
		}, onError );
	}
}

async function createRecursive( context ) {
  // console.log( "createRecursive: context=" + JSON.stringify(context) )
  
  // Bulk testing feature: Allow '#count' parameter
  var template = context.template
  var basename;
  var count = 1

  var filter;
  
  // Allow user to specify dependencies in creation, not only for POST but also for GET
  if ( context.template.depends ) {
	 var r = resolveStr( context.template.depends, context, function() { createRecursive( context ) } );
	 if (!r) {
		console.log( "Postponing object creation due to dependency: " + context.template.depends );
		return;
	}
  }
  
  // Take count from parent, unless overridden at this level
  if ( template['#count'] ) {
		count = template['#count']
		basename = template.name + " "

		if (count>5000) {
			count = 5000
			console.log( "Limiting #count to #5000" )
		} else {
			console.log( "Auto-count value: " + count );
		}
		context.count = count	// override any current count
		
		// GET all created entities, such that we can verify the count
		filter = ""
  } else {
	 // Not all objects have a 'name' attribute, but most do
	 if ( template.name ) {
		filter = "name == '"+template.name+"'";
     } else if ( typeof template.type != "undefined" ) {		// DHCP options
		filter = "type == '"+template.type+"'";
	 } else if ( typeof template.actualType != "undefined" ) { // DHCP options, 3.2 API
		filter = "actualType == "+template.actualType;
	 } else if ( typeof template.priority != "undefined" ) {	// ACL entries have 'priority'
		filter = "priority == "+template.priority;
	 } else if ( typeof template.value != "undefined" ) {	// VLANs have value, userMnemonic not unique! DHCP options also have value, check 'type' first
		filter = "value == "+template.value
	 } else if ( template.userName ) {
		filter = "userName == '"+template.userName+"'"
	 } else if ( template.nextHopIp ) {	// static routes
	    // resolveStr only supports 1 parameter per string, need to resolve 1 here too!
		var nhIP = resolveStr( template.nextHopIp, context, function() { createRecursive(context) } );
		if (!nhIP) return;
		filter = "nextHopIp == '"+nhIP+"' and address == '" + template.address +"'"
	 } else if ( template.address ) {	// ??
		filter = "address == '"+template.address+"'"
	 } else if ( template.minAddress ) {	// address ranges
		filter = "minAddress == '"+template.minAddress+"'"
	 } else {
		console.log( "Warning: Unable to filter object: " + JSON.stringify(template) )
		filter = ""
	 }
	 
	 // Resolve any variables in the filter? Should already be resolved...
	 if (filter && filter!="") {
		filter = resolveStr( filter, context, function() { createRecursive(context) } );
		if (!filter) return;
	 }
  }
  
  ++nesting;
  
  await api.get( context.root + '/' + context.set, filter, function (objs) {
	  if ( objs && (objs.length>0) ) {
		
		console.info( "RESULT: " + JSON.stringify(objs) );

		// If there are multiple, add all their IDs to the name mapping
		if ( count>1 ) {
		
			// Check that all objects are created, in case '#count' changes between runs
			if ( count != objs.length ) {
				console.log( "Detected mismatch between #count and number of objects: " + count + "!=" + objs.length )
				
				// If some are missing, recreate them ( starting from highest count )
				if ( count > objs.length ) {
					context.basename = basename
					createMulti( context, count )
					if ( --nesting==0 ) doExit()
					return
				}
			}
		
			for ( var o = 0; o<objs.length-1; ++o ) {
				var obj = objs[o]
				var key = getKey( obj )
				if ( typeof key != "undefined" ) {
					// Use the resolved name
					name_2_id[ context.set + "." + key ] = obj.ID
					
					// For VLANs, also add mnemonic
					if ( obj.userMnemonic ) {
						name_2_id[ context.set + "." + obj.userMnemonic ] = obj.ID
					}
				} else {
					console.log( "Warning: unable to add ID mapping for object, no unique property" )
				}
			}
		} else {
		    var obj = objs[0]
			var id = obj.ID
			
			// New: For redirection targets, save the name-2-ESI mapping
			if ( obj.ESI ) {
			    console.log( "Saving ESI for Redirection Target " + obj.name + ":" + obj.ESI )
				rt_2_esi[ "redirectiontargets." + obj.name ]  = obj.ESI
			}
			
			// PUT to update minor changes to a single object, some of the vCenter APIs only accept PUT, not POST
			updateObject( context, id );
		}

		var is_leaf = onResponse( context, objs[count-1] )	// Pass the last object
		// decRef(context.rs)
		
		// Delete the last layer of child objects
		if ( doDelete && is_leaf ) {
			++nesting;
			api.del( '/' + context.set + '/' + objs[0].ID, 
				function (r2) {
					if ( --nesting==0 ) doExit()
				},
				function (e2) {
					if ( --nesting==0 ) doExit()
				})
		}
		
	  } else if (!doDelete) {
	  
		 console.log( "No match found for " + context.root + '/' + context.set + " with filter '" + filter + "'" )
	  
		 if ( context.set == "gateways" ) {
			console.error( "Gateway not found: " + filter + " or no permissions to use it - please check the gateway name in your script, and make sure this organization has access" );
			process.exit(-8)
		 } else {
			 // Doesn't exist yet - create it
			 context.basename = basename
			 createMulti( context, count )
		 }
	  }
	  if ( --nesting==0 ) doExit()
  }, onError )
}

function addOffset( addr, offset ) {
	var prefix = addr.lastIndexOf(".");
	return addr.substring(0,prefix+1) + (parseInt( addr.substring(prefix+1) ) + offset);
}

function createOSNet( subnet, address_ranges, domainName /* not set for L2 domains */ )
{
	console.log( "createOSNet domain="+domainName+" subnet=" + JSON.stringify(subnet) + " ranges=" + JSON.stringify(address_ranges) );
	
	// Support JSON parameters in description
	var json = ( subnet.description && subnet.description[0]=='{' ) ? JSON.parse( subnet.description ) : {}
	
	// Support VLAN-aware SRIOV VMs
	var sriov = "";
	
    if ( json.skip_Openstack ) {
	   console.log( "Openstack import skipped for subnet " + subnet.name );
	   return;
	}
	
	// Expected: Name of physical network, create the parent network. TODO: VLAN networks, which CIDR to use?
	if ( json.sriov && json.vlan ) {
		sriov = "--segments type=dict list=true provider:physical_network='"+json.sriov+"',provider:network type=flat provider:physical_network='',provider:network_type=vxlan"
	}
	
	var name = domainName ? domainName + " - " + subnet.name : subnet.name;  // must be unique
	var Netmask = require('netmask').Netmask
	
	// For unmanaged L2 Neutron requires a dummy CIDR
	var cidr = new Netmask( subnet.address ? subnet.address+"/"+subnet.netmask : "101.101.101.0/24" );
	var gw = domainName && subnet.gateway ? " --gateway " + subnet.gateway : ""
	
	// Prior to 3.2R4 DHCP had to be disabled for Shared Subnets. Still need to specify the correct CIDR though
	if ( subnet.associatedSharedNetworkResourceID || (subnet.address == null) ) {
		gw += " --enable_dhcp False";
	}

	var exec = require('child_process').exec, child
	++nesting
	var pools = ""
	if ( address_ranges ) {
		for ( var a in address_ranges ) {
			var range = address_ranges[a];
			// Provide a way to provision non-overlapping ranges for Openstack
			var extId = range['externalID'];
			if ( extId && extId.indexOf("openstack:") == 0 ) {
				var offset = parseInt( extId.substring(10) );	// skip 'openstack:' prefix
				console.log( "Adding Openstack address offset: " + offset );
				range.minAddress = addOffset( range.minAddress, offset );
				range.maxAddress = addOffset( range.maxAddress, offset );
			}
			pools += " --allocation-pool start="+range.minAddress+",end="+range.maxAddress;
		}
	}
	var neutron_cmd = '(neutron net-list -F name --format csv | grep -q \'"' + name + '"\' || neutron net-create "' + name + '" ' + sriov + ') && '
		  + 'neutron subnet-create "' + name + '" ' + cidr + ' --name "' + subnet.name + '"'
		  + gw + pools + ' --nuagenet ' + subnet.ID + ' --net-partition "' + enterprise + '"';
		  
	console.info( "About to execute Neutron command: '" + neutron_cmd + "'" );
		
	child = exec( neutron_cmd, { 'env' : process.env },
		function (error, stdout, stderr) {
			console.log('createOSNet stdout: ' + stdout);
			console.log('createOSNet stderr: ' + stderr);
			if (error !== null) {
			  console.log('exec error: ' + error);
			}
			
			// For dual-stack subnets, also create IPv6 subnet
			if ( subnet.IPType == "DUALSTACK" && subnet.IPv6Address && subnet.IPv6Gateway ) {
				neutron_cmd = 'neutron subnet-create "' + name + '" ' + subnet.IPv6Address + ' --name "' + subnet.name + '-v6" --gateway '
							  + subnet.IPv6Gateway + ' --ip-version 6 --disable-dhcp --nuagenet ' + subnet.ID + ' --net-partition "' + enterprise + '"';
				
				++nesting
				child = exec( neutron_cmd, { 'env' : process.env },
					function (error, stdout, stderr) {
						console.log('createOSNetv6 stdout: ' + stdout);
						console.log('createOSNetv6 stderr: ' + stderr);
						if (error !== null) {
						  console.log('exec error: ' + error);
						}
						if ( --nesting==0 ) doExit()
					}
				);
			}
			
			// TODO: For SRIOV networks with VLANs, create a network+subnet for each vlan			
			
			if ( --nesting==0 ) doExit()
		}
	)	
}

/**
 * Import subnets for a given domain into OpenStack
 */
function createOpenstackSubnets( domainId, domainName ) {
	// This lists all subnets globally, filter for enterprise / domain instances
	++nesting
	api.get( "/domains/" + domainId + "/subnets", "", function(body) {
	    if (body.length>0) {
		  console.info( "Creating Openstack subnets: count=" + body.length );
		  for ( var subnet = 0; subnet < body.length; ++subnet ) {
			// Need to capture body[subnet] as a function param, else callbacks will all use last value in for loop!
			createOpenstackSubnet( body[subnet], domainName );
		  }
		} else {
		  console.log( "No subnets found in domain: " + domainName );
		}
		if ( --nesting==0 ) doExit()
	}, onError )
}

function createOpenstackSubnet( subnet, domainName ) {
	++nesting;
	
	// For shared subnets, address ranges are under /sharednetworkresources
	var adrPath = subnet.associatedSharedNetworkResourceID
				? "/sharednetworkresources/" + subnet.associatedSharedNetworkResourceID
				: "/subnets/" + subnet.ID;
	
	api.get( adrPath + "/addressranges", "", function (adrRange) {
				
			// For shared networks, subnet.address = null but we need to specify the correct CIDR...
			// BUG workaround: For shared networks, lookup the 'address','netmask' and 'gateway' properties!
			if ( subnet.associatedSharedNetworkResourceID && (!subnet.address)) {
				++nesting;
				api.get( "/sharednetworkresources/" + subnet.associatedSharedNetworkResourceID, "", function (shared_subnets) {
					var shared_subnet = shared_subnets[0];
					console.log( "Adding missing address/netmask: " + shared_subnet.address + "/" + shared_subnet.netmask );
					subnet.address = shared_subnet.address;
					subnet.netmask = shared_subnet.netmask;
					console.log( "Adding missing gateway: " + shared_subnet.gateway );
					subnet.gateway = shared_subnet.gateway;
						
					createOSNet( subnet, adrRange, domainName );
					
					if ( --nesting==0 ) doExit()
				});
			} else {
				createOSNet( subnet, adrRange, domainName );
			}
			if ( --nesting==0 ) doExit()
	}, onError )
}

/**
 * Import subnet for a given L2 domain into OpenStack
 */
function createOpenstackSubnetForL2domain( domainId, domainName ) {
	// This lists all subnets globally, filter for enterprise / domain instances
	++nesting
	api.get( "/l2domains/" + domainId, "", function(l2doms) {
		  if ( l2doms[0] ) {
		    // console.info( JSON.stringify(res.body[0]) )
			++nesting;
			api.get( "/l2domains/" + domainId + "/addressranges", "", function (adrRanges) {
				createOSNet( l2doms[0], adrRanges )
				if ( --nesting==0 ) doExit()
			}, onError )
		  }
		  if ( --nesting==0 ) doExit()
	}, onError )
}

/**
 * Very similar to per-enterprise objects update, but this also does PUT to modify an existing object
 */
function updateGlobals( set, values ) {
	if (values.forEach) values.forEach( function(r) { updateGlobal(set,r) } );
}
	
async function updateGlobal( set, r ) {
	// console.log( "updateGlobal set="+set+" r="+JSON.stringify(r) );
	var u = resolveVars( { template: r }, function() { updateGlobal(set,r) } );
	if (!u) return;	// resolution pending

	incRef( to_resolve[ set + "." + getKey(u) ] );
	
	++nesting
	await api.get( "/" + set, u.name ? "name == '"+u.name+"'" : null, function(globals) {

		if ( globals[0] ) {
			var cur = globals[0]
			var key = getKey(cur);
			if (typeof key != "undefined") {
				name_2_id[ set + "." + key ] = cur.ID;
				
				// Keep track of parent ID too, such that we can place shared subnets in the same zone
				name_2_parentId[ set + "." + key ] = cur.parentID;
			}
			
			msg += ( "Updating shared resource..." )
			
			// Cannot modify 'underlay' flag once created
			delete u.underlay;
		
			++nesting

			var root = "/" + set + "/" + cur.ID; 
			api.put( root, u, function(body) {

				decRef( to_resolve[ set + "." + key ] );
	
				createArrays( { template : u, set : set, count : 0 }, cur.ID );
				if ( --nesting==0 ) console.log('done'); // doExit()
			}, onError )
		} else {
			msg += ( "Global resource not found: " + u.name )
			
			// Then create it
			++nesting
			api.post( "/" + set, u, function(body) {
				if (body[0]) {
					var cur = body[0]
					var key = getKey(cur);
					if (typeof key != "undefined") {
						name_2_id[ set + "." + key ] = cur.ID;
						
						// Keep track of parent ID too, such that we can place shared subnets in the same zone
						name_2_parentId[ set + "." + key ] = cur.parentID;
						
						decRef( to_resolve[ set + "." + key ] );
					}
					
					createArrays( { template : u, set : set, count : 0 }, cur.ID );
				}
				if ( --nesting==0 ) doExit()
			}, onError )
		}
		if ( --nesting==0 ) doExit()
	}, onError )
}

function createContext(enterprise_id,set,template) {
	return {
		root : enterprise_id ? "/enterprises/" + enterprise_id : "",	// csp will use '/'
		set : set, 
		template: template
	}
}

function createVMImages( images ) {
  for ( var i in images ) {
     var img = images[i];
	 
	 var exec = require('child_process').exec, child;

	 // May already exist
	 var format = img.url.indexOf(".iso") > 0 ? "iso" : "qcow2";
	 var cmd = 'glance image-show "'+img.name+'" || glance image-create --name "'+img.name+'" --disk-format '+format+' --container-format bare --is-public True --copy-from ' + img.url + ' ';
	 if ( img.args ) cmd += img.args;
	 
	 console.log( "Importing Glance image: " + cmd );
	 
	 ++nesting;
	 child = exec( cmd, { 'env' : process.env },
	  function (error, stdout, stderr) {
		console.info( "createVMImage: " + error + stdout + stderr );
		if ( --nesting==0 ) doExit()
	  }
	 );
   }
}

function createFlavors( flavors ) {
  for ( var i in flavors ) {
     var fl = flavors[i];
	 
	 var exec = require('child_process').exec, child;

	 // May already exist
	 var cmd = 'nova flavor-show "'+fl.name+'" || nova flavor-create "'+fl.name+'" auto ' + fl.memory + ' ' + fl.disk + ' ' + fl.vcpus;
	 
	 console.log( "Creating Flavor: " + cmd );
	 
	 ++nesting;
	 child = exec( cmd, { 'env' : process.env },
	  function (error, stdout, stderr) {
		console.info( "createFlavor: " + error + stdout + stderr );
		if ( --nesting==0 ) doExit()
	  }
	 );
   }
}

function createVMs( vms ) {
	 var vm_in = vms.shift();
	 var vm = resolveVars( { template: vm_in } );
	 var exec = require('child_process').exec, child;

	 var cmd = ""
	 var ports = ""
	 for ( var j in vm.vnics ) {
	    var n = vm.vnics[j];
		if (( !n.domain || !n.subnet ) && !n.l2domain ) {
			console.error( "Either 'domain' and 'subnet' or 'l2domain' need to be specified for each VM vNIC. Check " + vm.name );
			continue;
		}
		var os_net_name = (n.l2domain ? n.l2domain : n.domain + ' - ' + n.subnet );
		
		// Need to use Neutron to specify a specific MAC, else use Nova to make it easier to delete VMs
		if ( n.mac || n.policy_groups || n.redirect_targets ) {
		    // Set the device owner such that it can be auto-deleted? --device-owner network:dhcp
			var neutron_create_port = "neutron port-create -c id -f value --name '" + vm.name + "-nic" + j + "'"
			if (n.ip) neutron_create_port += " --fixed-ip ip_address=" + n.ip
			if (n.ipv6) neutron_create_port += " --fixed-ip ip_address=" + n.ipv6
			if (n.mac && n.mac.length==17) neutron_create_port += " --mac-address " + n.mac;
			
			neutron_create_port += ' "' + os_net_name + '" | tail -n1' // Skip "Created a new port"
			ports += "nic"+j+"=$("+neutron_create_port+");"
			cmd += ' --nic port-id=$nic' + j

			if (n.policy_groups) {
				ports += 'neutron port-update $nic'+j+' --nuage-policy-groups list=true ' + n.policy_groups + ';';
			}
			if (n.redirect_targets) {
				ports += 'neutron port-update $nic'+j+' --nuage-redirect-targets ' + n.redirect_targets + ';';
			}
			
		} else {
			cmd += ' --nic net-id=`neutron net-show "'+os_net_name+'" -F id -f value`'
			if ( n.ip ) cmd += ',v4-fixed-ip=' + n.ip;
		}
	 }
	 if (vm.zone) cmd += ' --availability-zone "' + vm.zone + '"';
	 if (vm["user-data"]) cmd += ' --config-drive true --user-data `echo "' + vm["user-data"] + '" > ${tmpfile:=$(mktemp)}; echo $tmpfile`';
	 cmd += ' "' + vm.name + '"';
	 
	 // May already exist
	 cmd = 'nova show "'+vm.name+'" || ' + ports + ' nova boot --image "'+vm.image+'" --flavor "'+vm.flavor+'" ' + cmd;
	 console.log( "Launching new VM: " + cmd );
	 
	 ++nesting;
	 child = exec( cmd, { 'env' : process.env },
	  function (error, stdout, stderr) {
		console.info( "createVM: " + error + stdout + stderr );
		
		// Recurse
		if ( vms.length>0 ) createVMs( vms );
		
		if ( --nesting==0 ) doExit();
	  }
	 );
}

function processTemplate(template) {
 ++nesting;
 for ( var set in template ) {
   msg += ( "Processing: " + set );
   switch (set)
   {
   case "parameters": 
	  params = template[set];
	  
	  // Override with command line parameters
	  for ( var p in cmd_params ) {
		 console.log( "Command line parameter: " + p + " value=" + cmd_params[p] );
		 params[p] = cmd_params[p];
	  }
	  
	  // Resolve any references in the values
	  for ( var p in params ) {
			var res = resolveStr( params[p], { dont_postpone : true } );
			if ( res ) params[p] = res;
	  }
	  break
	  
   case "images":
      if (useOS) createVMImages( template[set] );
	  else console.warn( "'images' defined but no Openstack parameters" );
	  continue;
	  
   case "flavors":
      if (useOS) createFlavors( template[set] );
	  else console.warn( "'flavors' defined but no Openstack parameters" );
	  continue;

   case "vms":
      if (useOS) vms = template[set];	// postpone until networks are created
	  else console.warn( "'vms' defined but no Openstack parameters" );
	  continue;
	  
   case "sharednetworkresources": 
   case "sites":
   case "vcenters":
   case "vrsconfigs":
   case "systemconfigs":
   case "infrastructurevscprofiles":
   case "infrastructureportprofiles":
   case "infrastructuregatewayprofiles":
   case "nsgatewaytemplates":
	  updateGlobals( set, template[set] )
	  break

   case "aws-stacks":
     aws_stacks = template[set];
	 break;
	  
   case "domains":
	 domains = template[set];
	 break;
	 
   case "l2domains":
	 l2domains = template[set];
	 break;

   case "nsgateways":
	 nsgateways = template[set]; 
	 break;
   case "nsredundancygroups":
     nsredundancygroups = template[set];
	 break;
	 
   case "gateways":
	  // Always create WAN services globally and add permissions for enterprise
	  // if ( enterprise == "csp" ) {
	      updateGlobals( set, template[set] );
		  break;
	  // }
	  // else no break
	 
   default:
      // Support conditional inclusion of JSON sections: $if and $if-not
	  if ( set.indexOf("$if")==0 ) {
		 var colon = set.indexOf(":");
		 if ( colon>0 ) {
			var expr = set.substring(0,colon);
			switch ( expr ) {
		    case "$if":
			case "$if-not":
				var flag = set.substring(colon+1);
				
				// Tell user to specify a value of true or false for the variables
				if ( typeof(params[flag]) == "string" && params[flag].indexOf("ASK:")==0 ) {
					console.error( "Please provide a Boolean value for the following input parameter: " + flag );
					console.error( "Description: " + params[flag].substring(4) );
					console.error( "For example: add parameters='{\""+flag+"\" : 1}'" );
					process.exit(-10);
				}
				
				if ( params[flag] ^ (expr=="$if-not") ) {
					console.log( "Including conditional section: " + expr + ":" + flag + "=" + params[flag] );
					processTemplate( template[set] );
				} else {
					console.log( "Excluding conditional section: " + expr + ":" + flag + "=" + params[flag] );
				}
				break;
			
			default:
			   console.error( "Unsupported expression: " + set );
			}
		} else {
			console.error( "Missing ':' in " + set );
			process.exit(-11);
		}
	  } else {
		  for ( t in template[set] ) {
			createRecursive( createContext(enterprise_id,set,template[set][t]) );
		  }
	  }
   }
 }
 
 // When a template with only 'domains' is used, the import process hangs because nothing triggers the domain instantiation
 if ( --nesting==0 ) doExit()
 
}

async function doImport( vsd_ip, enterprise, template ) {

    api.set_verbose( true )
	++nesting2;
    await api.init( vsd_ip, "csp", "csproot", "csproot", function(res) {
		// csp_id = res[0].enterpriseID;
		if ( enterprise == "csp" ) {
			msg += ( "Processing template for CSP..." );
			processTemplate( template );
		} else {
			++nesting;
			api.get( "/enterprises", "name == '"+enterprise+"'", function(enterprises) {
				// console.log( res )
				if (enterprises && enterprises[0]) {
					enterprise_id = enterprises[0].ID;		// GLOBAL
					processTemplate( template );
				} else {
				   console.log( "Unable to find Organization named '" + enterprise + "'" );
				   process.exit(-3)
				}
				// process.exit(0) no, wait until all async calls have finished
				--nesting;
			}, function (err) {
				console.log( "Error getting enterprise '"+enterprise+"':" + err )
				process.exit(-2)
			} )
		}
		console.log( "doImport exiting;nesting="+nesting );
		--nesting2;
    })
}	// doImport

/**
 *  Copyright 2014 Nuage Networks
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */
var api = {}
 
var superagent = require('superagent')

var _host, _user, _authorization;
var _url = "https://localhost:8443/nuage/api/v3_0"
var _organization = "test"
var _token = null
var _verbose = true

// Maintain API call stats
var stats = { GET : 0, PUT : 0, DELETE : 0, POST : 0 };

var HttpsAgent = require('agentkeepalive').HttpsAgent;

var keepaliveAgent = new HttpsAgent({
  keepAlive: true,
  maxSockets: 100,
  maxFreeSockets: 10,
  timeout: 60000,
  keepAliveTimeout: 30000 // free socket keepalive for 30 seconds
});

api.set_verbose = function( verbose ) {
   _verbose = verbose
}

function pollForEvents(eventHandler,uuid,verbose) {
	api.get( "/events" + ( uuid ? "?uuid=" + uuid : ""), "", function (res) {
		if (verbose) console.log( "Event channel response:" + JSON.stringify(res) )
		for ( var e in res.events ) {
			eventHandler( res.events[e] )
		}
		// XXX May eventually run out of stack space
		pollForEvents( eventHandler, res.uuid, verbose );
	}, function (err) {
		console.error( "Error: event channel closed: " + err )
	}, !verbose )
}

function getLatestAPIVersionURL(host,callback) {
	if (_verbose) console.info( "Getting latest API info from VSD at " + host );
	superagent.get( "https://" + host + ":8443/nuage" )
		.agent(keepaliveAgent)
		.end( function(err,res) {
			if (res && res.ok) {
			
				// For some reason, superagent doesn't parse the body
				var body = JSON.parse( res.text );
				msg += ( "VSD API version: " + body.versions[0].url )
				callback( body.versions[0].url );
			} else {
				console.error( "Error determining VSD API version:" + err + " details=" + JSON.stringify(res) );
			}
		})
}

async function getToken(callback) {
	if (_verbose) {
		msg += ( "Getting token from :" + _url + "/me" );
		msg += ( "Authorization: " + _authorization )
	}
	await superagent.get( _url + "/me" )
		.agent(keepaliveAgent)
		.set( 'Authorization', "XREST " + _authorization )
		.set( 'X-Nuage-Organization', _organization )
		.end( function(err,res) {
			if (res && res.ok) {
				var apiKey = res.body[0].APIKey;
				_token = "XREST " + new Buffer( _user + ':' + apiKey ).toString('base64');
				if (_verbose) msg += ('getToken success! Body = ' + JSON.stringify(res.body) + '\nkey=' + apiKey + '\ntoken=' + _token );					
			} else {
				console.error('Oh no! error ' + err + ( res ? res.text : "" ));
			}
			// always, also in case of error
			callback(res);
		});
}

/**
 * VSD API initialization function - authenticates with VSD
 *
 * @param {String} host IP or FQDN for the VSD instance to address ( assumes v3_0 )
 * @param {String} organization VSD Organization context to use/modify
 * @param {String} user The username to connect as
 * @param {String} password Password for the given user
 * @param {Function} Callback to be called with the response upon completion
 */
api.init = async function( host, organization, user, password, callback ) {
	_host = host;
	_user = user;
	_authorization = new Buffer( user + ':' + password ).toString('base64')
	_organization = organization;

	// Ignore TLS error of self-signed cert
	process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0;

	await getLatestAPIVersionURL( host, async function(api_url) {
		_url = api_url;
		
		// get token
		await getToken( function(res) {
			// Allow app to receive push events
			callback( res, function(eventhandler,verbose) {
				pollForEvents( eventhandler, null, verbose );
			}); // always, also in case of error
		});
	})
}

/**
 * Internal helper function to make REST API calls
 */
function makeRESTcall( req, body, filter, onSuccess, onError, no_log, isRetry ) {

	// Update stats before making the call
	++stats[ req.method ];

	req.set( 'Authorization', _token )
		.set( 'X-Nuage-Organization', _organization )
		.set( 'X-Nuage-Filter', filter ? filter : "" )
		// .set( 'Connection', keep_alive ? "keep-alive" : "close" )
		.agent(keepaliveAgent)
		.send( body )
		.end( function(e,res) {
			var err = e || res.error;
			if (err) {
			
				// Get new token if expired, don't loop endlessly
				if ( err == "Error: Unauthorized" && !isRetry ) {
					console.info( "Refreshing token..." );
					getToken( function(res) {
						if ( res && res.ok ) {
							// need to clone 'req'
							makeRESTcall( req.clone(), body, filter, onSuccess, onError, no_log, true )
						}
					})
				} else if ( onError ) {
					onError( err );
				} else {
					console.error( "Error in REST call: " + err )
				}
			} else {
				if (_verbose && !no_log) msg += ( "REST call status: " + res.status );
				!onSuccess || onSuccess( res.body )	// body can be null
			}
		} )
}

/**
 * GET method to retrieve objects
 * @param {String} path Path to the object to retrieve
 * @param {String} filter Optional filter expression to use
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 * 
 */
api.get = async function( path, filter, onSuccess, onError, no_log ) {
   if (_verbose && !no_log) msg += ( "GET: path = " + path + " filter = " + filter )
   await makeRESTcall( superagent.get( _url + path ), "", filter, onSuccess, onError, no_log )
}

/**
 * POST method to create a new object
 * @param {String} path Path to the collection of objects in which to create
 * @param {String} body Properties of the new object
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.post = async function( path, body, onSuccess, onError ) {
   if (_verbose) console.info( "POST: path = " + path + " body = " + JSON.stringify(body) )
   await makeRESTcall( superagent.post( _url + path + "?responseChoice=1" ), body, "", onSuccess, onError )
}

/**
 * POST method to create a new object, with Proxy user header
 * @param {String} proxyUser Proxy user in the form 'enterprise@username'
 * @param {String} path Path to the collection of objects in which to create
 * @param {String} body Properties of the new object
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.proxy_post = async function( proxyUser, path, body, onSuccess, onError ) {
   if (_verbose) console.info( "POST with proxy user: proxyUser="+proxyUser+" path = " + path + " body = " + JSON.stringify(body) )
   await makeRESTcall( superagent.post( _url + path ).set( 'X-Nuage-ProxyUser', proxyUser ), body, "", onSuccess, onError )
}

/**
 * PUT method to modify an existing object
 * @param {String} path Path to the object to modify
 * @param {String} body Modifications to make
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.put = async function( path, body, onSuccess, onError ) {
   if (_verbose) msg += ( "PUT: path = " + path + " body = " + JSON.stringify(body) )
   await makeRESTcall( superagent.put( _url + path + "?responseChoice=1" ), body, "", onSuccess, onError )
}

/**
 * DELETE method to remove an object
 * @param {String} path Path to the object to remove
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.del = async function( path, onSuccess, onError ) {
   if (_verbose) console.info( "DELETE: path = " + path )
   await makeRESTcall( superagent.del( _url + path + "?responseChoice=1" ), "", "", onSuccess, onError )	// can use filter expression?
}

/**
 * First tries to retrieves an object, then calls POST to create it if not found
 * @param {String} path Path to find/create the object
 * @param {Object} obj Object to create if not found
 * @param {String} Filter expression for the lookup
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.get_post = async function( path, obj, filter, onSuccess, onError ) {
   if (_verbose) msg += ( "get_post: path = " + path + " obj=" + JSON.stringify(obj) )
   
   var create_if_not_exists = async function() {
	 await api.post( path, obj, function (res) {
		!onSuccess || onSuccess( res, true )
	 }, onError );
   }
   
   await api.get( path, filter, function (body) {
	 if ( body && body[0] ) {
		!onSuccess || onSuccess( body );	// pass as array
	 } else {
		create_if_not_exists();
	 }
   } , create_if_not_exists );
}

api.getHost = function() {
	return _host;
}

api.print_stats = function () {
 return ( "VSD API calls statistics: " + JSON.stringify(stats) );
}
