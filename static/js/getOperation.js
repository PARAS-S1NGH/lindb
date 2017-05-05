$(function() {
    $('#btnOperation').click(function(){

        $.ajax({
            url:'/getOperations',
            data: $('#getOps').serialize(),
            type: 'POST',
            success: function(response) {
                alert(response);
				
				populateTable(response);
				
            },
            error: function(error) {
				alert("ERROR");
                alert(error);
            }
        });
    });
});



function populateTable(data){
	
	var table = document.getElementById('resultsTable');
	
	for(var i=0; i<data.length; i++){
		
		var tr = document.createElement('tr');
		
		for(var j=0; j<5; j++){
			
			var td = document.createElement('td');
			
			td.innerHTML = data[i][j];
			
			tr.appendChild(td);
			
		}
		
		table.appendChild(tr);
		
	}
	
}