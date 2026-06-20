# ChronoVision – Photo Time Travel

A professional web application for digital image processing that transforms photos into different historical and futuristic styles using advanced OpenCV techniques.

## Project Overview

ChronoVision is a university Digital Image Processing project that demonstrates real image processing concepts—not just CSS filters. Users can upload any image and transform it into four different eras:

- **1920s**: Sepia tone, film grain, scratches, and faded old-photo effect
- **1970s**: Warm tones, low saturation, and analog film look
- **1990s**: Vintage camera style with slight blur and film contrast
- **2080s**: Futuristic neon/cyberpunk style with glow effects

## Technologies Used

### Backend
- **Python Flask**: Web framework for the backend server
- **OpenCV (cv2)**: Computer vision library for image processing
- **NumPy**: Numerical computing for matrix operations
- **Pillow**: Image processing library

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern responsive styling with CSS Grid and Flexbox
- **JavaScript (Vanilla)**: Client-side interactivity
- **No external frameworks**: Pure JavaScript for maximum performance

## Image Processing Techniques

Each filter uses specific image processing algorithms:

### 1920s Filter
- **Sepia Tone Transformation**: Matrix multiplication to convert RGB to sepia tones
- **Film Grain**: Gaussian noise addition for texture simulation
- **Scratches**: Random line drawing for film damage effect
- **Faded Effect**: Brightness and contrast reduction
- **Vignette**: Radial gradient for old lens darkening

### 1970s Filter
- **Warm Tone Shift**: RGB channel manipulation for warmth
- **Desaturation**: HSV color space saturation reduction
- **Color Balance**: Yellow/orange cast adjustment
- **Soft Contrast**: Reduced contrast for dreamy aesthetic
- **Gaussian Blur**: Soft focus simulation

### 1990s Filter
- **Color Temperature**: Cool tone shift for digital camera look
- **CLAHE**: Contrast Limited Adaptive Histogram Equalization
- **Color Boost**: HSV saturation enhancement
- **Motion Blur**: Gaussian blur for vintage softness
- **Unsharp Masking**: Edge enhancement while maintaining softness

### 2080s Filter
- **Neon Color Shift**: Cyan/magenta/blue channel boosting
- **High Contrast**: Dramatic contrast adjustment
- **Bilateral Filter**: Edge-preserving smoothing for neon glow
- **Color Grading**: HSV hue shift towards cool colors
- **Screen Blend Mode**: Additive blending for luminous effect
- **Laplacian Edge Enhancement**: Edge detection and enhancement

## Project Structure

```
chronovision/
├── app.py                      # Flask backend with image processing
├── requirements.txt            # Python dependencies
├── README.md                  # This file
├── static/
│   ├── css/
│   │   └── style.css         # Professional responsive styles
│   ├── js/
│   │   └── script.js         # Client-side JavaScript
│   ├── uploads/              # Uploaded images (auto-created)
│   └── results/              # Processed images (auto-created)
└── templates/
    └── index.html            # Main HTML template
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd chronovision
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install:
- Flask 3.0.0
- opencv-python 4.8.1.78
- Pillow 10.1.0
- numpy 1.26.2

### Step 4: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

### Step 5: Open in Browser
Navigate to `http://localhost:5000` in your web browser

## Usage

1. **Upload Image**: Click the upload area or drag and drop an image
2. **Select Era**: Choose from 1920s, 1970s, 1990s, or 2080s
3. **Apply Filter**: Click "Apply Filter" to process the image
4. **Compare**: Use the slider to compare original vs processed
5. **Download**: Click "Download Image" to save the result
6. **Try Again**: Click "Upload New Image" to start over

## Features

- **Drag & Drop Upload**: Easy file upload with drag and drop support
- **Real-time Processing**: Fast image processing with OpenCV
- **Before/After Comparison**: Interactive slider for comparison
- **Download Support**: Download processed images in PNG format
- **Loading Animation**: Visual feedback during processing
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Professional UI**: Modern, clean interface suitable for presentations

## File Size Limits

- Maximum file size: 16MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

## Educational Value

This project demonstrates:
- Color space transformations (RGB, HSV, LAB)
- Matrix operations for color effects
- Histogram equalization (CLAHE)
- Convolution operations (Gaussian blur, Laplacian)
- Bilateral filtering for edge preservation
- Blend modes (screen blending)
- Noise generation for texture simulation
- Edge detection and enhancement

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify the port in `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change to 5001 or another port
```

### Import Errors
If you encounter import errors, ensure all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Image Processing Errors
If image processing fails, ensure:
- The image file is valid and not corrupted
- OpenCV is properly installed
- Sufficient memory is available

## Presentation Tips

For university presentations:
1. Demonstrate the 1920s filter to show sepia transformation
2. Show the 2080s filter for futuristic effects
3. Explain the image processing techniques used
4. Highlight the comparison slider feature
5. Discuss the color space conversions (RGB, HSV, LAB)
6. Mention CLAHE for contrast enhancement

## License

This project is created for educational purposes as part of a Digital Image Processing course.

## Author

ChronoVision – Digital Image Processing Project
