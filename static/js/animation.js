// Animation variables
let animationPath = null;
let animationPoints = null;
let animationFrame = 0;
let animationSpeed = 5;
let animationInterval = null;
let isAnimating = false;

/**
 * Initialize animation controls
 */
function initAnimation() {
    // Animation controls
    document.getElementById('play-animation-btn').addEventListener('click', playAnimation);
    document.getElementById('pause-animation-btn').addEventListener('click', pauseAnimation);
    document.getElementById('reset-animation-btn').addEventListener('click', resetAnimation);
    
    // Animation speed control
    document.getElementById('animation-speed-control').addEventListener('input', function() {
        animationSpeed = parseInt(this.value);
        if (isAnimating) {
            // Restart animation with new speed
            pauseAnimation();
            playAnimation();
        }
    });
}

/**
 * Prepare animation for current path
 */
function prepareAnimation(path) {
    // Reset any existing animation
    resetAnimation();
    
    // Create animated path layer
    const animationData = createAnimatedPath(path);
    animationPath = animationData.polyline;
    animationPoints = animationData.points;
    
    // Show animation controls
    document.getElementById('animation-controls').classList.add('active');
}

/**
 * Play the path animation
 */
function playAnimation() {
    if (!animationPoints || animationPoints.length === 0) {
        return;
    }
    
    // Stop any existing animation
    pauseAnimation();
    
    // Set animation as active
    isAnimating = true;
    
    // Calculate interval based on speed
    const interval = 1000 / animationSpeed;
    
    // Start animation
    animationInterval = setInterval(() => {
        if (animationFrame < animationPoints.length) {
            // Update animated path with current segment
            updateAnimatedPath(animationPoints.slice(0, animationFrame + 1));
            
            // Update progress
            updateProgress(animationFrame / (animationPoints.length - 1) * 100);
            
            // Increment frame
            animationFrame++;
        } else {
            // Animation complete
            pauseAnimation();
            animationFrame = animationPoints.length - 1;
        }
    }, interval);
}

/**
 * Pause the path animation
 */
function pauseAnimation() {
    if (animationInterval) {
        clearInterval(animationInterval);
        animationInterval = null;
    }
    isAnimating = false;
}

/**
 * Reset the path animation
 */
function resetAnimation() {
    // Stop animation
    pauseAnimation();
    
    // Reset animation state
    animationFrame = 0;
    
    // Clear animated path
    if (animationPath) {
        map.removeLayer(animationPath);
        animationPath = null;
    }
    
    // Reset path points
    animationPoints = null;
    
    // Hide animation controls
    document.getElementById('animation-controls').classList.remove('active');
    
    // Reset progress
    updateProgress(0);
}

/**
 * Update progress display
 */
function updateProgress(percentage) {
    const progressBar = document.getElementById('route-progress-bar');
    const progressPercentage = document.getElementById('progress-percentage');
    
    progressBar.style.width = `${percentage}%`;
    progressBar.setAttribute('aria-valuenow', percentage);
    progressPercentage.textContent = `${Math.round(percentage)}%`;
    
    // Update metrics based on progress
    if (pathMetrics) {
        updateMetricsForProgress(percentage);
    }
}

/**
 * Update metrics based on current animation progress
 */
function updateMetricsForProgress(percentage) {
    if (!pathMetrics) return;
    
    const coveredDistance = pathMetrics.distance_km * (percentage / 100);
    const remainingDistance = pathMetrics.distance_km - coveredDistance;
    const timeMinutes = pathMetrics.time_minutes * (percentage / 100);
    const remainingTime = pathMetrics.time_minutes - timeMinutes;
    
    // Update distance display
    document.getElementById('distance-value').textContent = 
        `${coveredDistance.toFixed(2)} km / ${pathMetrics.distance_km.toFixed(2)} km`;
    
    // Update time display
    const formattedTimeRemaining = formatTime(remainingTime);
    document.getElementById('time-value').textContent = 
        `${formattedTimeRemaining} remaining`;
}
