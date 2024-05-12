$(document).ready(function() {
    $(".subtract_amount").click(function() {
        const productId = $(this).closest(".cart").data("product-id");
        const amount = $(this).closest(".amount-controls").find(".amount_index").val();

        console.log("Product ID:", productId);

        $.ajax({
            url: "/cart/change-amount/",
            method: "POST",
            data: { product_id: productId, amount: amount, action: "subtract" },
            success: function(response) {
                if (response["success"] && response["redirect_url"]) {
                    window.location.href = response["redirect_url"]
                }
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });

    $(".add_amount").click(function() {
        const productId = $(this).closest(".cart").data("product-id");
        const amount = $(this).closest(".amount-controls").find(".amount_index").val();

        console.log("Product ID:", productId);

        $.ajax({
            url: "/cart/change-amount/",
            method: "POST",
            data: { product_id: productId, amount: amount, action: "add" },
            success: function(response) {
                if (response["success"] && response["redirect_url"]) {
                    window.location.href = response["redirect_url"]
                }
            },
            error: function(xhr, status, error) {
                console.error("Error:", error);
            }
        });
    });
});