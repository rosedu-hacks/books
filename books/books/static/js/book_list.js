var current_tags = [];
var current_search_term = ""
$( document).ready(function() {initial_load();});

function load_tag_bar() {
	$.get("api/v1/tags/?format=json",function(data) {
			all_tags = ["all"];
			for (k in data.objects) {
				all_tags.push(data.objects[k].name)
			}
			$(".tag_bar").select2({
  		tags: all_tags,
  		tokenSeparators: [",", " "],
  		width: "resolve",
  		placeholder: "Tags",
  		maximumSelectionSize: 3}).on("change", function(e) {
  			ctags = []
  			tag_form = $(this).select2('data');
  			console.log(tag_form);
  			var usingAll = false;
  			for (var j in tag_form) {
  				ctags.push(tag_form[j].text);
  				if (tag_form[j].text == "all")
  					usingAll = true;
  				current_tags = ctags;
  			}
  			if (usingAll)
  				current_tags = [];
				$(".book_list").empty();
  			load_books(current_tags, current_search_term);
  		});
	});

}
function welcome_message(){
    if (document.cookie.indexOf("visitedabcd") >= 0) {
    }
    else {
        expiry = new Date();
        expiry.setTime(expiry.getTime()+(10*60*1000)); // Ten minutes
                 // Date()'s toGMTSting() method will format the date correctly for a cookie
        document.cookie = "visitedabcd=yes";
        $(".welcome").css({"display": "block"}) 
    }
}
function initial_load() {
	load_tag_bar();
    welcome_message();

	$('.search_bar').on('keyup', function() {
  	var search_term = $('.search_bar').val();

		$(".book_list").empty();
		current_search_term = search_term;
		load_books(current_tags, search_term);
  });
	load_books([]);
}

function load_books(tags, search_term) {
	var query_url = "api/v1/books/?format=json";
	if (tags.length) {
		query_url = query_url + "&taggings=" + JSON.stringify(tags);
	}
	if (search_term != null) {
		query_url = query_url + "&title__startswith=" + search_term;
	}

	$.get(query_url, function ( data ) {
		$.get("static/book_entry_template.html", function ( template_info ) {
			global_template = template_info;
			var template = Handlebars.compile(template_info);
			var books = data.objects;
			for (var i in books) {
				entry = $(".book_list").append(template(books[i]));
				$(".book_views", entry).text(Math.random() * 500 | 0);
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
}
