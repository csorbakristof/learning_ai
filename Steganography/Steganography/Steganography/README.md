# Steganography Application

A WinUI3 application for hiding text in PNG images using LSB (Least Significant Bit) steganography with optional XOR encryption.

## Features

- **LSB Steganography**: Hides text in the least significant bits of RGB channels
- **UTF-8 Encoding**: Supports international characters and emojis
- **XOR Encryption**: Optional 8-bit key for basic encryption layer
- **Capacity Calculation**: Automatically calculates and displays image capacity
- **User-Friendly UI**: Modern WinUI3 interface with tabbed views
- **PNG Support**: Reads and writes PNG image files

## How It Works

### LSB Steganography

The application uses the Least Significant Bit technique to hide data:
1. Each pixel has 3 color channels (RGB) - alpha is not used
2. Each channel stores 1 bit of data in its LSB
3. Each pixel can store 3 bits total
4. Data is terminated with a null byte (0x00)

### Encryption Workflow

Text ? UTF-8 Bytes ? XOR with Key ? Bit Distribution ? Image LSBs

## Usage

### Hiding Text

1. **Open an Image**: Click "Open Image" and select a PNG file
2. **Check Capacity**: The app displays how many characters can be hidden
3. **Set XOR Key** (optional): Enter a number between 0-255 (0 = no encryption)
4. **Enter Text**: Type your message in the "Hide Text" tab
5. **Hide and Save**: Click "Hide Text in Image" and choose where to save

### Extracting Text

1. **Open an Image**: Load the image containing hidden text
2. **Set XOR Key**: Enter the same key used for hiding (if any)
3. **Extract**: Click "Extract Text from Image" in the "Extract Text" tab
4. **View Result**: The hidden message appears in the text box

## Technical Details

### Pixel Format

- **Format**: BGRA8 (Blue-Green-Red-Alpha, 8 bits each)
- **Channels Used**: Only RGB (Blue=0, Green=1, Red=2)
- **Alpha Channel**: Preserved, not used for data storage

### Capacity Calculation

For an image with dimensions W×H:
- Total bits = W × H × 3 (3 channels per pixel)
- Total bytes = (W × H × 3) / 8
- Usable capacity = Total bytes - 1 (reserve 1 byte for null terminator)

### Example Capacities

- 100×100 px = ~3,749 characters
- 500×500 px = ~93,749 characters  
- 1920×1080 px = ~777,599 characters

## Code Structure

- **SteganographyEngine.cs**: Core LSB logic for hiding and extracting data
- **MainWindow.xaml**: UI layout with image selection, tabs, and controls
- **MainWindow.xaml.cs**: Code-behind for file operations and user interactions

## Requirements

- .NET 8.0
- Windows 10 version 17763.0 or higher
- Windows App SDK 2.0.1

## Security Notes

?? **This is not cryptographically secure!**

- XOR encryption with an 8-bit key is easily breakable
- LSB steganography can be detected with statistical analysis
- For serious security needs, use proper encryption algorithms

This application is designed for:
- Learning steganography concepts
- Basic data hiding for non-sensitive information
- Educational and experimental purposes

## Building and Running

```bash
# Build the project
dotnet build

# Run the application
dotnet run
```

Or open the solution in Visual Studio 2022 and press F5.

## License

This project is provided as-is for educational purposes.
