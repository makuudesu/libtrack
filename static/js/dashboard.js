// Get data passed from Django template via json_script
const borrowerCountData = JSON.parse(document.getElementById('borrower-data').textContent);
const transactionData = JSON.parse(document.getElementById('transaction-data').textContent);
const availabilityData = JSON.parse(document.getElementById('availability-data').textContent);

// Borrower Count Chart
const borrowerChart = new Chart(document.getElementById('borrowerChart'), {
    type: 'bar',
    data: {
        labels: Object.keys(borrowerCountData), // Borrow counts (0, 1, 2, etc.)
        datasets: [{
            label: 'Number of Borrowers',
            data: Object.values(borrowerCountData), // Corresponding borrower counts
            backgroundColor: '#34D399', // Tailwind Green
            borderColor: '#16A34A',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Transactions per day Chart
const transactionChart = new Chart(document.getElementById('transactionChart'), {
    type: 'bar',
    data: {
        labels: Object.keys(transactionData), // Dates (e.g., Jan 1, Jan 2, etc.)
        datasets: [{
            label: 'Transactions',
            data: Object.values(transactionData), // Corresponding transaction counts
            backgroundColor: '#34D399', // Tailwind Green
            borderColor: '#16A34A',
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});

// Book Availability Pie Chart
const availabilityChart = new Chart(document.getElementById('availabilityChart'), {
    type: 'pie',
    data: {
        labels: ['Available', 'Borrowed'],
        datasets: [{
            data: [availabilityData.available, availabilityData.borrowed],
            backgroundColor: ['#34D399', '#FF5733'], // Green for available, Red for borrowed
            borderColor: ['#16A34A', '#C0392B'],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            tooltip: {
                callbacks: {
                    label: function(tooltipItem) {
                        return tooltipItem.label + ': ' + tooltipItem.raw + ' books';
                    }
                }
            }
        }
    }
});

// Mobile Menu Toggle
const menuToggle = document.getElementById('menu-toggle');
const mobileMenu = document.getElementById('mobile-menu');
const line1 = document.getElementById('line-1');
const line2 = document.getElementById('line-2');
const line3 = document.getElementById('line-3');

if (menuToggle && mobileMenu) {
    menuToggle.addEventListener('click', () => {
        // Toggle the mobile menu
        mobileMenu.classList.toggle('hidden');
        mobileMenu.classList.toggle('transform');
        mobileMenu.classList.toggle('translate-y-0');
        mobileMenu.classList.toggle('translate-y-full');
        mobileMenu.classList.toggle('transition-transform');
        mobileMenu.classList.toggle('duration-300');
        
        // Toggle the hamburger icon to "X" animation
        line1.classList.toggle('rotate-45');
        line1.classList.toggle('translate-y-2');
        line2.classList.toggle('opacity-0');
        line3.classList.toggle('-rotate-45');
        line3.classList.toggle('-translate-y-2');
    });
}


// Display the current date and time in the footer
const datetimeElement = document.getElementById('datetime');
const updateDatetime = () => {
    const currentDate = new Date();
    const dateStr = currentDate.toLocaleString();
    datetimeElement.textContent = `${dateStr}`;
};
setInterval(updateDatetime, 1000);
