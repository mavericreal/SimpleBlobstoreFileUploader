$(document).ready(function() {

	$('#addFile').click(function(){
		var a = $('.file:first').clone();
		$(a).children('input').val('')
		$('#addFile').before(a);
	});
	
	
	$('form').submit(function(){
		console.log('aaaaaaaaaaa');
	});


});
