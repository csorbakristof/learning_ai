# Image Quantizer Application

Create a single-page HTML application with embedded JavaScript that performs image quantization with the following specifications:

## Core Functionality

1. **Image Upload**
   - Allow users to upload any standard image format (JPG, PNG, etc.)
   - Use a file input element for image selection

2. **Image Processing**
   - Resize the uploaded image to fit within a 64×64 pixel canvas
   - **Preserve aspect ratio** during resizing
   - Center the image on the canvas with white background filling empty space
   - Convert the image to grayscale using the luminosity method: `0.299*R + 0.587*G + 0.114*B`
   - Quantize the grayscale values to exactly 5 levels: 0 (black), 64, 128, 192, and 255 (white)
   - For each pixel, find the nearest gray level from the 5 available shades

3. **Display**
   - Show the original uploaded image (scaled for display, maintaining aspect ratio)
   - Show the processed 64×64 quantized image side-by-side
   - Display the 5-shade gray palette with values labeled
   - Use pixelated rendering for the quantized image (no blurring/antialiasing)

4. **Download**
   - Provide a download button to save the quantized image as PNG
   - Button should appear only after an image has been processed

## UI Requirements

- Modern, clean, and attractive design
- Responsive layout that works on different screen sizes
- Clear instructions explaining how the application works
- Visual feedback for the user throughout the process
- Professional color scheme and styling

## Technical Requirements

- Single HTML file with embedded CSS and JavaScript
- Use HTML5 Canvas API for image processing
- No external dependencies or libraries required
- Client-side processing only (no server interaction needed)

## Use Case

This tool is designed to prepare images for applications requiring simplified grayscale representation, such as LEGO mosaics or pixel art projects where a limited palette is needed.