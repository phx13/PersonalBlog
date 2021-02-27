var UEditor;
$(document).ready(function ($) {
    UEditor = UE.getEditor('UEditor', {
        autoHeightEnabled: true,
        autoFloatEnabled: true,
        initialFrameHeight: 500
    });
    $("#updateBtn")[0].style.display = "none";
    $("#deleteBtn")[0].style.display = "none";
    $("#draftBtn")[0].style.display = "none";
    $("#publishBtn")[0].style.display = "none";
});

function newBlog() {
    $("#blogId").val("");
    $("#blogTitle").val("");
    $("#blogType").val("");
    $("#filenameLabel").html("Choose thumb image");
    $("#thumb").attr("src", "");
    UEditor.setContent("");

    $("#updateBtn")[0].style.display = "none";
    $("#deleteBtn")[0].style.display = "none";
    $("#draftBtn")[0].style.display = "none";
    $("#publishBtn")[0].style.display = "none";
    $("#draftBtn")[0].style.display = "inline-block";
    $("#publishBtn")[0].style.display = "inline-block";
}

function loadBlog(id) {
    $.post('/post-blog/load', "id=" + id, function (data) {
        $("#blogId").val(data.id);
        $("#blogTitle").val(data.article);
        $("#blogType").val(data.type);
        $("#filenameLabel").html(data.thumb);
        $("#thumb").attr("src", data.thumb + "?r" + Math.random());
        base64src = data.thumb;
        UEditor.setContent(data.content);

        $("#updateBtn")[0].style.display = "none";
        $("#deleteBtn")[0].style.display = "none";
        $("#draftBtn")[0].style.display = "none";
        $("#publishBtn")[0].style.display = "none";
        if (data.draft === 0) {
            $("#draftBtn")[0].style.display = "inline-block";
            $("#updateBtn")[0].style.display = "inline-block";
            $("#deleteBtn")[0].style.display = "inline-block";
        } else {
            $("#draftBtn")[0].style.display = "inline-block";
            $("#publishBtn")[0].style.display = "inline-block";
            $("#deleteBtn")[0].style.display = "inline-block";
        }
    })
}

function postBlog(status) {
    let id = $.trim($("#blogId").val());
    let article = $.trim($("#blogTitle").val());
    let type = $.trim($("#blogType").val());
    let content = UEditor.getContent();
    let draft = 0;
    let update = 0;
    if (status == "draft") {
        draft = 1;
    } else if (status == "update") {
        update = 1;
    }

    let formData = new FormData();
    formData.append("id", id);
    formData.append("article", article);
    formData.append("type", type);
    formData.append("content", content);
    formData.append("thumb", base64src);
    formData.append("draft", draft);
    formData.append("update", update);
    $.ajax({
        url: "/post-blog/blog",
        type: "POST",
        cache: false,
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                setTimeout('location.reload()', 500);
            }
        }
    });
}

function deleteBlog() {
    let id = $.trim($("#blogId").val());
    $.ajax({
        url: "/post-blog/blog/" + id,
        type: 'delete',
        success: function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                setTimeout('location.reload()', 500);
            }
        }
    });
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
        $("#thumb").attr("src", reader.result);
    };
}