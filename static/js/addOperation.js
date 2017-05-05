$(function() {
    $('#btnAddOperation').click(function(){

            $.ajax({
            url:'/addOperation',
            data: $('#addOps').serialize(),
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