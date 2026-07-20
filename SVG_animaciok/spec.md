This project creates SVG file based animations using javascript and SVG.js .
We are creating visualizations to explain complex things.

For all demos, create a html file with embedded javascript using the SVG.js library. These html files show the SVG files and contain additional javascript to manipulate them. You can have a look at the documentation of the SVG.js library where: https://svgjs.dev/docs/3.0/


# DEMO1: marker_to_home

File to create: marker_to_home.html
Image to embed: marker_to_home.svg

The SVG file contains a rectangle (label: marker_red) and a path (an ellipse) with label "home_red". Create an animation which moves the marker between its initial position and the location indicated by home_red. Make home_red invisible.

## Further details

For DEMO1 (marker_to_home):
- Start the animation automatically when the page loads.
- Animate continuously in a back-and-forth loop.
- Use a duration of 2 seconds for one leg of the motion.
- Follow the ellipse path geometry for movement.
- Use ease-in-out easing.
- Hide `home_red` via a CSS class.
- Use the center of the moving rectangle (`marker_red`) as the point that follows the ellipse path (`home_red`).
- Rotate the rectangle while moving so its orientation follows the direction of motion along the path.
