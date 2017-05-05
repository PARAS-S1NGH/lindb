$(function() {
    $('#btnaddPatient').click(function(){

            $.ajax({
            url:'/addPatient',
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