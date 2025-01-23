// Tax Configuration
const SLABS = [
    { limit: 0, rate: 0 }, // First slab: tax-free
    { limit: 100000, rate: 0.05 },
    { limit: 400000, rate: 0.10 },
    { limit: 500000, rate: 0.15 },
    { limit: 500000, rate: 0.20 },
    { limit: 2000000, rate: 0.25 },
    { limit: Infinity, rate: 0.30 }
];
const INITIAL_SLAB_MAN = 350000;
const INITIAL_SLAB_WOMAN = 400000;
const MINIMUM_TAX = 5000;

// Calculate Tax Function
function calculateTax(income, gender) {
    const initialSlab = gender === "woman" ? INITIAL_SLAB_WOMAN : INITIAL_SLAB_MAN;
    let tax = 0;
    let remainingIncome = income - initialSlab;

    if (remainingIncome <= 0) return 0;

    for (const slab of SLABS) {
        if (remainingIncome <= slab.limit) {
            tax += remainingIncome * slab.rate;
            break;
        } else {
            tax += slab.limit * slab.rate;
            remainingIncome -= slab.limit;
        }
    }

    // Apply minimum tax rule
    if (tax > 0 && tax < MINIMUM_TAX) {
        tax = MINIMUM_TAX;
    }

    return tax;
}

// Initialize Chart
let taxChart;

function createChart(labels, data) {
    const ctx = document.getElementById("taxChart").getContext("2d");
    if (taxChart) taxChart.destroy(); // Destroy previous chart
    taxChart = new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Tax (BDT)",
                data: data,
                backgroundColor: "rgba(54, 162, 235, 0.2)",
                borderColor: "rgba(54, 162, 235, 1)",
                borderWidth: 2,
                pointRadius: 3,
                pointHoverRadius: 5,
            }, ],
        },
        options: {
            responsive: true,
            plugins: {
                tooltip: {
                    enabled: true,
                    callbacks: {
                        label: function(context) {
                            return `Tax: ${context.raw.toLocaleString()} BDT`;
                        },
                    },
                },
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: "Monthly Salary (BDT)"
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: "Tax (BDT)"
                    },
                    beginAtZero: true,
                },
            },
        },
    });
}

// Update Chart Function
function updateChart() {
    const monthlySalary = parseInt(document.getElementById("monthlySalary").value, 10);
    const gender = document.getElementById("gender").value;
    const bonusCount = parseInt(document.getElementById("bonusCount").value, 10);
    const annualSalary = monthlySalary * 12 + (monthlySalary * bonusCount);

    const labels = [];
    const data = [];

    for (let salary = 10000; salary <= 200000; salary += 5000) {
        const annual = salary * 12;
        labels.push(salary.toLocaleString());
        data.push(calculateTax(annual, gender));
    }

    createChart(labels, data);
}

// Initial Render
updateChart();