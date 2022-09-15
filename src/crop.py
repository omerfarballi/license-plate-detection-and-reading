import cv2
import numpy as np
import datetime 
from PIL import Image
import cv2
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pandas as pd
import numpy as np
# eğer foto siyah gelirse ona çözüm bul
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
        #x+200 değeri değişkendir ortalama bir değer test sonrası değiştirelecektr.
        # cropped_image = original_img[y-400:y+h+400, x-400:x+w+400]# original_img[y-33:y+h+33, x-33:x+w+33] 1270,690   1430,740
        cropped_image = original_img[y-50:y+h+150, x-750:x+w+750]
        print(cropped_image.shape)
        from PIL import Image
        im = Image.fromarray(cropped_image)
        im.save("C:\\Users\\oozer\\Desktop\\plate\\Kamre_Foto\\Crop\\cropped_image_plate_.jpeg")
        cropped_image_path=f'C:\\Users\\oozer\\Desktop\\plate\\Kamre_Foto\\Crop\\cropped_image_plate_{timee}.png'
        cv2.imwrite(cropped_image_path,cropped_image)
        cv2.waitKey(10)
        return cropped_image_path
# crop_plate('C:\\Users\\eargestajyer\\Desktop\\interface_plate\\Kamre_Foto\\Mask\\outpt_17 32 33.png','C:\\Users\\eargestajyer\\Desktop\\interface_plate\\Kamre_Foto\\Orginal\\image_6+9+2022  17+32+33.png')