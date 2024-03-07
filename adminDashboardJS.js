document.addEventListener('DOMContentLoaded', function() {
    var ctx = document.getElementById('trafficChart').getContext('2d');
    var trafficChart = new Chart(ctx, {
        type: 'bar', // You can change this to 'bar', 'pie', etc. depending on your needs
        data: {
            labels: ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
            datasets: [{
                label: 'Visits',
                data: [12, 19, 3, 5, 2, 3, 9], // Example data
                backgroundColor: [
                    'rgba(255, 99, 132, 0.2)',
                ],
                borderColor: [
                    'rgba(255, 99, 132, 1)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
document.addEventListener('DOMContentLoaded', function() {
    // Mock user activity data
    const userActivities = [
        { activity: "John Doe logged in", timestamp: "2023-03-06 09:00" },
        { activity: "Jane Smith uploaded a photo", timestamp: "2023-03-06 09:30" },
        { activity: "Carlos Gomez commented on a post", timestamp: "2023-03-06 10:00" },
        { activity: "Toto logged in", timestamp: "2023-03-07 09:00" },
        { activity: "Toto uploaded a photo", timestamp: "2023-03-08 09:30" },
        { activity: "Carlos Gomez commented on a post", timestamp: "2023-03-09 10:00" },
        // Add more activities as needed
    ];

    const tableBody = document.getElementById('userActivitiesTable').getElementsByTagName('tbody')[0];

    userActivities.forEach(({ activity, timestamp }) => {
        let row = tableBody.insertRow();
        let activityCell = row.insertCell(0);
        activityCell.textContent = activity;
        let timestampCell = row.insertCell(1);
        timestampCell.textContent = timestamp;
    });
});
