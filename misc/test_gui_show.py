import os
import sys
import argparse
from PIL import Image, ImageTk
import tkinter as tk
import numpy as np

class CaptionEditor(tk.Frame):
    def __init__(self, parent, image_file_chunks, num_rows=4, num_cols=5):
        tk.Frame.__init__(self, parent)
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.image_file_chunks = image_file_chunks
        self.current_chunk_index = 0

        # Create the buttons
        self.next_button = tk.Button(self, text="Next", command=self.next_chunk)
        self.previous_button = tk.Button(self, text="Previous", command=self.previous_chunk)

        # Show the first chunk of images
        self.show_grid(self.image_file_chunks[self.current_chunk_index])

        self.pack()

    def show_grid(self, image_files):
        # Clear the old widgets
        for widget in self.grid_slaves():
            widget.grid_forget()

        self.image_labels = []
        self.caption_texts = []

        # Create new labels and text widgets
        for i in range(self.num_rows):
            for j in range(self.num_cols):
                if self.num_cols*i+j < len(image_files):
                    image_file, caption_file = image_files[self.num_cols*i+j]
                    with Image.open(image_file) as img:
                        img.thumbnail((200, 200), Image.ANTIALIAS)
                        photo = ImageTk.PhotoImage(img)

                    label = tk.Label(self, image=photo)
                    label.image = photo  # Keep a reference to the image object to prevent garbage collection
                    label.grid(row=2*i, column=j)

                    text = tk.Text(self, height=4, width=30)
                    with open(caption_file, 'r') as f:
                        text.insert('1.0', f.read())
                    text.config(state='disabled')  # Make it read-only by default
                    text.bind('<Double-1>', self.enable_editing)  # Bind a double-click to the enable_editing method
                    text.bind('<Return>', self.disable_editing)  # Bind the Return key to the disable_editing method
                    text.bind('<Shift-Return>', lambda event: text.insert(tk.END, '\n')) # Bind Shift-Return to insert newline
                    text.grid(row=2*i+1, column=j)

                    self.image_labels.append(label)
                    self.caption_texts.append(text)

        # Position the buttons
        self.next_button.grid(row=2*self.num_rows, column=self.num_cols-1)
        self.previous_button.grid(row=2*self.num_rows, column=0)

    def next_chunk(self):
        if self.current_chunk_index < len(self.image_file_chunks) - 1:
            self.current_chunk_index += 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])

    def previous_chunk(self):
        if self.current_chunk_index > 0:
            self.current_chunk_index -= 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])

    def enable_editing(self, event):
        text_widget = event.widget
        text_widget.config(state='normal')  # Make it editable

    def disable_editing(self, event):
        text_widget = event.widget
        text_widget.config(state='disabled')  # Make it read-only again
        # Here, you could add code to save the changes to the caption file
        idx, caption_file = next((i, cf) for i, (_, cf) in enumerate(self.image_file_chunks[self.current_chunk_index]) if self.caption_texts[i] == text_widget)
        with open(caption_file, 'w') as f:
            f.write(text_widget.get('1.0', tk.END).strip())  # Write the current text to the caption file


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Image Caption Editor")

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_rows", type=int, default=4, help="Number of rows in the grid")
    parser.add_argument("--num_cols", type=int, default=5, help="Number of columns in the grid")
    parser.add_argument("--image_directory", type=str, default="./", help="Directory where the images are located")
    args = parser.parse_args()

    image_directory = args.image_directory
    caption_directory = image_directory
    
    image_files = sorted([f for f in os.listdir(image_directory) if f.endswith('.jpg')])
    
    image_files = [(os.path.join(image_directory, f), os.path.join(caption_directory, os.path.splitext(f)[0] + '.caption')) for f in image_files]
    
    num_images_per_chunk = args.num_rows * args.num_cols
    image_file_chunks = [image_files[i:i + num_images_per_chunk] for i in range(0, len(image_files), num_images_per_chunk)]
    
    app = CaptionEditor(root, image_file_chunks, args.num_rows, args.num_cols)
    root.mainloop()