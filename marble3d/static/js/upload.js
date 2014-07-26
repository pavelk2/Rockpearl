$(document).ready(function(){
	
	var selector = '[role=uploadcare-uploader]';
	var widget = uploadcare.MultipleWidget(selector);

	widget.onChange(function(group) {
		if ( ! group) {
			return;
		}
		$.when.apply(null, group.files()).done(function() {
			// Store each image in the database
			$.each(arguments, function() {
				var fileInfo = this;
				console.log(fileInfo);
				$.post(store_image_url,{
					'image_url':fileInfo.cdnUrl,
					'filename':fileInfo.name,
					'csrfmiddlewaretoken':csrf_token
				},function(response){
					alert(response);
				},'json');
			});
		});
	
	});
});