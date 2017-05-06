$(function() {
    $('#btnaddValue').click(function(){

            $.ajax({
            url:'/addValue',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                alert(response);
            },
            error: function(error) {
                alert(error);
            }
        });
    });
});