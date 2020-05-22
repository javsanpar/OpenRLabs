

function reset_modal(){	
	document.getElementById("text_consolelog").value = '';    
	document.getElementById("buttonConsole").style.display = 'none';
	reset_progress_bar();
	delete_pcs();
	delete_images();
	delete_disponibles();
}
