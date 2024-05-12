document.addEventListener("DOMContentLoaded", () => {
    const add_amount_btn = document.querySelector("#add_amount")
    const amount_index = document.querySelector("#amount_index")
    const subtract_amount_btn = document.querySelector("#subtract_amount")

    add_amount_btn.addEventListener("click", () => {
        const currentValue = parseInt(amount_index.value);
        if (currentValue < 20) {
            amount_index.value = currentValue + 1;
        }
    })
    subtract_amount_btn.addEventListener("click", () => {
        const currentValue = parseInt(amount_index.value);
        if (currentValue > 1) {
            amount_index.value = currentValue - 1;
        }
    })
})