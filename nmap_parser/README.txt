There are two scripts in this folder.

1. pps_formatter.py: 
	~~> ingests a copy pasted text file of the <Ports, Protocols, Services.docx>
	~~> removes weird new line artifact
	~~> removes everything except digits
	~~> spits out a list of approved ports new line separated 

2. nmap_parser.py: 
	~~> ingests non verbose, single host port scan (xml format)
	~~> extracts xml elements
	~~> appends non-closed ports to list, converts datatype of elements in list to int
	~~> ingests pps file, generates list, converts datatype of elements in list to int
	~~> compares if nmap non-closed port is in approved ports list
	~~> warns you if not in console text (correct this)

Usage Notes:
	~~~ Currently only compatible with single host, TCP port scan outout
	~~~ Comments derived from learning the XML library are retained for future reference
	~~~ Comments regarding script function are also present
	~~~ Version 1.0 LOTS of room for improvement. Sorry for lack of convenience features