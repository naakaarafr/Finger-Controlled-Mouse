import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Disable pyautogui failsafe
pyautogui.FAILSAFE = False

class FingerMouse:
    def __init__(self):
        # Initialize MediaPipe hands
        self.mp_hands = mp.solutions.hands
        self.handf.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        
        # Get screen dimensions
        self.screen_width, self.screen_height = pyautogui.size()
        
        # Camera setup
        self.camera = cv2.VideoCapture(0)
        self.camera_width = 640
        self.camera_height = 480
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.camera_width)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.camera_height)
        
        # Mouse control variables
        self.prev_x, self.prev_y = 0, 0
        self.curr_x, self.curr_y = 0, 0
        self.smoothening = 5  # Smoothening factor for mouse movement
        self.click_threshold = 60  # Distance threshold for click detection (increased for sensitivity)
        
        # State variables
        self.left_click_state = False
        self.right_click_state = False
        self.dragging = False
        self.scroll_mode = False
        
        # Timing variables
        self.last_left_click_time = 0
        self.last_right_click_time = 0
        self.click_cooldown = 0.15  # Reduced cooldown for faster clicking
        self.gesture_hold_time = 0.05  # Reduced hold time for quicker response
        
        print("Finger Mouse Controls:")
        print("- Index finger alone: Move cursor")
        print("- Thumb + Index close: Left click")
        print("- Thumb + Index + Middle close: Right click")  
        print("- Index + Middle close: Drag")
        print("- Index + Middle + Ring up: Scroll mode")
        print("- Fist: Stop all actions")
        print("- Press 'q' to quit")
        
    def get_distance(self, point1, point2):
        """Calculate distance between two points"""
        return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_finger_up(self, landmarks, finger_tip, finger_pip):
        """Check if finger is up based on landmarks"""
        return landmarks[finger_tip].y < landmarks[finger_pip].y
    
    def get_finger_positions(self, landmarks):
        """Get positions of finger tips"""
        # Landmark indices for fingertips
        thumb_tip = 4
        index_tip = 8
        middle_tip = 12
        ring_tip = 16
        pinky_tip = 20
        
        positions = {
            'thumb': (int(landmarks[thumb_tip].x * self.camera_width), 
                     int(landmarks[thumb_tip].y * self.camera_height)),
            'index': (int(landmarks[index_tip].x * self.camera_width), 
                     int(landmarks[index_tip].y * self.camera_height)),
            'middle': (int(landmarks[middle_tip].x * self.camera_width), 
                      int(landmarks[middle_tip].y * self.camera_height)),
            'ring': (int(landmarks[ring_tip].x * self.camera_width), 
                    int(landmarks[ring_tip].y * self.camera_height)),
            'pinky': (int(landmarks[pinky_tip].x * self.camera_width), 
                     int(landmarks[pinky_tip].y * self.camera_height))
        }
        return positions
    
    def detect_gesture(self, landmarks):
        """Detect hand gestures"""
        # Get finger states (up/down)
        fingers_up = []
        
        # Thumb (special case - compare x coordinates)
        if landmarks[4].x > landmarks[3].x:  # Right hand
            fingers_up.append(1)
        else:
            fingers_up.append(0)
            
        # Other fingers
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            if self.is_finger_up(landmarks, tip, pip):
                fingers_up.append(1)
            else:
                fingers_up.append(0)
        
        return fingers_up
    
    def move_mouse(self, x, y):
        """Move mouse with smoothening"""
        # Convert camera coordinates to screen coordinates
        screen_x = np.interp(x, [100, self.camera_width - 100], [0, self.screen_width])
        screen_y = np.interp(y, [100, self.camera_height - 100], [0, self.screen_height])
        
        # Apply smoothening
        self.curr_x = self.prev_x + (screen_x - self.prev_x) / self.smoothening
        self.curr_y = self.prev_y + (screen_y - self.prev_y) / self.smoothening
        
        pyautogui.moveTo(self.curr_x, self.curr_y)
        self.prev_x, self.prev_y = self.curr_x, self.curr_y
    
    def perform_left_click(self):
        """Perform left mouse click with proper state management"""
        current_time = time.time()
        
        if not self.left_click_state and (current_time - self.last_left_click_time) > self.click_cooldown:
            pyautogui.click()
            self.left_click_state = True
            self.last_left_click_time = current_time
            print("Left Click!")
    
    def perform_right_click(self):
        """Perform right mouse click with proper state management"""
        current_time = time.time()
        
        if not self.right_click_state and (current_time - self.last_right_click_time) > self.click_cooldown:
            pyautogui.rightClick()
            self.right_click_state = True
            self.last_right_click_time = current_time
            print("Right Click!")
    
    def check_click_gesture(self, finger1_pos, finger2_pos, threshold):
        """Check if two fingers are close enough for a click gesture"""
        distance = self.get_distance(finger1_pos, finger2_pos)
        return distance < threshold
    
    def perform_drag(self, start=True):
        """Perform drag operation"""
        if start and not self.dragging:
            pyautogui.mouseDown()
            self.dragging = True
        elif not start and self.dragging:
            pyautogui.mouseUp()
            self.dragging = False
    
    def perform_scroll(self, direction):
        """Perform scroll operation"""
        if direction == 'up':
            pyautogui.scroll(3)
        elif direction == 'down':
            pyautogui.scroll(-3)
    
    def reset_states(self):
        """Reset all state variables"""
        if self.dragging:
            pyautogui.mouseUp()
        self.left_click_state = False
        self.right_click_state = False
        self.dragging = False
        self.scroll_mode = False
    
    def run(self):
        """Main loop"""
        while True:
            ret, frame = self.camera.read()
            if not ret:
                break
                
            # Flip frame horizontally for mirror effect
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            # Process frame
            results = self.hands.process(rgb_frame)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    # Draw landmarks
                    self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    # Get finger positions and gestures
                    fingers = self.detect_gesture(hand_landmarks.landmark)
                    positions = self.get_finger_positions(hand_landmarks.landmark)
                    
                    # Calculate distances between fingers with more sensitive thresholds
                    thumb_index_dist = self.get_distance(positions['thumb'], positions['index'])
                    thumb_middle_dist = self.get_distance(positions['thumb'], positions['middle'])
                    index_middle_dist = self.get_distance(positions['index'], positions['middle'])
                    
                    # More sensitive click detection
                    thumb_index_close = self.check_click_gesture(positions['thumb'], positions['index'], self.click_threshold)
                    thumb_middle_close = self.check_click_gesture(positions['thumb'], positions['middle'], self.click_threshold)
                    index_middle_close = self.check_click_gesture(positions['index'], positions['middle'], self.click_threshold)
                    
                    # Gesture recognition and actions
                    if sum(fingers) == 1 and fingers[1] == 1:  # Only index finger up
                        self.move_mouse(positions['index'][0], positions['index'][1])
                        self.reset_states()
                        cv2.putText(frame, "MOVE", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                        
                    elif fingers[0] == 1 and fingers[1] == 1 and sum(fingers) == 2 and thumb_index_close:  
                        # Thumb + Index close (left click) - more sensitive
                        self.move_mouse(positions['index'][0], positions['index'][1])
                        self.perform_left_click()
                        if self.dragging:
                            pyautogui.mouseUp()
                            self.dragging = False
                        cv2.putText(frame, "LEFT CLICK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                        
                    elif (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 3 and 
                          thumb_index_close and thumb_middle_close):  
                        # Thumb + Index + Middle close (right click) - more sensitive
                        self.move_mouse(positions['index'][0], positions['index'][1])
                        self.perform_right_click()
                        if self.dragging:
                            pyautogui.mouseUp()
                            self.dragging = False
                        cv2.putText(frame, "RIGHT CLICK", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                        
                    elif (fingers[1] == 1 and fingers[2] == 1 and sum(fingers) == 2 and 
                          index_middle_close):  
                        # Index + Middle close (drag) - more sensitive
                        self.move_mouse(positions['index'][0], positions['index'][1])
                        self.perform_drag(True)
                        # Reset click states when dragging
                        self.left_click_state = False
                        self.right_click_state = False
                        cv2.putText(frame, "DRAG", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                        
                    elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and fingers[0] == 0 and fingers[4] == 0:  
                        # Three fingers up for scroll (excluding thumb and pinky)
                        if not self.scroll_mode:
                            self.scroll_start_y = positions['index'][1]
                            self.scroll_mode = True
                        else:
                            # Determine scroll direction with more sensitivity
                            y_diff = self.scroll_start_y - positions['index'][1]
                            if abs(y_diff) > 15:  # Reduced threshold for more sensitive scrolling
                                if y_diff > 0:
                                    self.perform_scroll('up')
                                else:
                                    self.perform_scroll('down')
                                self.scroll_start_y = positions['index'][1]
                        cv2.putText(frame, "SCROLL", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                        
                    elif sum(fingers) == 0:  # Fist - stop all actions
                        self.reset_states()
                        cv2.putText(frame, "STOP", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (128, 128, 128), 2)
                        
                    else:
                        # Reset click states when gesture changes - more sensitive reset
                        if not (fingers[0] == 1 and fingers[1] == 1 and thumb_index_close):
                            self.left_click_state = False
                        if not (fingers[0] == 1 and fingers[1] == 1 and fingers[2] == 1 and 
                               thumb_index_close and thumb_middle_close):
                            self.right_click_state = False
                        if self.dragging and not (fingers[1] == 1 and fingers[2] == 1 and index_middle_close):
                            pyautogui.mouseUp()
                            self.dragging = False
                        if self.scroll_mode and not (fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1):
                            self.scroll_mode = False
                        cv2.putText(frame, "READY", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                    
                    # Display debug information with sensitivity indicators
                    cv2.putText(frame, f"Fingers: {fingers}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    cv2.putText(frame, f"T-I: {int(thumb_index_dist)} ({'CLOSE' if thumb_index_close else 'FAR'}) | I-M: {int(index_middle_dist)} ({'CLOSE' if index_middle_close else 'FAR'})", (50, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                    cv2.putText(frame, f"L-Click: {self.left_click_state} | R-Click: {self.right_click_state} | Drag: {self.dragging}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
                    cv2.putText(frame, f"Threshold: {self.click_threshold} | Cooldown: {self.click_cooldown}s", (50, 160), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)
            else:
                self.reset_states()
                cv2.putText(frame, "NO HAND DETECTED", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            
            # Display instructions
            cv2.putText(frame, "Press 'q' to quit", (50, self.camera_height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Show frame
            cv2.imshow("Finger Controlled Mouse", frame)
            
            # Check for exit
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q') or key == 27:  # 'q' or ESC
                break
        
        # Cleanup
        self.reset_states()
        self.camera.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        finger_mouse = FingerMouse()
        finger_mouse.run()
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        print(f"Error: {e}")
        cv2.destroyAllWindows()