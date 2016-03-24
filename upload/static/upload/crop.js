(function($){
	$.imageCrop = function(object, customOptions){
		var defaultOptions = {
			allowMove: true,
			allowResize: true,
			allowSelect: true,
			aspectRatio: 0,
			minSelect: [50, 50],
			minSize: [0, 0],
			maxSize: [0, 0],
			outlineOpacity: 0.5,
			areaPos: [0, 0],
			areaWidth: 0,
			areaHeight: 0,
			onChange: function(){},
			onSelect: function(){}
		};
		var op = defaultOptions;
		setOptions(customOptions);
		var $image = $(object);
		var $overlay = $('<div id="overlay" />').width($image.width()).height($image.height()).insertAfter($image);
		var $trigger = $('<div id="trigger" />').width($image.width()).height($image.height()).insertAfter($overlay);
		var $outline = $('<div id="outline" />').insertAfter($trigger);
		var $area = $('<div />').css({position: 'absolute', background: 'url(' + $image.attr('src') + ') no-repeat'})
			.insertAfter($outline);
		var $nwResizeHandler = $('<div class="resize-handler" id="nw-resize-handler" />').insertAfter($area),
			 $nResizeHandler = $('<div class="resize-handler" id= "n-resize-handler" />').insertAfter($area),
			$neResizeHandler = $('<div class="resize-handler" id="ne-resize-handler" />').insertAfter($area),
			 $wResizeHandler = $('<div class="resize-handler" id= "w-resize-handler" />').insertAfter($area),
			 $eResizeHandler = $('<div class="resize-handler" id= "e-resize-handler" />').insertAfter($area),
			$swResizeHandler = $('<div class="resize-handler" id="sw-resize-handler" />').insertAfter($area),
			 $sResizeHandler = $('<div class="resize-handler" id= "s-resize-handler" />').insertAfter($area),
			$seResizeHandler = $('<div class="resize-handler" id="se-resize-handler" />').insertAfter($area);
		var resizeHorizontally = true,
			resizeVertically = true,
			areaExists = false,
			areaOffset = [0, 0],
			areaOrigin = [0, 0];
		if(op.areaWidth  > op.minSelect[0] &&
		   op.areaHeight > op.minSelect[1]){
			areaExists = true;
		}
		updateInterface();
		if(op.allowSelect){$trigger.mousedown(setArea);}
		if(op.allowMove  ){$area.mousedown(pickArea);}
		if(op.allowResize){$('.resize-handler').mousedown(pickResizeHandler);}
		
		function setOptions(customOptions){
			op = $.extend(op, customOptions);
		}
		function getElementOffset(object){
			var offset = $(object).offset();
			return [offset.left, offset.top];
		}
		function getMousePos(event){
			var imageOffset = getElementOffset($image);
			var x = event.pageX - imageOffset[0],
				y = event.pageY - imageOffset[1];
			x = (x < 0) ? 0 : (x > $image.width( )) ? $image.width( ) : x;
			y = (y < 0) ? 0 : (y > $image.height()) ? $image.height() : y;
			return [x, y];
		}
		function updateOverlayLayer(){
			$overlay.css({display: areaExists ? 'block' : 'none'});
		}
		function updateTriggerLayer(){
			$trigger.css({cursor: op.allowSelect ? 'crosshair' : 'default'});
		}
		function updateArea(){
			$outline.css({
				cursor: 'default',
				display: areaExists ? 'block' : 'none',
				left: op.areaPos[0],
				top:  op.areaPos[1]
			})
			.width( op.areaWidth )
			.height(op.areaHeight);
			
			$area.css({
				backgroundPosition: ( - op.areaPos[0] - 1) + 'px ' +
									( - op.areaPos[1] - 1) + 'px',
				cursor: op.allowMove ? 'move'  : 'default',
				display: areaExists  ? 'block' : 'none',
				left: op.areaPos[0] + 1,
				top:  op.areaPos[1] + 1
			})
			.width( (op.areaWidth  - 2 > 0) ? (op.areaWidth  - 2) : 0)
			.height((op.areaHeight - 2 > 0) ? (op.areaHeight - 2) : 0);
		}
		function updateCursor(cursorType){
			$trigger.css(  {cursor: cursorType});
			$outline.css(  {cursor: cursorType});
			$area.css({cursor: cursorType});
		}
		function updateInterface(sender){
			switch(sender){
				case 'setArea' :
					updateOverlayLayer();
					updateArea();
					updateResizeHandlers('hide-all');
					break;
				case 'pickArea' :
					updateResizeHandlers('hide-all');
					break;
				case 'pickResizeHandler':
					updateResizeHandlers('hide-all');
					break;
				case 'resizeArea':
					updateArea();
					updateResizeHandlers('hide-all');
					updateCursor('crosshair');
					break;
				case 'moveArea':
					updateArea();
					updateResizeHandlers('hide-all');
					updateCursor('move');
					break;
				case 'releaseArea':
					updateTriggerLayer();
					updateOverlayLayer();
					updateArea();
					updateResizeHandlers();
					break;
				default:
					updateTriggerLayer();
					updateOverlayLayer();
					updateArea();
					updateResizeHandlers();
			}
		}
		function setArea(event){
			event.preventDefault();
			event.stopPropagation();
			$(document).mousemove(resizeArea).mouseup(releaseArea);
			areaExists = true;
			op.areaWidth  = 0;
			op.areaHeight = 0;
			areaOrigin = getMousePos(event);
			op.areaPos[0] = areaOrigin[0];
			op.areaPos[1] = areaOrigin[1];
			updateInterface('setArea');
		}
		function resizeArea(event){
			event.preventDefault();
			event.stopPropagation();
			var mousePos = getMousePos(event);
			var height = mousePos[1] - areaOrigin[1], width = mousePos[0] - areaOrigin[0];
			if(Math.abs(width ) < op.minSize[0]) width  = (width  >= 0) ? op.minSize[0] : - op.minSize[0];
			if(Math.abs(height) < op.minSize[1]) height = (height >= 0) ? op.minSize[1] : - op.minSize[1];
			if(areaOrigin[0] + width  < 0 || areaOrigin[0] + width  > $image.width( )) width  = - width;
			if(areaOrigin[1] + height < 0 || areaOrigin[1] + height > $image.height()) height = - height;
			if(op.maxSize[0] > op.minSize[0] &&
				op.maxSize[1] > op.minSize[1]) {
				if(Math.abs(width ) > op.maxSize[0]) width  = (width  >= 0) ? op.maxSize[0] : - op.maxSize[0];
				if(Math.abs(height) > op.maxSize[1]) height = (height >= 0) ? op.maxSize[1] : - op.maxSize[1];
			}
			if(resizeHorizontally) op.areaWidth = width;
			if(resizeVertically) op.areaHeight = height;
			if(op.aspectRatio){
				if((width > 0 && height > 0) || (width < 0 && height < 0))
					if(resizeHorizontally) height = Math.round(width / op.aspectRatio);
					else width = Math.round(height * op.aspectRatio);
				else
					if(resizeHorizontally) height = - Math.round(width / op.aspectRatio);
					else width = - Math.round(height * op.aspectRatio);
				if (areaOrigin[0] + width > $image.width()) {
					width = $image.width() - areaOrigin[0];
					height = (height > 0) ? Math.round(width / op.aspectRatio) : - Math.round(width / op.aspectRatio);
				}
				if (areaOrigin[1] + height < 0) {
					height = - areaOrigin[1];
					width = (width > 0) ? - Math.round(height * op.aspectRatio) : Math.round(height * op.aspectRatio);
				}
				if (areaOrigin[1] + height > $image.height()) {
					height = $image.height() - areaOrigin[1];
					width = (width > 0) ? Math.round(height * op.aspectRatio) : - Math.round(height * op.aspectRatio);
				}
				op.areaWidth = width;
				op.areaHeight = height;
			}
			if (op.areaWidth < 0) {
				op.areaWidth = Math.abs(op.areaWidth);
				op.areaPos[0] = areaOrigin[0] - op.areaWidth;
			} else op.areaPos[0] = areaOrigin[0];
			if (op.areaHeight < 0) {
				op.areaHeight = Math.abs(op.areaHeight);
				op.areaPos[1] = areaOrigin[1] - op.areaHeight;
			} else op.areaPos[1] = areaOrigin[1];
			op.onChange(getCropData());
			updateInterface('resizeArea');
		}
		function moveArea(event){
			event.preventDefault();
			event.stopPropagation();
			var mousePos = getMousePos(event);
			if(mousePos[0] - areaOffset[0] > 0)
				if(mousePos[0] - areaOffset[0] + op.areaWidth < $image.width())
					op.areaPos[0] = mousePos[0] - areaOffset[0];
				else op.areaPos[0] = $image.width() - op.areaWidth;
			else op.areaPos[0] = 0;
			if(mousePos[1] - areaOffset[1] > 0)
				if(mousePos[1] - areaOffset[1] + op.areaHeight < $image.height())
					op.areaPos[1] = mousePos[1] - areaOffset[1];
				else op.areaPos[1] = $image.height() - op.areaHeight;
				else op.areaPos[1] = 0;
			op.onChange(getCropData());
			updateInterface('moveArea');
		}
		function releaseArea(event){
			event.preventDefault();
			event.stopPropagation();
			$(document).unbind('mousemove').unbind('mouseup');
			areaOrigin[0] = op.areaPos[0];
			areaOrigin[1] = op.areaPos[1];
			resizeHorizontally = true;
			resizeVertically = true;
			if (op.areaWidth > op.minSelect[0] &&
				op.areaHeight > op.minSelect[1])
				areaExists = true;
			else areaExists = false;
			op.onSelect(getCropData());
			updateInterface('releaseArea');
		}
		function pickArea(event){
			event.preventDefault();
			event.stopPropagation();
			$(document).mousemove(moveArea).mouseup(releaseArea);
			var mousePos = getMousePos(event);
			areaOffset[0] = mousePos[0] - op.areaPos[0];
			areaOffset[1] = mousePos[1] - op.areaPos[1];
			updateInterface('pickArea');
		}
		function getCropData(){
			return{
				areaX: op.areaPos[0],
				areaY: op.areaPos[1],
				areaWidth: op.areaWidth,
				areaHeight: op.areaHeight,
				areaExists: function(){
					return areaExists;
				}
			};
		}
		
		function updateResizeHandlers(action){
			switch(action){
				case 'hide-all':
					$('.resize-handler').each(function(){
						$(this).css({display: 'none'});
					});
					break;
				default:
					var display = (areaExists && op.allowResize) ? 'block' : 'none';
					$nwResizeHandler.css({
						cursor: 'nw-resize',
						display: display,
						left: op.areaPos[0] - Math.round($nwResizeHandler.width() / 2),
						top: op.areaPos[1] - Math.round($nwResizeHandler.height() / 2)
					});
					$nResizeHandler.css({
						cursor: 'n-resize',
						display: display,
						left: op.areaPos[0] + Math.round(op.areaWidth / 2 - $neResizeHandler.width() / 2) - 1,
						top: op.areaPos[1] - Math.round($neResizeHandler.height() / 2)
					});
					$neResizeHandler.css({
						cursor: 'ne-resize',
						display: display,
						left: op.areaPos[0] + op.areaWidth - Math.round($neResizeHandler.width() / 2) - 1,
						top: op.areaPos[1] - Math.round($neResizeHandler.height() / 2)
					});
					$wResizeHandler.css({
						cursor: 'w-resize',
						display: display,
						left: op.areaPos[0] - Math.round($neResizeHandler.width() / 2),
						top: op.areaPos[1] + Math.round(op.areaHeight / 2 - $neResizeHandler.height() / 2) - 1
					});
					$eResizeHandler.css({
						cursor: 'e-resize',
						display: display,
						left: op.areaPos[0] + op.areaWidth - Math.round($neResizeHandler.width() / 2) - 1,
						top: op.areaPos[1] + Math.round(op.areaHeight / 2 - $neResizeHandler.height() / 2) - 1
					});
					$swResizeHandler.css({
						cursor: 'sw-resize',
						display: display,
						left: op.areaPos[0] - Math.round($swResizeHandler.width() / 2),
						top: op.areaPos[1] + op.areaHeight - Math.round($swResizeHandler.height() / 2) - 1
					});
					$sResizeHandler.css({
						cursor: 's-resize',
						display: display,
						left: op.areaPos[0] + Math.round(op.areaWidth / 2 - $seResizeHandler.width() / 2) - 1,
						top: op.areaPos[1] + op.areaHeight - Math.round($seResizeHandler.height() / 2) - 1
					});
					$seResizeHandler.css({
						cursor: 'se-resize',
						display: display,
						left: op.areaPos[0] + op.areaWidth - Math.round($seResizeHandler.width() / 2) - 1,
						top: op.areaPos[1] + op.areaHeight - Math.round($seResizeHandler.height() / 2) - 1
					});
			}
		}
		function pickResizeHandler(event){
			event.preventDefault();
			event.stopPropagation();
			switch (event.target.id) {
				case 'nw-resize-handler':
					areaOrigin[0] += op.areaWidth;
					areaOrigin[1] += op.areaHeight;
					op.areaPos[0] = areaOrigin[0] - op.areaWidth;
					op.areaPos[1] = areaOrigin[1] - op.areaHeight;
					break;
				case 'n-resize-handler':
					areaOrigin[1] += op.areaHeight;
					op.areaPos[1] = areaOrigin[1] - op.areaHeight;
					resizeHorizontally = false;
					break;
				case 'ne-resize-handler':
					areaOrigin[1] += op.areaHeight;
					op.areaPos[1] = areaOrigin[1] - op.areaHeight;
					break;
				case 'w-resize-handler':
					areaOrigin[0] += op.areaWidth;
					op.areaPos[0] = areaOrigin[0] - op.areaWidth;
					resizeVertically = false;
					break;
				case 'e-resize-handler':
					resizeVertically = false;
					break;
				case 'sw-resize-handler':
					areaOrigin[0] += op.areaWidth;
					op.areaPos[0] = areaOrigin[0] - op.areaWidth;
					break;
				case 's-resize-handler':
					resizeHorizontally = false;
					break;
			}
			$(document).mousemove(resizeArea).mouseup(releaseArea);
			updateInterface('pickResizeHandler');
		};
		
		function updateCursor(cursorType){
			var c = {cursor: cursorType};
			$trigger.css(c);
			$outline.css(c);
			$area.css(c);
		}
	};
	$.fn.imageCrop = function(customOptions){
		this.each(function(){
			var currentObject = this,
				image = new Image();
			image.onload = function(){
				$.imageCrop(currentObject, customOptions);
			};
			image.src = currentObject.src;
		});
		return this;
	};
})(jQuery);