import cv2
import numpy as np
import datetime 
from PIL import Image
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pandas as pd
import numpy as np

def crop_plate(mask_path,original_path):
    if mask_path==None:
        cropped_image_path=None
        return cropped_image_path
    else:
        e = datetime.datetime.now()
        timee=str(e.hour) +' '+ str(e.minute) +' '+ str(e.second)
        img = cv2.imread(mask_path)
        img = load_img(mask_path) 
        img= np.array(img,dtype=np.uint8)
        original_img = load_img(original_path) # PIL object
        original_img = np.array(original_img,dtype=np.uint8) # 8 bit array (0,255)
        
        t_lower = 25 # Lower Threshold
        t_upper = 255 # Upper threshold
        
        
        # Applying the Canny Edge filter 
        # with Aperture Size and L2Gradient
        edge = cv2.Canny(img, t_lower, t_upper ) 
        
        
        contors, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


        contors = max(contors, key=cv2.contourArea, default=0)	

        x,y,w,h = cv2.boundingRect(contors)
        print(x,y,w,h)
        
        cropped_image = original_img[y-50:y+h+150, x-750:x+w+750]
        print(cropped_image.shape)
        from PIL import Image
        im = Image.fromarray(cropped_image)
        im.save("C:\\Users\\omer\\Desktop\\plate\\Kamre_Foto\\Crop\\cropped_image_plate_.jpeg")
        cropped_image_path=f'C:\\Users\\omer\\Desktop\\plate\\Kamre_Foto\\Crop\\cropped_image_plate_{timee}.png'
        cv2.imwrite(cropped_image_path,cropped_image)
        cv2.waitKey(10)
        return cropped_image_path
