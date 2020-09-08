console.log("aasdsas");
$(document).ready(function (e) {
    $(document).on('click','.image_field_hover',(e)=>{
        $(e.target).siblings('input').click();
    })
    $(document).on('change','input[data-input="image"]',(e)=>{
        var input = e.currentTarget;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $(input).siblings('.image_field_img').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    })
    
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