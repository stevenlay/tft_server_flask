import numpy as np
import urllib.request
import cv2
import pytesseract

def url_to_image(url):
	resp = urllib.request.urlopen(url)
	image = np.asarray(bytearray(resp.read()), dtype="uint8")
	image = cv2.imdecode(image, cv2.IMREAD_COLOR)
 
	return image

def crop_image(image, h, w, x, y):
    crop = image[y:y+h, x:x+w]
    return crop

def image_to_string(image, language):
    return pytesseract.image_to_string(image, lang=language, config='--psm 7')

def increase_brightness(img, value=30):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    lim = 255 - value
    v[v > lim] = 255
    v[v <= lim] += value

    final_hsv = cv2.merge((h, s, v))
    img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
    return img

def img_pipeline(url, streamer_name):
    image = url_to_image(url)
    image = increase_brightness(image)
    crop = crop_image(image, 22, 367, 786, 0).copy()
    cv2.imwrite('images/output_%s.jpg' %streamer_name,crop)
    upsize = cv2.resize(crop, None, fx = 2, fy = 2, interpolation = cv2.INTER_CUBIC)
    return image_to_string(upsize, 'eng')