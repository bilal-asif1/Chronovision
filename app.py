"""
ChronoVision – Photo Time Travel
A Digital Image Processing Project
Flask Backend with OpenCV Image Processing
"""

from flask import Flask, render_template, request, send_file, jsonify
import os
import cv2
import numpy as np
from PIL import Image
import uuid
from datetime import datetime

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
RESULTS_FOLDER = 'static/results'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULTS_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULTS_FOLDER'] = RESULTS_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def apply_1920s_filter(image):
    """
    1920s Filter: Sepia, grain, scratches, faded old-photo effect
    
    Image Processing Techniques Used:
    1. Sepia Tone: Matrix transformation to convert RGB to sepia tones
    2. Film Grain: Add random noise to simulate old film texture
    3. Scratches: Draw random lines to simulate film damage
    4. Faded Effect: Reduce overall brightness and contrast
    5. Vignette: Darken edges to simulate old lens vignetting
    """
    # Convert to float for precise calculations
    img_float = image.astype(np.float32) / 255.0
    
    # 1. Sepia Tone Transformation
    # Sepia matrix: converts RGB to warm brown tones typical of old photographs
    sepia_matrix = np.array([
        [0.393, 0.769, 0.189],  # Red channel
        [0.349, 0.686, 0.168],  # Green channel
        [0.272, 0.534, 0.131]   # Blue channel
    ])
    
    # Apply sepia transformation
    sepia_img = cv2.transform(img_float, sepia_matrix)
    sepia_img = np.clip(sepia_img, 0, 1)
    
    # 2. Film Grain Effect
    # Add random noise to simulate film grain texture
    grain_intensity = 0.08
    noise = np.random.normal(0, grain_intensity, sepia_img.shape)
    sepia_img = np.clip(sepia_img + noise, 0, 1)
    
    # 3. Scratches Effect
    # Draw random thin lines to simulate film scratches/damage
    height, width = sepia_img.shape[:2]
    num_scratches = np.random.randint(3, 8)
    
    for _ in range(num_scratches):
        x = np.random.randint(0, width)
        scratch_length = np.random.randint(height // 4, height // 2)
        y_start = np.random.randint(0, height - scratch_length)
        thickness = np.random.randint(1, 3)
        
        # Darken scratch area
        cv2.line(sepia_img, (x, y_start), (x, y_start + scratch_length), 
                 (0.1, 0.1, 0.1), thickness)
    
    # 4. Faded Effect
    # Reduce brightness and contrast to simulate aged photo
    alpha = 0.85  # Contrast factor
    beta = 0.1    # Brightness offset
    faded_img = cv2.convertScaleAbs(sepia_img * 255, alpha=alpha, beta=beta * 255)
    faded_img = faded_img.astype(np.float32) / 255.0
    faded_img = np.clip(faded_img, 0, 1)
    
    # 5. Vignette Effect
    # Create radial gradient to darken edges (old lens effect)
    rows, cols = faded_img.shape[:2]
    kernel_x = cv2.getGaussianKernel(cols, cols // 3)
    kernel_y = cv2.getGaussianKernel(rows, rows // 3)
    kernel = kernel_y * kernel_x.T
    
    # Invert and normalize kernel for vignette
    vignette = kernel / kernel.max()
    vignette = 1 - (vignette * 0.4)  # Adjust vignette intensity
    
    # Apply vignette to each channel
    final_img = faded_img * vignette[:, :, np.newaxis]
    final_img = np.clip(final_img * 255, 0, 255).astype(np.uint8)
    
    return final_img


def apply_1970s_filter(image):
    """
    1970s Filter: Warm tones, low saturation, analog film look
    
    Image Processing Techniques Used:
    1. Warm Tone Shift: Increase red/yellow channels for vintage warmth
    2. Desaturation: Reduce saturation for muted film look
    3. Color Balance: Adjust RGB channels for analog film color cast
    4. Soft Contrast: Reduce contrast for dreamy film aesthetic
    5. Slight Blur: Gaussian blur to simulate soft focus lens
    """
    # Convert to float
    img_float = image.astype(np.float32) / 255.0
    
    # 1. Warm Tone Shift
    # Boost red and yellow channels for warm vintage look
    img_float[:, :, 0] = np.clip(img_float[:, :, 0] * 1.15, 0, 1)  # Red boost
    img_float[:, :, 1] = np.clip(img_float[:, :, 1] * 1.05, 0, 1)  # Green slight boost
    img_float[:, :, 2] = np.clip(img_float[:, :, 2] * 0.85, 0, 1)  # Blue reduction
    
    # 2. Convert to HSV for saturation adjustment
    hsv = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float32)
    
    # 3. Desaturation
    # Reduce saturation for muted film look (70% of original)
    hsv[:, :, 1] = hsv[:, :, 1] * 0.70
    hsv = np.clip(hsv, 0, 255).astype(np.uint8)
    
    # Convert back to BGR
    desaturated = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0
    
    # 4. Color Balance Adjustment
    # Add slight yellow/orange cast typical of 70s film
    desaturated[:, :, 0] = np.clip(desaturated[:, :, 0] + 0.05, 0, 1)  # Red
    desaturated[:, :, 1] = np.clip(desaturated[:, :, 1] + 0.02, 0, 1)  # Green
    
    # 5. Soft Contrast
    # Reduce contrast for dreamy aesthetic
    alpha = 0.90  # Lower contrast
    beta = 0.05   # Slight brightness increase
    soft_contrast = cv2.convertScaleAbs(desaturated * 255, alpha=alpha, beta=beta * 255)
    soft_contrast = soft_contrast.astype(np.float32) / 255.0
    
    # 6. Slight Gaussian Blur
    # Soft focus effect typical of vintage lenses
    blurred = cv2.GaussianBlur(soft_contrast, (3, 3), 0.5)
    
    # Blend original and blurred for subtle effect
    final_img = cv2.addWeighted(soft_contrast, 0.7, blurred, 0.3, 0)
    final_img = np.clip(final_img * 255, 0, 255).astype(np.uint8)
    
    return final_img


def apply_1990s_filter(image):
    """
    1990s Filter: Vintage camera style, slight blur, film contrast
    
    Image Processing Techniques Used:
    1. Color Temperature: Cool tone shift for 90s digital camera look
    2. Increased Contrast: Higher contrast for vivid film look
    3. Slight Blur: Motion blur simulation for vintage camera effect
    4. Color Boost: Enhance certain colors for vibrant 90s aesthetic
    5. Sharpening: Unsharp mask for crisp but vintage look
    """
    # Convert to float
    img_float = image.astype(np.float32) / 255.0
    
    # 1. Color Temperature - Cool Tone
    # Reduce red, increase blue for cool 90s digital look
    img_float[:, :, 0] = np.clip(img_float[:, :, 0] * 0.92, 0, 1)  # Red reduction
    img_float[:, :, 2] = np.clip(img_float[:, :, 2] * 1.08, 0, 1)  # Blue boost
    
    # 2. Convert to LAB color space for better contrast adjustment
    lab = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    # 3. Increase Luminance Contrast
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l_enhanced = clahe.apply(l)
    
    # Merge back
    lab_enhanced = cv2.merge([l_enhanced, a, b])
    enhanced = cv2.cvtColor(lab_enhanced, cv2.COLOR_LAB2BGR).astype(np.float32) / 255.0
    
    # 4. Color Boost
    # Enhance saturation for vibrant 90s look
    hsv = cv2.cvtColor((enhanced * 255).astype(np.uint8), cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float32)
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.15, 0, 255)  # Saturation boost
    hsv = hsv.astype(np.uint8)
    color_boosted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0
    
    # 5. Slight Blur - Vintage Camera Softness
    # Gaussian blur for slight softness
    blurred = cv2.GaussianBlur(color_boosted, (5, 5), 1.0)
    
    # 6. Unsharp Masking for Sharpening
    # Sharpen while maintaining vintage softness
    gaussian = cv2.GaussianBlur(blurred, (0, 0), 2.0)
    unsharp_mask = cv2.addWeighted(blurred, 1.5, gaussian, -0.5, 0)
    
    final_img = np.clip(unsharp_mask * 255, 0, 255).astype(np.uint8)
    
    return final_img


def apply_2080s_filter(image):
    """
    2080s Filter: Futuristic neon/cyberpunk style, glow effect
    
    Image Processing Techniques Used:
    1. Neon Color Shift: Boost cyan, magenta, and electric blue
    2. High Contrast: Dramatic contrast for cyberpunk aesthetic
    3. Glow Effect: Bilateral filter for neon glow simulation
    4. Color Grading: Shift towards cool/cyberpunk color palette
    5. Edge Enhancement: Enhance edges for futuristic sharpness
    6. Additive Blending: Screen blend mode for luminous effect
    """
    # Convert to float
    img_float = image.astype(np.float32) / 255.0
    
    # 1. Neon Color Shift
    # Boost cyan (blue+green) and magenta (red+blue) channels
    img_float[:, :, 0] = np.clip(img_float[:, :, 0] * 1.1, 0, 1)   # Red
    img_float[:, :, 1] = np.clip(img_float[:, :, 1] * 1.2, 0, 1)   # Green (cyan component)
    img_float[:, :, 2] = np.clip(img_float[:, :, 2] * 1.3, 0, 1)   # Blue (cyan+magenta)
    
    # 2. Convert to HSV for color grading
    hsv = cv2.cvtColor((img_float * 255).astype(np.uint8), cv2.COLOR_BGR2HSV)
    hsv = hsv.astype(np.float32)
    
    # 3. Cyberpunk Color Grading
    # Shift hue towards cool colors (cyans, blues, magentas)
    hsv[:, :, 0] = (hsv[:, :, 0] + 10) % 180  # Hue shift
    hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.3, 0, 255)  # Boost saturation
    hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.1, 0, 255)  # Boost brightness
    hsv = hsv.astype(np.uint8)
    
    color_graded = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR).astype(np.float32) / 255.0
    
    # 4. High Contrast
    # Dramatic contrast for cyberpunk look
    alpha = 1.3  # High contrast
    beta = -0.1  # Darker shadows
    high_contrast = cv2.convertScaleAbs(color_graded * 255, alpha=alpha, beta=beta * 255)
    high_contrast = high_contrast.astype(np.float32) / 255.0
    
    # 5. Glow Effect using Bilateral Filter
    # Bilateral filter preserves edges while smoothing for neon glow
    bilateral = cv2.bilateralFilter((high_contrast * 255).astype(np.uint8), 15, 80, 80)
    bilateral = bilateral.astype(np.float32) / 255.0
    
    # 6. Screen Blend Mode for Luminous Effect
    # Screen blend: 1 - (1-a)(1-b) for additive luminous look
    screen = 1 - (1 - high_contrast) * (1 - bilateral * 0.5)
    screen = np.clip(screen, 0, 1)
    
    # 7. Edge Enhancement
    # Use Laplacian for edge detection and enhancement
    gray = cv2.cvtColor((screen * 255).astype(np.uint8), cv2.COLOR_BGR2GRAY)
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    laplacian = np.uint8(np.absolute(laplacian))
    laplacian = laplacian.astype(np.float32) / 255.0
    
    # Add edge enhancement
    edges = laplacian[:, :, np.newaxis] * 0.15
    final_img = screen + edges
    final_img = np.clip(final_img * 255, 0, 255).astype(np.uint8)
    
    return final_img


