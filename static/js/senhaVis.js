$(document).ready(function() {
    $('#show-password-checkbox').click(function(){
        var passwordInput = $('#id-password');
        var icon = $('#show-password-icon');

        if(passwordInput.attr('type') == 'password'){
            passwordInput.attr('type', 'text');
            icon.removeClass('fa-eye').addClass('fa fa-eye-slash');
        }else {
            passwordInput.attr('type', 'password');
            icon.removeClass('fa fa-eye-slash').addClass('fa-eye');
        }
    })
})