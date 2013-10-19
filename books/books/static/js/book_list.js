global_template = {}
$(function() {
	$.get("api/v1/books/?format=json", function ( data ) {
		$.get("static/book_entry_template.html", function ( template_info ) {
			global_template = template_info;
			var template = Handlebars.compile(template_info);
			var books = data.objects;
			for (var i in books) {
				console.log(books[i]);
				$(".book_list").append(template(books[i]));
			}
		});
	});

	$.get( "static/handlebar_test_template.html", function( data ) {
		var template = Handlebars.compile(data);
		var context = {title: "My New Post", body: "This is my first post!"}
		$(".list").html(template(context));
	});
});
