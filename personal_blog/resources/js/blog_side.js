function searchBlog() {
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

function sortArticle() {
    let currentSort = $.trim($("#sort").html());
    if (currentSort === "Sort By Desc") {
        let param = "sort=1";
        $.get(location.href, param, function (data) {
            $(document.body).html(data);
            $("#sort").html(" Sort By Asc");
        })
    } else if (currentSort === "Sort By Asc") {
        let param = "sort=0";
        $.get(location.href, param, function (data) {
            $(document.body).html(data);
            $("#sort").html(" Sort By Desc");
        })
    }
}

function typeBlog(element) {
    let currentType = element.text;
    location.href = "/blog-type/1-" + currentType;
}