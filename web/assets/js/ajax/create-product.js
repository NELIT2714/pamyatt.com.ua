$(document).ready(function() {
    $("#product-form").submit(function(e) {
        e.preventDefault()

        const formData = new FormData(this);

        formData.append('product_options', JSON.stringify([...document.querySelectorAll('input[type="hidden"]')].map(input => input.value)));
        console.log([...document.querySelectorAll('input[type="hidden"]')].map(input => input.value))

        $.ajax({
            type: "POST",
            url: "/admin/products/new/",
            data: formData,
            contentType: false,
            processData: false,
            cache: false,
            success: function(response) {
                if (response["success"] && response["redirect_url"]) {
                    window.location.href = response["redirect_url"]
                } else {
                    $(".add-product-messages").text(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error(status, error)
            }
        })
    })
})