#! node

// WANT_JSON

const fs = require('fs');
const util = require('util');

const argsReg = /(\w+)="(\w+)"/g;

function parseJSON(str){
    try{
        return JSON.parse(str);
    } catch(e){
        return undefined;
    }
}

function readArguments() {
    return new Promise((resolve, reject) => {
        fs.readFile(process.argv[2], (err, data) => {
            if (err) {
                reject(err);
            }

            const content = data.toString('utf-8');
            let args = parseJSON(content);

            if (args === undefined){
                args = {};
                let matching;

                while((matching = argsReg.exec(content)) != null) {
                    args[matching[1]] = matching[2];
                }
            }

            args.content = content;
            resolve(args);
        });
    });
}

function main(callback) {
    return readArguments()
        .then(callback)
        .then((result) => {
            if (!util.isNullOrUndefined(result)) {
                console.log(JSON.stringify(result));
            }
        })
        .catch((err) => {
            console.log(`{"failed":true, "msg":"${err.message}"}`);
            throw err;
        });
}

var msg = "";

// require the EventEmitter from the events module
//const EventEmitter = require('events').EventEmitter

// create an instance of the EventEmitter object
//const eventEmitter = new EventEmitter()
//eventEmitter.on( 'exit', function (result) {
//  console.error( result );
//});

