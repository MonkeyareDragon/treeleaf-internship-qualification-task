import cv2
import numpy as np

def align_rectangles(image_path):
    # Load the image
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    result_image = np.ones_like(image) * 255  
    aligned_mask = np.zeros_like(image)  
    
    # Loop over the contours
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) == 4:  
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.intp(box)  
            
            width = int(rect[1][0])
            height = int(rect[1][1])
            
            center = (int(rect[0][0]), int(rect[0][1]))
            
            src_pts = box.astype("float32")
            dst_pts = np.array([[0, height-1],
                                [0, 0],
                                [width-1, 0],
                                [width-1, height-1]], dtype="float32")
            
            # Compute the perspective transform matrix and then apply it
            M = cv2.getPerspectiveTransform(src_pts, dst_pts)
            warped = cv2.warpPerspective(image, M, (width, height))
            
            # Ensure dimensions match before assignment
            target_area = result_image[center[1]-height//2:center[1]+height//2, center[0]-width//2:center[0]+width//2]
            aligned_mask[center[1]-height//2:center[1]+height//2, center[0]-width//2:center[0]+width//2] = 255
            
            if target_area.shape == warped.shape:
                result_image[center[1]-height//2:center[1]+height//2, center[0]-width//2:center[0]+width//2] = warped
            else:
                warped_resized = cv2.resize(warped, (target_area.shape[1], target_area.shape[0]))
                result_image[center[1]-height//2:center[1]+height//2, center[0]-width//2:center[0]+width//2] = warped_resized
    
    result_image = cv2.bitwise_and(result_image, aligned_mask)
    
    cv2.imwrite('image_task/data/processed/aligned_rectangles.png', result_image)

if __name__ == "__main__":
    align_rectangles('image_task/data/raw/rectangle_image.png')
    