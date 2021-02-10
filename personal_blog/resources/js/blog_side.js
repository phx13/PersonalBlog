function searchArticle() {
    let keyword = $.trim($("#search").val());
    if (keyword.length == 0 || keyword.length > 10 || keyword.indexOf("%") >= 0) {
        alert("Fail: Search invalid");
        $("#search").focus();
        $("#search").val("");
        return false;
    }
    location.href = "/blog-search/1-" + keyword;
}