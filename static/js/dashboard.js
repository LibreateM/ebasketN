

console.log("Months:", {{ months| safe}});
console.log("Revenue:", {{ revenue_data| safe}});

const ctx = document.getElementById('revenueChart');

if (ctx) {
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: {{ months| safe }},
datasets: [{
    label: 'Revenue',
    data: {{ revenue_data| safe}},
    borderWidth: 2
                  }]
        }
      });
    } else {
    console.log("Canvas not found");
}
const ctx2 = document.getElementById('donutChart');

console.log("Category Labels:", {{ cat_labels| safe}});
console.log("Category Data:", {{ cat_data| safe}});

if (ctx2) {
    new Chart(ctx2, {
        type: 'doughnut',
        data: {
            labels: {{ cat_labels| safe }},
datasets: [{
    data: {{ cat_data| safe}}
            }]
        }
    });
    } else {
    console.log("Donut canvas not found");
}
