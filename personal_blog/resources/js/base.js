function loginOrRegister() {
    if ($("#login-tab")[0].ariaSelected === 'true') {
        if ($("#loginEmailVerification").html() == "Valid email" && $("#loginPasswordVerification").html() == "Valid password") {
            let email = $.trim($("#loginEmail").val());
            let password = $.trim($("#loginPassword").val());
            let imageCode = $.trim($("#loginCode").val());

            $("#loginAndRegister").attr("disabled", true);

            let param = "email=" + email;
            param += "&password=" + password;
            param += "&image_code=" + imageCode;
            $.post('/login', param, function (data) {
                alert(data);
                if (data.startsWith("Success")) {
                    setTimeout('location.reload()', 500);
                } else {
                    $("#loginAndRegister").attr("disabled", false);
                    $("#loginEmail").attr("disabled", false);
                    $("#loginEmail").val("");
                    $("#loginPassword").val("");
                    $("#loginCode").val("");
                    $("#loginEmail").focus();
                }
            })
        } else {
            alert("Fail (Front) : Invalid email or password");
            return false;
        }
    } else {
        if ($("#registerEmailVerification").html() == "Valid email" && $("#registerPasswordVerification").html() == "Valid password" && $("#registerNameVerification").html() == "Valid name") {
            let firstName = $.trim($("#registerFirstName").val());
            let lastName = $.trim($("#registerLastName").val());
            let email = $.trim($("#registerEmail").val());
            let password = $.trim($("#registerPassword").val());
            let emailCode = $.trim($("#registerCode").val());

            $("#loginAndRegister").attr("disabled", true);

            let param = "email=" + email;
            param += "&password=" + password;
            param += "&name=" + firstName + " " + lastName;
            param += "&email_code=" + emailCode;
            $.post('/register', param, function (data) {
                alert(data);
                if (data.startsWith("Success")) {
                    setTimeout('location.reload()', 500);
                } else {
                    $("#loginAndRegister").attr("disabled", false);
                    $("#registerEmail").attr("disabled", false);
                    $("#registerCodeBtn").attr("disabled", false);
                    $("#registerEmail").val("");
                    $("#registerPassword").val("");
                    $("#registerCode").val("");
                    $("#registerEmail").focus();
                }
            })
        } else {
            alert("Fail (Front) : Invalid name or email or password");
            return false;
        }
    }
}

function sendVerificationEmail() {
    changeVerificationState("sending");
    let email = $.trim($("#registerEmail").val());
    if (email.match(/.+@.+\..+/)) {
        let param = "email=" + email;
        $.post('/verification/email', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#registerCode").val("");
                $("#registerCode").focus();
                changeVerificationState("tick");
            } else {
                changeVerificationState("retry");
            }
        })
    } else {
        alert("Fail (Front) : Invalid email");
        return false;
    }
}

function sendForgetPasswordEmail() {
    changeForgetState("sending");
    let email = $.trim($("#loginEmail").val());
    if (email.match(/.+@.+\..+/)) {
        let param = "email=" + email;
        $.post('/forget', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#loginPassword").val("");
                $("#loginCode").val("");
                $("#loginPassword").focus();
                changeForgetState("tick");
            } else {
                changeForgetState("retry");
            }
        })
    } else {
        alert("Fail (Front) : Invalid email");
        return false;
    }
}

function changeForgetState(status) {
    let ticks = 30;
    let tick = function () {
        if (ticks > 0) {
            setTimeout(function () {
                $("#loginPasswordBtn").html("Sent(" + ticks + ")");
                ticks--;
                tick();
            }, 1000);
        } else {
            changeForgetState("retry");
        }
    };
    ticks = 30;
    switch (status) {
        case "sending": {
            $("#loginPasswordBtn").attr("disabled", true);
            $("#loginPasswordBtn").html("Sending");
            $("#loginEmail").attr("disabled", true);
            break;
        }
        case "tick": {
            $("#loginPasswordBtn").attr("disabled", true);
            tick("Sent");
            break;
        }
        case "retry": {
            $("#loginPasswordBtn").attr("disabled", false);
            $("#loginPasswordBtn").html("Forget password");
            $("#loginEmail").attr("disabled", false);
            break;
        }
    }
}

