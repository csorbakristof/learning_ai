This project creates SVG file based animations using javascript and SVG.js .
We are creating visualizations to explain complex things.

For all demos, create a html file with embedded javascript using the SVG.js library. These html files show the SVG files and contain additional javascript to manipulate them. You can have a look at the documentation of the SVG.js library where: https://svgjs.dev/docs/3.0/

Use SVG.js directly for operations where the library provides built-in support, such as selecting SVG elements, attaching events, animating movement, changing classes/styles, and positioning elements. Prefer concise and readable code. Do not reimplement these behaviors manually with low-level DOM APIs or custom interpolation logic when SVG.js already supports them.

In the description of the tasks, I will refer to the SVG objects by their labels. During the animations, use the center of the objects as anchor points. Use 1 second animations and easing on both ends.

# DEMO1: marker_to_home

File to create: marker_to_home.html
Image to embed: marker_to_home.svg

Preparation: hide home_red via CSS. All phase labels should be red (original color).

The demo contains the following animations, each triggered by a mouse click after each other:

1. marker_red moves to home_red. Select "txt phase 1" by changing its stroke color to blue.
2. marker_blu moves to home_red as well. Select "txt phase 2" by making it blue and "txt phase 1" back to its original color.
3. marker_red and marker_blu return to their original position. Select "txt phase 3".

# Further details

- If user clicks during an animation, ignore the click.
- Every click advances only 1 phase in the animation.
- "Original color" refers to the color defined in the SVG file.
- Every marker should preserve their shape during the animations.
- Clicks should be detected inside the SVG.
- For DEMO1, the movement is between object centers: from each marker's original center position to the center of `home_red`, and back if required. Do not move along the perimeter or geometry of `home_red`.
- The phase text color change should affect the actually visible SVG styling. If the source SVG defines text color via CSS style properties, update that visible style accordingly.
