$(document).ready(function() {
    $("#admin-auth").submit(function(e) {
        e.preventDefault()

        const formData = $(this).serialize()

        $.ajax({
            type: "POST",
            url: "/admin/auth/",
            data: formData,
            success: function(response) {
                if (response["success"] && response["redirect_url"]) {
                    window.location.href = response["redirect_url"]
                } else {
                    $(".authorization-errors").text(response.message);
                }
            },
            error: function(xhr, status, error) {
                console.error(status, error)
            }
        })
    })
})