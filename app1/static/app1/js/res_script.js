console.log("aasdsas");
$(document).ready(function (e) {
    $(document).on('click','.dropdown-item-option',(e)=>{
        var ele = $(e.target)
        var data_for = ele.attr('data-traget'),
            data_text = ele.text();
        if(data_for && data_text){
            $(data_for).text(data_text);
            if(data_for == '#Categories') $('#book_filter_name').text(data_text);
            $('.product-main-div').html('<div class="center-child w-100"><img src="https://i.pinimg.com/originals/ee/1d/08/ee1d081c5bdf966b058c1a6588e73e8a.gif" alt="Loading..."></div>');
            $.ajax({
                url : '/next_level/books/filter/',
                data : {'categories':data_text, 'price':$('#price').text() },
                dataType : 'json',
                type: 'POST',
                success: function (response) {
                    if(response.result)
                    $('.product-main-div').html(response.result);
                },
                error: function(xhr, status) {
                    $('.product-main-div').html('Server Error.Our genius Engineer are fixing it.');
                }
            });
        }
    })
})