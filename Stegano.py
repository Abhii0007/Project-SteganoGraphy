import sys
import ctypes
import os,time
import time,os,requests

from PIL import Image
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QLabel, QLineEdit, QTextEdit



#start--------------------------This code first crop the image then save to png image------------------------------\
def resize_image(input_path, output_path, target_size=(140, 140)):
    try:
        # Open the image file
        with Image.open(input_path) as img:
            # Resize the image to the target size
            resized_img = img.resize(target_size)
            # Save the resized image
            resized_img.save(output_path)
            print(f"Image resized and saved to {output_path}")
    except Exception as e:
        print(f"Error: {e}")
#end---------------------------------------------------------------------------------------------------------------/





#start----------------This code uses general encryption method to use for encrypt the given password to access the program-------------------\

print(" "*20+"WELCOME TO THE PROJECT LSB STEGANOGRAPHY\n\n")





ctypes.windll.kernel32.GetConsoleWindow()   #This code call the win API to access the OS features and internal functions
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)    #this code hide the program command window

#start to encode the message in image, we provide message, image path, and output path, to encode and save a new image with name encoded_image.png----------\
def encode_message(message, image_path, output_path):
    # Open the image
    img = Image.open(image_path)
    # Convert the message to binary
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    # Get the image size
    img_width, img_height = img.size
    # Embed the binary message into the image
    index = 0
    for i in range(img_width):
        for j in range(img_height):
            pixel = list(img.getpixel((i, j)))
            for color_channel in range(3):  # Iterate over RGB channels
                if index < len(binary_message):
                    pixel[color_channel] = int(format(pixel[color_channel], '08b')[:-1] + binary_message[index], 2)
                    index += 1
    
            img.putpixel((i, j), tuple(pixel))

    # Save the encoded image
    img.save(output_path)
#end---------------------------------------------------------------------------------------------------------------------------------------------------------/


#start-------------------------------This code first decode the message and print decoded message in text box--------------------------------------------------\
def decode_message(image_path):
    # Open the encoded image
    img = Image.open(image_path)
    
    binary_message = ''

    # Extract the binary message from the image
    for i in range(img.width):
        for j in range(img.height):
            pixel = img.getpixel((i, j))
            for color_channel in range(3):
                binary_message += format(pixel[color_channel], '08b')[-1]

    # Convert binary message to text
    decoded_message = ''.join([chr(int(binary_message[i:i+8], 2)) for i in range(0, len(binary_message), 8)])
    
    return decoded_message

#end-----------------------------------------------------------------------------------------------------------------------------------------------------------/

