# Goal overview

This project aims to create a Microsoft Word macro which removes all text from the current document which has yellow highlighting. The goal is to remove the sample solutions from exam tasks.

# Details

- Remove character-by-charater the yellow parts. There may be only a few letters to remove from the middle of a text.
- The macro should be trigged by the hotkey Ctrl-Shift-Y.
- The macro should allow Undo.
- The macro should work on the current document, no copy is needed.
- A character should be removed if and only if it has yellow background (highlight or other type of yellow background).
- Images do not need to be handled.
- In tables, the same rules apply. If a cell has yellow background, remove the whole content of the cell. If only a part of the text has yellow background, only remove those characters.

