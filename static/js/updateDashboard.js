function generateDashboardHTML() {
    const container = document.getElementById('dashboardCards');
    
    dashboardConfig.sections.forEach((section, index) => {
        const card = document.createElement('div');
        card.className = 'dashboard-card p-6 animate__animated animate__fadeInUp';
        card.style.animationDelay = `${index * 0.2}s`;
        
        card.innerHTML = `
            <div class="card-header">
                <h2 class="text-xl font-semibold text-gray-800">${section.title}</h2>
            </div>
            <div class="space-y-4">
                ${section.fields.map(field => `
                    <div class="data-group">
                        <div class="data-label">${field.label}</div>
                        <div class="data-value" id="${field.id}"></div>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(card);
    });
}

function updateDashboard(data) {
    dashboardConfig.sections.forEach(section => {
        section.fields.forEach(field => {
            const element = document.getElementById(field.id);
            let value = data[field.key];
            
            if (field.format === 'date') {
                value = formatDate(value);
            }
            
            element.textContent = value;
        });
    });

    // Update last updated timestamp and latency
    document.getElementById('lastUpdated').innerHTML = 
        ` Last updated: ${new Date().toLocaleString()}`;

    const latencyBadge = document.getElementById('latencyBadge');
    if (data._latency) {
        latencyBadge.textContent = `API Latency: ${(data._latency * 1000).toFixed(2)} ms`;
        latencyBadge.classList.remove('hidden');
    }
}