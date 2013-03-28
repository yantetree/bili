var SEARCH_URL = 'search/';
var SINGLE_SEARCH_URL = 'search/a/';
var E_DICT = ['tmall', 'amazon'];
var NAME_DICT = {
    tmall: "天猫",
    amazon: "亚马逊"
}

var REPLACE_HTML = 
    "<div class=\"res row\">" +  
    "   <a href=\"%HREF%\"><img class=\"img-rounded\"src=\"%SRC%\" height=\"150\"></a>" +
    "   <span class=\"label label-info\">%ENAME%</span>" +
    "   <span class=\"price\">%PRICE%</span>" +
    "</div>";

function searchRequest(term){
    var data = {
        k: $('#cmp-input').val()
    };
    data[term] = '';
    $.ajax({
        type: "GET",
        timeout: 5000,
        url: SINGLE_SEARCH_URL,
        data: data,
        error: function(){ alert("error occurred"); },
        success: function(json){
            var value = json.data[term].value;
            html = REPLACE_HTML.replace(/%HREF%/, value.href)
                               .replace(/%SRC%/, value.img)
                               .replace(/%ENAME%/, NAME_DICT[term])
                               .replace(/%PRICE%/, value.price);
            $("#res-wrap").append(html);
        },
        dataType: "json"
    });
};

$('document').ready(function(){
    var slideFlag = false;

    $('#cmp-btn').click(function(){
        if(!slideFlag){
            slideFlag = ~slideFlag;
            $("#search-wrap").animate({
                marginTop: "2em"
            }, 500);
        }
        var terms = [];
        $("#res-wrap").html("");
        $("#checkbox-wrap input[type='checkbox']").each(function(){
            if($(this).prop("checked")){
                terms.push($(this).attr("value"));
            }
        })
        for(var i = 0; i != terms.length; ++i){
            searchRequest(terms[i]);
        }
    });
})
