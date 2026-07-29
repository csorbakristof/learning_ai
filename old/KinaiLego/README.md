# Image Quantizer

Transform your images into 64×64 pixels with 5 perceptually uniform shades of gray.

## Features

- **Image Upload**: Upload images via file chooser or drag-and-drop
- **Background Color**: Choose custom background color for letterboxing
- **Smart Resizing**: Maintains aspect ratio while fitting within 64×64 pixels
- **Grayscale Conversion**: Uses luminosity method (0.299R + 0.587G + 0.114B)
- **Quantization**: Reduces to 5 gamma-corrected gray levels: [0, 76, 128, 179, 255]
- **Visual Comparison**: Interactive slider to compare before/after results
- **Multiple Views**: Tabbed interface showing original, quantized, and comparison views

## Requirements

- Java Development Kit (JDK) 8 or higher
- Supports JPG, PNG, GIF, BMP image formats

## Running the Application

### Windows

#### Option 1: Using batch file (easiest)
```batch
start.bat
```

#### Option 2: Manual compilation and run
```batch
javac ImageQuantizer.java
java ImageQuantizer
```

### PowerShell
```powershell
.\start.ps1
```

### macOS/Linux
```bash
javac ImageQuantizer.java
java ImageQuantizer
```

## How It Works

1. **Upload**: Click "📂 Upload Image" or drag-and-drop an image file
2. **Customize**: Optionally change the background color using "🎨 Background Color"
3. **View Results**: 
   - **Images tab**: See original and quantized side-by-side
   - **Comparison tab**: Drag slider to compare before/after
   - **Info tab**: Learn about the process and see the color palette

## Technical Details

### Quantization Palette

The 5 gray levels are perceptually uniform, calculated using gamma 2.2 correction:
- **0** - Black
- **76** - Dark Gray (25% brightness)
- **128** - Medium Gray (50% brightness)
- **179** - Light Gray (75% brightness)
- **255** - White

### Processing Steps

1. Image is loaded and centered on a background of your chosen color
2. Resized to fit within 64×64 pixels while preserving aspect ratio
3. Each pixel converted to grayscale using luminosity formula
4. Grayscale value quantized to nearest of the 5 predefined levels
5. Results displayed at 320×320 for easy viewing (scaled 5x using nearest-neighbor)

## Versions

- **HTML Version**: [index.html](index.html) - Web browser version with same functionality
- **Java Version**: [ImageQuantizer.java](ImageQuantizer.java) - Desktop application

Both versions use identical algorithms and produce the same results.
