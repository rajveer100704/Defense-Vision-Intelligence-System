// Dashboard UI Logic
const markers = {};
const activeNodes = new Set();
const missionList = document.getElementById('mission-list');
const nodeList = document.getElementById('node-list');

const map = L.map('map', {
    zoomControl: false,
    attributionControl: false
}).setView([36.1627, -115.1391], 13);

L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    maxZoom: 20
}).addTo(map);

const markers = {};
const targetList = document.getElementById('target-list');
const alertList = document.getElementById('alert-list');
const wsStatus = document.getElementById('ws-status');

// WebSocket Connection
const socket = new WebSocket(`ws://${window.location.host}/ws`);

socket.onopen = () => {
    wsStatus.textContent = 'LINK ESTABLISHED';
    wsStatus.className = 'status-indicator online';
    console.log('Tactical link established.');
};

socket.onclose = () => {
    wsStatus.textContent = 'LINK SEVERED';
    wsStatus.className = 'status-indicator offline';
    console.error('Tactical link lost.');
};

const activeNodes = new Set();
const nodeList = document.getElementById('node-list');

socket.onmessage = (event) => {
    const data = JSON.parse(event.data);
    updateTarget(data);
    updateNodeRegistry(data.node);
};

function updateNodeRegistry(nodeId) {
    if (!nodeId) return;
    if (!activeNodes.has(nodeId)) {
        activeNodes.add(nodeId);
        const nodeEl = document.createElement('div');
        nodeEl.className = 'node-item';
        nodeEl.innerHTML = `<span class="pulse-small"></span> NODE: ${nodeId}`;
        nodeList.appendChild(nodeEl);
        
        const placeholder = nodeList.querySelector('.no-data');
        if (placeholder) placeholder.remove();
    }
}

    // Update or Create Marker
    const isReplay = target.is_replay || false;
    
    if (!markers[id]) {
        markers[id] = L.marker([lat, lon], {
            icon: L.divIcon({
                className: `target-marker ${target.threat_level?.toLowerCase() || 'low'} ${isReplay ? 'replay-active' : ''}`,
                html: `<div class="marker-id">${id}</div>`
            })
        }).addTo(map).bindPopup(`Target #${id} | ${cls} | Node: ${target.node || 'Unknown'} ${isReplay ? '(REPLAY)' : ''}`);

        // Path Forecast (Elite LSTM)
        markers[`${id}_path`] = L.polyline([], {
            color: '#ff3e3e',
            dashArray: '10, 10',
            weight: 2,
            opacity: 0.5
        }).addTo(map);

        // Create Ghost Marker for Prediction
        markers[`${id}_ghost`] = L.circleMarker([lat, lon], {
            radius: 5,
            color: '#00f2ff',
            dashArray: '5, 5',
            fillOpacity: 0.1,
            className: 'ghost-marker'
        }).addTo(map);
        
        // Add to Sidebar
        const targetEl = document.createElement('div');
        targetEl.id = `target-${id}`;
        targetEl.className = 'target-item';
        targetEl.innerHTML = `
            <div class="target-meta">
                <span class="id">#${id}</span>
                <span class="cls">${cls.toUpperCase()}</span>
                <span class="node" style="font-size: 0.7rem; opacity: 0.6; margin-left: auto;">${target.node || 'SRC:LOCAL'}</span>
            </div>
            <div class="target-stats">
                <span>CONF: ${(confidence * 100).toFixed(0)}%</span>
                <span class="threat">THREAT: ${target.threat_level || 'LOW'}</span>
            </div>
        `;
        targetList.prepend(targetEl);
        
        // Remove "No Data" if present
        const placeholder = targetList.querySelector('.no-data');
        if (placeholder) placeholder.remove();
    } else {
        markers[id].setLatLng([lat, lon]);
        markers[id].getElement().className = `leaflet-marker-icon target-marker ${target.threat_level?.toLowerCase() || 'low'} leaflet-zoom-animated leaflet-interactive`;
        
        // Update Ghost Position
        if (target.predicted_lat && target.predicted_lon) {
            markers[`${id}_ghost`].setLatLng([target.predicted_lat, target.predicted_lon]);
        }
        
        // Update LSTM Path
        if (target.long_term_path) {
            markers[`${id}_path`].setLatLngs(target.long_term_path);
        }
    }

    // Handle Alerts (Simulated from backend message properties if added later)
    if (target.alert) {
        addAlert(target.alert);
    }
}

// Handle Alerts
function addAlert(alert) {
    const alertEl = document.createElement('div');
    alertEl.className = `alert-item ${alert.level.toLowerCase()}`;
    alertEl.innerHTML = `
        <div class="alert-header">${alert.type}</div>
        <div class="alert-body">TARGET #${alert.target_id} in ${alert.zone_id}</div>
    `;
    alertList.prepend(alertEl);
    
    const placeholder = alertList.querySelector('.no-data');
    if (placeholder) placeholder.remove();
}

// Mission Replay System
async function loadMissions() {
    try {
        const res = await fetch('/missions/list');
        const data = await res.json();
        
        missionList.innerHTML = '';
        if (data.missions.length === 0) {
            missionList.innerHTML = '<div class="no-data">NO MISSION DATA FOUND</div>';
            return;
        }

        data.missions.forEach(m => {
            const el = document.createElement('div');
            el.className = 'mission-item';
            el.innerHTML = `
                <span>${m.replace('.jsonl', '')}</span>
                <button onclick="triggerReplay('${m}')">REPLAY</button>
            `;
            missionList.appendChild(el);
        });
    } catch (e) {
        console.error("Failed to load missions:", e);
    }
}

async function triggerReplay(filename) {
    console.log(`Command: Replay Mission ${filename}`);
    await fetch(`/missions/replay/${filename}`);
    // Clear current markers for clean replay
    Object.keys(markers).forEach(k => {
        map.removeLayer(markers[k]);
        delete markers[k];
    });
}

// Initial Load
loadMissions();
setInterval(loadMissions, 15000); // Refresh every 15s

// Update System Time
setInterval(() => {
    document.getElementById('system-time').textContent = new Date().toISOString().slice(11, 19) + ' UTC';
}, 1000);
