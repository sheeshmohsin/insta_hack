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

// uploadFormDiv
// waitDiv
// analyzeDiv
// successDiv
// errorDiv
// errorMessage

function check_status(data_id){
	var authorizationToken = "Token dddfe7aeaf208c1b5234d92b2f56e7271862b044";
	$.ajax({
		type: 'GET',
		url: '/v1/check_status/'+ String(data_id) +'/',
		beforeSend: function(request){
			request.setRequestHeader("Authorization", authorizationToken)
		},
	}).done(function(rs, textStatus, xhr){
		if (rs.status){
			if (rs.is_invalid_auto){
				$("#uploadFormDiv").hide();
				$("#waitDiv").hide();
				$("#analyzeDiv").hide();
				$("#successDiv").hide();
				$("#errorMessage").html(rs.error_msg);
				$("#errorDiv").show();
			}
			else{
				$("#uploadFormDiv").hide();
				$("#waitDiv").hide();
				$("#analyzeDiv").hide();
				$("#successDiv").show();
				$("#errorDiv").hide();
			}
			clearInterval(window.interval);
		}
	});
}
$(document).ready(function() {
	$("#uploadForm").submit(function(e){
		var authorizationToken = "Token dddfe7aeaf208c1b5234d92b2f56e7271862b044";
		var formData = new FormData(this);
		console.log(formData);
		$("#uploadFormDiv").hide();
		$("#waitDiv").show();
		$("#analyzeDiv").hide();
		$("#successDiv").hide();
		$("#errorDiv").hide();
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
			},
		}).done(function(rs, textStatus, xhr){
			if (xhr.status === 201){
				$("#uploadFormDiv").hide();
				$("#waitDiv").hide();
				$("#analyzeDiv").show();
				$("#successDiv").hide();
				$("#errorDiv").hide();
				 window.interval = setInterval(function(){check_status(rs.id)}, 1000);
			} else {
				$("#uploadFormDiv").hide();
				$("#waitDiv").hide();
				$("#analyzeDiv").hide();
				$("#successDiv").hide();
				$("#errorDiv").show();
			}
		});
		return false;
	});
});
