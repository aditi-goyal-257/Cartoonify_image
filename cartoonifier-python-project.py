import cv2 #cv2 module for computer vision(image processing)
import easygui #to open the filebox
import numpy as np #to represent and store image as array
import imageio #image input output

import sys
import matplotlib.pyplot as plt #plot image
import os
import tkinter as tk #gui for pyhton
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image

picture=tk.Tk()
picture.geometry('400x400')
picture.title('Cartoonify Your Picture !')
picture.configure(background='white')
label=Label(picture,background='#CDCDCA', font=('Arial',22))

def upload():
    ImagePath=easygui.fileopenbox()#opens filebox and stores path of selected image as a string
    cartoonify_image(ImagePath)


def cartoonify_image(ImagePath):
    input_image = cv2.imread(ImagePath)#read input image from the path
    input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)#image stored in numbers


    # check if image is chosen
    if input_image is None:
        print("Please select appropriate file")
        exit()

    Output_1 = cv2.resize(input_image, (960, 540))
   


    #converting an image to grayscale
    grayScaleImage= cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    Output_2 = cv2.resize(grayScaleImage, (960, 540))
    


    #applying median blur to smoothen an image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 5)
    Output_3 = cv2.resize(smoothGrayScale, (960, 540))
    

    #get the edges for cartoon effect 
    edge = cv2.adaptiveThreshold(smoothGrayScale, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 3)
    Output_4 = cv2.resize(edge, (960, 540))
    

    #bilateral filter to remove noise and keep edges sharp
    colorImage = cv2.bilateralFilter(input_image, 9, 300, 300)
    Output_5 = cv2.resize(colorImage, (960, 540))


    #masking edged image with our "BEAUTIFY" image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=edge)

    Output_6 = cv2.resize(cartoonImage, (960, 540))
   

    # Plotting images at different stages
    images=[Output_1, Output_2, Output_3, Output_4, Output_5, Output_6]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')

    save1=Button(top,text="Save cartoon image",command=lambda: save(Output_6, ImagePath),padx=30,pady=5)
    save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
    save1.pack(side=TOP,pady=50)
    
    plt.show()
    
    
def save(Output_6, ImagePath):
    #saving an image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(Output_6, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)

upload=Button(picture,text="Cartoonify an Image",command=upload,padx=10,pady=5)
upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

picture.mainloop()



