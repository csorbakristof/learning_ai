using System;
using System.IO;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using System.Threading.Tasks;
using Microsoft.UI.Xaml;
using Microsoft.UI.Xaml.Controls;
using Microsoft.UI.Xaml.Media.Imaging;
using Windows.Graphics.Imaging;
using Windows.Storage;
using Windows.Storage.Pickers;
using Windows.Storage.Streams;

namespace Steganography
{
    /// <summary>
    /// Main window for the steganography application.
    /// </summary>
    public sealed partial class MainWindow : Window
    {
        private WriteableBitmap? _currentBitmap;
        private StorageFile? _currentImageFile;

        public MainWindow()
        {
            InitializeComponent();
            Title = "Steganography Application";
        }

        /// <summary>
        /// Opens an image file and loads it into memory.
        /// </summary>
        private async void OpenImageButton_Click(object sender, RoutedEventArgs e)
        {
            var picker = new FileOpenPicker();
            
            // Get the window handle for the picker
            var hwnd = WinRT.Interop.WindowNative.GetWindowHandle(this);
            WinRT.Interop.InitializeWithWindow.Initialize(picker, hwnd);
            
            picker.FileTypeFilter.Add(".png");
            picker.SuggestedStartLocation = PickerLocationId.PicturesLibrary;

            StorageFile? file = await picker.PickSingleFileAsync();
            if (file != null)
            {
                await LoadImageAsync(file);
            }
        }

        /// <summary>
        /// Loads an image file into a WriteableBitmap.
        /// </summary>
        private async Task LoadImageAsync(StorageFile file)
        {
            try
            {
                _currentImageFile = file;
                
                using (IRandomAccessStream stream = await file.OpenAsync(FileAccessMode.Read))
                {
                    BitmapDecoder decoder = await BitmapDecoder.CreateAsync(stream);
                    
                    // Create WriteableBitmap with BGRA8 format
                    _currentBitmap = new WriteableBitmap((int)decoder.PixelWidth, (int)decoder.PixelHeight);
                    
                    // Get pixel data
                    PixelDataProvider pixelData = await decoder.GetPixelDataAsync(
                        BitmapPixelFormat.Bgra8,
                        BitmapAlphaMode.Premultiplied,
                        new BitmapTransform(),
                        ExifOrientationMode.RespectExifOrientation,
                        ColorManagementMode.ColorManageToSRgb);
                    
                    byte[] pixels = pixelData.DetachPixelData();
                    
                    // Copy to WriteableBitmap
                    using (Stream bitmapStream = _currentBitmap.PixelBuffer.AsStream())
                    {
                        await bitmapStream.WriteAsync(pixels, 0, pixels.Length);
                    }
                }

                // Update UI
                ImagePathTextBox.Text = file.Path;
                int capacity = SteganographyEngine.CalculateCapacity(_currentBitmap.PixelWidth, _currentBitmap.PixelHeight);
                CapacityTextBlock.Text = $"Image loaded: {_currentBitmap.PixelWidth}x{_currentBitmap.PixelHeight} pixels. Capacity: ~{capacity} characters";
                CapacityTextBlock.Foreground = new Microsoft.UI.Xaml.Media.SolidColorBrush(Microsoft.UI.Colors.Green);
                
                ShowStatus("Image loaded successfully!", InfoBarSeverity.Success);
                
                // Clear previous operations
                InputTextBox.Text = string.Empty;
                OutputTextBox.Text = string.Empty;
                HideWarningInfoBar.IsOpen = false;
            }
            catch (Exception ex)
            {
                ShowStatus($"Error loading image: {ex.Message}", InfoBarSeverity.Error);
            }
        }

