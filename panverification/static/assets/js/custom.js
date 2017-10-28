'use strict';

;( function ( document, window, index )
{
	var inputs = document.querySelectorAll( '.inputfile' );
	Array.prototype.forEach.call( inputs, function( input )
	{
		var label	 = input.nextElementSibling,
			labelVal = label.innerHTML;

		input.addEventListener( 'change', function( e )
		{
			var fileName = '';
			if( this.files && this.files.length > 1 )
				fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
			else
				fileName = e.target.value.split( '\\' ).pop();

			if( fileName )
				label.querySelector( 'span' ).innerHTML = fileName;
			else
				label.innerHTML = labelVal;
		});

		// Firefox bug fix
		input.addEventListener( 'focus', function(){ input.classList.add( 'has-focus' ); });
		input.addEventListener( 'blur', function(){ input.classList.remove( 'has-focus' ); });
	});
}( document, window, 0 ));

$(document).ready(function() {
	$("#uploadForm").submit(function(e){
		var authorizationToken = "Token dddfe7aeaf208c1b5234d92b2f56e7271862b044";
		var formData = new FormData(this);
		console.log(formData);
		$.ajax({
			data: formData,
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			// enctype: 'multipart/form-data',
			contentType: false,
			processData: false,
			headers: {'Authorization': authorizationToken},
			beforeSend: function(request){
				request.setRequestHeader("Authorization", authorizationToken)
			}
		}).done(function(data){
			console.log("done");
		});
		return false;
	});
});
