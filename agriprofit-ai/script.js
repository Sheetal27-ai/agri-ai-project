/**
 * AgriProfit AI - Core Application Logic
 * Handling SPA Navigation, Soil Upload Simulation, and Analysis Display
 */

// --- NAVIGATION LOGIC ---
function navigateTo(pageId) {
    const pages = ['home', 'dashboard', 'results'];
    const body = document.body;
    const sidebar = document.getElementById('sidebar');
    const topNav = document.getElementById('top-nav');

    // Update visibility
    pages.forEach(p => {
        const section = document.getElementById(`page-${p}`);
        if (p === pageId) {
            section.classList.remove('hidden');
        } else {
            section.classList.add('hidden');
        }
    });

    // Sidebar/TopNav behavior based on page
    if (pageId === 'home') {
        body.classList.remove('sidebar-active');
        sidebar.classList.add('-translate-x-full');
        topNav.classList.remove('hidden');
    } else {
        body.classList.add('sidebar-active');
        sidebar.classList.remove('-translate-x-full');
        // On smaller screens, the top nav stays, on large we might modify it
        if (window.innerWidth > 768) {
            topNav.classList.add('hidden');
        }
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });

    // Update active state in sidebar
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('onclick').includes(pageId)) {
            link.classList.add('active');
        }
    });
}

// --- GPS INTEGRATION ---
let currentLat = null;
let currentLon = null;

function initGPS() {
    const statusElement = document.getElementById('gps-status');
    statusElement.innerText = "Requesting Location...";
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                currentLat = position.coords.latitude.toFixed(4);
                currentLon = position.coords.longitude.toFixed(4);
                statusElement.innerText = `Lat: ${currentLat}° N, Lon: ${Math.abs(currentLon)}° W`;
                statusElement.classList.add('text-gold-accent', 'font-bold');
            },
            (error) => {
                statusElement.innerText = "Location Denied. Using Default.";
                currentLat = "41.8781";
                currentLon = "-87.6298";
            }
        );
    } else {
        statusElement.innerText = "Geolocation not supported.";
    }
}

function toggleManualGPS() {
    const isManual = document.getElementById('manual-gps-toggle').checked;
    const manualInputs = document.getElementById('manual-gps-inputs');
    const statusElement = document.getElementById('gps-status');

    if (isManual) {
        manualInputs.classList.remove('hidden');
        statusElement.innerText = "Manual Input Active";
        statusElement.classList.remove('text-gold-accent', 'font-bold');
        statusElement.classList.add('text-sand/50');
        
        // Auto-fill the manual inputs with the exact fetched current location!
        if (currentLat && currentLon) {
            document.getElementById('manual-lat').value = currentLat;
            document.getElementById('manual-lon').value = Math.abs(currentLon); // Optional: keep as positive or exact depending on how you read it, let's just do exact.
            document.getElementById('manual-lon').value = currentLon;
        }
    } else {
        manualInputs.classList.add('hidden');
        statusElement.classList.add('text-gold-accent', 'font-bold');
        statusElement.classList.remove('text-sand/50');
        if (currentLat && currentLon) {
             statusElement.innerText = `Lat: ${currentLat}° N, Lon: ${Math.abs(currentLon)}° W`;
        } else {
             initGPS(); // Try to fetch again if they turn manual off and we had none
        }
    }
}

// --- SOIL UPLOAD PREVIEW ---
const fileInput = document.getElementById('file-input');
const dropZone = document.getElementById('drop-zone');
const previewImg = document.getElementById('soil-preview');
const previewContainer = document.getElementById('preview-container');

fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            previewImg.src = event.target.result;
            previewContainer.classList.remove('hidden');
            dropZone.querySelector('h3').innerText = "Soil Sample Locked";
            dropZone.classList.add('border-forest');
        };
        reader.readAsDataURL(file);
    }
});

