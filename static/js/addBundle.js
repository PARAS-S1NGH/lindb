$(function() {
    $('#btnaddBundle').click(function(){

            $.ajax({
            url:'/addBundle',
            data: $('#addBundleForm').serialize(),
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