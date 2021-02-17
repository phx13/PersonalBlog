function loginOrRegister() {
    if ($("#login-tab")[0].ariaSelected === 'true') {
        let email = $.trim($("#loginEmail").val());
        let password = $.trim($("#loginPassword").val());

        let param = "email=" + email;
        param += "&password=" + password;
        $.post('/login', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                setTimeout('location.reload()', 500);
                $("#loginEmail").val("");
                $("#loginPassword").val("");
            }
        })
    } else {
        let email = $.trim($("#registerEmail").val());
        let password = $.trim($("#registerPassword").val());
        let param = "email=" + email;
        param += "&password=" + password;
        $.post('/register', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                setTimeout('location.reload()', 500);
                $("#registerEmail").val("");
                $("#registerPassword").val("");
            }
        })
    }
}

function showModel(){
    $('#accountModal').modal('show');
}

$(".navbar-nav").find("li").click(function() {
    $(this).siblings().find("a").removeClass("active");
    $(this).find("a").addClass("active");
})