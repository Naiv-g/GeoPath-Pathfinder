// Global map variables
let map;
let roadLayers = [];
let pathLayer = null;
let animatedPathLayer = null;
let startMarker = null;
let endMarker = null;
let isSettingStart = false;
let isSettingEnd = false;
let currentBounds = null;

/**
 * Initialize the map and load road data
 */
function initMap() {
    // Create the map
    map = L.map('map-container', {
        zoomControl: false
    }).setView([30.3256, 78.0437], 13); // Dehradun center

    // Add zoom control to the bottom-right
    L.control.zoom({
        position: 'bottomright'
    }).addTo(map);

    // Add tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
        maxZoom: 19
    }).addTo(map);

    // Load road data
    loadRoadData();

    // Map click handler
    map.on('click', handleMapClick);
}

/**
 * Load road data from the backend API
 */
function loadRoadData() {
    showLoading();
    
    fetch('/api/map-data')
        .then(response => response.json())
        .then(data => {
            // Clear existing road layers
            clearRoadLayers();
            
            // Add roads to the map
            data.roads.forEach(road => {
                const points = road.map(point => [point[1], point[0]]); // [lat, lon]
                const roadLine = L.polyline(points, {
                    color: '#888',
                    weight: 2,
                    opacity: 0.7
                });
                roadLine.addTo(map);
                roadLayers.push(roadLine);
            });
            
            // Set map bounds
            if (data.bounds) {
                currentBounds = [
                    [data.bounds.minLat, data.bounds.minLon],
                    [data.bounds.maxLat, data.bounds.maxLon]
                ];
                map.fitBounds(currentBounds);
            }
            
            hideLoading();
        })
        .catch(error => {
            console.error('Error loading road data:', error);
            hideLoading();
            showError('Failed to load map data. Please refresh the page.');
        });
}

/**
 * Handle map click events for setting start and end points
 */
function handleMapClick(e) {
    if (isSettingStart) {
        setStartPoint(e.latlng);
        isSettingStart = false;
        document.getElementById('set-start-btn').classList.remove('active');
    } else if (isSettingEnd) {
        setEndPoint(e.latlng);
        isSettingEnd = false;
        document.getElementById('set-end-btn').classList.remove('active');
    }
    
    // Enable the find path button if both markers are set
    if (startMarker && endMarker) {
        document.getElementById('find-path-btn').disabled = false;
    }
}

/**
 * Set the start point on the map
 */
function setStartPoint(latlng) {
    // Remove existing marker if any
    if (startMarker) {
        map.removeLayer(startMarker);
    }
    
    // Find nearest node to clicked point
    findNearestNode([latlng.lng, latlng.lat])
        .then(nearestPoint => {
            // Create a custom icon marker
            startMarker = L.marker([nearestPoint[1], nearestPoint[0]], {
                icon: L.divIcon({
                    className: 'start-marker',
                    html: '<i class="fa-solid fa-location-dot"></i>'
                }),
                draggable: false
            }).addTo(map);
            
            // Update UI
            document.querySelector('#set-start-btn').innerHTML = 
                '<i class="fa-solid fa-location-dot me-2"></i>Change Start';
        })
        .catch(error => {
            console.error('Error finding nearest node:', error);
            showError('Failed to set start point. Please try again.');
        });
}

/**
 * Set the end point on the map
 */
function setEndPoint(latlng) {
    // Remove existing marker if any
    if (endMarker) {
        map.removeLayer(endMarker);
    }
    
    // Find nearest node to clicked point
    findNearestNode([latlng.lng, latlng.lat])
        .then(nearestPoint => {
            // Create a custom icon marker
            endMarker = L.marker([nearestPoint[1], nearestPoint[0]], {
                icon: L.divIcon({
                    className: 'end-marker',
                    html: '<i class="fa-solid fa-flag-checkered"></i>'
                }),
                draggable: false
            }).addTo(map);
            
            // Update UI
            document.querySelector('#set-end-btn').innerHTML = 
                '<i class="fa-solid fa-flag-checkered me-2"></i>Change End';
        })
        .catch(error => {
            console.error('Error finding nearest node:', error);
            showError('Failed to set end point. Please try again.');
        });
}

/**
 * Find the nearest node in the road network
 */
function findNearestNode(point) {
    return fetch('/api/nearest-node', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ point: point })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        return data.node;
    });
}

/**
 * Draw the path on the map
 */
function drawPath(path) {
    // Clear existing path
    clearPath();
    
    // Convert path points to [lat, lon] format for Leaflet
    const points = path.map(point => [point[1], point[0]]);
    
    // Create the path layer
    pathLayer = L.polyline(points, {
        color: window.getVar('--secondary-color', '#43A047'),
        weight: 5,
        opacity: 0.7,
        lineCap: 'round',
        lineJoin: 'round'
    }).addTo(map);
    
    // Fit the map to the path bounds with padding
    map.fitBounds(pathLayer.getBounds(), {
        padding: [50, 50]
    });
    
    return pathLayer;
}

/**
 * Create animated path layer
 */
function createAnimatedPath(path) {
    // Convert path points to [lat, lon] format for Leaflet
    const points = path.map(point => [point[1], point[0]]);
    
    // Create an empty polyline for animation
    animatedPathLayer = L.polyline([], {
        color: window.getVar('--accent-color', '#FF5722'),
        weight: 6,
        opacity: 0.9,
        lineCap: 'round',
        lineJoin: 'round'
    }).addTo(map);
    
    return {
        polyline: animatedPathLayer,
        points: points
    };
}

/**
 * Update animated path with current points
 */
function updateAnimatedPath(pointsArray) {
    if (animatedPathLayer) {
        animatedPathLayer.setLatLngs(pointsArray);
    }
}

/**
 * Clear the path from the map
 */
function clearPath() {
    if (pathLayer) {
        map.removeLayer(pathLayer);
        pathLayer = null;
    }
    
    if (animatedPathLayer) {
        map.removeLayer(animatedPathLayer);
        animatedPathLayer = null;
    }
}

/**
 * Clear all road layers
 */
function clearRoadLayers() {
    roadLayers.forEach(layer => map.removeLayer(layer));
    roadLayers = [];
}

/**
 * Reset the map view
 */
function resetMapView() {
    if (currentBounds) {
        map.fitBounds(currentBounds);
    }
}

/**
 * Reset all map elements
 */
function resetMap() {
    // Clear markers
    if (startMarker) {
        map.removeLayer(startMarker);
        startMarker = null;
    }
    
    if (endMarker) {
        map.removeLayer(endMarker);
        endMarker = null;
    }
    
    // Clear path
    clearPath();
    
    // Reset button text
    document.querySelector('#set-start-btn').innerHTML = 
        '<i class="fa-solid fa-location-dot me-2"></i>Set Start';
    document.querySelector('#set-end-btn').innerHTML = 
        '<i class="fa-solid fa-flag-checkered me-2"></i>Set End';
    
    // Disable find path button
    document.getElementById('find-path-btn').disabled = true;
    
    // Reset map view
    resetMapView();
}

/**
 * Show loading overlay
 */
function showLoading() {
    document.getElementById('loading-overlay').classList.add('active');
}

/**
 * Hide loading overlay
 */
function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('active');
}

/**
 * Show error message
 */
function showError(message) {
    alert(message);
}

// Add CSS variables to window for direct access
const style = getComputedStyle(document.documentElement);
window.getVar = function(name, fallback) {
    return style.getPropertyValue(name).trim() || fallback;
};
