

function show_PCs(PCs){
	reset_style_table_lab(PCs.images_info[0].lab_id)
	delete_pcs();
	delete_images();
	delete_spaces();
	hide_footer();	
	PCs.images_info.forEach(show_images);
	if (PCs.images_info[0] !== undefined){
		insert_space_table_lab(PCs.images_info[0].lab_id);
	}
	delete_disponibles();
	insert_disponibles_before_pcs(PCs.disponibles_info);	
	PCs.PCs_info.forEach(show_PC);
	cursor_wait('pointer');
	table_lab = document.getElementById('lab_' + PCs.images_info[0].lab_id);
	table_lab.setAttribute("style", "background : white;display:block;");;
	
	
}

function reset_style_table_lab(table_lab_id){
	table_lab = document.getElementById('lab_' + table_lab_id);
	table_lab.setAttribute("style", "background : white;display:block;cursor:pointer");
	
}


function show_PC(PC, index){		
	var img = getImg_pc(PC.pc.status);	

	// Buscar span id y añadir elemento 
	var table = document.getElementById("table_lab_" + PC.pc.lab.id );
	
	var new_row = table.insertRow();
	new_row.setAttribute("id", "pc_" + PC.pc.id);
	new_row.setAttribute("style", "display:block;");
	new_row.setAttribute("class", "pc");
	var new_cell = new_row.insertCell();
	new_cell.innerHTML ="<img class='status_equipo' src='../static/images/" + img + "' " +
							"data-id='" + PC.pc.id + 
							"'>" 
	new_cell = new_row.insertCell();
	new_cell.innerHTML = "<table id='table_PCs' class='nivel2 table_PCs'>" +
							"<tr id='PC_" + PC.pc.id + "'>" +
								"<td>" +
									"<span data-id='" + PC.pc.id + 
										"'> " +
									PC.pc.name + "</span>" +
								"</td>"	+
							"</tr>" +
							"<tr>" +
								"<table id='table_partitions_" + PC.pc.id + "' class='nivel3 partitions_table'>" +
							"</tr>" +
					"</table>"
	
}

function delete_pcs(){
	delete_by_class('pc');	
}


function insert_space_table_lab(lab_id){
	var table = document.getElementById("table_lab_" + lab_id );	
	var new_row = table.insertRow();
	new_row.setAttribute("class", "space");
	var new_cell = new_row.insertCell();
	new_cell.innerHTML = "<span>&nbsp;</span>"	
}

function delete_spaces(){
	delete_by_class('space');	
}

function getImg_pc(status){	
	var img;
	if ((typeof(status.status) === "undefined")) {
		img = 'odernador_OFF.png'
	} else {							
		switch (status.status) {
			case 'off':
				img ="odernador_OFF.png"
				break;							
		
			case 'WIN':
			case 'windows':
				if (('loggedin' in status) && (status.loggedin == true)) {
					img = 'odernador_WINS.png'
				} else {
					img = 'odernador_WIN.png'
				}
				break;
			case 'LNX':
			case 'linux':
				if (('loggedin' in status) && (status.loggedin == true)) {
					img = 'odernador_LINS.png'
				} else {
					img = 'odernador_LIN.png'
				}
				break;
			case 'OSX':
				img = "odernador_OSX.png"
				break;
			case 'oglive':
				img = "odernador_OPG.png"
				break;
			case 'busy':
				img ="odernador_BSY.png"
				break;
			default:
				img = "odernador_OSX.png";
		
		}
	}
		
	return img;
}



