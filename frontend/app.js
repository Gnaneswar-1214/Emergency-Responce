let charts = {};

async function runBenchmark() {
    const sizesInput = document.getElementById('datasets').value;
    const distribution = document.getElementById('distribution').value;
    
    const sizes = sizesInput.split(',').map(s => parseInt(s.trim())).filter(s => !isNaN(s));
    
    if (sizes.length === 0) {
        alert("Please enter valid dataset sizes.");
        return;
    }

    document.getElementById('loading').classList.remove('hidden');
    document.getElementById('resultsSection').classList.add('hidden');
    document.getElementById('runBtn').disabled = true;

    try {
        const response = await fetch('/benchmark', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sizes, distribution })
        });
        
        const res = await response.json();
        
        if (res.status === 'success') {
            renderResults(res.data, sizes);
            document.getElementById('resultsSection').classList.remove('hidden');
        } else {
            alert("Error running benchmarks.");
        }
    } catch (error) {
        console.error("Benchmark error:", error);
        alert("Failed to connect to the backend.");
    } finally {
        document.getElementById('loading').classList.add('hidden');
        document.getElementById('runBtn').disabled = false;
    }
}

function renderResults(data, sizes) {
    const structures = Object.keys(data);
    const colors = {
        "Heap": "#2f81f7",
        "Sorted Array": "#e34c26",
        "Hash Map": "#f1e05a",
        "Balanced BST": "#2ea043"
    };

    // Prepare datasets for charts
    const getDataset = (metric) => structures.map(name => ({
        label: name,
        data: data[name].map(d => d[metric]),
        borderColor: colors[name],
        backgroundColor: colors[name] + '40',
        tension: 0.1,
        borderWidth: 2,
        pointRadius: 4
    }));

    updateChart('insertChart', sizes, getDataset('insert_time_ms'), 'Time (ms)');
    updateChart('extractChart', sizes, getDataset('extract_time_ms'), 'Time (ms)');
    updateChart('updateChart', sizes, getDataset('update_time_ms'), 'Time (ms)');
    updateChart('deleteChart', sizes, getDataset('delete_time_ms'), 'Time (ms)');
    updateChart('topkChart', sizes, getDataset('top_k_time_ms'), 'Time (ms)');
    updateChart('memoryChart', sizes, getDataset('memory_bytes'), 'Memory (Bytes)');

    renderTable(data, sizes, structures);
}

function updateChart(canvasId, labels, datasets, yAxisLabel) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    
    if (charts[canvasId]) {
        charts[canvasId].destroy();
    }

    charts[canvasId] = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: { 
                    title: { display: true, text: 'Dataset Size (N)', color: '#8b949e' },
                    ticks: { color: '#8b949e' },
                    grid: { color: '#30363d' }
                },
                y: { 
                    title: { display: true, text: yAxisLabel, color: '#8b949e' },
                    ticks: { color: '#8b949e' },
                    grid: { color: '#30363d' }
                }
            },
            plugins: {
                legend: { labels: { color: '#e6edf3' } }
            }
        }
    });
}

function renderTable(data, sizes, structures) {
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    // Let's just pick the largest size for the summary table
    const largestSize = sizes[sizes.length - 1];

    structures.forEach(name => {
        const metricsList = data[name];
        const largestMetrics = metricsList.find(m => m.size === largestSize) || metricsList[metricsList.length - 1];
        
        let advanced = "";
        if (largestMetrics.swaps !== undefined) advanced += `Swaps: ${largestMetrics.swaps}<br>`;
        if (largestMetrics.comparisons !== undefined) advanced += `Comps: ${largestMetrics.comparisons}<br>`;
        if (largestMetrics.height !== undefined) advanced += `Height: ${largestMetrics.height}<br>`;
        if (largestMetrics.resorts !== undefined) advanced += `Resorts: ${largestMetrics.resorts}<br>`;
        if (largestMetrics.rotations !== undefined) advanced += `Rotations: ${largestMetrics.rotations}<br>`;

        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><strong>${name}</strong></td>
            <td>${largestMetrics.size}</td>
            <td>${largestMetrics.insert_time_ms.toFixed(3)}</td>
            <td>${largestMetrics.extract_time_ms.toFixed(3)}</td>
            <td>${largestMetrics.update_time_ms.toFixed(3)}</td>
            <td>${largestMetrics.top_k_time_ms.toFixed(3)}</td>
            <td>${largestMetrics.memory_bytes}</td>
            <td style="font-size: 0.85em; color: #8b949e;">${advanced || "N/A"}</td>
        `;
        tbody.appendChild(tr);
    });
}
