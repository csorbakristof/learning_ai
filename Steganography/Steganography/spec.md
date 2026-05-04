Create a steganography application in C# which can hide a text into a png image file. It should use the least significant bit of every chsnnel snd every pixel to store the data. End of data should be marked with a null byte (character). Use UTF-8 encoding.
Create also the function to read the data from the file.
Add a simple  encryption layer: if a key (8 bit number) is given, all hidden bytes are XOR-ed with it to make it harder to detect.

Create a very simple user interface using WinUI3 for the application. Use WriteableBitmap for image processing.

Use as few dependencies as possible for the project. Create maintainable, professional code.

Workflow:

- Open image, see its capacity.
- Set xor key
- When writing into the image:
	- Enter text
	- Show warning if image capacity is too small
	- Encode using XOR
	- Save text into image
- When reading from image:
	- Extract text from the image
	- Decode using XOR
	- Show text in the UI

Further details:

- Pixel Format & Channels: use 8-bit RGB channels, do not use alpha.
- XOR Layer: To confirm the logic, the workflow would be: Text -> UTF-8 Bytes -> XOR with Key -> Bit Distribution.