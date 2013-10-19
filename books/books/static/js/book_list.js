var handle_bar_template = {}

$(function() {
  callFact();
});
$.get( "static/book_entry_template.html", function( data ) {
	handle_bar_template = data;
});

$.get("/api/v1/books/?format=json"), function ( data ) {
	alert("merge");
}

