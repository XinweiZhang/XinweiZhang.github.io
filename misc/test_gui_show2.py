import os
import argparse
from PIL import Image, ImageTk
import tkinter as tk


class CaptionEditor(tk.Frame):
    def __init__(self, parent, image_file_chunks, grid_size):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.image_file_chunks = image_file_chunks
        self.grid_size = grid_size
        self.current_chunk_index = 0
        self.image_labels = []
        self.caption_texts = []
        self.images = []  # Keep a list of both versions of each image

        self.prev_button = tk.Button(self, text="<< Prev", command=self.prev)
        self.next_button = tk.Button(self, text="Next >>", command=self.next)

        self.show_grid(self.image_file_chunks[self.current_chunk_index])

        self.pack()

    def show_grid(self, image_files):
        for widget in self.winfo_children():
            widget.destroy()

        self.image_labels = []
        self.caption_texts = []
        self.images = []

        self.prev_button = tk.Button(self, text="Prev", command=self.prev)
        self.next_button = tk.Button(self, text="Next", command=self.next)

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid_size[1]*i+j < len(image_files):
                    image_file, caption_file = image_files[self.grid_size[1]*i+j]
                    with Image.open(image_file) as img:
                        img.thumbnail((200, 200), Image.ANTIALIAS)
                        original_photo = ImageTk.PhotoImage(img)
                        filled_photo = original_photo
                        
                        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                            filled_img = img.convert("RGBA")
                            filled_img = Image.alpha_composite(Image.new("RGB", filled_img.size), filled_img)
                            filled_img.thumbnail((200, 200), Image.ANTIALIAS)
                            filled_photo = ImageTk.PhotoImage(filled_img)

                    label = tk.Label(self, image=original_photo)
                    label.image = original_photo  # Keep a reference to the image object to prevent garbage collection
                    label.grid(row=2*i, column=j)
                    label.bind('<Double-1>', lambda e, l=label, o=original_photo, f=filled_photo: self.switch_image(l, o, f))  # Bind a double-click to the switch_image method

                    text = tk.Text(self, height=4, width=30)
                    text.insert('1.0', open(caption_file).read())
                    text.config(state='disabled')  # Make it read-only by default
                    text.bind('<Double-1>', self.enable_editing)  # Bind a double-click to the enable_editing method
                    text.grid(row=2*i+1, column=j)

                    self.image_labels.append(label)
                    self.caption_texts.append(text)
                    self.images.append([original_photo, filled_photo])

        self.prev_button.grid(row=2*self.grid_size[0], column=0, columnspan=self.grid_size[1], sticky='w')
        self.next_button.grid(row=2*self.grid_size[0], column=0, columnspan=self.grid_size[1], sticky='e')


    def switch_image(self, label, original_photo, filled_photo):
        if label.image == original_photo:
            label.configure(image=filled_photo)
            label.image = filled_photo
        else:
            label.configure(image=original_photo)
            label.image = original_photo

    def enable_editing(self, event):
        text_widget = event.widget
        text_widget.config(state='normal')  # Make it editable
        text_widget.bind('<Return>', self.disable_editing)  # Bind the Return key to the disable_editing method
        text_widget.bind('<Shift-Return>', lambda event: text_widget.insert(tk.INSERT, '\n'))  # Add a newline character

    def disable_editing(self, event):
        text_widget = event.widget
        text_widget.config(state='disabled')  # Make it read-only again
        # Here, you could add code to save the changes to the caption file

    def next(self):
        if self.current_chunk_index < len(self.image_file_chunks) - 1:
            self.current_chunk_index += 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])

    def prev(self):
        if self.current_chunk_index > 0:
            self.current_chunk_index -= 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Image and Caption Viewer.')
    parser.add_argument('--image_dir', type=str, default='./', help='The directory where images and caption files are stored.')
    parser.add_argument('--grid_size', type=int, nargs=2, default=[4, 5], help='The size of the grid to display images (rows cols).')
    parser.add_argument('--caption_extension', type=str, default=".caption", help='Extension of caption files.')

    args = parser.parse_args()

    root = tk.Tk()
    root.title("Image Caption Editor:")
    image_extension = (".jpg", ".png")
    image_directory = args.image_dir
    image_files = sorted([f for f in os.listdir(image_directory) if f.endswith(image_extensions)])
    image_files = [(os.path.join(image_directory, f), os.path.join(image_directory, os.path.splitext(f)[0] + args.caption_extension)) for f in image_files]

    # Split image list into chunks according to the grid size
    chunk_size = args.grid_size[0] * args.grid_size[1]
    image_file_chunks = [image_files[i:i+chunk_size] for i in range(0, len(image_files), chunk_size)]

    app = CaptionEditor(root, image_file_chunks, args.grid_size)
    root.mainloop()
