import cv2
import numpy as np
from picamera2 import Picamera2

# ------------------------
# Initialize Camera
# ------------------------
def init_camera():
    picam2 = Picamera2()
    picam2.configure(picam2.create_preview_configuration())
    picam2.start()
    return picam2

# ------------------------
# Load Haar Cascade
# ------------------------
def Haar_Cascade():
    face_cascade = cv2.CascadeClassifier('./haarcascades/haarcascade_frontalface_alt2.xml') #pretrained model
    if face_cascade.empty():
        print("Error loading face cascade")
        exit()
    return face_cascade

# ------------------------
# Load Cat Image (with alpha)
# ------------------------
def loadCatImage(number):
    img = cv2.imread('cats.png', cv2.IMREAD_UNCHANGED)
    h = 997
    w = 1000
    y = [0, int(h/4-60), int(h/2-60), int(3*h/4-80), int(h-80)]
    x = [0, int(w/4), int(w/2), int(3*w/4), int(w)]
    i = number // 4
    j = number % 4
    print("number", number)
    print("i,j", i, j)
    print("y,x", y, x)
    smaller_img = img[y[j+0]:y[j+1], x[i+0]:x[i+1], :]
    return smaller_img

# ------------------------
# Remove White Background
# ------------------------
def RemoveBackgroundOpenCV(img):
    # Convert to BGRA if needed
    if img.shape[2] == 3:
        result = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
    else:
        result = img.copy()
    
    # Create a mask for white pixels (with tolerance for near-white)
    # This handles RGB values close to white (e.g., 250-255)
    lower_white = np.array([240, 240, 240, 0])
    upper_white = np.array([255, 255, 255, 255])
    
    # Create mask for white pixels
    mask = cv2.inRange(result, lower_white, upper_white)
    
    # Set alpha channel to 0 (transparent) for white pixels
    result[mask > 0] = [255, 255, 255, 0]
    
    return result

# ------------------------
# Function to Overlay PNG
# ------------------------
def overlay_png(background, overlay, x, y, w, h):
    bg_h, bg_w = background.shape[:2]
    
    # Resize overlay to face size
    overlay = cv2.resize(overlay, (w, h))
    
    # Compute coordinates safely
    x1, y1 = max(0, x), max(0, y)
    x2, y2 = min(bg_w, x + w), min(bg_h, y + h)
    
    # Adjust overlay in case it's partially outside frame
    overlay = overlay[y1 - y:y2 - y, x1 - x:x2 - x]
    
    if overlay.shape[2] == 4:
        b, g, r, a = cv2.split(overlay)
        alpha = a / 255.0
        alpha_inv = 1.0 - alpha
    else:
        b, g, r = cv2.split(overlay)
        alpha = np.ones((overlay.shape[0], overlay.shape[1]))
        alpha_inv = 1.0 - alpha
    
    for c, channel in enumerate([b, g, r]):
        background[y1:y2, x1:x2, c] = (
            alpha * channel + alpha_inv * background[y1:y2, x1:x2, c]
        )
    
    return background

# ------------------------
# Main Loop
# ------------------------
def main():
    picam2 = init_camera()
    detectClassifier = Haar_Cascade()
    
    # Preprocess all cat images
    print("Loading cat images...")
    cat_imgs = [RemoveBackgroundOpenCV(loadCatImage(i)) for i in range(16)]
    print(f"Loaded {len(cat_imgs)} cat images")
    
    # Initialize index
    cat_index = 0
    num_cats = len(cat_imgs)
    
    print("\nControls:")
    print("- Right Arrow: Next cat")
    print("- Left Arrow: Previous cat")
    print("- Q: Quit")
    
    while True:
        # shape is 480,640,4
        frame = picam2.capture_array()
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        overlayed_frame = frame_bgr.copy()
        
        # Detect faces
        faces = detectClassifier.detectMultiScale(frame_gray, scaleFactor=1.3, minNeighbors=5)
        
        # Overlay current cat on all detected faces
        if len(faces) > 0:
            current_cat = cat_imgs[cat_index]
            for (x, y, w, h) in faces:
                overlayed_frame = overlay_png(overlayed_frame, current_cat, x, y, w, h)
        
        # Display current cat number
        cv2.putText(overlayed_frame, f"Cat: {cat_index + 1}/{num_cats}", 
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Show frame
        cv2.imshow("Face Detection - Cat Overlay", overlayed_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            break
        elif key == 83:  # Right arrow keyq
            cat_index = (cat_index + 1) % num_cats
            print(f"Switched to cat {cat_index + 1}/{num_cats}")
        elif key == 81:  # Left arrow key
            cat_index = (cat_index - 1) % num_cats
            print(f"Switched to cat {cat_index + 1}/{num_cats}")
    
    # Cleanup
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()