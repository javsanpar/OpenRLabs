

function delete_by_class(class_name){
	var class_items = document.getElementsByClassName(class_name);
	for (i = class_items.length - 1; i > -1 ; i --){
		class_items[i].remove();
	}		
}

function hide_by_class(class_name){
	var class_items = document.getElementsByClassName(class_name);	
	for (i = 0; i < class_items.length -1; i ++){
		class_items[i].style.display = 'none';
	}		
}

