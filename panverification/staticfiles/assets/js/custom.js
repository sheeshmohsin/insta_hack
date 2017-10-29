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

function createCookie(name, value, days) {
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        var expires = "; expires=" + date.toGMTString();
    }
    else var expires = "";               

    document.cookie = name + "=" + value + expires + "; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for (var i = 0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0) == ' ') c = c.substring(1, c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length, c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name, "", -1);
}

function logout(){
	eraseCookie('api_key')
	eraseCookie('entity_type')
	eraseCookie('username')
	window.location = '/login/';
}

// if (readCookie('api_key')){
// 	if (readCookie('entity_type') == 'user'){

// 	}
// }

$(document).ready(function() {
	$("#uploadForm").submit(function(e){
		var authorizationToken = "Token "+ String(readCookie('api_key'));
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
	$("#LoginForm").submit(function(e){
		// var authorizationToken = "Token " + String(readCookie('api_key'));
		$.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
        }).done(function(rs, textStatus, xhr){
        	if (xhr.status === 200){
        		if(rs.entity_type == 'user'){
        			createCookie('api_key', rs.api_key, 3)
        			createCookie('entity_type', rs.entity_type, 3)
        			createCookie('username', rs.username, 3)
        			window.location = '/user/'
        		}
        		else if (rs.entity_type == 'agent') {
        			createCookie('api_key', rs.api_key, 3)
        			createCookie('entity_type', rs.entity_type, 3)
        			createCookie('username', rs.username, 3)
        			window.location = '/agent/'
        		}
        	} else {
        		console.log("Login Failed");
        	}
        });
        e.preventDefault();
	})
	$("#signupForm").submit(function(e){
		// var authorizationToken = "Token " + String(readCookie('api_key'));
		$.ajax({ // create an AJAX call...
            data: $(this).serialize(), // get the form data
            type: $(this).attr('method'), // GET or POST
            url: $(this).attr('action'), // the file to call
        }).done(function(rs, textStatus, xhr){
        	if (xhr.status === 201){
        		window.location = '/login/';
        	} else {
        		console.log("Signup Failed");
        	}
        });
        e.preventDefault();
	})
	$("#username-corner").text(readCookie('username'));
	if (window.location.pathname == '/user/'){
		if (readCookie('entity_type') != 'user'){
			logout();
		}
	}
	if (window.location.pathname == '/agent/'){
		if (readCookie('entity_type') != 'agent'){
			logout();
		}
	}
});