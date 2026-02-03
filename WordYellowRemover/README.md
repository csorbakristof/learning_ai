# --- MÉG HIBÁS ---

# Yellow Text Remover - Word Macro

This macro removes all text with yellow background (highlighting or shading) from a Word document.

## Features

- Removes characters with yellow highlighting
- Removes characters with yellow shading/background color
- Works character-by-character (partial word removal supported)
- Handles table cells (removes entire cell content if cell has yellow background)
- Single Undo operation
- Triggered by **Ctrl+Shift+Y** hotkey

## Installation

1. Open your Word document
2. Press `Alt+F11` to open the VBA editor
3. Go to `File` → `Import File...`
4. Select `yellowRemover.bas`
5. Close the VBA editor

## Setting up the Hotkey (Ctrl+Shift+Y)

### Method 1: Using VBA Editor
1. In the VBA editor, go to `Tools` → `Macros` → `Macros`
2. Select `RemoveYellowText`
3. Click `Options`
4. In the "Shortcut key" field, press `Shift+Y` (Ctrl is automatically added)
5. Click OK

### Method 2: Using Word Options
1. In Word, go to `File` → `Options` → `Customize Ribbon`
2. Click `Customize...` button next to "Keyboard shortcuts:"
3. In Categories, select `Macros`
4. In Macros, select `YellowRemover.RemoveYellowText`
5. Click in "Press new shortcut key" field
6. Press `Ctrl+Shift+Y`
7. Click `Assign` and then `Close`

### Method 3: Add to ThisDocument (for document-specific hotkey)

Add this code to the `ThisDocument` module in the VBA editor:

```vba
Private Sub Document_Open()
    CustomizationContext = ActiveDocument
    KeyBindings.Add KeyCode:=BuildKeyCode(wdKeyY, wdKeyControl, wdKeyShift), _
                    KeyCategory:=wdKeyCategoryMacro, _
                    Command:="RemoveYellowText"
End Sub
```

## Usage

1. Open your Word document with yellow highlighted text
2. Press **Ctrl+Shift+Y**
3. The macro will remove all yellow text
4. A message will show how many characters/cells were removed
5. You can press **Ctrl+Z** to undo if needed

## How It Works

- **Regular text**: Scans character-by-character and removes any character with yellow highlighting or yellow background
- **Table cells**: If the entire cell has yellow background, clears all cell content. Otherwise, removes only yellow-highlighted characters within the cell
- **Yellow color detection**: Detects standard yellow (RGB 255,255,0) and common variations

## Notes

- The macro creates a single undo action, so one Ctrl+Z will restore all removed text
- Images are not processed (as per specification)
- The macro works on the active document without creating a copy
