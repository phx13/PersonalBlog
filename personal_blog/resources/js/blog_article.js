function cancelCollection(articleId) {
    $.ajax({
        url: '/collection/' + articleId,
        type: 'delete',
        success: function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#collection").html("Welcome you collect again");
                $("#collection").attr("onclick", "").unbind("click");
                setTimeout('location.reload()', 1000);
            }
        }
    });
}

function addCollection(articleId) {
    let param = "article_id=" + articleId;
    $.post('/collection', param, function (data) {
        alert(data);
        if (data.startsWith("Success")) {
            $("#collection").html("Thanks for your collection");
            $("#collection").attr("onclick", "").unbind("click");
            setTimeout('location.reload()', 1000);
        }
    })
}

function addComment(articleId) {
    let content = $.trim($("#commentArea").val());
    let param = "article_id=" + articleId + "&content=" + content;
    $.post('/comment', param, function (data) {
        alert(data);
        if (data.startsWith("Success")) {
            setTimeout('location.reload()', 500);
        }
    })
}