main((args) => {

    doImport( args.vsd, args.organization, args.config ) 

    /* The way this is structured does not allow to take advantage of Node async processing	
    return {
      changed: true,
      failed:  false,
      rc: 0
    };
	*/
	return null;
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

// Mapping of NSG obj ID to ZFB request result
var job_results = {}

var templated_objects = { "nsgateways" : 1, "domains" : 1, "l2domains" : 1 }

// Nuage object key fields, these are used in filter expressions
var key_fields = [ "name", "priority", "type", "actualType", "value", "userName", "nextHopIp", "role", "address", "minAddress" ];

// Determines a unique key for the object. Most objects have 'name', but some are special ( VLANs, users, ACL entries, address ranges, static routes, DHCP options... )
function getKey(obj) {
	for ( var f in key_fields ) {
		var key = obj[ key_fields[f] ]
		if ( typeof key != "undefined" ) return key;
	}
	msg += ( "Warning: No key defined for object: " + JSON.stringify(obj) )
	return undefined		// could use 'externalId' and generate a hash
}

function finishResolution(rs) {
  for ( var i=0; i<rs.waiting.length; ++i ) {
	var c = rs.waiting[i];
	// c.dont_postpone = true;		// avoid infinite loop? Can have more than 1 ID to resolve, sequentially
	msg += ( "Finish resolving context=" + JSON.stringify(c) );
	if ( c.callback ) {
		c.callback();
	} else {
		console.error( "No callback provided!" );
		process.exit( -11 );
	}
  }
  delete to_resolve[ rs.key ]
}

// Postpone instantiation of domains and l2domains, and Job creation
var domains, l2domains, jobs;

// Also postpone NSGateways and NSGRedundancyGroups, else VLAN conflict may arise
var nsgateways, nsgredundancygroups;

var enterprise_id;

function doExit() {

  msg += "doExit nsgateways="+(nsgateways!=null)+" jobs="+(jobs!=null);

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
  } else if (jobs) {
     var js = jobs;
	 jobs = null;
	 // Need to wait before all uplinks have been created, XXX ugly!
	 // setTimeout( function() {
	 for ( var j in js ) {
	    // Dont try to seach for existing jobs, always create new
		createMulti( createContext(enterprise_id,"jobs",js[j]), 1 );
	 }
	 // }, 5000 );
  } else {
		var exitCode = apiErrors ? 100 : 0;	// exit with error in case of API error responses
		for ( r in to_resolve ) {
		   msg += ( "Unable to resolve: '" + r + "' (check spelling, case sensitive!) recurse="+to_resolve[r].recurse )
		   ++exitCode;
		}
		
		console.error( '{ "doExit": "exiting nesting=' + nesting + ' API errors=' + apiErrors + '"}' );
		// api.print_stats();
		// process.exit( exitCode );
                // eventEmitter.emit('exit', msg)
				
		var result = {
			changed: true,
			failed:  apiErrors>0,
			rc: exitCode,
			debug: msg,
			ids: name_2_id,
			job_results: job_results
		}
		console.log(JSON.stringify(result));
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
				msg += ( "createArrays: calling createRecursive root="+root );
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
	msg += ( "onResponse -> Object created/obtained in set "+context.set+" key='"+key+"' ID=" + id )

	if (typeof key != "undefined") {
		name_2_id[ context.set + "." + key ] = id;
		msg += ( "Added mapping '" + context.set + "." + key + "' => " + id );
		
		// For VLANs, also add mapping for user mnemonic ( VLAN ID not unique for different ports )
		if ( obj.userMnemonic ) {
			msg += ( "Adding mapping for VLAN using mnemonic: " + obj.userMnemonic )
			name_2_id[ context.set + "." + obj.userMnemonic ] = id;
			incRef( to_resolve[ context.set + "." + obj.userMnemonic ] );
			vlanMapped = true;
		} else if ( context.set=="vlans" ) {
			console.error( "Unable to map VLAN userMnemonic: " + JSON.stringify(obj) );
		}
	} else if ( context.set=="jobs" ) {
		job_results[ obj.parameters.associatedEntityID ] = obj.result;
	}
	
	// Check if any pending calls are now resolvable
	// Make sure object is fully constructed before resuming
	incRef( to_resolve[ context.set + "." + key ] )
	// incRef( context.rs )
	
	createArrays( context, id );
	
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
	   msg += ( "Resolved: " + m + " => " + v );
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
	  msg += ( "Resolved " + val + " to " + resolved )
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
	  
	  msg += ( "Resolution postponed for " + val )
  } else {
      msg += ( "Unable to resolve: " + obj + " but dont_postpone flag set!" );
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
	   msg += ( "Resolving array of strings ( vPorttags or user IDs )" )
	   var vals = []
	   for ( var i = 0; i < t.length; ++i ) {
	      var resolved = resolveStr( t[i], context, callback ) 
		  if (!resolved) return null
		  vals.push( resolved )
	   }
	   msg += ( "Resolved array: " + JSON.stringify(vals) )
	   instance[p] = vals
	} else if ( typeof(t) === "string" && (t.length > 1) ) {
	   var resolved = resolveStr( t, context, callback )
	   if (!resolved) return null	// postpone, restart from scratch next time
	   instance[p] = resolved
	} else if (p[0]!="#") {
	    if ( typeof(t) === "object" ) {
			// Pass original callback
			t = resolveVars( { template: t }, callback );
			if (!t) return;
		}
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
	msg += ( "Error response from API call: " + JSON.stringify(err) );
	++apiErrors;
	if ( --nesting==0 ) doExit()
}

function createMulti( context, count, callback ) {
	var instance = resolveVars( context, function() { createMulti(context,count,callback) } );
	if (!instance) {
		// More variables to resolve
		return;
	}

	++nesting
	if (context.basename && context.template.name) {
		instance.name = context.basename + count // zeropad(count,4)
	}
	api.post( context.root + '/' + context.set, instance, function (body) {
		  if (body.length>0) {
			var id = body[0].ID
			msg += ( "POST: Object created in " + context.set + " ID=" + id + " body=" + JSON.stringify(body[0]) )
			// instance["#count"] = count
			var resultContext = {
				root : context.root,
				set  : context.set, 
				template: instance,		// This one has the accurate #count and real name / resolved strings
				count: context.count
			}
			onResponse( resultContext, body[0] )
			
			// For templated objects, use callback to lookup resulting object
			if (callback) callback();
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
			createMulti( nextContext, count-1, null )	// no callback, or callback with new context?
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

function createRecursive( context ) {
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
		msg += ( "Postponing object creation due to dependency: " + context.template.depends );
		return;
	}
  }
  
  // Take count from parent, unless overridden at this level
  if ( template['#count'] ) {
		count = template['#count']
		basename = template.name + " "

		if (count>5000) {
			count = 5000
			msg += ( "Limiting #count to #5000" )
		} else {
			msg += ( "Auto-count value: " + count );
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
	 } else if ( template.role ) {	// uplinkconfig
		filter = "role == '"+template.role+"'"
	 } else if ( template.address ) {	// ??
		filter = "address == '"+template.address+"'"
	 } else if ( template.minAddress ) {	// address ranges
		filter = "minAddress == '"+template.minAddress+"'"
	 } else {
		msg += ( "Warning: Unable to filter object: " + JSON.stringify(template) )
		filter = ""
	 }
	 
	 // Resolve any variables in the filter? Should already be resolved...
	 if (filter && filter!="") {
		filter = resolveStr( filter, context, function() { createRecursive(context) } );
		if (!filter) return;
	 }
  }
  
  ++nesting;
  
  api.get( context.root + '/' + context.set, filter, function (objs) {
	  if ( objs && (objs.length>0) ) {
		
		msg += ( "RESULT: " + JSON.stringify(objs) );

		// If there are multiple, add all their IDs to the name mapping
		if ( count>1 ) {
		
			// Check that all objects are created, in case '#count' changes between runs
			if ( count != objs.length ) {
				msg += ( "Detected mismatch between #count and number of objects: " + count + "!=" + objs.length )
				
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
	  
		 msg += ( "No match found for " + context.root + '/' + context.set + " with filter '" + filter + "'" )
	  
		 if ( context.set == "gateways" ) {
			console.error( "Gateway not found: " + filter + " or no permissions to use it - please check the gateway name in your script, and make sure this organization has access" );
			process.exit(-8)
		 } else {
			 // Doesn't exist yet - create it
			 context.basename = basename
			 
			 //
			 // When creating a templated object like an NSG, we need to lookup the inherited properties ( like VLANs )
			 // and then continue processing
			 //
			 createMulti( context, count, (context.set in templated_objects) ? function() { createRecursive(context) } : null )
		 }
	  }
	  if ( --nesting==0 ) doExit()
  }, onError )
}

function addOffset( addr, offset ) {
	var prefix = addr.lastIndexOf(".");
	return addr.substring(0,prefix+1) + (parseInt( addr.substring(prefix+1) ) + offset);
}

/**
 * Very similar to per-enterprise objects update, but this also does PUT to modify an existing object
 */
function updateGlobals( set, values ) {
	if (values.forEach) values.forEach( function(r) { updateGlobal(set,r) } );
}
	
function updateGlobal( set, r ) {
	msg += ( "updateGlobal set="+set+" r="+JSON.stringify(r) );
	var u = resolveVars( { template: r }, function() { updateGlobal(set,r) } );
	if (!u) return;	// resolution pending

	incRef( to_resolve[ set + "." + getKey(u) ] );
	
	++nesting
	api.get( "/" + set, u.name ? "name == '"+u.name+"'" : null, function(globals) {

		if ( globals[0] ) {
			var cur = globals[0]
			var key = getKey(cur);
			if (typeof key != "undefined") {
				name_2_id[ set + "." + key ] = cur.ID;
				
				// Keep track of parent ID too, such that we can place shared subnets in the same zone
				name_2_parentId[ set + "." + key ] = cur.parentID;
			}
			
			console.error( "Updating shared resource..." )
			
			// Cannot modify 'underlay' flag once created
			delete u.underlay;
		
			++nesting

			var root = "/" + set + "/" + cur.ID; 
			api.put( root, u, function(body) {

				decRef( to_resolve[ set + "." + key ] );
	
				createArrays( { template : u, set : set, count : 0 }, cur.ID );
				if ( --nesting==0 ) doExit()
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

   case "jobs":
     jobs = template[set];
	 break;
	  
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

function doImport( vsd_ip, enterprise, template ) {

    api.set_verbose( true )
	++nesting;
    api.init( vsd_ip, "csp", "csproot", "csproot", function(res) {
		// csp_id = res[0].enterpriseID;
		if ( enterprise == "csp" ) {
			console.error( "Processing template for CSP..." );
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
				if (--nesting==0) doExit();
			}, function (err) {
				console.log( "Error getting enterprise '"+enterprise+"':" + err )
				process.exit(-2)
			} )
		}
		console.error( "doImport exiting;nesting="+nesting );
		if (--nesting==0) doExit();
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
	if (_verbose) console.error( "Getting latest API info from VSD at " + host );
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

function getToken(callback) {
	if (_verbose) {
		msg += ( "Getting token from :" + _url + "/me" );
		msg += ( "Authorization: " + _authorization )
	}
	superagent.get( _url + "/me" )
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
api.init = function( host, organization, user, password, callback ) {
	_host = host;
	_user = user;
	_authorization = new Buffer( user + ':' + password ).toString('base64')
	_organization = organization;

	// Ignore TLS error of self-signed cert
	process.env.NODE_TLS_REJECT_UNAUTHORIZED = 0;

	getLatestAPIVersionURL( host, function(api_url) {
		_url = api_url;
		
		// get token
		getToken( function(res) {
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
api.get = function( path, filter, onSuccess, onError, no_log ) {
   if (_verbose && !no_log) msg += ( "GET: path = " + path + " filter = " + filter )
   makeRESTcall( superagent.get( _url + path ), "", filter, onSuccess, onError, no_log )
}

/**
 * POST method to create a new object
 * @param {String} path Path to the collection of objects in which to create
 * @param {String} body Properties of the new object
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.post = function( path, body, onSuccess, onError ) {
   if (_verbose) msg += ( "POST: path = " + path + " body = " + JSON.stringify(body) )
   makeRESTcall( superagent.post( _url + path + "?responseChoice=1" ), body, "", onSuccess, onError )
}

/**
 * POST method to create a new object, with Proxy user header
 * @param {String} proxyUser Proxy user in the form 'enterprise@username'
 * @param {String} path Path to the collection of objects in which to create
 * @param {String} body Properties of the new object
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.proxy_post = function( proxyUser, path, body, onSuccess, onError ) {
   if (_verbose) msg += ( "POST with proxy user: proxyUser="+proxyUser+" path = " + path + " body = " + JSON.stringify(body) )
   makeRESTcall( superagent.post( _url + path ).set( 'X-Nuage-ProxyUser', proxyUser ), body, "", onSuccess, onError )
}

/**
 * PUT method to modify an existing object
 * @param {String} path Path to the object to modify
 * @param {String} body Modifications to make
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.put = function( path, body, onSuccess, onError ) {
   if (_verbose) msg += ( "PUT: path = " + path + " body = " + JSON.stringify(body) )
   makeRESTcall( superagent.put( _url + path + "?responseChoice=1" ), body, "", onSuccess, onError )
}

/**
 * DELETE method to remove an object
 * @param {String} path Path to the object to remove
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.del = function( path, onSuccess, onError ) {
   if (_verbose) msg += ( "DELETE: path = " + path )
   makeRESTcall( superagent.del( _url + path + "?responseChoice=1" ), "", "", onSuccess, onError )	// can use filter expression?
}

/**
 * First tries to retrieves an object, then calls POST to create it if not found
 * @param {String} path Path to find/create the object
 * @param {Object} obj Object to create if not found
 * @param {String} Filter expression for the lookup
 * @param {Function} onSuccess Callback to call upon completion (res)
 * @param {Function} onError [optional] callback to call upon errors (err)
 */
api.get_post = function( path, obj, filter, onSuccess, onError ) {
   if (_verbose) msg += ( "get_post: path = " + path + " obj=" + JSON.stringify(obj) )
   
   var create_if_not_exists = function() {
	 api.post( path, obj, function (res) {
		!onSuccess || onSuccess( res, true )
	 }, onError );
   }
   
   api.get( path, filter, function (body) {
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
