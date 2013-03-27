var SEARCH_URL = 'search/';
var SINGLE_SEARCH_URL = 'search/a/';
var E_DICT = ['tmall', 'amazon'];

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
            alert(json.data[term].value.price);
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
