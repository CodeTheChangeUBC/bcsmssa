$(document).ready(function() {
	
	function update_stats() {
		console.log("create post is working!");
		$.ajax({ 
			url : "",
			type : "POST",
			data : { the_post : $('#randtext').val() },		

			// Successful response
			success : function(json) {
				console.log(json);
				console.log('success');
			},

			// Failure 
			error : function(xhr, errmsg, err) {
				console.log("FAIL");
			}

		});
	}

	$('#stats-form').on('submit', function(event) {
		event.preventDefault();
		console.log('Form submitted!');
		update_stats();
	});

	
});

