
const cleanOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
        legend: { display: false }
    },
    scales: {
        x: { grid: { display: false }, ticks: { color: '#666' } },
        y: { grid: { display: false }, ticks: { color: '#666' } }
    },
    animation: { duration: 1500 }
};


const paymentLabels = JSON.parse(document.getElementById('payment-labels').textContent);
const paymentData = JSON.parse(document.getElementById('payment-data').textContent);

const categoryLabels = JSON.parse(document.getElementById('cat-labels').textContent);
const categoryData = JSON.parse(document.getElementById('cat-data').textContent);

const months = JSON.parse(document.getElementById('months').textContent);
const monthData = JSON.parse(document.getElementById('month-data').textContent);


new Chart(document.getElementById('doughnutChart'), {
    type: 'doughnut',
    data: {
        labels: paymentLabels,
        datasets: [{
            data: paymentData,
            backgroundColor: ['#4dd82edb', '#36A2EB', '#FFCE56', '#FF6384'],
            borderWidth: 0
        }]
    },
    options: { ...cleanOptions, cutout: '60%' }
});

new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: categoryLabels,
        datasets: [{
            label: 'Orders',
            data: categoryData,
            backgroundColor: '#36A2EB',
            borderRadius: 8,
            borderSkipped: false
        }]
    },
    options: cleanOptions
});

new Chart(document.getElementById('lineChart'), {
    type: 'line',
    data: {
        labels: months,
        datasets: [{
            label: 'Orders',
            data: monthData,
            borderColor: '#4dd82edb',
            backgroundColor: 'rgba(77, 216, 46, 0.1)',
            tension: 0.4,
            fill: true,
            pointRadius: 6,
            pointHoverRadius: 8
        }]
    },
    options: cleanOptions
});