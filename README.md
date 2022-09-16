# license-plate-detection-and-reading
## license plate detection and reading system

The artificial intelligence segmentation model developed for the license plate recognition system is based on the U-Net with backbone pretrained resnet50 architecture. The model is trained in 80 epochs. test success rate is 85%. Figure 1 shows the original photo and the predicted photo.

![image](https://user-images.githubusercontent.com/71135790/190699460-34aff292-ed06-4d8d-89ad-923a3e153bab.png)


 Figure 1
 
The success and loss functions are in Figure 2.

![image](https://user-images.githubusercontent.com/71135790/190699800-d9edb9a3-3b51-46ba-b4a2-cb2b155746ac.png)

 Figure 2
 
The masked photo and the original photo are the same size. The guessed part, that is, the masked part, was cut from the original photo and saved as a new png file. In this process, OpenCV and Pillow are used together.

With OpenCV and Pillow library, operations can be done by converting photos to matrix format. These libraries were used to identify the corners of the predicted plate. By using the Canny, findCounters, boundingRect functions in the Opencv library together, the boundary points on the x and y axes of the plate are determined. Using these points, only the photo with the license plate is recorded.

The result obtained as a result of these processes and the photograph given as input to the model are shown in Figure 3.

![image](https://user-images.githubusercontent.com/71135790/190700250-d906aa67-ae66-4678-a863-1f83b9213d6f.png)![image](https://user-images.githubusercontent.com/71135790/190700277-ad88c268-e307-4685-b791-f89e0ab738aa.png)

Figure 3


## What is optical character recognition (OCR)?

It is a system used to read the texts in a photograph. This system is a system that can be used in reading the texts on the shopping receipts and converting the texts in the photos into Word files.

This system is used to read the plate in the cropped photo.

MMOCR library was used in the project. In the work of the library used here, the artificial intelligence model works in the background. This artificial intelligence model acts according to natural language processing procedures.


![image](https://user-images.githubusercontent.com/71135790/190700809-a417207e-9bab-4dc2-a6d7-8a2d328470d1.png)

Original image

![image](https://user-images.githubusercontent.com/71135790/190700949-b5e8e966-311a-45aa-a4d5-c75789d70537.png)

Image obtained as a result of segmentation

![image](https://user-images.githubusercontent.com/71135790/190701033-c5a1af16-bfdf-403a-bfcd-6c58d2bd93b1.png)

Cropped image

![image](https://user-images.githubusercontent.com/71135790/190701095-74b62ccf-2b4a-46cf-a112-549b4608b88d.png)![image](https://user-images.githubusercontent.com/71135790/190701117-712be092-4aeb-46d7-93b7-6d410afe478f.png)

Output of the characters read by the MMOCR library

Figure 4

The interface developed using PyQt5 is shown in Figure 5. Within the scope of the project, QTable and QImage functions were used.

![image](https://user-images.githubusercontent.com/71135790/190703141-e236d094-e8a9-4b97-b69a-345f05231c3c.png)

Figure 5





