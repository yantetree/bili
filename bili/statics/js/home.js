var SEARCH_URL = 'search/'
$('document').ready(function(){
    $('#cmp-btn').click(function(){
        alert("hehe");
        var data = {
            k: $('#cmp-input').attr('value'),
        };
        $("#checkbox-wrap input[type='checkbox']").each(function(){
            if($(this).prop("checked")){
                data[$(this).attr("value")] = null;
            }
        })
        $.getJSON(
            SEARCH_URL,
            data,
            function(json){
                alert(json.data.value.tmall.price);
            }
        );
    });
});
