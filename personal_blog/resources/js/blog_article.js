function cancelCollection(articleId) {
    $.ajax({
        url: '/collection/' + articleId,
        type: 'delete',
        success: function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                $("#collection").html("Welcome you collect again");
                $("#collection").attr("onclick", "").unbind("click");
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
        }
    })
}