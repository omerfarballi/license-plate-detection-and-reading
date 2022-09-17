import datetime
import tensorflow as tf
from skimage import io
import cv2
import numpy as np
import pandas as pd
from keras.models import load_model
from PIL import Image 
#original path isteniyor
def plaka_detection_(path):
    e = datetime.datetime.now()
    timee=str(e.hour) +' '+ str(e.minute) +' '+ str(e.second)
    path=[path]
    
    smooth = 1
    
    def prediction(test, model, model_seg):
        '''
        Predcition function which takes dataframe containing ImageID as Input and perform 2 type of prediction on the image
        Initially, image is passed through the classification network which predicts whether the image has defect or not, if the model
        is 99% sure that the image has no defect, then the image is labeled as no-defect, if the model is not sure, it passes the image to the
        segmentation network, it again checks if the image has defect or not, if it has defect, then the type and location of defect is found
        '''
        # empty list to store results
        mask, image_id, has_mask = [], [], []
        
        #itetrating through each image in test data
        for i in test.path_original:
            
            img = io.imread(i)
            #normalizing
            img = img *1./255.
            #reshaping
            img = cv2.resize(img, (256,256))
            # converting img into array
            img = np.array(img, dtype=np.float64)
            #reshaping the image from 256,256,3 to 1,256,256,3
            img = np.reshape(img, (1,256,256,3))
            
            #making prediction for plate in image
            is_defect = model.predict(img)
            
            #if plate is not present we append the details of the image to the list
            if np.argmax(is_defect)==0:
                image_id.append(i)
                has_mask.append(0)
                mask.append('No mask :)')
                continue
            
            #Creating a empty array of shape 1,256,256,1
            X = np.empty((1,256,256,3))
            # read the image
            img = io.imread(i)
            #resizing the image and coverting them to array of type float64
            img = cv2.resize(img, (256,256))
            img = np.array(img, dtype=np.float64)
            
            # standardising the image
            img -= img.mean()
            img /= img.std()
            #converting the shape of image from 256,256,3 to 1,256,256,3
            X[0,] = img
            
            #make prediction of mask
            predict = model_seg.predict(X)
            
            # if sum of predicted mask is 0 then there is not tumour
            if predict.round().astype(int).sum()==0:
                image_id.append(i)
                has_mask.append(0)
                mask.append('No mask :)')
            else:
            #if the sum of pixel values are more than 0, then there is tumour
                image_id.append(i)
                has_mask.append(1)
                mask.append(predict)
                
        return pd.DataFrame({'image_path': image_id,'predicted_mask': mask,'has_mask': has_mask})
    def tversky(y_true, y_pred):
        y_true_pos = K.flatten(y_true)
        y_pred_pos = K.flatten(y_pred)
        true_pos = K.sum(y_true_pos * y_pred_pos)
        false_neg = K.sum(y_true_pos * (1-y_pred_pos))
        false_pos = K.sum((1-y_true_pos)*y_pred_pos)
        alpha = 0.7
        return (true_pos + smooth)/(true_pos + alpha*false_neg + (1-alpha)*false_pos + smooth)

    def focal_tversky(y_true,y_pred):
        y_true = tf.cast(y_true, tf.float32)
        y_pred = tf.cast(y_pred, tf.float32)
        
        pt_1 = tversky(y_true, y_pred)
        gamma = 0.75
        return K.pow((1-pt_1), gamma)

    def tversky_loss(y_true, y_pred):
        return 1 - tversky(y_true,y_pred)
    
    seg_model=load_model("C:\\Users\\omer\\Desktop\\plate\\ResUNet-segModel-weights_ensembl.hdf5",custom_objects={"focal_tversky": focal_tversky,"tversky": tversky })
    
    
    df_test= pd.DataFrame(path,columns=['path_original'])
    
    df_pred_test = prediction(df_test, seg_model, seg_model)
    df_pred=df_pred_test
    if type(df_pred.predicted_mask[0])==str:
        out_path=None
        return out_path
    else:
        
        #read predicted mask
        pred = np.array(df_pred.predicted_mask[0],dtype = np.uint8).squeeze().round()
        pred= cv2.resize(pred, (2688, 1520)) # pixels values it can change
        print(pred.shape)
        
        result = Image.fromarray((pred * 255).astype(np.uint8))
        out_path=f'C:\\Users\\omer\\Desktop\\plate\\Kamre_Foto\\Mask\\outpt_{timee}.png'
        result.save(out_path)
        return out_path
