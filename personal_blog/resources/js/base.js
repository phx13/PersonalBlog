function loginOrRegister() {
    if ($("#login-tab")[0].ariaSelected === 'true') {
        if ($("#loginEmailVerification").html() == "Valid Email" && $("#loginPasswordVerification").html() == "Valid Password") {
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
                    $("#loginEmail").val("");
                    $("#loginPassword").val("");
                    // $("#loginCode").val("");
                    $("#loginEmail").focus();
                }
            })
        } else {
            alert("Fail (Front) : Invalid email or password");
            return false;
        }
    } else {
        if ($("#registerEmailVerification").html() == "Valid Email" && $("#registerPasswordVerification").html() == "Valid Password" && $("#registerNameVerification").html() == "Valid Name") {
            let firstName = $.trim($("#registerFirstName").val());
            let lastName = $.trim($("#registerLastName").val());
            let email = $.trim($("#registerEmail").val());
            let password = $.trim($("#registerPassword").val());
            // let emailCode = $.trim($("#registerCode").val());

            $("#loginAndRegister").attr("disabled", true);

            let param = "email=" + email;
            param += "&password=" + password;
            param += "&name=" + firstName + " " + lastName;
            // param += "&email_code=" + emailCode;
            $.post('/register', param, function (data) {
                alert(data);
                if (data.startsWith("Success")) {
                    setTimeout('location.reload()', 500);
                } else {
                    $("#loginAndRegister").attr("disabled", false);
                    $("#registerEmail").attr("disabled", false);
                    // $("#registerCodeBtn").attr("disabled", false);
                    $("#registerEmail").val("");
                    $("#registerPassword").val("");
                    // $("#registerCode").val("");
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
    let email = $.trim($("#registerEmail").val());
    let registerCodeBtn = $.trim($("#registerCodeBtn").html());
    if (registerCodeBtn == "Email has sent") {
        alert("Fail (Front) : Email has sent");
        return false;
    }
    if (email.match(/.+@.+\..+/)) {
        $("#registerEmail").attr("disabled", true);
        $("#registerCodeBtn").attr("disabled", true);
        let param = "email=" + email;
        $.post('/verification/email', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#registerCodeBtn").html("Email has sent");
            } else {
                $("#registerEmail").attr("disabled", false);
                $("#registerCodeBtn").attr("disabled", false);
            }
        })
    } else {
        alert("Fail (Front) : Invalid email");
        return false;
    }
}

function sendForgetPasswordEmail() {
    let email = $.trim($("#loginEmail").val());
    let loginPasswordBtn = $.trim($("#loginPasswordBtn").html());
    if (loginPasswordBtn == "Password has sent") {
        alert("Fail (Front) : Password has sent");
        return false;
    }
    if (email.match(/.+@.+\..+/)) {
        $("#loginEmail").attr("disabled", true);
        $("#loginPasswordBtn").attr("disabled", true);
        let param = "email=" + email;
        $.post('/forget', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#loginPassword").val("");
                $("#loginCode").val("");
                $("#loginPasswordBtn").html("Password has sent");
                $("#loginPassword").focus();
            } else {
                $("#loginEmail").attr("disabled", false);
                $("#loginPasswordBtn").attr("disabled", false);
            }
        })
    } else {
        alert("Fail (Front) : Invalid email");
        return false;
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

$(".navbar-nav").find("li").click(function () {
    $(this).siblings().find("a").removeClass("active");
    $(this).find("a").addClass("active");
})

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
        $("#loginEmailVerification").html("Invalid Email");
    } else {
        $("#loginEmail").attr("class", "form-control is-valid");
        $("#loginEmailVerification").attr("class", "valid-feedback");
        $("#loginEmailVerification").html("Valid Email");
    }

    if (!$.trim($("#registerEmail").val()).match(/.+@.+\..+/)) {
        $("#registerEmail").attr("class", "form-control is-invalid");
        $("#registerEmailVerification").attr("class", "invalid-feedback");
        $("#registerEmailVerification").html("Invalid Email");
    } else {
        $("#registerEmail").attr("class", "form-control is-valid");
        $("#registerEmailVerification").attr("class", "valid-feedback");
        $("#registerEmailVerification").html("Valid Email");
    }

    if ($.trim($("#loginPassword").val()).length < 3) {
        $("#loginPassword").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#loginPasswordVerification").attr("class", "invalid-feedback");
        $("#loginPasswordVerification").html("Password less than 3 letters");
    } else {
        $("#loginPassword").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#loginPasswordVerification").attr("class", "valid-feedback");
        $("#loginPasswordVerification").html("Valid Password");
    }

    if ($.trim($("#registerPassword").val()).length < 3) {
        $("#registerPassword").attr("class", "form-control is-invalid");
        $("#registerPasswordVerification").attr("class", "invalid-feedback");
        $("#registerPasswordVerification").html("Password less than 3 letters");
    } else {
        $("#registerPassword").attr("class", "form-control is-valid");
        $("#registerPasswordVerification").attr("class", "valid-feedback");
        $("#registerPasswordVerification").html("Valid Password");
    }

    let re = new RegExp(/[.,\/#!$%\^&\*;:{}=\-_`~()?0-9]/g);
    if (re.test($.trim($("#registerFirstName").val())) || $.trim($("#registerFirstName").val()) == "") {
        $("#registerFirstName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#registerNameVerification").attr("class", "invalid-feedback");
        $("#registerNameVerification").html("Invalid name");
    } else {
        $("#registerFirstName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#registerNameVerification").attr("class", "valid-feedback");
        $("#registerNameVerification").html("Valid Name");
    }

    if (re.test($.trim($("#registerLastName").val())) || $.trim($("#registerLastName").val()) == "") {
        $("#registerLastName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-invalid");
        $("#registerNameVerification").attr("class", "invalid-feedback");
        $("#registerNameVerification").html("Invalid name");
    } else {
        $("#registerLastName").attr("class", "form-control col-sm-12 col-md-6 col-lg-6 is-valid");
        $("#registerNameVerification").attr("class", "valid-feedback");
        $("#registerNameVerification").html("Valid Name");
    }
}