// URL of our FastAPI Backend
const API_BASE_URL = "http://127.0.0.1:8000";

// --- Tab Switching Logic ---
function switchTab(tabName) {
    // Update button styling
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');

    // Hide both sections, then show the requested one
    document.getElementById('encode-section').classList.replace('active-section', 'hidden-section');
    document.getElementById('decode-section').classList.replace('active-section', 'hidden-section');
    document.getElementById(`${tabName}-section`).classList.replace('hidden-section', 'active-section');
}

// --- Encode Process ---
document.getElementById('encode-form').addEventListener('submit', async (e) => {
    e.preventDefault(); // Stop the page from reloading
    
    const statusBox = document.getElementById('encode-status');
    statusBox.classList.remove('hidden');
    statusBox.innerHTML = "[*] Initiating secure encoding sequence... Please wait.";
    statusBox.style.borderLeftColor = "#00ffcc";

    // 1. Prepare FormData: This is crucial for sending files + text over HTTP.
    const formData = new FormData(e.target);

    try {
        // 2. Send the request to FastAPI
        const response = await fetch(`${API_BASE_URL}/api/encode`, {
            method: 'POST',
            body: formData 
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Server failed to process image.");
        }

        // 3. Handle FileResponse: FastAPI sends back an image file (a Blob)
        const imageBlob = await response.blob();
        
        // Create a temporary, invisible download link in the browser
        const downloadUrl = window.URL.createObjectURL(imageBlob);
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = "encoded_safe_image.png"; // Force download name
        document.body.appendChild(a);
        a.click(); // Trigger the download programmatically
        a.remove(); // Clean up

        statusBox.innerHTML = "[+] SUCCESS: Payload embedded. Encoded PNG downloaded to your machine.";
        e.target.reset(); // Clear the form
    } catch (error) {
        statusBox.style.borderLeftColor = "#ff4c4c";
        statusBox.innerHTML = `[-] ERROR: ${error.message}`;
    }
});

// --- Decode Process ---
document.getElementById('decode-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const statusBox = document.getElementById('decode-status');
    const textOutput = document.getElementById('extracted-text');
    
    statusBox.classList.remove('hidden');
    textOutput.innerHTML = "[*] Scanning LSBs and attempting decryption...";

    // Prepare FormData
    const formData = new FormData(e.target);

    try {
        const response = await fetch(`${API_BASE_URL}/api/decode`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Decryption failed.");
        }

        // Display the decrypted text returned by FastAPI JSON
        textOutput.innerText = data.secret_message;
        textOutput.style.color = "#00ffcc";
        e.target.reset();
    } catch (error) {
        textOutput.innerText = `[-] FATAL: ${error.message}`;
        textOutput.style.color = "#ff4c4c";
    }
});