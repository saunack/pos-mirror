img_raw = cv2.imread("/kaggle/input/temp-dataset-pos/machine2.png")
image = img_raw.copy()
gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

blurred_gray_image = cv2.blur(gray_image,(21,21))
_,thresholded_blurry_image = cv2.threshold(blurred_gray_image,165,255,cv2.THRESH_BINARY)
contours, hierarchy = cv2.findContours(thresholded_blurry_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

page = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
con = np.zeros_like(image)
con = cv2.drawContours(con, page, -1, (0, 255, 255), 3)

output = image.copy()
if len(contours) != 0:
    c = max(contours, key = cv2.contourArea)
    # coordinates of the contour
    x,y,w,h = cv2.boundingRect(c)
    cv2.rectangle(output,(x,y),(x+w,y+h),(0,255,0),2)

output = cv2.cvtColor(output,cv2.COLOR_BGR2RGB)
