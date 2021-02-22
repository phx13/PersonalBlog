var UEditor;
$(document).ready(function ($) {
    UEditor = UE.getEditor('UEditor', {
        autoHeightEnabled: true,
        autoFloatEnabled: true,
        initialFrameHeight: 500
    });
});

function newBlog() {
    $("#blogId").val("");
    $("#blogTitle").val("");
    $("#blogType").val("");
    $("#filenameLabel").html("");
    document.getElementById('thumb').src = "";
    UEditor.setContent("");
}

function loadBlog(id) {
    $.post('/post-blog/draft', "id=" + id, function (data) {
        $("#blogId").val(data.id);
        $("#blogTitle").val(data.article);
        $("#blogType").val(data.type);
        $("#filenameLabel").html(data.thumb);
        document.getElementById('thumb').src = data.thumb;
        base64src = data.thumb;
        UEditor.setContent(data.content);
    })
}

function postBlog(status) {
    let id = $.trim($("#blogId").val());
    let article = $.trim($("#blogTitle").val());
    let type = $.trim($("#blogType").val());
    let content = UEditor.getContent();
    let draft = 0;
    if (status == 'draft') {
        draft = 1;
    }
    let param = "content=" + content;
    param += "&draft=" + draft;
    param += "&article=" + article;
    param += "&type=" + type;
    param += "&thumb=" + base64src;
    param += "&id=" +id;
    $.post('/post-blog/post', param, function (data) {
        alert(data);
        if (data.startsWith("Success")) {
            setTimeout('location.reload()', 500);
        }
    })
}

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
        document.getElementById('thumb').src = reader.result;
    };
}