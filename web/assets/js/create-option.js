document.addEventListener("DOMContentLoaded", () => {
    const option_name_input = document.querySelector("#option_name")
    const option_price_input = document.querySelector("#option_price")
    const add_option_btn = document.querySelector("#add-option-btn")

    add_option_btn.addEventListener("click", () => {
        const option_name = option_name_input.value
        const option_price = option_price_input.value

        if (option_name && option_price) {
            const product_form = document.querySelector("#product-form")
            const product_options = document.querySelector("#product_options")

            const hiddenInput = document.createElement("input")
            const new_option = document.createElement("option")

            hiddenInput.type = "hidden"
            hiddenInput.id = "product_option[]"
            hiddenInput.name = "product_option[]"
            hiddenInput.value = `${option_name}-${option_price}`

            new_option.value = option_name
            new_option.text = `${option_name} — ${option_price} UAH`

            product_form.appendChild(hiddenInput)
            product_options.appendChild(new_option)

            option_name_input.value = ""
            option_price_input.value = ""
        } else {
            console.log("НЕ ВСЕ ПОЛЯ БЫЛИ ЗАПОЛНЕНЫ")
        }
    })
})