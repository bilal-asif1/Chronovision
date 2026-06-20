# ChronoVision - Photo Time Travel

ChronoVision is a professional web application for digital image processing that transforms uploaded photos into different historical and futuristic styles using OpenCV, NumPy, Flask, and vanilla JavaScript.

## Project Banner / Title

**ChronoVision**  
*Photo Time Travel for Digital Image Processing*

ChronoVision is a university Digital Image Processing project that demonstrates real image processing concepts, not just CSS filters. Users can upload an image and transform it into four different eras:

- 1920s: Sepia tone, film grain, scratches, and a faded old-photo effect
- 1970s: Warm tones, low saturation, and an analog film look
- 1990s: Vintage camera style with slight blur and film contrast
- 2080s: Futuristic neon and cyberpunk style with glow effects

## Project Overview

ChronoVision is designed to demonstrate practical image processing rather than simple style overlays. Each era uses specific algorithms and transformations to create a distinct visual identity.

## Features

- Drag and drop image upload
- Support for PNG, JPG, JPEG, GIF, BMP, and WEBP files
- Four era-based image filters
- Real-time before-and-after comparison slider
- Downloadable processed images
- Responsive layout for desktop, tablet, and mobile
- OpenCV-powered image processing pipeline
- No frontend framework required

## Installation

### Prerequisites

- Python 3.8 or higher
- `pip`

### Setup

```bash
git clone https://github.com/bilal-asif1/Chronovision.git
cd Chronovision
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Run the application

```bash
python app.py
```

Open the app in your browser at:

```text
http://localhost:5000
```

## Usage

1. Open the application in your browser.
2. Upload an image by clicking the upload area or dragging and dropping a file.
3. Choose one of the available eras: 1920s, 1970s, 1990s, or 2080s.
4. Click **Apply Filter** to process the image.
5. Compare the original and processed versions using the slider.
6. Click **Download Image** to save the result.
7. Use **Upload New Image** to start over.

## Technologies Used

### Backend

- Python Flask
- OpenCV (`cv2`)
- NumPy
- Pillow

### Frontend

- HTML5
- CSS3
- JavaScript
- Vanilla DOM APIs

### Image Processing Techniques

- Color space transformations
- Matrix multiplication for sepia conversion
- HSV and LAB adjustments
- CLAHE contrast enhancement
- Gaussian blur
- Bilateral filtering
- Laplacian edge enhancement
- Noise generation for film grain
- Screen blending

## Filter Breakdown

### 1920s Filter

- Sepia tone transformation
- Film grain
- Scratches for film damage simulation
- Faded effect
- Vignette

### 1970s Filter

- Warm tone shift
- Desaturation
- Color balance adjustment
- Soft contrast
- Gaussian blur

### 1990s Filter

- Cool color temperature adjustment
- CLAHE contrast enhancement
- Color boost
- Slight blur
- Unsharp masking

### 2080s Filter

- Neon color shift
- High contrast
- Bilateral filter glow effect
- Color grading
- Screen blend mode
- Laplacian edge enhancement

## Project Structure

```text
chronovision/
|-- app.py                 # Flask backend and image processing logic
|-- requirements.txt       # Python dependencies
|-- README.md              # Project documentation
|-- .gitignore             # Git ignore rules
|-- static/
|   |-- css/
|   |   |-- style.css      # Responsive styling
|   |-- js/
|   |   |-- script.js      # Frontend interactivity
|   |-- uploads/           # Uploaded images generated at runtime
|   `-- results/           # Processed images generated at runtime
`-- templates/
    `-- index.html         # Main application template
```

## Educational Value

This project demonstrates:

- Color transformations in RGB, HSV, and LAB spaces
- Matrix operations for image effects
- Histogram equalization with CLAHE
- Convolution-based filters
- Noise modeling for film grain simulation
- Edge detection and enhancement
- Edge-preserving smoothing with bilateral filtering
- Practical client-server image processing workflows

## Troubleshooting

### Port already in use

If port 5000 is occupied, change the port in `app.py`:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Dependency errors

If Python cannot find a package, reinstall dependencies:

```bash
pip install -r requirements.txt
```

### Image upload or processing fails

Check the following:

- The file is a supported image type
- The image is not corrupted
- The file is under 16 MB
- OpenCV and Pillow installed correctly

### Blank or missing preview

- Refresh the page and upload the image again
- Try a different image file
- Make sure JavaScript is enabled in the browser

## File Size Limits

- Maximum file size: 16 MB
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP

## Presentation Tips

For a class or demo presentation:

1. Start with the 1920s filter to show sepia and grain effects.
2. Use the 2080s filter to highlight the futuristic look.
3. Explain the image processing techniques used in each era.
4. Demonstrate the before-and-after comparison slider.
5. Mention the color space conversions and CLAHE enhancement.


## License

This project is created for educational purposes as part of a Digital Image Processing course.
