xhr=new XMLHttpRequest();function requestAJAX(url,parametros,callbackFunction){xhr.open("POST",url,true);xhr.setRequestHeader('Content-type','application/x-www-form-urlencoded');document.getElementById("table_ous").setAttribute("style","cursor:progress;");document.body.setAttribute("style","cursor:progress;");xhr.send(parametros);xhr.onreadystatechange=function(){if(xhr.readyState==4&&xhr.status==200){var respuesta=JSON.parse(xhr.responseText);document.getElementById("table_ous").setAttribute("style","cursor:pointer;");document.body.style.cursor="pointer";if(respuesta.error===undefined){callbackFunction(respuesta);}else{alert(respuesta.error);refresh_page();}}}}
function insert_disponibles_before_pcs(disponibles_info){var table=document.getElementById("table_lab_"+disponibles_info.lab_id);var new_row=table.insertRow();new_row.setAttribute("style","display:block;");new_row.setAttribute("id","disponibles_before_pcs_lab_"+disponibles_info.lab_id);new_row.setAttribute("class","disponible");var new_cell=new_row.insertCell();new_cell.innerHTML=disponibles_info.disponibles+" de "+disponibles_info.total+" equipos disponibles";}
function delete_disponibles(){delete_by_class('disponible');}
function delete_disponible_before_images(lab_id){document.getElementById("disponibles_before_images_lab_"+lab_id).remove();}
function hide_footer(){var footers=document.getElementsByClassName('footer');footers[0].style.display='none';}
function show_footer(){var footers=document.getElementsByClassName('footer');footers[0].style.display='block';}
function show_Labs(labs){delete_labs();labs.forEach(show_Lab);}
function delete_labs(){delete_by_class('lab');}
function show_Lab(lab,index){delete_disponibles();var table=document.getElementById("table_ou_"+lab.ou.id);table.setAttribute("style","background:NONE;");var new_row=table.insertRow();new_row.setAttribute("id","lab_"+lab.id);new_row.setAttribute("class","lab");new_row.setAttribute("style","display:block;");var htmlRow="<td width='16'>"+
"<img src='../static/images/aula.png' "+
"data-ou='"+lab.ou.id+"' "+
"data-lab_id='"+lab.id+"' onClick='get_remotePCs(event)'>"+
"</td>"+
"<td>"+
"<table id='table_lab_"+lab.id+"'>"+
"<tbody>"+
"<tr>"+
"<td>"+
"<span class='labs' "+
"data-ou='"+lab.ou.id+"' "+
"data-lab_id='"+lab.id+"' onClick='get_remotePCs(event)'>"+
lab.name+"</span>"+
"</td>"+
"</tr>"
if(typeof(lab.status)!=='undefined'){console.log(lab);htmlRow=htmlRow+"<tr>"+
"<td>"+
"<span id='disponibles_before_images_lab_"+lab.id+"' class='disponible' "+
"data-ou='"+lab.ou.id+"' "+
"data-lab_id='"+lab.id+"' onClick='get_remotePCs(event)'>   "+
lab.status.clients_disponibles+" de "+lab.status.clients_total+" equipos disponibles</span>"+
"</td>"+
"</tr>"}
htmlRow=htmlRow+"</tbody>"+"</table>"+"</td>"
new_row.innerHTML=htmlRow;}
function reset_modal(){document.getElementById("text_consolelog").value='';document.getElementById("buttonConsole").style.display='none';reset_progress_bar();delete_pcs();delete_images();delete_disponibles();}
function show_images(image,index){img=getImg_sys(image.os);var table=document.getElementById("table_lab_"+image.lab_id);var new_row=table.insertRow();new_row.setAttribute("class","image");var new_cell=new_row.insertCell();new_cell.setAttribute("style","text-align: right;");new_cell.innerHTML="<img class='status_equipo' height='30px' src='../static/images/"+img+"' "+
"data-lab_id='"+image.lab_id+"'>"
new_cell=new_row.insertCell();new_cell.innerHTML="<span> "+image.os+" </span>"
new_cell=new_row.insertCell();new_cell.innerHTML="<span><button type='button' class='btn btn-outline-secondary'"+
"onClick='select_mode_connect(event)'"+
"data-ou_id='"+image.ou_id+"'"+
"data-image_id='"+image.id+"'"+
"data-lab_id='"+image.lab_id+"'"+
">Reservar</button></span>"}
function delete_images(){delete_by_class('image');}
function getImg_sys(sys){var os=sys.split(" ")[0];var img;switch(os){case 'Windows':img='windows.png'
break;case 'OSX':img='osx.png'
break;default:img='tux.png'
break;}
return img;}
function show_PCs(PCs){reset_style_table_lab(PCs.images_info[0].lab_id)
delete_pcs();delete_images();delete_spaces();hide_footer();PCs.images_info.forEach(show_images);if(PCs.images_info[0]!==undefined){insert_space_table_lab(PCs.images_info[0].lab_id);}
delete_disponibles();insert_disponibles_before_pcs(PCs.disponibles_info);PCs.PCs_info.forEach(show_PC);cursor_wait('pointer');table_lab=document.getElementById('lab_'+PCs.images_info[0].lab_id);table_lab.setAttribute("style","background : white;display:block;");;}
function reset_style_table_lab(table_lab_id){table_lab=document.getElementById('lab_'+table_lab_id);table_lab.setAttribute("style","background : white;display:block;cursor:pointer");}
function show_PC(PC,index){var img=getImg_pc(PC.pc.status);var table=document.getElementById("table_lab_"+PC.pc.lab.id);var new_row=table.insertRow();new_row.setAttribute("id","pc_"+PC.pc.id);new_row.setAttribute("style","display:block;");new_row.setAttribute("class","pc");var new_cell=new_row.insertCell();new_cell.innerHTML="<img class='status_equipo' src='../static/images/"+img+"' "+
"data-id='"+PC.pc.id+
"'>"
new_cell=new_row.insertCell();new_cell.innerHTML="<table id='table_PCs' class='nivel2 table_PCs'>"+
"<tr id='PC_"+PC.pc.id+"'>"+
"<td>"+
"<span data-id='"+PC.pc.id+
"'> "+
PC.pc.name+"</span>"+
"</td>"+
"</tr>"+
"<tr>"+
"<table id='table_partitions_"+PC.pc.id+"' class='nivel3 partitions_table'>"+
"</tr>"+
"</table>"}
function delete_pcs(){delete_by_class('pc');}
function insert_space_table_lab(lab_id){var table=document.getElementById("table_lab_"+lab_id);var new_row=table.insertRow();new_row.setAttribute("class","space");var new_cell=new_row.insertCell();new_cell.innerHTML="<span>&nbsp;</span>"}
function delete_spaces(){delete_by_class('space');}
function getImg_pc(status){var img;if((typeof(status.status)==="undefined")){img='odernador_OFF.png'}else{switch(status.status){case 'off':img="odernador_OFF.png"
break;case 'WIN':case 'windows':if(('loggedin'in status)&&(status.loggedin==true)){img='odernador_WINS.png'}else{img='odernador_WIN.png'}
break;case 'LNX':case 'linux':if(('loggedin'in status)&&(status.loggedin==true)){img='odernador_LINS.png'}else{img='odernador_LIN.png'}
break;case 'OSX':img="odernador_OSX.png"
break;case 'oglive':img="odernador_OPG.png"
break;case 'busy':img="odernador_BSY.png"
break;default:img="odernador_OSX.png";}}
return img;}
function hide_progress_bar(animator){var progress_bar_container=document.getElementById("progress_bar_container");progress_bar_container.style.display='none';clearInterval(animator);document.getElementById("progress_bar").setAttribute("value","0");document.getElementById("progress_value").innerHTML="0%";}
function show__progress_bar(){var progress_bar=document.getElementById("progress_bar_container");progress_bar.style.display='block';var data_time=parseInt(document.getElementById('progress_bar').getAttribute('data-time'));var time=data_time*10
var progressbar=$('#progress_bar'),max=progressbar.attr('max'),time=time,value=progressbar.val();var loading=function(){value+=1;addValue=progressbar.val(value);$('.progress_value').html(value+'%');if(value==max){clearInterval(animate);}};var animate=setInterval(function(){loading();},time);return animate;}
function stop_progress_bar(){clearInterval(animator);document.getElementById("progress_bar").setAttribute("value","100");}
function reset_progress_bar(){clearInterval(animator);document.getElementById("progress_bar").setAttribute("value","0");document.getElementById("progress_value").innerHTML="0%";}
function delete_by_class(class_name){var class_items=document.getElementsByClassName(class_name);for(i=class_items.length-1;i>-1;i--){class_items[i].remove();}}
function hide_by_class(class_name){var class_items=document.getElementsByClassName(class_name);for(i=0;i<class_items.length-1;i++){class_items[i].style.display='none';}}