// --- AI ANALYSIS DATA ---
function populateAnalysisData(data) {
    // Populate simple text
    document.getElementById('ph-level').innerText = data.pH_range + " pH";
    document.getElementById('moisture-level').innerText = data.moisture;
    document.getElementById('soil-type').innerText = data.soil_type;

    // We can show Risk Factor in crop-3 spot or elsewhere, for now let's just populate the top 3 crops.
    // The backend provides a list of recommended_crops (strings), we will assign arbitrary profits for the demo UI.
    
    document.getElementById('crop-1-name').innerText = data.recommended_crops[0] || "Unknown";
    document.getElementById('crop-1-profit').innerText = "$1,450.00/ac";
    
    document.getElementById('crop-2-name').innerText = data.recommended_crops[1] || "Unknown";
    document.getElementById('crop-2-profit').innerText = "$980.00/ac";
    
    document.getElementById('crop-3-name').innerText = data.recommended_crops[2] || "Unknown";
    document.getElementById('crop-3-profit').innerText = "$620.00/ac"; // Demo specific profit

    // Populate Climate and Weather Info exactly as required by DOM bindings
    if (data.location) {
        document.getElementById('climate').innerText = data.location.climate || "Unknown";
    }
    
    if (data.weather) {
        document.getElementById('temperature').innerText = data.weather.temperature ? `${data.weather.temperature}°C` : "N/A";
        document.getElementById('humidity').innerText = data.weather.humidity || "N/A";
        document.getElementById('condition').innerText = data.weather.condition || "N/A";
    }

    document.getElementById('risk-factor').innerText = data.risk_factor || "None";

    // Set bar widths
    let phValue = parseFloat(data.pH_range ? data.pH_range.split("-")[0] : 7);
    if(isNaN(phValue)) phValue = 7;
    document.getElementById('ph-bar').style.width = (phValue / 14 * 100) + "%";
    document.getElementById('moisture-bar').style.width = parseFloat(data.moisture) + "%";
}

function getFinalLocation() {
    const isManual = document.getElementById('manual-gps-toggle').checked;
    if (isManual) {
        return {
            lat: document.getElementById('manual-lat').value,
            lon: document.getElementById('manual-lon').value
        };
    }
    return { lat: currentLat, lon: currentLon };
}

// --- BACKEND API INTEGRATION ---
async function startAnalysis() {
    const btn = event.currentTarget || document.querySelector('button[onclick="startAnalysis()"]');
    const originalContent = btn.innerHTML;
    
    const fileInput = document.getElementById('file-input');
    if (!fileInput.files[0]) {
        alert("Please upload a soil image first.");
        return;
    }

    btn.disabled = true;
    btn.innerHTML = `
        <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
        </svg>
        Analyzing ML Pipeline...
    `;

    try {
        console.log("🚀 Initializing API Request to http://127.0.0.1:8000/analyze");
        const formData = new FormData();
        formData.append("file", fileInput.files[0]);
        
        const loc = getFinalLocation();
        if (loc.lat) formData.append("lat", loc.lat);
        if (loc.lon) formData.append("lon", loc.lon);
        
        console.log("📦 Payload attached: ", fileInput.files[0].name, "| Lat:", loc.lat, "| Lon:", loc.lon);

        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });
        
        console.log("🌐 Server responded with status:", response.status);

        if (!response.ok) {
            const errData = await response.json().catch(() => ({}));
            throw new Error(errData.detail || `Server returned ${response.status}`);
        }
        
        const data = await response.json();
        console.log("✅ Data successfully parsed:", data);
        
        // Push original image to results page
        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('result-soil-img').src = e.target.result;
        };
        reader.readAsDataURL(fileInput.files[0]);

        populateAnalysisData(data);
        navigateTo('results');
        
        // Re-trigger progress bar animations
        animateProgressBars();

    } catch (error) {
        console.error("❌ CRITICAL ERROR connecting to backend:", error);
        alert(`Connection Failed: ${error.message}\n\nPlease ensure your FastAPI python server is running on port 8000!`);
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalContent;
    }
}

function animateProgressBars() {
    const bars = document.querySelectorAll('.h-full.transition-all');
    bars.forEach(bar => {
        const finalWidth = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.width = finalWidth;
        }, 100);
    });
}

// --- INITIALIZE ---
window.onload = () => {
    // Check if URL has hash for specific page
    const hash = window.location.hash.replace('#', '');
    if (hash && ['home', 'dashboard', 'results'].includes(hash)) {
        navigateTo(hash);
    } else {
        navigateTo('home');
    }
    
    initGPS();
};

// Handle window resize for sidebar/nav logic
window.onresize = () => {
    const currentSection = document.querySelector('section:not(.hidden)');
    if (currentSection && currentSection.id !== 'page-home') {
        if (window.innerWidth > 768) {
            document.getElementById('top-nav').classList.add('hidden');
        } else {
            document.getElementById('top-nav').classList.remove('hidden');
        }
    }
};
