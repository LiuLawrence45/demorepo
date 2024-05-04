# Download the helper library from https://www.twilio.com/docs/python/install
import os
from twilio.rest import Client
import cv2
import numpy as np
# import mediapipe as mp
import tensorflow as tf
# Set environment variables for your credentials
# Read more at http://twil.io/secure

account_sid = "AC1322e254b1ecc1169dc491b8a1984c4a"
auth_token = "b54ba0b9b31511a9fe078e5596e68feb"
client = Client(account_sid, auth_token)


print("hello world")
print("Helo world 2 this is what is working now")


def call_person():
    call = client.calls.create(
    url="http://demo.twilio.com/docs/voice.xml",
    to="+14122251447",
    from_="+18447492281"
    )

# print(call.sid)


call_made = False

def detect_thumbs_up(frame):
    # Convert to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Define range for skin color
    lower_skin = np.array([0, 48, 80], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)
    
    # Threshold the HSV image to get only skin colors
    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        # Find the largest contour and its properties
        largest_contour = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(largest_contour, returnPoints=False)
        defects = cv2.convexityDefects(largest_contour, hull)
        
        if defects is not None:
            thumbs_up_count = 0
            
            # Loop over the defects to count potential thumbs up
            for i in range(defects.shape[0]):
                s, e, f, d = defects[i, 0]
                start = tuple(largest_contour[s][0])
                end = tuple(largest_contour[e][0])
                far = tuple(largest_contour[f][0])
                
                # Apply your logic to detect thumbs up based on the defects
                # This is a simplified example and may need refinement
                if d > 10000:  # Example condition for thumbs up
                    thumbs_up_count += 1
            
            if thumbs_up_count >= 1:  # If at least one condition met, consider it a thumbs up
                return True
    
    return False

cap = cv2.VideoCapture(0)



try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

         
        if detect_thumbs_up(frame) and not call_made:
            print("Thumbs Up Detected!")
            call_person()
            call_made = True  # Set flag to True after making call
        elif not call_made:
            print("No Thumbs Up Detected")
        
        
        cv2.imshow('Video', frame)
    
        # Break the loop with the 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()

