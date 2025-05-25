// Global pathfinding variables
let currentPath = null;
let pathMetrics = null;

/**
 * Initialize pathfinding functionality
 */
function initPathfinding() {
    // Setup button event listeners
    document.getElementById('set-start-btn').addEventListener('click', function() {
        isSettingStart = true;
        isSettingEnd = false;
        this.classList.add('active');
        document.getElementById('set-end-btn').classList.remove('active');
        document.querySelector('body').style.cursor = 'crosshair';
    });
    
    document.getElementById('set-end-btn').addEventListener('click', function() {
        isSettingEnd = true;
        isSettingStart = false;
        this.classList.add('active');
        document.getElementById('set-start-btn').classList.remove('active');
        document.querySelector('body').style.cursor = 'crosshair';
    });
    
    document.getElementById('find-path-btn').addEventListener('click', findPath);
    document.getElementById('reset-btn').addEventListener('click', resetAll);
    
    // Reset cursor when clicking elsewhere
    document.getElementById('map-container').addEventListener('click', function() {
        document.querySelector('body').style.cursor = '';
    });
}

/**
 * Find path between start and end points
 */
function findPath() {
    if (!startMarker || !endMarker) {
        showError('Please set both start and end points');
        return;
    }
    
    showLoading();
    
    const start = [startMarker.getLatLng().lng, startMarker.getLatLng().lat];
    const end = [endMarker.getLatLng().lng, endMarker.getLatLng().lat];
    const algorithm = document.getElementById('algorithm-select').value;
    
    fetch('/api/find-path', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start: start,
            end: end,
            algorithm: algorithm
        })
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(err => { throw new Error(err.error || 'Path finding failed'); });
        }
        return response.json();
    })
    .then(data => {
        // Store path and metrics
        currentPath = data.path;
        pathMetrics = data.metrics;
        
        // Draw path on map
        const pathLayer = drawPath(currentPath);
        
        // Show path metrics
        updateMetricsDisplay(pathMetrics);
        
        // Prepare animation
        prepareAnimation(currentPath);
        
        hideLoading();
    })
    .catch(error => {
        console.error('Error finding path:', error);
        hideLoading();
        showError(error.message || 'Failed to find path. Please try different points.');
    });
}

/**
 * Reset all map elements and pathfinding state
 */
function resetAll() {
    // Reset map elements
    resetMap();
    
    // Reset pathfinding state
    currentPath = null;
    pathMetrics = null;
    
    // Reset animation
    resetAnimation();
    
    // Hide metrics
    resetMetrics();
    
    // Hide animation controls
    document.getElementById('animation-controls').classList.remove('active');
}

/**
 * Calculate distance between two points in kilometers
 */
function calculateDistance(point1, point2) {
    // Convert to radians
    const toRad = function(n) {
        return n * Math.PI / 180;
    };
    
    const lat1 = point1[1];
    const lon1 = point1[0];
    const lat2 = point2[1];
    const lon2 = point2[0];
    
    const R = 6371; // Earth radius in km
    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);
    const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
              Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
              Math.sin(dLon/2) * Math.sin(dLon/2);
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
    const distance = R * c;
    
    return distance;
}

/**
 * Calculate estimated travel time in minutes
 */
function calculateTravelTime(distanceKm, speedKmh = 40) {
    return (distanceKm / speedKmh) * 60; // Convert to minutes
}
