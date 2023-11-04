import cv2 
import numpy as np

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


def findBrightAreas(image):
    
    #image = cv2.imread("image1.jpg")

    #  constants
    BINARY_THRESHOLD = 20
    CONNECTIVITY = 4
    JELLY_THRESHOLD = 1000

    #  convert to gray
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #  extract edges
    binary_image = cv2.Laplacian(gray_image, cv2.CV_8UC1)

    #  fill in the holes between edges with dilation
    dilated_image = cv2.dilate(binary_image, np.ones((5, 5)))

    #  threshold the black/ non-black areas
    _, thresh = cv2.threshold(dilated_image, BINARY_THRESHOLD, 255, cv2.THRESH_BINARY)

    #  find connected components
    (numLabels, labels, stats, centroids) =  cv2.connectedComponentsWithStats(thresh, CONNECTIVITY, cv2.CV_32S)



    # clone our original image (so we can draw on it) and then draw
    # a bounding box surrounding the connected component along with
    # a circle corresponding to the centroid
    output = image.copy()

    blobPositionsAndArea = []

        # loop over the number of unique connected component labels
    for i in range(0, numLabels):
        # if this is the first component then we examine the
        # *background* (typically we would just ignore this
        # component in our loop)
        if i == 0:
            text = "examining component {}/{} (background)".format(
                i + 1, numLabels)
        # otherwise, we are examining an actual connected component
        else:
            text = "examining component {}/{}".format( i + 1, numLabels)
        # print a status message update for the current connected
        # component
        print("[INFO] {}".format(text))
        # extract the connected component statistics and centroid for
        # the current label
        x = stats[i, cv2.CC_STAT_LEFT]
        y = stats[i, cv2.CC_STAT_TOP]
        w = stats[i, cv2.CC_STAT_WIDTH]
        h = stats[i, cv2.CC_STAT_HEIGHT]
        area = stats[i, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[i]

        if i != 0 and area > JELLY_THRESHOLD:
            blobPositionsAndArea.append([cX, cY, area])
            cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
            cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

    cv2.imshow("result", output)
    #cv2.waitKey(1)
    return blobPositionsAndArea

