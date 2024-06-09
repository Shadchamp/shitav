import tkinter as tk
from tkinter import filedialog
from ebooklib import epub

def open_epub():
    file_path = filedialog.askopenfilename(filetypes=[("EPUB Files", "*.epub")])
    if file_path:
        book = epub.read_epub(file_path)
        # Get the list of items in the EPUB
        items = book.get_items()

        # Iterate over each item
        for item in items:
            # Check if the item is an HTML file
            if item.get_type() == epub.ITEM_DOCUMENT:
                # Get the HTML content
                content = item.get_content()

                # Display the HTML content in a text widget
                text_widget = tk.Text(window)
                text_widget.insert(tk.END, content)
                text_widget.pack()

            # Check if the item is an image file
            elif item.get_type() == epub.ITEM_IMAGE:
                # Get the image data
                image_data = item.get_content()

                # Create a PhotoImage object from the image data
                photo = tk.PhotoImage(data=image_data)

                # Display the image in a label widget
                image_label = tk.Label(window, image=photo)
                image_label.pack()

# Create the main window
window = tk.Tk()

# Create a button to open EPUB files
open_button = tk.Button(window, text="Open EPUB", command=open_epub)
open_button.pack()

# Run the main event loop
window.mainloop()