function changeVerificationState(status) {
    let ticks = 30;
    let tick = function () {
        if (ticks > 0) {
            setTimeout(function () {
                $("#registerCodeBtn").html("Sent(" + ticks + ")");
                ticks--;
                tick();
            }, 1000);
        } else {
            changeForgetState("retry");
        }
    };
    ticks = 30;
    switch (status) {
        case "sending": {
            $("#registerCodeBtn").attr("disabled", true);
            $("#registerCodeBtn").html("Sending");
            $("#registerEmail").attr("disabled", true);
            break;
        }
        case "tick": {
            $("#registerCodeBtn").attr("disabled", true);
            tick("Sent");
            break;
        }
        case "retry": {
            $("#registerCodeBtn").attr("disabled", false);
            $("#registerCodeBtn").html("Get email code");
            $("#registerEmail").attr("disabled", false);
            break;
        }
    }
}

function refreshImageCode() {
    $.ajax({
        type: "get",
        url: "/verification/image",
        headers: {
            "Accept": "text/html"
        },
        success: function (data) {
            $('#loginCodeImg').attr("src", data);
        }
    })
}

function showModel() {
    $('#accountModal').modal('show');
}

// $(".navbar-nav").find("li").click(function () {
//     $(this).siblings().find("a").removeClass("active");
//     $(this).find("a").addClass("active");
// })

$(document).ready(function () {
    $("#loginEmail").bind('input propertychange', monitorInput);
    $("#registerEmail").bind('input propertychange', monitorInput);
    $("#loginPassword").bind('input propertychange', monitorInput);
    $("#registerPassword").bind('input propertychange', monitorInput);
    $("#registerFirstName").bind('input propertychange', monitorInput);
    $("#registerLastName").bind('input propertychange', monitorInput);
    refreshImageCode();
})

function monitorInput() {
    if (!$.trim($("#loginEmail").val()).match(/.+@.+\..+/)) {
        $("#loginEmail").attr("class", "form-control is-invalid");
        $("#loginEmailVerification").attr("class", "invalid-feedback");
        $("#loginEmailVerification").html("Invalid email");
    } else {
        $("#loginEmail").attr("class", "form-control is-valid");
        $("#loginEmailVerification").attr("class", "valid-feedback");
        $("#loginEmailVerification").html("Valid email");
    }

    if (!$.trim($("#registerEmail").val()).match(/.+@.+\..+/)) {
        $("#registerEmail").attr("class", "form-control is-invalid");
        $("#registerEmailVerification").attr("class", "invalid-feedback");
        $("#registerEmailVerification").html("Invalid email");
    } else {
        $("#registerEmail").attr("class", "form-control is-valid");
        $("#registerEmailVerification").attr("class", "valid-feedback");
        $("#registerEmailVerification").html("Valid email");
    }

    if ($.trim($("#loginPassword").val()).length < 3) {
        $("#loginPassword").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#loginPasswordVerification").attr("class", "invalid-feedback");
        $("#loginPasswordVerification").html("Password less than 3 letters");
    } else {
        $("#loginPassword").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#loginPasswordVerification").attr("class", "valid-feedback");
        $("#loginPasswordVerification").html("Valid password");
    }

    if ($.trim($("#registerPassword").val()).length < 3) {
        $("#registerPassword").attr("class", "form-control is-invalid");
        $("#registerPasswordVerification").attr("class", "invalid-feedback");
        $("#registerPasswordVerification").html("Password less than 3 letters");
    } else {
        $("#registerPassword").attr("class", "form-control is-valid");
        $("#registerPasswordVerification").attr("class", "valid-feedback");
        $("#registerPasswordVerification").html("Valid password");
    }

    let re = new RegExp(/[.,\/#!$%\^&\*;:{}=\-_`~()?0-9]/g);
    if (re.test($.trim($("#registerFirstName").val())) || $.trim($("#registerFirstName").val()) == "") {
        $("#registerFirstName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#registerNameVerification").attr("class", "invalid-feedback");
        $("#registerNameVerification").html("Invalid name");
    } else {
        $("#registerFirstName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#registerNameVerification").attr("class", "valid-feedback");
        $("#registerNameVerification").html("Valid name");
    }

    if (re.test($.trim($("#registerLastName").val())) || $.trim($("#registerLastName").val()) == "") {
        $("#registerLastName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#registerNameVerification").attr("class", "invalid-feedback");
        $("#registerNameVerification").html("Invalid name");
    } else {
        $("#registerLastName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#registerNameVerification").attr("class", "valid-feedback");
        $("#registerNameVerification").html("Valid name");
    }
}