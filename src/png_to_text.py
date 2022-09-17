from mmocr.utils.ocr import MMOCR
def png_to_text(crop_path):
    if crop_path==None:
        result='  '
        return result
    else:
        ocr = MMOCR(det='PS_CTW', recog='SAR')
        results = ocr.readtext(crop_path, output='Kamre_Foto\Text\cropped_image_plate_75_text.jpg', export='C:\\Users\\omer\\Desktop\\Kamre_Foto',print_result=True)
        result=results[0]['text']#[0]
        if len(result)==0:
            result='  '
            return result
        else:
            return result[0]

