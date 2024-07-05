import numpy as np
import cv2 as cv
import easyocr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize EasyOCR reader
reader = easyocr.Reader(['en'])  # You can specify the languages you want to support

# Setup Chrome driver using WebDriverManager
driver = webdriver.Chrome(ChromeDriverManager().install())

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit()

# Open a file to save the recognized text
with open('recognized_text.txt', 'w') as f:
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        # Convert frame to grayscale
        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Perform text detection
        result = reader.readtext(gray)

        # Draw bounding boxes and text on the frame
        for (bbox, text, prob) in result:
            # Extract the bounding box coordinates
            (top_left, top_right, bottom_right, bottom_left) = bbox
            top_left = tuple(map(int, top_left))
            bottom_right = tuple(map(int, bottom_right))

            # Draw a rectangle around the text
            cv.rectangle(frame, top_left, bottom_right, (0, 255, 0), 2)

            # Put the recognized text
            cv.putText(frame, text, (top_left[0], top_left[1] - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Save the recognized text to the file
            f.write(f'{text}\n')

            # Use Selenium to search the recognized text on Google
            driver.get("https://www.google.com")
            search_box = driver.find_element_by_name("q")
            search_box.send_keys(text)
            search_box.send_keys(Keys.RETURN)

            # Wait for a few seconds to see the search results
            time.sleep(5)

        # Display the resulting frame
        cv.imshow('frame', frame)

        if cv.waitKey(1) == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv.destroyAllWindows()

# Close the browser
driver.quit()
