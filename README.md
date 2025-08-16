# Finger Controlled Mouse

A computer vision-based application that allows you to control your mouse cursor using hand gestures captured through your webcam. This project uses MediaPipe for hand detection and tracking, OpenCV for video processing, and PyAutoGUI for mouse control.

![Demo](https://img.shields.io/badge/Python-3.7+-blue.svg)
![OpenCV](https://img.shields.io/badge/OpenCV-4.0+-green.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Latest-orange.svg)

## Features

- **Gesture-Based Mouse Control**: Control your mouse cursor with intuitive hand gestures
- **Multiple Click Types**: Perform left clicks, right clicks, and drag operations
- **Scroll Functionality**: Scroll up and down using three-finger gestures
- **Real-Time Feedback**: Visual feedback showing current gesture and system state
- **Smooth Movement**: Configurable smoothening for precise cursor control
- **Debug Information**: Real-time display of finger positions and gesture states

## Hand Gestures

| Gesture | Action | Description |
|---------|--------|-------------|
| 👆 Index finger alone | **Move cursor** | Point with your index finger to move the mouse cursor |
| 👍👆 Thumb + Index close | **Left click** | Bring your thumb and index finger close together |
| 👍👆🖕 Thumb + Index + Middle close | **Right click** | Bring your thumb, index, and middle fingers close together |
| 👆🖕 Index + Middle close | **Drag** | Bring your index and middle fingers close to start dragging |
| 👆🖕🖖 Index + Middle + Ring up | **Scroll mode** | Three fingers up (excluding thumb and pinky) for scrolling |
| ✊ Fist | **Stop all actions** | Close your hand into a fist to stop all mouse actions |

## Requirements

### System Requirements
- Python 3.7 or higher
- Webcam (built-in or external)
- Windows, macOS, or Linux

### Python Dependencies
- `opencv-python` (cv2) - For video capture and processing
- `mediapipe` - For hand detection and landmark tracking
- `pyautogui` - For mouse control
- `numpy` - For mathematical operations

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/naakaarafr/Finger-Controlled-Mouse.git
   cd Finger-Controlled-Mouse
   ```

2. **Install required packages**:
   ```bash
   pip install opencv-python mediapipe pyautogui numpy
   ```

   Or using the requirements file:
   ```bash
   pip install -r requirements.txt
   ```

3. **Grant necessary permissions**:
   - **macOS**: You may need to grant camera and accessibility permissions
   - **Linux**: Ensure your user has access to the camera device

## Usage

1. **Run the application**:
   ```bash
   python finger_controlled_mouse.py
   ```

2. **Position yourself**: Sit in front of your webcam with good lighting

3. **Calibrate**: Hold your hand in the camera view and wait for hand detection

4. **Start controlling**: Use the gestures listed above to control your mouse

5. **Exit**: Press 'q' or 'ESC' to quit the application

## Configuration

You can modify these parameters in the code to customize the behavior:

```python
# Mouse control variables
self.smoothening = 5          # Higher = smoother but slower movement
self.click_threshold = 60     # Distance threshold for click detection
self.click_cooldown = 0.15    # Minimum time between clicks (seconds)

# Camera settings
self.camera_width = 640       # Camera resolution width
self.camera_height = 480      # Camera resolution height

# Detection confidence
min_detection_confidence=0.7  # Hand detection confidence
min_tracking_confidence=0.5   # Hand tracking confidence
```

## How It Works

### 1. Hand Detection
The application uses Google's MediaPipe library to detect and track hand landmarks in real-time. It identifies 21 key points on your hand, including fingertips and joints.

### 2. Gesture Recognition
The system analyzes the positions and states of your fingers to determine which gesture you're making:
- **Finger Up/Down Detection**: Compares fingertip positions with finger joints
- **Distance Calculation**: Measures distances between fingertips for click gestures
- **State Management**: Tracks gesture states to prevent unwanted repeated actions

### 3. Mouse Control
PyAutoGUI translates the detected gestures into mouse actions:
- **Coordinate Mapping**: Maps camera coordinates to screen coordinates
- **Smoothening**: Applies smoothening algorithms for stable cursor movement
- **Action Execution**: Performs clicks, drags, and scrolls based on gestures

## Troubleshooting

### Common Issues

**Camera not detected**:
- Ensure your webcam is connected and not being used by another application
- Try changing the camera index in the code: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`

**Hand not detected**:
- Improve lighting conditions
- Ensure your hand is clearly visible in the camera frame
- Lower the detection confidence values
- Keep your hand steady for a few seconds to allow detection

**Mouse movements are jerky**:
- Increase the `smoothening` value for smoother movement
- Ensure stable lighting conditions
- Keep your hand steady while moving

**Clicks not registering**:
- Adjust the `click_threshold` value (lower for more sensitive detection)
- Make sure you're bringing the correct fingers close together
- Check that the gesture is held for the minimum `gesture_hold_time`

**Performance issues**:
- Close other applications using the camera
- Lower the camera resolution in the code
- Reduce the detection confidence slightly

### Debug Information

The application displays real-time debug information including:
- Current finger states (up/down)
- Distances between fingers
- Current gesture recognition
- System states (clicking, dragging, etc.)

## Technical Details

### Architecture
```
Camera Input → MediaPipe Processing → Gesture Recognition → Mouse Control
     ↓              ↓                      ↓                   ↓
  OpenCV         Hand Landmarks        Custom Logic        PyAutoGUI
```

### Key Classes and Methods

- `FingerMouse`: Main class handling all functionality
- `get_distance()`: Calculates Euclidean distance between points
- `detect_gesture()`: Determines which fingers are up/down
- `move_mouse()`: Handles cursor movement with smoothening
- `perform_left_click()`: Manages left click actions with state control
- `reset_states()`: Resets all gesture states

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## Potential Improvements

- [ ] Add gesture customization through configuration file
- [ ] Implement zoom gestures
- [ ] Add support for multiple hands
- [ ] Create a GUI for easy configuration
- [ ] Add gesture training mode
- [ ] Implement voice commands for additional control
- [ ] Add support for custom gesture macros

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Google MediaPipe team for the excellent hand tracking library
- OpenCV community for computer vision tools
- PyAutoGUI developers for mouse control functionality

## Support

If you encounter any issues or have questions:
1. Check the troubleshooting section above
2. Open an issue on GitHub with detailed information about your problem
3. Include your system specifications and error messages

---

**Note**: This application is designed for accessibility and productivity purposes. Please ensure you comply with your local laws and regulations regarding automated mouse control.