#start--This is a class in which Qwidget class inherited, and when we create a object, its initialize all the elements and run codes of initUI() function to add GUI-\
class FileDialogExample(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):
        global search_bar,text_edit,btn2   #this variables are global so that any function can use its properties

        icon = QIcon("pic1.ico")  # this code add a icon to the program
        self.setWindowIcon(icon)
        #this bunch of code set size of main window and set background for frontend
        self.setFixedSize(700, 438)
        background_image = QLabel(self)
        pixmap = QPixmap('banner3.jpg')  # Replace with the path to your image
        background_image.setPixmap(pixmap)
        background_image.resize(self.size())
        background_image.setScaledContents(True)
        self.setWindowTitle('Steganography Program')
        self.setWindowOpacity(0.9)
        

        #his bunch of code add a text label inside top of window
        self.label = QLabel('Welcome To the LSB Steganography Program V1.1', self)
        font = QFont()
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setStyleSheet('color: white')
        self.label.setGeometry(60, 6, 600, 40)

        # this code also add a text lable inside top of window
        self.label1 = QLabel('Tip: 1st Type the message in searchbar then press on Encode image', self)
        font1 = QFont()
        font1.setPointSize(10)
        self.label1.setFont(font1)
        self.label1.setStyleSheet('color: white') 
        self.label1.setGeometry(60, 28, 600, 60)
        
    

        #this bunch of code add a search bar gui inside window
        search_bar = QLineEdit(self)
        search_bar.setPlaceholderText('Enter your Message here before Encode...')
        search_bar.setGeometry(10, 95, 680, 30)

        
        # This type of bunch of code add a button in window, and when clicked, it connect and run the funtion 
        self.btn = QPushButton('Encode Image', self)
        self.btn.clicked.connect(self.changeLabelText) # it means when pressed it run the changelabelText function
        self.btn.setFixedSize(120, 35)
        self.btn.move(185, 395)
        font3 = QFont()
        font3.setPointSize(10)  # Adjust the font size as needed
        self.btn.setFont(font3)
        self.btn.setCursor(Qt.PointingHandCursor)
        self.show()

        self.btn1 = QPushButton('Decode Image', self)
        self.btn1.clicked.connect(self.showDialog1)
        self.btn1.setFixedSize(120, 35)
        self.btn1.move(333, 395)
        self.btn1.setFont(font3)
        self.btn1.setCursor(Qt.PointingHandCursor)
        self.btn1.show()

        btn2 = QPushButton('Save Image to Telegram', self)
        btn2.clicked.connect(self.Image_save_to_telegram)
        btn2.setFixedSize(200, 35)
        btn2.move(480, 395)
        btn2.setFont(font3)

        #self.btn2.setStyleSheet('background-color: black; color: lightgreen;')
        btn2.setStyleSheet('background-color: white; color: black; border: 3px solid darkblue')
        btn2.setCursor(Qt.PointingHandCursor)
        btn2.show()

        # Create a QVBoxLayout
        layout = QVBoxLayout()
        # This type of bunch of code add a text box like notepad inside window
        text_edit = QTextEdit(self)
        text_edit.setGeometry(185, 152, 500, 180)
        text_edit.setText("Press Decode image button to show Hidden Encoded Message.")
        font4 = QFont()
        font4.setPointSize(13)
        text_edit.setFont(font4)
        text_edit.setStyleSheet("background-color: black; color: lightblue;")
        text_edit.show()

    #start, this code uploads and save the selected image to the private telegram channel server, using telegram BOTFATHER Api-------------------------\
    def Image_save_to_telegram(self):
        btn2.setStyleSheet('background-color: black; color: white; border: 3px solid darkblue')
        tmp =  'Bot api not found!\nhere you can use teleragm api to save the image to telegram bot channel using botfather api'
        print(tmp)
  


            
    #start, this function executes after decode button pressed-------------------------------------------------\
    def showDialog1(self):
        global picture_label
        #search_bar.hide()

        current_dir = os.getcwd()
        fname1 = QFileDialog.getOpenFileName(self, 'Select PNG image for Decoding', current_dir)

        if fname1[0]:
            print(f'Selected file: {fname1[0]}')
            locator2 = fname1[0]

            encoded_image_path = locator2
            # Decode the message from the image
            decoded_message = decode_message(encoded_image_path)
            header2 = ''

            for abhi in decoded_message:
                if abhi.isdigit():
                    header2 = header2 + abhi
                else:
                    break

            secret = decoded_message[len(header2):int(header2)+2]

            picture_label = QLabel(self)
            picture_label.setGeometry(8, 144, 162, 195)  # Set position to (10, 10) and size to 120x120 pixels
            # Load an image (replace 'path/to/your/image.png' with the actual path)
            image_path = fname1[0]
            pixmap = QPixmap(image_path)
            picture_label.setPixmap(pixmap)
            picture_label.setScaledContents(True)
            picture_label.setStyleSheet('background-color: red; border: 4px solid black;')
            picture_label.show()

            self.label1.setText("Decoded Message of Selected image is in Textbox")
            text_edit.setText(f'Secret Message = {secret}')

        btn2.setStyleSheet('background-color: white; color: black; border: 3px solid darkblue')
        btn2.setText("Save Image to Telegram")
    #end----------------------------------------------------------------------------------------------------------------------/



    
        
    #start, This function executes when encode button is pressed-----------------------------------------------------------\
    def changeLabelText(self):
        current_dir1 = os.getcwd()
        text = search_bar.text()
        self.label1.setText(f'Select the png image to encode with')
        text_edit.setText(f'Secret Message To Encode: {text}')
        fname = QFileDialog.getOpenFileName(self, 'Select PNG image for Encoding', current_dir1)


        if fname[0]:
            
            input_image_path = fname[0]
            output_image_path = "resized_image.png"

            # Call the resize_image function
            resize_image(input_image_path, output_image_path)
            

            picture_label3 = QLabel(self)
            picture_label3.setGeometry(8, 144, 162, 195)  # Set position to (10, 10) and size to 120x120 pixels
            image_path3 = fname[0]
            pixmap3 = QPixmap(image_path3)
            picture_label3.setPixmap(pixmap3)
            picture_label3.setScaledContents(True)
            picture_label3.setStyleSheet('background-color: red; border: 4px solid black;')
            picture_label3.show()


            print(f'Selected file: {fname[0]}')
            locator1 = output_image_path
            user_input = str(len(text)) + text
            encoded_image_path = "encoded_image.png"
            encode_message(user_input, locator1, encoded_image_path)
            self.label1.setText('Message Successfully Encoded.')
            text_edit.setText('Message Successfully Encoded to this image\n\nEncoded File name = encoded_image.png')
            print("Message Successfully Encoded.")
            os.remove(locator1)


        btn2.setStyleSheet('background-color: white; color: black; border: 3px solid darkblue')
        btn2.setText("Save Image to Telegram")
    #end-------------------------------------------------------------------------------------------------------------------------------------/

if __name__ == '__main__':  
    app = QApplication(sys.argv)
    ex = FileDialogExample() 
    sys.exit(app.exec()) 
        
        
        




            

                

            




           
   

                

            


                






