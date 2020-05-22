
function hide_progress_bar(animator){
	var progress_bar_container = document.getElementById("progress_bar_container");
	progress_bar_container.style.display = 'none';
	clearInterval(animator);
	document.getElementById("progress_bar").setAttribute("value","0");
	document.getElementById("progress_value").innerHTML="0%";
}

function show__progress_bar(){
	var progress_bar = document.getElementById("progress_bar_container");
	progress_bar.style.display = 'block';
		
	var data_time = parseInt(document.getElementById('progress_bar').getAttribute('data-time'));
	/*
	 *  value = 100 -> 100 inttervalos
	 *  
	 *  (date-time segundos * 1000) milisegundos -------- 100 intervalos
	 *                            X milisegundos -------- 1 intervalo
	 *                            
	 *   1 intervalo tendrá = (date-time * 1000) / 100 milisegundos = date-time * 10 milisegundos                          
	 *           
	 */
	
	var time = data_time * 10
	
	var progressbar = $('#progress_bar'),
	    max = progressbar.attr('max'),
	    time =  time,
	    value = progressbar.val();

	 
	var loading = function() {
	      value += 1;
	      addValue = progressbar.val(value);
	       
	      $('.progress_value').html(value + '%');
	 
	      if (value == max) {
	          clearInterval(animate);                
	      }
	};
	 
	var animate = setInterval(function() {
	      loading();
	}, time);
	
	return animate;
}

function stop_progress_bar(){
	clearInterval(animator);
	document.getElementById("progress_bar").setAttribute("value","100");
	//document.getElementById("progress_value").innerHTML="100%";	
}

function reset_progress_bar(){
	clearInterval(animator);
	document.getElementById("progress_bar").setAttribute("value","0");
	document.getElementById("progress_value").innerHTML="0%";	
}
