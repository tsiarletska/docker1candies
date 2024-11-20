const API_URL = "/api";

async function loadCandies() {
  try {
    const response = await fetch(`${API_URL}/candies`);
    const candies = await response.json();
    const candiesGrid = document.getElementById("candies-grid");
    console.log("candies ", candies);
    if (candiesGrid) {
      candiesGrid.innerHTML = candies
        .map(
          (candy) => `
                <div class="card">
                    <h3>${candy.name}</h3>
                    <p><strong>Price:</strong> $${candy.price}</p>
                    <p><strong>Type:</strong> ${candy.type}</p>
                    <p>${candy.description}</p>
                </div>
            `,
        )
        .join("");
    }
  } catch (error) {
    console.error("Error loading candies:", error);
  }
}

async function loadTypes() {
  try {
    const response = await fetch(`${API_URL}/types`);
    const types = await response.json();
    const typesList = document.getElementById("types-list");

    if (typesList) {
      typesList.innerHTML = types
        .map(
          (type) => `
                <div class="list-item">
                    <h3>${type.name}</h3>
                </div>
            `,
        )
        .join("");
    }
  } catch (error) {
    console.error("Error loading types:", error);
  }
}
