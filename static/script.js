$(document).ready(function() {
	$('#myForm').validator()

	$('#button1').click(function(e) {
    	e.preventDefault();
    	$("#splash").toggleClass("hide");
     	$("#survey").toggleClass("hide");
    });

    $('#myForm').validator().on('submit', function (e) {
	  if (e.isDefaultPrevented()) {
	    $('body').animate({
	    	scrollTop : 0
	    },800);
	  } else {
	  	
	    
	  }
	});

});
