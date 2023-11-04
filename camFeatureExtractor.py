import cv2

# Given an opencv image, extract the mean brightness over the image, normalized to [0,1]
def extractNormalizedBrightness(img):
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Extract the value channel
    v = hsv[:,:,2]
    # Compute the mean
    mean = v.mean()
    # Normalize to [0,1]
    normalized = mean / 255.0
    return normalized
