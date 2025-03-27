function createPieChart(ctx, labels, data, colors) {
    Chart.register(ChartDataLabels);
    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 0,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend:{
                    position: 'right', // Position legend on the right
                    labels: {
                        usePointStyle: true, // Use colored squares as legend markers
                        pointStyle: 'rect',
                    },
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += context.parsed + '%'; // Add percentage symbol
                            }
                            return label;
                        }
                    }
                },
                datalabels: {
                    color: '#000',
                    font: {
                        weight: 'bold',
                        size: 14
                    },
                    formatter: (value, context) => {
                        return value + '%';
                    },
                }
            }
        },
    });
    
}