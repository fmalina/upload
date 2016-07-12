// Utilities
function ID(id){return document.getElementById(id);}
function N1(t,e){return e.getElementsByTagName(t)[0];}
function addEvent(element, eventName, fn) {
    if (element.addEventListener)
        element.addEventListener(eventName, fn, false);
    else if (element.attachEvent)
        element.attachEvent('on' + eventName, fn);
}

// Upload class
var Up = {
	// configurable URL of the file upload handler
	url: '',
	// configurable HTML template to render each uploaded file
	form_tpl: '',
	// device and browser capability tests
	tests: {
		// is filereader supported
		filereader: typeof FileReader != 'undefined',
		// is drag and drop supported
		dnd: 'draggable' in document.createElement('span'),
		formdata: !!window.FormData,
		// will progress bars work
		progress: "upload" in new XMLHttpRequest,
		// is file input supported at all (not on < iOS4)
		fileinput: function(){
			var test = document.createElement("input");
			test.setAttribute("type", "file");
			return test.disabled === false;
		}
	},
	// handle adding file forms to a formset
	add_form: function(i){
		var drop = ID('drop'),
			total = ID('id_file_set-TOTAL_FORMS');
		var form = Up.form_tpl.replace(/__prefix__/g, total.value),
			id = 'id_file_set-' + total.value + '-',
			tmp = document.createElement('div');
		tmp.innerHTML = form;
		form = tmp.firstChild;
		form.id = id;
		drop.parentNode.insertBefore(form, drop.nextSibling);
		total.value = parseInt(total.value, 10) + 1;
		return id;
	},
	fill_form: function(id, xhr_response){
		var data = eval('(' + xhr_response + ')'); // safe source
		var box = ID(id);
		var img = N1('img', box);
		img.src = data.url;
		ID(id+'id').value = data.id;
		var tools = box.getElementsByTagName('a');
		var toolbox = box.querySelector('.tools');
		// show tools
		toolbox.className = toolbox.className.replace(' hide', '');
		for(var i=0; i<tools.length; i++){
			var e = tools[i];
			if(e.href.indexOf('/0') > -1){
				e.href = e.href.replace('/0', '/'+data.id);
			};
		}
	},
	post: function(i, data){
		return function(){
			var xhr = new XMLHttpRequest();
			var id = Up.add_form();
			xhr.onreadystatechange = function(){
				if(xhr.readyState==4){
					if(xhr.responseText=='error' || xhr.responseText=='small'){
						var box = ID(id);
						box.parentNode.removeChild(box);
					}
					if(xhr.responseText=='error'){
						alert('Upload a valid image. The file uploaded was '+
						'either not an image or corrupted. See FAQ for hints.');
					} else if(xhr.responseText=='small'){
						alert('Too small. Upload a larger image.');
					} else {
						Up.fill_form(id, xhr.responseText);
					}
				}
			};
			// Progress bar
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
				data.append(token, 					document.forms.namedItem('upload_form')[token].value);
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
			file = ID('file');
		if(Up.tests.dnd && Up.tests.filereader){
			d.style.display = 'block';
			d.ondragover = function( ){this.className='hover';return false;}
			d.ondragend  = function( ){this.className='';     return false;}
			d.ondrop     = function(e){this.className='';
				e.preventDefault();
				Up.read(e.dataTransfer.files);
			}
		}
		if(Up.tests.filereader || !Up.tests.fileinput()){
			var rm = document.getElementsByClassName('default-upload');
			for(var i=rm.length;i--;){rm[i].parentNode.removeChild(rm[i]);}
		}
		if(Up.tests.filereader){
			d.onclick = function(e){
				e.preventDefault();
				file.click();
			}
			file.onchange = function(e){
				Up.read(e.target.files);
			}
		}
	}
}


function sortable_uploads(){
    var list = ID("sortable");
    Sortable.create(list, {
        draggable: '.photo-edit',
        onUpdate: function(evt){
            var inputs = document.querySelectorAll('input[name$="pos"]');
			for(var i=inputs.length; i--;){
				inputs[i].value = i;
			}
        }
    });
}


// UI jQuery dependent
$(function(){
	$(document).on('click', '.rotate', function(e){
		e.preventDefault();
		var i = $(this).parent().parent().find('.img')[0];
		$.get($(this).attr('href'), function(){
			i.style.opacity = '0';
			bg = i.src;
			i.src = bg + '?';
			$(i).animate({opacity: 1}, 400);
		});
	});
	$(document).on('click', '.cover', function(e){
		e.preventDefault();
		var p = $(this).parents('.photo-edit');
		var pos = 'input[name$="pos"]';
		$(pos).val('1');
		$('.cover').removeClass('main');
		p.find(pos).val('0');
		$(this).addClass('main');
	});
});
