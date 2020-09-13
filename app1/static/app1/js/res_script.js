console.log("aasdsas");
$(document).ready(function (e) {
    //universal
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
    function get_data_from_form(form){
        var data = {};
        form.find('input').map((index,input)=>{
            if( $(input).attr('type') == 'file')
               data[$(input).attr('name')] = $($(input).attr('preview-ele')).attr('src');
            if( $(input).attr('type') == 'text' || $(input).attr('type') == 'number' || $(input).attr('type') == 'password' || $(input).attr('type') == 'email' )
                data[$(input).attr('name')] = $(input).val();
        });
        return data;
    }



    // manage book list page
    
    $(document).on('click','#book-table-view tr',(e)=>{
        window.location = $(e.target).parents('tr').attr('edit-book-url');
    });
    // specific profile page
    $(document).on('click','.form-check-label',(e)=>{
        var ele = $(e.target);
        var input = $(ele.find('input'));
        input.attr("checked", !input.attr("checked"));
        ele.toggleClass('check_account_type_active');
        if( $('.profile_submit').hasClass('d-none')) $('.profile_submit').removeClass('d-none'); 
    })
    // specific profile page
    $(document).on('change','.update_profile',(e)=>{

        if( $('.profile_submit').hasClass('d-none')) 
            $('.profile_submit').removeClass('d-none'); 
    });
    

    // books list page filter 
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
    });


    // edit a book page 
    $(document).on('click','#preview_book_page,#preview_homepage_book',(e)=>{
        var btn = $(e.target);
        var data = get_data_from_form($('#edit-book-form'));
        data['preview_for'] = btn.attr('id') == 'preview_book_page' ? 'full_page' : 'home_page';
        console.log(data['preview_for']);
        $.ajax({
            url : '/next_level/manage/books/preview/',
            data : data,
            dataType : 'json',
            type: 'POST',
            success: function (response) {
                if(response.result)
                $('#preview-ajax-div').html(response.result);
                $.fancybox.open({
                    src  : '#preview-ajax-div',
                    // type : 'iframe',
                });
            },
            error: function(xhr, status) {
                $('.product-main-div').html('Server Error.Our genius Engineer are fixing it.');
            }
        });

    });
})