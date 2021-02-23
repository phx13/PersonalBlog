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

function showModel() {
    $('#accountModal').modal('show');
}

$(".navbar-nav").find("li").click(function () {
    $(this).siblings().find("a").removeClass("active");
    $(this).find("a").addClass("active");
})

let loginEmail = document.getElementById("loginEmail");
let registerEmail = document.getElementById("registerEmail");
let loginPassword = document.getElementById("loginPassword");
let registerPassword = document.getElementById("registerPassword");

let monitorInput = function () {
    let loginEmailValue = loginEmail.value;
    let loginEmailValidation = document.getElementById("loginEmailValidation");
    if (!loginEmailValue.match(/.+@.+\..+/)) {
        loginEmail.setAttribute("class", "form-control is-invalid");
        loginEmailValidation.setAttribute("class", "invalid-feedback");
        loginEmailValidation.innerHTML = "Invalid Email";
    } else {
        loginEmail.setAttribute("class", "form-control is-valid");
        loginEmailValidation.setAttribute("class", "valid-feedback");
        loginEmailValidation.innerHTML = "Valid Email";
    }

    let registerEmailValue = registerEmail.value;
    let registerEmailValidation = document.getElementById("registerEmailValidation");
    if (!registerEmailValue.match(/.+@.+\..+/)) {
        registerEmail.setAttribute("class", "form-control is-invalid");
        registerEmailValidation.setAttribute("class", "invalid-feedback");
        registerEmailValidation.innerHTML = "Invalid Email";
    } else {
        registerEmail.setAttribute("class", "form-control is-valid");
        registerEmailValidation.setAttribute("class", "valid-feedback");
        registerEmailValidation.innerHTML = "Valid Email";
    }

    let loginPasswordValue = loginPassword.value;
    let loginPasswordValidation = document.getElementById("loginPasswordValidation");
    if (loginPasswordValue.length < 3) {
        loginPassword.setAttribute("class", "form-control is-invalid");
        loginPasswordValidation.setAttribute("class", "invalid-feedback");
        loginPasswordValidation.innerHTML = "Password less than 3 letters";
    } else {
        loginPassword.setAttribute("class", "form-control is-valid");
        loginPasswordValidation.setAttribute("class", "valid-feedback");
        loginPasswordValidation.innerHTML = "Valid Password";
    }

    let registerPasswordValue = registerPassword.value;
    let registerPasswordValidation = document.getElementById("registerPasswordValidation");
    if (registerPasswordValue.length < 3) {
        registerPassword.setAttribute("class", "form-control is-invalid");
        registerPasswordValidation.setAttribute("class", "invalid-feedback");
        registerPasswordValidation.innerHTML = "Password less than 3 letters";
    } else {
        registerPassword.setAttribute("class", "form-control is-valid");
        registerPasswordValidation.setAttribute("class", "valid-feedback");
        registerPasswordValidation.innerHTML = "Valid Password";
    }
};

if (!+[1,]) {
    loginEmail.onpropertychange = monitorInput;
    registerEmail.onpropertychange = monitorInput;
    loginPassword.onpropertychange = monitorInput;
    registerPassword.onpropertychange = monitorInput;
} else {
    loginEmail.oninput = monitorInput;
    registerEmail.oninput = monitorInput;
    loginPassword.oninput = monitorInput;
    registerPassword.oninput = monitorInput;
}