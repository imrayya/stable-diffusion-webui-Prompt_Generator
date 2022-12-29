# training-picker

Adds a tab to the webui that allows the user to automatically extract keyframes from video, and manually extract 512x512 crops of those frames for use in model training.

![image](https://user-images.githubusercontent.com/2313721/200236386-5fed34df-03e4-4ea6-a653-e1b60393afcd.png)

## Installation:

1. Install [AUTOMATIC1111's Stable Diffusion Webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)
2. Install [ffmpeg](https://ffmpeg.org/) for your operating system
3. Clone this repository into the `extensions` folder inside the webui

Make sure you don't already have `python-ffmpeg` installed globally, as the library this program uses is `ffmpeg-python`, and your installation will conflict with it.

## Usage:

### Creating an extracted frame set

1. Drop videos you want to extract cropped frames from into the `training-picker/videos` folder
2. Open up the Training Picker tab of the webui
3. Select one of the videos you placed in the `training-picker/videos` folder from the dropdown on the left
4. Click 'Extract Frames`
5. After the extraction finishes, a new keyframe set for the video should be selectable in the dropdown on the right
6. Select the keyframe set, and the frames will appear in the browser below

Optionally, you can also just supply a large collection of individual images you would like to work with directly by placing them into a folder within `training-picker/extracted-frames`.

### Cropping

* Scroll up and down to increase or decrease the size of the crop brush
* Ctrl+scroll to adjust the aspect ratio of the crop, and middle-click to reset the aspect ratio to 1:1
* Shift+scroll to adjust the size / aspect ratio by smaller increments
* Click to save a crop at the brush's position
* Navigate between frames in the collection by clicking the navigation buttons, entering a number into the counter, or by using the arrow keys / AD
* Select an outfill method to outfill the non-square area of a rectangular crop into a square shape
* Click "Bulk process frames with chosen outfill method" to automatically process every image in the current frame set using the outfill method chosen, outputting to the directory under "Save crops to:"
* Crops will be saved to `training-picker/cropped-frames` by default
