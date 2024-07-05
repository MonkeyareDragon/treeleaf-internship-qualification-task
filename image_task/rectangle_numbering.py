import cv2
import numpy as np

def sort_rectangles_by_line_length(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rectangles = []
    
    # Loop over the contours
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            roi = gray[y:y+h, x:x+w]
            
            # Find the lines inside the rectangle
            lines = cv2.HoughLinesP(roi, 1, np.pi/180, threshold=30, minLineLength=30, maxLineGap=5)
            if lines is not None:
                line_lengths = [np.sqrt((line[0][2] - line[0][0])**2 + (line[0][3] - line[0][1])**2) for line in lines]
                max_length = max(line_lengths)
                rectangles.append((x, y, w, h, max_length))
    
    # Sort rectangles by line length
    rectangles = sorted(rectangles, key=lambda x: x[4])
    
    # Annotate the rectangles with numbers
    for i, (x, y, w, h, _) in enumerate(rectangles):
        cv2.putText(image, str(i + 1), (x + w // 2, y + h // 2), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    
    # Save the result
    cv2.imwrite('image_task/data/processed/numbered_rectangles.png', image)

if __name__ == "__main__":
    sort_rectangles_by_line_length('image_task/data/raw/rectangle_image.png')
