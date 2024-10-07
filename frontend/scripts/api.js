async function getWinLossPercentage() {
    const cardName = document.getElementById('card-name').value;

    const startDateInput = document.getElementById('start-date').value;
    const endDateInput = document.getElementById('end-date').value;

    let timestampStart = null;
    let timestampEnd = null;

    if (startDateInput && endDateInput) {
        const startDate = new Date(startDateInput);
        const endDate = new Date(endDateInput);
        
        timestampStart = startDate.toISOString().slice(0, 19) + 'Z';
        timestampEnd = endDate.toISOString().slice(0, 19) + 'Z';
    }
    
    const dados = {
        card_name: cardName,
        start_date: timestampStart,
        end_date: timestampEnd
    };

    console.log(dados)

    try {
        const response = await fetch('http://127.0.0.1:5000/win-loss-percentage', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        const result = await response.json();
        console.log(result); 
        
        if (response.ok) {
            if(result == '404'){
                document.getElementById('results').innerHTML = `
                <p>Nenhum jogador encontrado.</p>`;
            } else if(result == '405'){
               document.getElementById('results').innerHTML = `
                <p>Nenhuma partida encontrada para os parâmetros fornecidos.</p>`;
            } else {
                document.getElementById('results').innerHTML = `
                    <p>Total de Partidas: ${result.total_battles}</p>
                    <p>Vitórias: ${result.wins}</p>
                    <p>Derrotas: ${result.losses}</p>
                    <p>Porcentagem de Vitórias: ${result.win_percentage.toFixed(2)}%</p>
                    <p>Porcentagem de Derrotas: ${result.loss_percentage.toFixed(2)}%</p>
                `;
            }
        } else {
            document.getElementById('results').innerHTML = `<p>Error: ${result.error}</p>`;
        }
        
    } catch (error) {
        console.error("Erro na requisição:", error);
        document.getElementById('results').innerHTML = `<p>Erro ao buscar dados</p>`;
    }
}
