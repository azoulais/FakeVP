import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk


def open_image():
    def open():
        file_path = filedialog.askopenfilename()
        if file_path:
            image = Image.open(file_path)
            photo = ImageTk.PhotoImage(image)
            label.config(image=photo)
            label.image = image
            root.destroy()


    # Create the main window
    root = tk.Tk()
    root.title("Image Uploader")

    # Create a label to display the uploaded image
    label = tk.Label(root)
    label.pack(padx=10, pady=10)

    # Create a button to open the file dialog
    button = tk.Button(root, text="Upload Image", command=open)
    button.pack(pady=10)

    # Run the application
    root.mainloop()
    return label.image