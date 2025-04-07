# Importing Necessary Libraries
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import numpy as np
from keras.metrics import mean_absolute_error
from keras.models import load_model

# Loading the model with custom metric
model = load_model('Age_Sex_Detection_2.h5', custom_objects={'mae': mean_absolute_error})

# Initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Senior Citizen Identifier')
top.configure(background='#CDCDCD')

# Initializing the Labels (for Age, Gender, Senior Citizen)
label_age = Label(top, background="#CDCDCD", font=('arial', 15, "bold"))
label_gender = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
label_senior = Label(top, background="#CDCDCD", font=('arial', 15, 'bold'))
sign_image = Label(top)

# Predict Age, Gender, and determine Senior Citizen
def Detect(file_path):
    image = Image.open(file_path).convert('RGB')
    image = image.resize((48, 48))
    image = np.array(image).astype('float32') / 255.0
    image = np.expand_dims(image, axis=0)

    # Predict
    pred = model.predict(image)
    age = int(np.round(pred[1][0]))
    gender = 'Female' if pred[0][0][0] > 0.7 else 'Male'
    senior_citizen = 'Yes' if age > 60 else 'No'

    # Display
    label_age.configure(foreground="#011638", text=f"Age: {age}")
    label_gender.configure(foreground="#011638", text=f"Gender: {gender}")
    label_senior.configure(foreground="#011638", text=f"Senior Citizen: {senior_citizen}")

    print(f"Predicted Age: {age}")
    print(f"Predicted Gender: {gender}")
    print(f"Senior Citizen: {senior_citizen}")

# Show Detect Button
def show_Detect_button(file_path):
    Detect_b = Button(top, text="Detect Image", command=lambda: Detect(file_path), padx=10, pady=5)
    Detect_b.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
    Detect_b.place(relx=0.79, rely=0.46)

# Upload Image Function
def upload_image():
    try:
        file_path = filedialog.askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width() / 2.25), (top.winfo_height() / 2.25)))
        im = ImageTk.PhotoImage(uploaded)

        sign_image.configure(image=im)
        sign_image.image = im
        label_age.configure(text='')
        label_gender.configure(text='')
        label_senior.configure(text='')
        show_Detect_button(file_path)
    except Exception as e:
        print("Error:", e)

# GUI Buttons and Layout
upload = Button(top, text="Upload an Image", command=upload_image, padx=10, pady=5)
upload.configure(background="#364156", foreground='white', font=('arial', 10, 'bold'))
upload.pack(side='bottom', pady=50)

sign_image.pack(side='bottom', expand=True)
label_age.pack(side="bottom", expand=True)
label_gender.pack(side="bottom", expand=True)
label_senior.pack(side="bottom", expand=True)

heading = Label(top, text="Senior Citizen Identifier", pady=20, font=('arial', 20, "bold"))
heading.configure(background="#CDCDCD", foreground="#364156")
heading.pack()

top.mainloop()
