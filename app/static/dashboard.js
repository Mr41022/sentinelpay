document
.getElementById("fraud-form")
.addEventListener("submit", async e => {

    e.preventDefault();

    const response = await fetch(
        "/transactions",
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                amount: document
                    .getElementById("amount")
                    .value,

                card_holder_country: "GB",

                channel: "contactless",

                country_code: document
                    .getElementById("country")
                    .value,

                currency: "GBP",

                hour_of_day: 14,

                is_international: false,

                merchant_category_code: "5411"
            })
        }
    );

    const data = await response.json();

    document.getElementById("score")
        .innerText =
        Math.round(data.score * 100) + "%";

    const decisionEl = document.getElementById("decision");
    decisionEl.innerText = data.decision.toUpperCase();
    decisionEl.className = data.decision.toLowerCase();
});
