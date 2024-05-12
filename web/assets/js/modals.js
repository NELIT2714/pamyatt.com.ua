$(document).ready(function($) {
	// Add product modal

	$("#add-new").click(function() {
		$("#add-product").fadeIn()
		return false
	});

	$("#close-add-product").click(function() {
		$(this).parents("#add-product").fadeOut()
		return false
	})

	$(document).keydown(function(e) {
		if (e.keyCode === 27) {
			e.stopPropagation()
			$(".popup-fade").fadeOut()
		}
	})

	// Add category modal

	$("#add-category-btn").click(function() {
		$("#add-category").fadeIn()
		return false
	})

	$("#popup-category-close").click(function() {
		$(this).parents("#add-category").fadeOut()
		return false
	})
})