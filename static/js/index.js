// Generate HTML structure
generateDashboardHTML();

// Fetch data when page loads
fetch('/api/student-data')
    .then(response => {
        if (!response.ok) {
            return response.json().then(data => {
                throw new Error(data.error || 'Failed to load data');
            });
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        updateDashboard(data);
    })
    .catch(error => {
        console.error('Error:', error);
        
        document.getElementById('lastUpdated').innerHTML = 
            ` Failed to load data`;
        
        const errorContainer = document.createElement('div');
        errorContainer.className = 'bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative mt-4';
        errorContainer.innerHTML = `
            <strong>Error: </strong>
            ${error.message}
        `;
        
        // Remove any existing error messages before adding new one
        const existingError = document.querySelector('.dashboard-container .bg-red-100');
        if (existingError) {
            existingError.remove();
        }
        
        document.querySelector('.dashboard-container').appendChild(errorContainer);
    });