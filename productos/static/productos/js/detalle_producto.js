document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll(".star");
    const ratingInput = document.querySelector("#id_calificacion"); // tu input hidden
    const ratingValueDisplay = document.getElementById("ratingValue");

    stars.forEach((star) => {
        star.addEventListener("click", () => {
            const rating = star.dataset.value;

            // Actualiza el input hidden
            if (ratingInput) ratingInput.value = rating;

            // Marca visualmente las estrellas
            stars.forEach((s) => {
                const svg = s.querySelector("svg"); // toma el SVG dentro del botón
                if (svg) {
                    if (s.dataset.value <= rating) {
                        svg.classList.add("filled");
                    } else {
                        svg.classList.remove("filled");
                    }
                }
            });

            // Actualiza el texto
            if (ratingValueDisplay) ratingValueDisplay.textContent = rating;
        });
    });
});
