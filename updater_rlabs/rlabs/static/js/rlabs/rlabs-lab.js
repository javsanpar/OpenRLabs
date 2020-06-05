

function show_Labs(labs){
	delete_labs();	
	labs.forEach(show_Lab);
}


function delete_labs(){	
	delete_by_class('lab');
}


function show_Lab(lab, index){	
	delete_disponibles();
	// Buscar span id y añadir elemento 	
	var table = document.getElementById("table_ou_" + lab.ou.id);
	table.setAttribute("style", "background:NONE;");
	var new_row = table.insertRow();
	new_row.setAttribute("id", "lab_" + lab.id);
	new_row.setAttribute("class", "lab");
	new_row.setAttribute("style", "display:block;");
	var htmlRow =	"<td width='16'>" +
							"<img src='../static/images/aula.png' "  + 
									"data-ou='" + lab.ou.id + "' " +
									"data-lab_id='" + lab.id + "' onClick='get_remotePCs(event)'>" +
						"</td>" +
						"<td>" +
							"<table id='table_lab_" + lab.id + "'>" +
								"<tbody>" +
									"<tr>" +
										"<td>" +									
											"<span class='labs' " +
												"data-ou='" + lab.ou.id + "' " +
												"data-lab_id='" + lab.id + "' onClick='get_remotePCs(event)'>" +
												lab.name + "</span>" +
										"</td>"+
									"</tr>"
	
	if (typeof(lab.status) !== 'undefined') {
		console.log(lab);
		htmlRow = htmlRow +			"<tr>" +
										"<td>" +									
										"<span id='disponibles_before_images_lab_" + lab.id + "' class='disponible' " +
										"data-ou='" + lab.ou.id + "' " +
										"data-lab_id='" + lab.id + "' onClick='get_remotePCs(event)'>   " +
										lab.status.clients_disponibles + " de " + lab.status.clients_total + " equipos disponibles</span>" +
										"</td>"+																					
									"</tr>"
	}
	
	
	htmlRow = htmlRow + "</tbody>" + "</table>" + "</td>"
								
    new_row.innerHTML = htmlRow;
}

