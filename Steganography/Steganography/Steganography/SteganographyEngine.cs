using System;
using System.IO;
using System.Runtime.InteropServices.WindowsRuntime;
using System.Text;
using Windows.Storage.Streams;
using Microsoft.UI.Xaml.Media.Imaging;

namespace Steganography
{
    /// <summary>
    /// Core steganography engine for hiding and extracting text in PNG images using LSB method.
    /// </summary>
    public class SteganographyEngine
    {
        /// <summary>
        /// Calculates the maximum text capacity (in characters) that can be hidden in an image.
        /// </summary>
        /// <param name="width">Image width in pixels</param>
        /// <param name="height">Image height in pixels</param>
        /// <returns>Maximum number of characters (assuming UTF-8 encoding)</returns>
        public static int CalculateCapacity(int width, int height)
        {
            // Each pixel has 3 channels (RGB), each channel can store 1 bit
            // So each pixel can store 3 bits total
            int totalBits = width * height * 3;
            int totalBytes = totalBits / 8;
            
            // Reserve 1 byte for null terminator
            return totalBytes - 1;
        }

        /// <summary>
        /// Hides text in an image using LSB steganography with optional XOR encryption.
        /// </summary>
        /// <param name="bitmap">WriteableBitmap to hide data in</param>
        /// <param name="text">Text to hide</param>
        /// <param name="xorKey">Optional XOR key (0-255), 0 means no encryption</param>
        /// <returns>True if successful, false if image capacity is too small</returns>
        public static bool HideText(WriteableBitmap bitmap, string text, byte xorKey)
        {
            // Convert text to UTF-8 bytes and add null terminator
            byte[] textBytes = Encoding.UTF8.GetBytes(text);
            byte[] dataToHide = new byte[textBytes.Length + 1]; // +1 for null terminator
            Array.Copy(textBytes, dataToHide, textBytes.Length);
            dataToHide[textBytes.Length] = 0; // Null terminator

            // Apply XOR encryption if key is provided
            if (xorKey != 0)
            {
                for (int i = 0; i < dataToHide.Length; i++)
                {
                    dataToHide[i] ^= xorKey;
                }
            }

            // Check capacity
            int requiredBits = dataToHide.Length * 8;
            int availableBits = bitmap.PixelWidth * bitmap.PixelHeight * 3;
            if (requiredBits > availableBits)
            {
                return false;
            }

            // Get pixel data
            byte[] pixelData = new byte[bitmap.PixelWidth * bitmap.PixelHeight * 4]; // BGRA format
            using (var stream = bitmap.PixelBuffer.AsStream())
            {
                stream.Position = 0;
                stream.Read(pixelData, 0, pixelData.Length);
            }

            // Hide data in LSBs (skip alpha channel, use only RGB)
            int bitIndex = 0;
            for (int i = 0; i < dataToHide.Length && bitIndex < requiredBits; i++)
            {
                byte currentByte = dataToHide[i];
                
                for (int bit = 7; bit >= 0; bit--)
                {
                    int pixelIndex = bitIndex / 3;
                    int channelIndex = bitIndex % 3;
                    
                    // Calculate position in BGRA buffer (B=0, G=1, R=2, A=3)
                    int bufferIndex = pixelIndex * 4 + channelIndex;
                    
                    // Extract bit from data byte
                    byte dataBit = (byte)((currentByte >> bit) & 1);
                    
                    // Clear LSB and set new value
                    pixelData[bufferIndex] = (byte)((pixelData[bufferIndex] & 0xFE) | dataBit);
                    
                    bitIndex++;
                }
            }

            // Write modified pixel data back
            using (var stream = bitmap.PixelBuffer.AsStream())
            {
                stream.Position = 0;
                stream.Write(pixelData, 0, pixelData.Length);
            }

            bitmap.Invalidate();
            return true;
        }

        /// <summary>
        /// Extracts hidden text from an image using LSB steganography with optional XOR decryption.
        /// </summary>
        /// <param name="bitmap">WriteableBitmap to extract data from</param>
        /// <param name="xorKey">Optional XOR key (0-255), 0 means no encryption</param>
        /// <returns>Extracted text, or null if no valid data found</returns>
        public static string? ExtractText(WriteableBitmap bitmap, byte xorKey)
        {
            // Get pixel data
            byte[] pixelData = new byte[bitmap.PixelWidth * bitmap.PixelHeight * 4]; // BGRA format
            using (var stream = bitmap.PixelBuffer.AsStream())
            {
                stream.Position = 0;
                stream.Read(pixelData, 0, pixelData.Length);
            }

            // Extract data from LSBs until null terminator is found
            var extractedBytes = new System.Collections.Generic.List<byte>();
            int bitIndex = 0;
            int maxBits = bitmap.PixelWidth * bitmap.PixelHeight * 3;

            while (bitIndex < maxBits)
            {
                byte extractedByte = 0;
                
                // Extract 8 bits to form one byte
                for (int bit = 7; bit >= 0; bit--)
                {
                    int pixelIndex = bitIndex / 3;
                    int channelIndex = bitIndex % 3;
                    
                    // Calculate position in BGRA buffer (B=0, G=1, R=2, A=3)
                    int bufferIndex = pixelIndex * 4 + channelIndex;
                    
                    // Extract LSB
                    byte lsb = (byte)(pixelData[bufferIndex] & 1);
                    extractedByte |= (byte)(lsb << bit);
                    
                    bitIndex++;
                }

                // Apply XOR decryption if key is provided
                if (xorKey != 0)
                {
                    extractedByte ^= xorKey;
                }

                // Check for null terminator
                if (extractedByte == 0)
                {
                    break;
                }

                extractedBytes.Add(extractedByte);

                // Safety limit to prevent infinite loops
                if (extractedBytes.Count > 10000000) // 10MB limit
                {
                    return null;
                }
            }

            // Convert bytes to string
            try
            {
                return Encoding.UTF8.GetString(extractedBytes.ToArray());
            }
            catch
            {
                return null;
            }
        }
    }
}
