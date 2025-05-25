/**
 * Initialize metrics display
 */
function initMetrics() {
    // Initially hide metrics content
    resetMetrics();
}

/**
 * Update metrics display with path data
 */
function updateMetricsDisplay(metrics) {
    if (!metrics) return;
    
    // Show metrics container
    document.getElementById('metrics-content').classList.add('active');
    
    // Update distance
    document.getElementById('distance-value').textContent = `${metrics.distance_km.toFixed(2)} km`;
    
    // Update time
    const formattedTime = formatTime(metrics.time_minutes);
    document.getElementById('time-value').textContent = formattedTime;
    
    // Reset progress bar
    updateProgress(0);
}

/**
 * Update metrics for a specific segment of the path
 */
function updateMetricsForSegment(segment, totalSegments) {
    if (!pathMetrics) return;
    
    const percentage = (segment / totalSegments) * 100;
    updateProgress(percentage);
}

/**
 * Reset metrics display
 */
function resetMetrics() {
    document.getElementById('metrics-content').classList.remove('active');
    document.getElementById('distance-value').textContent = '-';
    document.getElementById('time-value').textContent = '-';
    updateProgress(0);
}

/**
 * Format time in minutes to a human-readable string
 */
function formatTime(minutes) {
    if (minutes < 1) {
        return "Less than a minute";
    }
    
    const hours = Math.floor(minutes / 60);
    const mins = Math.round(minutes % 60);
    
    if (hours === 0) {
        return `${mins} minutes`;
    } else if (hours === 1 && mins === 0) {
        return "1 hour";
    } else if (mins === 0) {
        return `${hours} hours`;
    } else {
        return `${hours} hours ${mins} minutes`;
    }
}
