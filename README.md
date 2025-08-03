# Floating Image Popup Tool

A lightweight, draggable, and resizable popup tool for Windows that displays animated or static images (GIF, PNG, JPG, WEBP, etc.) on your desktop with transparent background.  
**No installation required!** Just run the EXE and enjoy.

## Features

- Supports GIF (animated), PNG, JPG, JPEG, WEBP images
- Displays image with a transparent background and no window frame
- User can drag and resize the image popup freely
- Easy image selection at startup (choose any image from the `gif` folder)
- Users can add or remove image files in the `gif` folder at any time
- No Python or library installation required (standalone EXE)

## How to Use

1. **Download and unzip the release package.**
2. **Make sure the following structure exists:**
    ```
    /your-folder/
      ├─ index.exe
      └─ gif/
          ├─ ad.gif
          ├─ my_image.png
          └─ ...
    ```
3. **Add any GIF, PNG, JPG, JPEG, or WEBP files you want to the `gif` folder.**
4. **Run `index.exe`.**
5. **Select the image you want to display.**
6. **Drag or resize the image window as you like!**
    - To resize, drag from the bottom-right corner of the window.

## Tips

- You can add or remove images in the `gif` folder at any time.
- Animated GIFs will play automatically.
- PNG/JPG/WEBP images are displayed statically.
- If the `gif` folder does not exist, it will be created automatically.

## Troubleshooting

- If you see a message like "No image files found", add your images to the `gif` folder and restart.
- For best results, use images with transparent backgrounds.
- This app is Windows-only (PyQt5 EXE build).

## Credits

Developed with [PyQt5](https://pypi.org/project/PyQt5/).

---

**Enjoy your floating image popup!**
