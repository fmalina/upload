function ID(id){return document.getElementById(id);}
function N1(t,e){return e.getElementsByTagName(t)[0];}
var Up = {
	tests: {
		filereader: typeof FileReader != 'undefined',
		dnd: 'draggable' in document.createElement('span'),
		formdata: !!window.FormData,
		progress: "upload" in new XMLHttpRequest
	},
	url: '',
	form_tpl: '',
	add_form: function(i){
		var drop = ID('drop'),
			total = ID('id_file_set-TOTAL_FORMS');
		var form = Up.form_tpl.replace(/__prefix__/g, total.value),
			id = 'id_file_set-' + total.value + '-',
			tmp = document.createElement('div');
		tmp.innerHTML = form; form = tmp.firstChild; form.id = id;
		drop.parentNode.insertBefore(form, drop);
		total.value = parseInt(total.value) + 1;
		return id;
	},
	fill_form: function(id, xhr_response){
		console.log(xhr_response);
		var data = eval('(' + xhr_response + ')'); // safe source
		var img = N1('img', ID(id));
		img.src = data.url;
		ID(id+'id').value = data.id;
	},
	post: function(i, data){
		return function(){
			var xhr = new XMLHttpRequest();
			var id = Up.add_form();
			xhr.onreadystatechange = function(){
				if(xhr.readyState==4){
					Up.fill_form(id, xhr.responseText);
				}
			};
			// Progress bar shows how much we've got
			var bar = N1('span', ID(id));
			var got = N1('i', bar);
			bar.style.display = 'block';
			xhr.onload = function() {
				got.style.width = '100%';
				setTimeout(function(){bar.style.display = 'none';}, 1000);
			};
			if(Up.tests.progress){
				xhr.upload.onprogress = function(event){
					if(event.lengthComputable){
						var complete = (event.loaded / event.total * 140 | 0);
						got.style.width = complete + 'px';
					}
				}
			}
			xhr.open('POST', Up.url);
			xhr.setRequestHeader("X-Requested-With", "XMLHttpRequest");
			xhr.send(data);
		}
	},
	read: function(files){
		var qs = [];
		for(var i=0; i < files.length; i++){
			if(Up.tests.formdata){
				var data = new FormData();
				var token = 'csrfmiddlewaretoken';
				data.append(token, document.forms[0][token].value);
				data.append('file', files[i]);
				qs[i] = Up.post(i, data);
			}
		}
		for(var j=0; j < qs.length; j++){
			qs[j](); // run requests
		}
	},
	load: function(){
		var d = ID('droparea'),
			file = ID('file'),
			add = ID('add');
		if(Up.tests.dnd && Up.tests.filereader){
			d.style.display = 'block';
			d.ondragover = function( ){this.className='hover';return false;}
			d.ondragend  = function( ){this.className='';     return false;}
			d.ondrop     = function(e){this.className='';
				e.preventDefault();
				Up.read(e.dataTransfer.files);
			}
		}
		if(Up.tests.filereader){
			add.style.display = 'block';
			var rm = document.getElementsByClassName('default-upload');
			for(var i=rm.length;i--;){rm[i].parentNode.removeChild(rm[i]);}
			add.onclick = d.onclick = function(e){
				e.preventDefault();
				file.click();
			}
			file.onchange = function(e){
				Up.read(e.target.files);
			}
		}
	}
}