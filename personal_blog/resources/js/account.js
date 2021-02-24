var base64src = ""

function fileChange(element) {
    $("#filenameLabel").html(element.files[0].name);
    if (!/image\/\w+/.test(element.files[0].type)) {
        return false;
    }
    let reader = new FileReader();
    reader.readAsDataURL(element.files[0]);
    reader.onload = function () {
        base64src = reader.result;
        document.getElementById('avatar').src = reader.result;
    };
}

function updateProfile() {
    let nickname = $("#inputNickname").val();
    let password = $("#inputPassword").val();
    let profile = $("#inputProfile").val();
    let formData = new FormData();
    formData.append("avatar", base64src);
    formData.append("nickname", nickname);
    formData.append("password", password);
    formData.append("profile", profile);
    $.ajax({
        url: "/account/profile",
        type: 'POST',
        cache: false,
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data);
            setTimeout('window.location.href="/logout";', 500)
        },
        error: function (data) {
        }
    });
}

function cancelCollection(articleId) {
    $.ajax({
        url: '/collection/' + articleId,
        type: 'delete',
        success: function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#collection").html("Welcome you collect again");
                setTimeout('location.reload()', 1000);
            }
        }
    });
}