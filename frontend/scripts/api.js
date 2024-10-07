async function getWinLossPercentage() {
  // Coletar todas as cartas selecionadas
  const selectedCards = Array.from(document.querySelectorAll('#card-container select'))
  .map(select => select.value) // Extrai o valor de cada select
  .filter(card => card); // Filtra cartas não selecionadas (vazias)

  const startDateInput = document.getElementById("start-date").value;
  const endDateInput = document.getElementById("end-date").value;

  let timestampStart = null;
  let timestampEnd = null;

  if (startDateInput && endDateInput) {
    const startDate = new Date(startDateInput);
    const endDate = new Date(endDateInput);

    timestampStart = startDate.toISOString().slice(0, 19) + "Z";
    timestampEnd = endDate.toISOString().slice(0, 19) + "Z";
  }

  const dados = {
    selected_cards: selectedCards, // Enviar uma lista de cartas
    start_date: timestampStart,
    end_date: timestampEnd,
  };

  console.log(dados);

  try {
    const response = await fetch("http://127.0.0.1:5000/win-loss-percentage", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });

    const result = await response.json();
    console.log(result);

    if (response.ok) {
      if (result === "404") {
        document.getElementById(
          "results"
        ).innerHTML = `<p>Nenhum jogador encontrado.</p>`;
      } else if (result === "405") {
        document.getElementById(
          "results"
        ).innerHTML = `<p>Nenhuma partida encontrada para os parâmetros fornecidos.</p>`;
      } else {
        document.getElementById("results").innerHTML = `
                    <p>Total de Partidas: ${result.total_battles}</p>
                    <p>Vitórias: ${result.wins}</p>
                    <p>Derrotas: ${result.losses}</p>
                    <p>Porcentagem de Vitórias: ${result.win_percentage.toFixed(
                      2
                    )}%</p>
                    <p>Porcentagem de Derrotas: ${result.loss_percentage.toFixed(
                      2
                    )}%</p>
                `;
      }
    } else {
      document.getElementById(
        "results"
      ).innerHTML = `<p>Error: ${result.error}</p>`;
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
    document.getElementById(
      "results"
    ).innerHTML = `<p>Erro ao buscar dados</p>`;
  }
}

function addCardInput() {
  const cardContainer = document.getElementById("card-inputs");

  const newCardInput = document.createElement("input");
  newCardInput.setAttribute("type", "text");
  newCardInput.setAttribute("name", "card");
  newCardInput.setAttribute("placeholder", "Digite o nome da carta");

  cardContainer.appendChild(newCardInput);
}

async function calculateWinPercentage() {
  // Coletar os dados dos inputs
  const minWinPercentage = document.getElementById("porcent_min").value;
  const startDateInput = document.getElementById("start-date1").value;
  const endDateInput = document.getElementById("end-date1").value;

  let timestampStart = null;
  let timestampEnd = null;

  if (startDateInput && endDateInput) {
    const startDate = new Date(startDateInput);
    const endDate = new Date(endDateInput);

    timestampStart = startDate.toISOString().slice(0, 19) + "Z";
    timestampEnd = endDate.toISOString().slice(0, 19) + "Z";
  }

  const dados = {
    min_win_percentage: minWinPercentage,
    start_date: timestampStart,
    end_date: timestampEnd,
  };

  console.log(dados);

  try {
    const response = await fetch("http://127.0.0.1:5000/decks", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(dados),
    });

    const result = await response.json();
    console.log("resultado fetch", result);
    console.log(result.length);
    if (response.ok) {
      if (result.length === 0) {
        document.getElementById("decks_porcent").innerHTML = `
                    <p>Nenhum deck encontrado com a porcentagem mínima especificada.</p>`;
      } else {
        displayDecks(result);
      }
    } else {
      document.getElementById(
        "decks_porcent"
      ).innerHTML = `<p>Error: ${result.error}</p>`;
    }
  } catch (error) {
    console.error("Erro na requisição:", error);
    document.getElementById(
      "decks_porcent"
    ).innerHTML = `<p>Erro ao buscar dados</p>`;
  }
}

function displayDecks(decks) {
  const decksDiv = document.getElementById("decks_porcent");
  decksDiv.innerHTML = ""; // Limpa a div antes de adicionar novos resultados

  if (!decks || decks.length === 0) {
    decksDiv.innerHTML =
      "<p>Nenhum deck encontrado com a porcentagem especificada.</p>";
    return;
  }

  decks.forEach((deck) => {
    // Verifique se deck e deck.deck existem
    if (deck && deck.deck) {
      const deckDiv = document.createElement("div");
      deckDiv.innerHTML = `
                <h3>Deck: ${deck.deck.join(", ")}</h3>
                <p>Porcentagem de Vitórias: ${deck.win_percentage.toFixed(
                  2
                )}%</p>
            `;
      decksDiv.appendChild(deckDiv);
    } else {
      console.warn("Deck ou propriedade 'deck' ausente:", deck);
    }
  });
}
