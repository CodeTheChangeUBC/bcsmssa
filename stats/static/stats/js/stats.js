$(document).ready(function() {

	// Tables to load with DataTablles
	var tables = [	'#clientTable', 
					'#servicesTable', 
					'#referralsTable',
					'#abuseTable',
					'#sitchTable',
				]

	// Load tables
	for (var i=0; i<tables.length; i++) {
		$(tables[i]).DataTable();	
	}
});