/*
ChronoVision – Photo Time Travel
JavaScript for image upload, processing, and comparison slider
*/

// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const browseBtn = document.getElementById('browseBtn');
const uploadContent = document.getElementById('uploadContent');
const previewContainer = document.getElementById('previewContainer');
const imagePreview = document.getElementById('imagePreview');
const changeImageBtn = document.getElementById('changeImageBtn');
const filterSection = document.getElementById('filterSection');
const filterBtns = document.querySelectorAll('.filter-btn');
const filterDescs = document.querySelectorAll('.filter-desc');
const applyFilterBtn = document.getElementById('applyFilterBtn');
const loadingSection = document.getElementById('loadingSection');
const resultsSection = document.getElementById('resultsSection');
const originalImage = document.getElementById('originalImage');
const processedImage = document.getElementById('processedImage');
const processedLabel = document.getElementById('processedLabel');
const comparisonSlider = document.getElementById('comparisonSlider');
const sliderHandle = document.getElementById('sliderHandle');
const newImageBtn = document.getElementById('newImageBtn');
const downloadBtn = document.getElementById('downloadBtn');

// State
let selectedFile = null;
let selectedFilter = '1920s';
let processedImagePath = '';

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
});

function setupEventListeners() {
    // Upload area click (only if not showing preview)
    uploadArea.addEventListener('click', (e) => {
        if (previewContainer.style.display === 'none') {
            fileInput.click();
        }
    });

    // Browse button click
    browseBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // Change image button click
    changeImageBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        fileInput.click();
    });

    // File input change
    fileInput.addEventListener('change', handleFileSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', handleDragOver);
    uploadArea.addEventListener('dragleave', handleDragLeave);
    uploadArea.addEventListener('drop', handleDrop);

    // Filter button selection
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            selectFilter(btn);
        });
    });

    // Apply filter button
    applyFilterBtn.addEventListener('click', applyFilter);

    // New image button
    newImageBtn.addEventListener('click', resetUpload);

    // Download button
    downloadBtn.addEventListener('click', downloadImage);

    // Comparison slider
    setupComparisonSlider();
}

function handleFileSelect(e) {
    const file = e.target.files[0];
    if (file) {
        processFile(file);
    }
}

function handleDragOver(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#6366f1';
    uploadArea.style.background = 'rgba(99, 102, 241, 0.1)';
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#334155';
    uploadArea.style.background = 'transparent';
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.style.borderColor = '#334155';
    uploadArea.style.background = 'transparent';
    
    const file = e.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
        processFile(file);
    }
}

function processFile(file) {
    // Validate file type
    if (!file.type.startsWith('image/')) {
        alert('Please select an image file');
        return;
    }

    // Validate file size (16MB max)
    if (file.size > 16 * 1024 * 1024) {
        alert('File size must be less than 16MB');
        return;
    }

    selectedFile = file;

    // Show image preview using FileReader
    const reader = new FileReader();
    reader.onload = function(e) {
        imagePreview.src = e.target.result;
        uploadContent.style.display = 'none';
        previewContainer.style.display = 'flex';
    };
    reader.readAsDataURL(file);

    // Show filter selection
    filterSection.style.display = 'block';
    
    // Select first filter by default
    selectFilter(filterBtns[0]);
    
    // Scroll to filter section
    filterSection.scrollIntoView({ behavior: 'smooth' });
}

function selectFilter(btn) {
    // Remove selected class from all buttons
    filterBtns.forEach(b => b.classList.remove('selected'));
    
    // Add selected class to clicked button
    btn.classList.add('selected');
    
    // Update selected filter
    selectedFilter = btn.dataset.filter;
    
    // Update filter descriptions
    filterDescs.forEach(desc => desc.classList.remove('active'));
    const activeDesc = document.getElementById(`desc-${selectedFilter}`);
    if (activeDesc) {
        activeDesc.classList.add('active');
    }
}

async function applyFilter() {
    if (!selectedFile) {
        alert('Please select an image first');
        return;
    }

    // Show loading
    loadingSection.style.display = 'block';
    filterSection.style.display = 'none';
    resultsSection.style.display = 'none';

    // Create form data
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('filter', selectedFilter);

    try {
        // Send to backend
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (data.success) {
            // Update images
            originalImage.src = data.original_path;
            processedImage.src = data.processed_path;
            processedLabel.textContent = data.filter_type;
            processedImagePath = data.processed_path;

            // Show results
            loadingSection.style.display = 'none';
            resultsSection.style.display = 'block';
            
            // Scroll to results
            resultsSection.scrollIntoView({ behavior: 'smooth' });
        } else {
            throw new Error(data.error || 'Processing failed');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error processing image: ' + error.message);
        loadingSection.style.display = 'none';
        filterSection.style.display = 'block';
    }
}

function setupComparisonSlider() {
    let isDragging = false;

    // Mouse events
    sliderHandle.addEventListener('mousedown', startDrag);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', stopDrag);

    // Touch events
    sliderHandle.addEventListener('touchstart', startDrag);
    document.addEventListener('touchmove', drag);
    document.addEventListener('touchend', stopDrag);

    function startDrag(e) {
        isDragging = true;
        e.preventDefault();
    }

    function drag(e) {
        if (!isDragging) return;

        const rect = comparisonSlider.getBoundingClientRect();
        let x;

        if (e.type.startsWith('touch')) {
            x = e.touches[0].clientX - rect.left;
        } else {
            x = e.clientX - rect.left;
        }

        // Clamp x within bounds
        x = Math.max(0, Math.min(x, rect.width));

        // Calculate percentage
        const percentage = (x / rect.width) * 100;

        // Update slider position
        sliderHandle.style.left = percentage + '%';

        // Update clip-path for processed image
        const processedImg = document.querySelector('.comparison-processed');
        processedImg.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
    }

    function stopDrag() {
        isDragging = false;
    }

    // Click on slider to jump to position
    comparisonSlider.addEventListener('click', (e) => {
        if (e.target === sliderHandle || sliderHandle.contains(e.target)) return;

        const rect = comparisonSlider.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const percentage = (x / rect.width) * 100;

        sliderHandle.style.left = percentage + '%';
        const processedImg = document.querySelector('.comparison-processed');
        processedImg.style.clipPath = `inset(0 ${100 - percentage}% 0 0)`;
    });
}

function resetUpload() {
    // Reset state
    selectedFile = null;
    selectedFilter = '1920s';
    processedImagePath = '';

    // Reset file input
    fileInput.value = '';

    // Reset preview
    imagePreview.src = '';
    previewContainer.style.display = 'none';
    uploadContent.style.display = 'flex';

    // Reset filter selection
    filterBtns.forEach(btn => btn.classList.remove('selected'));
    filterBtns[0].classList.add('selected');
    filterDescs.forEach(desc => desc.classList.remove('active'));

    // Hide results, show upload
    resultsSection.style.display = 'none';
    filterSection.style.display = 'none';
    
    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

function downloadImage() {
    if (!processedImagePath) {
        alert('No processed image to download');
        return;
    }

    // Create download link
    const link = document.createElement('a');
    link.href = processedImagePath;
    link.download = `chronovision_${selectedFilter}_processed.png`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
