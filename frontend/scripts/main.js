async function getCards() {
  try {
    const response = await fetch("http://127.0.0.1:5000/cards", {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    });

    const result = await response.json();
    return result; // Retorne os resultados
  } catch (error) {
    console.log("Erro na requisição:", error);
    return []; // Retorne uma lista vazia em caso de erro para evitar o undefined
  }
}

async function populateCardDropdown(dropdownElement) {
  const availableCards = await getCards();
  availableCards.forEach((card) => {
    const option = document.createElement("option");
    option.value = card;
    option.text = card;
    dropdownElement.appendChild(option);
  });
}

async function addCardSelect() {
    const cardContainer = document.getElementById('card-container');
    const newSelect = document.createElement('select');

    // Verifique se o cardContainer foi encontrado
    if (!cardContainer) {
        console.error("Elemento 'card-container' não encontrado.");
        return;
    }

    // Popula o novo select com as cartas
    await populateCardDropdown(newSelect);

    // Adiciona o novo select ao contêiner
    cardContainer.appendChild(newSelect);
}

// Função para definir as datas iniciais como a data de hoje
function setDefaultDates() {
  const today = new Date().toISOString().split("T")[0];
  document.getElementById("start-date").value = today;
  document.getElementById("end-date").value = today;
  document.getElementById("start-date1").value = today;
  document.getElementById("end-date1").value = today;
}

// Executar as funções ao carregar a página
document.addEventListener("DOMContentLoaded", function () {
  populateCardDropdown();
  setDefaultDates();
});


window.onload = async function() {
    const dropdown = document.getElementById("card-dropdown");
    await populateCardDropdown(dropdown);
};
/* async function displayCards() {
    const cards = await getCards()  // Supondo que você tenha uma função para obter os dados

    const cardListDiv = document.getElementById('card-list');
    cards.forEach(card => {
        const cardDiv = document.createElement('div');
        cardDiv.innerHTML = `
            <h3>${card.name}</h3>
            <img src="${card.icon}" alt="${card.name}" />
        `;
        cardListDiv.appendChild(cardDiv);
    });
} */
