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

function addReply(articleId, commentId) {
    let content = $.trim($("#replyArea" + commentId).val());
    let param = "article_id=" + articleId + "&comment_id=" + commentId + "&content=" + content;
    $.post('/reply', param, function (data) {
        alert(data);
        if (data.startsWith("Success")) {
            setTimeout('location.reload()', 500);
        }
    })
}

function updateOpinion(commentId, type) {
    let param = "comment_id=" + commentId + "&type=" + type;
    $.post('/opinion', param, function (data) {
        alert(data);
        if (data.startsWith("Success")) {
            setTimeout('location.reload()', 500);
        }
    })
}

function addRate(articleId) {
    try {
        let rateBtn = $.trim($("#rateBtn").html());
        if (rateBtn == "Rated") {
            alert("Fail: You have rated");
            return false;
        }
        let rate = $("input[name='rate']:checked")[0].value;
        let param = "article_id=" + articleId + "&rate=" + rate;
        $.post('/rate', param, function (data) {
            alert(data);
            if (data.startsWith("Success")) {
                setTimeout('location.reload()', 500);
            }
        })
    } catch (error) {
        alert("Fail: Please choose a rate star");
    }
}

$(document).ready(function () {
    $(".custom-section img").each(function(){
        $(this).attr("src", $(this).attr("src") + "?r" + Math.random());
    });
})