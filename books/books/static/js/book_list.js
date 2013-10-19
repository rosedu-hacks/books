global_template = {}
var global_book_entry = {}

$(load_books([]));
function load_books(tags) {
	var query_url = "api/v1/books/?format=json";
	if (tags.length) {
		query_url = query_url + "&taggings=" + JSON.stringify(tags);
	}

	$.get(query_url, function ( data ) {
		$.get("static/book_entry_template.html", function ( template_info ) {
			global_template = template_info;
			var template = Handlebars.compile(template_info);
			var books = data.objects;
			for (var i in books) {
				entry = $(".book_list").append(template(books[i]));
				load_entry(entry, books[i]);
			}
		});
	});

	$.get( "static/handlebar_test_template.html", function( data ) {
		var template = Handlebars.compile(data);
		var context = {title: "My New Post", body: "This is my first post!"}
		$(".list").html(template(context));
	});
}

function load_entry(entry, book) {
	$(".book_taglist", entry).each(function (){
		var entry_taglist = $(this);
		for (var i in book.tags) {
			$.get(book.tags[i], function (data){ 
				var tag_html = "<div class='badge hand_on_hover'>" + data.name + "</div>";
				entry_taglist.append(tag_html).click(function() { tag_click(data.name); });
			});
		}
	});
}

function tag_click(name) {
	$(".book_list").empty();
	tags = [name];
	load_books(tags);
}