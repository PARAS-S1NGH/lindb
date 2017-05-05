$(function() {
    $('#btnAddOperation').click(function(){

            $.ajax({
            url:'/addOperation',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                alert(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});

$(function() {
    $('#btnSignUp').click(function(){

            $.ajax({
            url:'/addOperation',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});