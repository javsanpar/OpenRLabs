

xhr = new XMLHttpRequest();

function requestAJAX(url, parametros, callbackFunction){

    xhr.open("POST", url, true);
    xhr.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');    
    document.getElementById("table_ous").setAttribute("style", "cursor:progress;");
    document.body.setAttribute("style", "cursor:progress;");
    xhr.send(parametros);        

    xhr.onreadystatechange = function() {
        if (xhr.readyState == 4 && xhr.status == 200) {        	
        	var respuesta = JSON.parse(xhr.responseText);        	
        	document.getElementById("table_ous").setAttribute("style", "cursor:pointer;");
        	document.body.style.cursor = "pointer";
        	if (respuesta.error === undefined) { 
	        	
	        	// Use callback for synchronize ajax response with html view        	
	            callbackFunction(respuesta);
	            
	        } else {
	        	alert(respuesta.error);
	        	refresh_page();
	        	//document.getElementById("buttonConsole").style.display = 'block';
	        	//reset_progress_bar();
	        }
        } 
    }    	
}
