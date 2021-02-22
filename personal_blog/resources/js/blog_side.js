function searchArticle() {
    let keyword = $.trim($("#search").val());
    let type = $("input[name='searchRadio']:checked")[0].id;
    if (keyword.length == 0 || keyword.length > 20 || keyword.indexOf("%") >= 0) {
        alert("Fail: Keyword is invalid or over 20 letters");
        $("#search").focus();
        $("#search").val("");
        return false;
    }
    if (type == "searchArticle") {
        location.href = "/blog-search-article/1-" + keyword;
    } else {
        location.href = "/blog-search-content/1-" + keyword;
    }
}