@app.route('/')
def index():
    """Render the main landing page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle image upload and apply selected filter"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    filter_type = request.form.get('filter', '1920s')
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        filename = f"{timestamp}_{unique_id}_{file.filename}"
        
        # Save uploaded file
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(upload_path)
        
        # Read image with OpenCV
        img = cv2.imread(upload_path)
        
        if img is None:
            return jsonify({'error': 'Could not read image'}), 400
        
        # Apply selected filter
        if filter_type == '1920s':
            processed_img = apply_1920s_filter(img)
        elif filter_type == '1970s':
            processed_img = apply_1970s_filter(img)
        elif filter_type == '1990s':
            processed_img = apply_1990s_filter(img)
        elif filter_type == '2080s':
            processed_img = apply_2080s_filter(img)
        else:
            processed_img = img
        
        # Save processed image
        result_filename = f"processed_{filter_type}_{filename}"
        result_path = os.path.join(app.config['RESULTS_FOLDER'], result_filename)
        cv2.imwrite(result_path, processed_img)
        
        # Return paths for frontend
        return jsonify({
            'success': True,
            'original_path': f'/static/uploads/{filename}',
            'processed_path': f'/static/results/{result_filename}',
            'filter_type': filter_type
        })
    
    return jsonify({'error': 'Invalid file type'}), 400


@app.route('/download/<filename>')
def download_file(filename):
    """Download processed image"""
    try:
        return send_file(
            os.path.join(app.config['RESULTS_FOLDER'], filename),
            as_attachment=True
        )
    except FileNotFoundError:
        return jsonify({'error': 'File not found'}), 404


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
