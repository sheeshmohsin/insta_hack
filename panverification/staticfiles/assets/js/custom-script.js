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

$(document).ready(function(){
	$("#edit_name").hide();
  	$("#edit_dob").hide();
  	$("#edit_pan").hide();
  	$("#details_correct").hide();
  	$("#hr_line").hide();

    var authorizationToken = "Token " + readCookie('api_key');
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
      window.data = data;
      if (Object.keys(data).length > 0) {
        $('#no-data').addClass('hide');
        $('#pan-card-data').removeClass('hide');
        img_url = data.user_data.extracted_image.split('/panverification')
        window.userdata_id = data.user_data.id;
        $('#extracted-name').text(data.user_data.extracted_name);
        $('#extracted-dob').text(data.user_data.extracted_dob);
        $('#extracted-pan').text(data.user_data.extracted_pan);
        $('#image-url').attr('src', img_url[1]);
      } else {
        $('#no-data').removeClass('hide');
        $('#pan-card-data').addClass('hide');
      }
    }).fail(function(response, status, error) {
        error = response.responseJSON;
        $('#data_next').html('Save and Next &nbsp; <i class="fa fa-arrow-circle-right" aria-hidden="true"></i>');
        e.preventDefault();
        return false;
    });
});
function valueChecked(){
  	if($('.name1').is(":checked")){
     	$("#edit_name").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
      $('#name').prop('checked', false);
  	}else{
     	$("#edit_name").hide(300);
  	}
  	if($(".dob1").is(":checked")){
     	$("#edit_dob").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
      $('#dob').prop('checked', false);
  	}else{
     	$("#edit_dob").hide(300);
  	}
  	if($(".pan1").is(":checked")){
     	$("#edit_pan").show(300);
     	$("#details_correct").show(300);
     	$("#hr_line").show(300);
      $('#pan').prop('checked', false);
  	}else{
     	$("#edit_pan").hide(300);
  	}
  	if(!$('.name1').is(":checked") && !$(".dob1").is(":checked") && !$(".pan1").is(":checked")){
  		$("#details_correct").hide(300);
  		$("#hr_line").hide(300);
  	}
}
function set_error(msg) {
  $('#validation-error').html(msg);
  $('#validation-error').removeClass('hide');
}

function clear_error() {
    $('#validation-error').html('');
    $('#validation-error').hide();
}

$(document.body).on('click', '#data_next', function(e){
  var authorizationToken = "Token " + readCookie('api_key');
  data_val = [];
  var verified_agent = false;
  if (!($('#name').is(':checked')) && !($('#name1').is(':checked'))){
    set_error('Please verify Name');
    return e.preventDefault();
  }
  if(!($('#dob').is(':checked')) && !($('#dob1').is(':checked'))){
    set_error('Please verify DOB');
    return e.preventDefault();
  }
  if(!($('#pan').is(':checked')) && !($('#pan1').is(':checked'))){
    set_error('Please verify PAN Number');
    return e.preventDefault();
  }
  if ($('#name1').is(':checked') || $('#dob1').is(':checked') || $('#pan').is(':checked')) {
    if ($('#name1').is(':checked')){
      if ($('#first_name').val()){
        var name = {}
        name['feedback_for'] = '1',
        name['details'] = $('#first_name').val()
        data_val.push(name);
      }
    }
    if ($('#dob1').is(':checked')){
      if ($('#date_of_birth').val()){
        var dob = {}
        dob['feedback_for'] = '2',
        dob['details'] = $('#date_of_birth').val()
        data_val.push(dob);
      }
    }
    if ($('#pan1').is(':checked')){
      if ($('#pan_no').val()){
        var pan = {}
        pan['feedback_for'] = '3',
        pan['details'] = $('#pan_no').val()
        data_val.push(pan);
      }
    }
  } else {
    verified_agent=true;
  }
  total_data_val = {'feedback_data':data_val, 'verified_agent':verified_agent}
  clear_error();
  $.ajax({
      type: 'PUT',
      url: '/v1/verification_details/'+window.userdata_id+'/',
      // enctype: 'multipart/form-data',
      dateType: 'json',
      contentType: 'application/json',
      data: JSON.stringify(total_data_val),
      headers: {'Authorization': authorizationToken},
      beforeSend: function(request){
        request.setRequestHeader("Authorization", authorizationToken)
      }
    }).done(function(data){
      location.reload();
    }).fail(function(response, status, error) {
        error = response.responseJSON;
        $('#data_next').html('Save and Next &nbsp; <i class="fa fa-arrow-circle-right" aria-hidden="true"></i>');
        e.preventDefault();
        return false;
    });
})


$('#name').on('click', function () {
    var is_correct_name = $('#name').is(':checked');
    if (is_correct_name){
      $('#name1').prop('checked', false);
      valueChecked();
    }
});

$('#dob').on('click', function () {
    var is_correct_dob = $('#dob').is(':checked');
    if (is_correct_dob){
      $('#dob1').prop('checked', false);
      valueChecked();
    }
});

$('#pan').on('click', function () {
    var is_correct_pan = $('#pan').is(':checked');
    if (is_correct_pan){
      $('#pan1').prop('checked', false);
      valueChecked();
    }
});


