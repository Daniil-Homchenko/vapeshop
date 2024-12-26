const labels = {{ labels|safe }};
        const data = {
            labels: labels,
            datasets: [{
                label: 'Продажи',
                data: {{ data|safe }},
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        };
        const config = {
            type: 'line',
            data: data,
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        };
        new Chart(document.getElementById('salesChart'), config);