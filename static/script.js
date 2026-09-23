document.addEventListener("DOMContentLoaded", function () {

    const rideOptions = document.querySelectorAll(".ride-option");
    const fareElement = document.getElementById("fare");
    const bookingForm = document.getElementById("bookingForm");
    const bookButton = document.getElementById("bookButton");


    /* =========================
       RIDE SELECTION
    ========================= */

    rideOptions.forEach(option => {

        const radio = option.querySelector("input");

        option.addEventListener("click", function () {

            rideOptions.forEach(item => {
                item.classList.remove("active");
            });

            option.classList.add("active");

            const price = radio.dataset.price;

            fareElement.textContent = `₹${price}`;
        });

    });


    /* =========================
       FORM SUBMISSION
    ========================= */

    if (bookingForm) {

        bookingForm.addEventListener("submit", function () {

            bookButton.classList.add("loading");

            bookButton.querySelector("span:first-child").textContent =
                "Processing...";

            bookButton.querySelector(".arrow").textContent = "⏳";

        });

    }


    /* =========================
       LOCATION INPUT EFFECT
    ========================= */

    const inputs = document.querySelectorAll(
        ".input-wrapper input"
    );

    inputs.forEach(input => {

        input.addEventListener("focus", function () {

            this.closest(".location-input").style.opacity = "1";

        });

    });

});