        /// <summary>
        /// Hides text in the current image using LSB steganography.
        /// </summary>
        private async void HideTextButton_Click(object sender, RoutedEventArgs e)
        {
            if (_currentBitmap == null || _currentImageFile == null)
            {
                ShowStatus("Please load an image first!", InfoBarSeverity.Warning);
                return;
            }

            string textToHide = InputTextBox.Text;
            if (string.IsNullOrEmpty(textToHide))
            {
                ShowStatus("Please enter text to hide!", InfoBarSeverity.Warning);
                return;
            }

            byte xorKey = (byte)XorKeyNumberBox.Value;

            // Check capacity
            int textLength = Encoding.UTF8.GetByteCount(textToHide);
            int capacity = SteganographyEngine.CalculateCapacity(_currentBitmap.PixelWidth, _currentBitmap.PixelHeight);
            
            if (textLength > capacity)
            {
                HideWarningInfoBar.IsOpen = true;
                HideWarningInfoBar.Message = $"Text size ({textLength} bytes) exceeds image capacity ({capacity} bytes)!";

                return;
            }
            else
            {
                HideWarningInfoBar.IsOpen = false;
            }

            try
            {
                // Hide the text
                bool success = SteganographyEngine.HideText(_currentBitmap, textToHide, xorKey);
                
                if (!success)
                {
                    ShowStatus("Failed to hide text in image!", InfoBarSeverity.Error);
                    return;
                }

                // Save the modified image
                var savePicker = new FileSavePicker();
                var hwnd = WinRT.Interop.WindowNative.GetWindowHandle(this);
                WinRT.Interop.InitializeWithWindow.Initialize(savePicker, hwnd);
                
                savePicker.FileTypeChoices.Add("PNG Image", new[] { ".png" });
                savePicker.SuggestedFileName = Path.GetFileNameWithoutExtension(_currentImageFile.Name) + "_stego";
                savePicker.SuggestedStartLocation = PickerLocationId.PicturesLibrary;

                StorageFile? outputFile = await savePicker.PickSaveFileAsync();
                if (outputFile != null)
                {
                    await SaveBitmapAsync(_currentBitmap, outputFile);
                    ShowStatus($"Text hidden successfully! Image saved to: {outputFile.Name}", InfoBarSeverity.Success);
                }
            }
            catch (Exception ex)
            {
                ShowStatus($"Error hiding text: {ex.Message}", InfoBarSeverity.Error);
            }
        }

        /// <summary>
        /// Extracts hidden text from the current image.
        /// </summary>
        private void ExtractTextButton_Click(object sender, RoutedEventArgs e)
        {
            if (_currentBitmap == null)
            {
                ShowStatus("Please load an image first!", InfoBarSeverity.Warning);
                return;
            }

            byte xorKey = (byte)XorKeyNumberBox.Value;

            try
            {
                string? extractedText = SteganographyEngine.ExtractText(_currentBitmap, xorKey);
                
                if (extractedText != null)
                {
                    OutputTextBox.Text = extractedText;
                    ShowStatus("Text extracted successfully!", InfoBarSeverity.Success);
                }
                else
                {
                    OutputTextBox.Text = string.Empty;
                    ShowStatus("No valid hidden text found in the image.", InfoBarSeverity.Warning);
                }
            }
            catch (Exception ex)
            {
                ShowStatus($"Error extracting text: {ex.Message}", InfoBarSeverity.Error);
            }
        }

        /// <summary>
        /// Saves a WriteableBitmap to a PNG file.
        /// </summary>
        private async Task SaveBitmapAsync(WriteableBitmap bitmap, StorageFile file)
        {
            using (IRandomAccessStream stream = await file.OpenAsync(FileAccessMode.ReadWrite))
            {
                BitmapEncoder encoder = await BitmapEncoder.CreateAsync(BitmapEncoder.PngEncoderId, stream);
                
                // Get pixel data from WriteableBitmap
                byte[] pixels = new byte[bitmap.PixelWidth * bitmap.PixelHeight * 4];
                using (Stream bitmapStream = bitmap.PixelBuffer.AsStream())
                {
                    bitmapStream.Position = 0;
                    await bitmapStream.ReadAsync(pixels, 0, pixels.Length);
                }
                
                encoder.SetPixelData(
                    BitmapPixelFormat.Bgra8,
                    BitmapAlphaMode.Premultiplied,
                    (uint)bitmap.PixelWidth,
                    (uint)bitmap.PixelHeight,
                    96.0,
                    96.0,
                    pixels);
                
                await encoder.FlushAsync();
            }
        }

        /// <summary>
        /// Shows a status message in the InfoBar.
        /// </summary>
        private void ShowStatus(string message, InfoBarSeverity severity)
        {
            StatusInfoBar.Message = message;
            StatusInfoBar.Severity = severity;
            StatusInfoBar.IsOpen = true;
        }
    }
}
