$(document).ready(function() {
	$('#button1').click(function(e) {
    	e.preventDefault();
    	$("#splash").toggleClass("hide");
     	$("#survey").toggleClass("hide");
    });

    $('#button2').click(function(e) {
    	e.preventDefault();
     	$("#completed").toggleClass("hide");
     	$("#survey").toggleClass("hide");
    });
});