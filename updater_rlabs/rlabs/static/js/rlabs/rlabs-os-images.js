


function show_images(image, index){	
	img = getImg_sys(image.os);
	var table = document.getElementById("table_lab_" + image.lab_id );
	var new_row = table.insertRow();
	new_row.setAttribute("class", "image");	
	var new_cell = new_row.insertCell();
	new_cell.setAttribute("style", "text-align: right;");
	new_cell.innerHTML ="<img class='status_equipo' height='30px' src='../static/images/" + img + "' " +
						"data-lab_id='" + image.lab_id + "'>" 
	new_cell = new_row.insertCell();	
	new_cell.innerHTML = "<span> " + image.os + " </span>"
	new_cell = new_row.insertCell();
	new_cell.innerHTML = "<span><button type='button' class='btn btn-outline-secondary'" +
							"onClick='select_mode_connect(event)'" +
							"data-ou_id='" +image.ou_id + "'" +
							"data-image_id='" + image.id + "'" +
							"data-lab_id='" + image.lab_id + "'" +
						">Reservar</button></span>"

}


function delete_images(){
	delete_by_class('image');	
}

function getImg_sys(sys){	
	var os = sys.split(" ")[0];	
	var img;
	
	switch (os) {
		case 'Windows':
				img = 'windows.png'
			break;
		case 'OSX':
			img = 'osx.png'
		break;
			
		default:
			img = 'tux.png'		
			break;
	}
	
	return img;
}
