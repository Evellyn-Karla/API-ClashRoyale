async function getWinLossPercentage() {
    const cardName = document.getElementById('card-name').value;
    const startDate = new Date(document.getElementById('start-date').value).getTime() / 1000;
    const endDate = new Date(document.getElementById('end-date').value).getTime() / 1000;

    const data = {
        card_name: cardName,
        start_date: startDate,
        end_date: endDate
    };

    try {
        const response = await fetch('http://127.0.0.1:5000/win-loss-percentage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        
        if (response.ok) {
            document.getElementById('results').innerHTML = `
                <p>Total de Partidas: ${result.total_matches}</p>
                <p>Vitórias: ${result.wins}</p>
                <p>Derrotas: ${result.losses}</p>
                <p>Porcentagem de Vitórias: ${result.win_percentage.toFixed(2)}%</p>
                <p>Porcentagem de Derrotas: ${result.loss_percentage.toFixed(2)}%</p>
            `;
        } else {
            document.getElementById('results').innerHTML = `<p>Error: ${result.error}</p>`;
        }
        
    } catch (error) {
        console.error("Erro na requisição:", error);
        document.getElementById('results').innerHTML = `<p>Erro ao buscar dados</p>`;
    }
}
