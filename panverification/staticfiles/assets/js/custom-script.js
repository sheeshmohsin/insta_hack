$(document).ready(function(){
	$("#edit_name").hide();
  	$("#edit_dob").hide();
  	$("#edit_pan").hide();
  	$("#details_correct").hide();
  	$("#hr_line").hide();

    var authorizationToken = "Token efcaccbcb4cdf7cfe24ec163ae1e65ad23d4f21e";
    $.ajax({
      type: 'GET',
      url: '/v1/next_data/',
      // enctype: 'multipart/form-data',
      dateType: 'json',
      headers: {'Authorization': authorizationToken},
      beforeSend: function(request){
        request.setRequestHeader("Authorization", authorizationToken)
      }
    }).done(function(data){
      console.log("here in done");
      console.log(data);
      window.data = data;
      $('#extracted-name').text(data.user_data.extracted_name);
      $('#extracted-dob').text(data.user_data.extracted_dob);
      $('#extracted-pan').text(data.user_data.extracted_pan);
      $('#image-url').attr('src', data.user_data.extracted_image);
    }).fail(function(response, status, error) {
        error = response.responseJSON;
        $('#data_next').html('Save and Next &nbsp; <i class="fa fa-arrow-circle-right" aria-hidden="true"></i>');
        $('#data_next').attr('disabled', false);
        e.preventDefault();
        return false;
    });
});
function valueChecked(){
  	if($('.name1').is(":checked")){
     	$("#edit_name").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
  	}else{
     	$("#edit_name").hide(300);
  	}
  	if($(".dob1").is(":checked")){
     	$("#edit_dob").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
  	}else{
     	$("#edit_dob").hide(300);
  	}
  	if($(".pan1").is(":checked")){
     	$("#edit_pan").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
  	}else{
     	$("#edit_pan").hide(300);
  	}
  	if(!$('.name1').is(":checked") && !$(".dob1").is(":checked") && !$(".pan1").is(":checked")){
  		$("#details_correct").hide(300);
  		$("#hr_line").hide(300);
  	}
}