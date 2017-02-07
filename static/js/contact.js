$(document).ready(function(){
    $('.g-recaptcha').attr("data-callback", "validate_fields");
    $("#contact-form input, #contact-form select, #contact-form textarea").on("keyup", validate_fields);
});


function validate_fields() {
    var is_valid = grecaptcha.getResponse();
    if (is_valid) {
        $('#contact-form input, #contact-form textarea').each(function() {
            if ($(this).val().length == 0) {
                is_valid = false;
                return false;
            }
        });
    }
    $("#contact-submit").toggleClass("disabled", !is_valid);
}

$("#key").on("click", function() {
    location.href = '/pgp';
});