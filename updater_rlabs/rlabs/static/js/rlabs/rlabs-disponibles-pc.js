

function insert_disponibles_before_pcs(disponibles_info){
	var table = document.getElementById("table_lab_" + disponibles_info.lab_id );	
	var new_row = table.insertRow();
	new_row.setAttribute("style", "display:block;");
	new_row.setAttribute("id", "disponibles_before_pcs_lab_" + disponibles_info.lab_id);
	new_row.setAttribute("class", "disponible");
	var new_cell = new_row.insertCell();
	new_cell.innerHTML = disponibles_info.disponibles + " de " + disponibles_info.total + " equipos disponibles"; 
	
}


function delete_disponibles(){
	delete_by_class('disponible');
}

function delete_disponible_before_images(lab_id){	
	document.getElementById("disponibles_before_images_lab_" + lab_id).remove();
}

