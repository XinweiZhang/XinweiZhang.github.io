import os
import argparse
from PIL import Image, ImageTk
import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, container):
        super().__init__(container)
        canvas = tk.Canvas(self)
        v_scrollbar = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        h_scrollbar = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)

        self.scrollable_frame = tk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")


class CaptionEditor(ScrollableFrame):
    def __init__(self, parent, image_file_chunks, grid_size, preload_images):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.image_file_chunks = image_file_chunks
        self.grid_size = grid_size
        self.current_chunk_index = 0
        self.image_labels = []
        self.caption_texts = []
        self.images = []  # Keep a list of both versions of each image
        self.preload_images = preload_images

        if self.preload_images:
            self.load_all_images(image_file_chunks)

        self.show_grid(self.image_file_chunks[self.current_chunk_index])


    def load_all_images(self, image_file_chunks):
        for chunk in image_file_chunks:
            chunk_images = []
            for image_file, caption_file in chunk:
                with Image.open(image_file) as img:
                    img.thumbnail((200, 200), Image.ANTIALIAS)
                    original_photo = ImageTk.PhotoImage(img)
                    filled_photo = original_photo

                    if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                        filled_img = img.convert("RGBA")
                        filled_img = Image.alpha_composite(Image.new("RGB", filled_img.size), filled_img)
                        filled_img.thumbnail((200, 200), Image.ANTIALIAS)
                        filled_photo = ImageTk.PhotoImage(filled_img)

                caption_text = open(caption_file).read()
                chunk_images.append((original_photo, filled_photo, caption_text))

            self.images.append(chunk_images)

    def show_grid(self, image_files):
        for widget in self.winfo_children():
            widget.destroy()

        self.image_labels = []
        self.caption_texts = []
        self.images = []

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

        self.prev_button = tk.Button(self, text="Prev", command=self.prev)
        self.next_button = tk.Button(self, text="Next", command=self.next)

        self.prev_button.grid(row=2*self.grid_size[0], column=0, sticky='ew')
        self.next_button.grid(row=2*self.grid_size[0], column=self.grid_size[1]-1, sticky='ew')

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
        index = self.caption_texts.index(text_widget)
        caption_file = self.image_file_chunks[self.current_chunk_index][index][1]  # Get the corresponding caption file
        with open(caption_file, 'w') as f:
            f.write(text_widget.get('1.0', 'end').strip())  # Write the text to the caption file

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
    parser.add_argument('--preload_images', type=bool, default=True, help='Whether to preload all images into memory. If False, images will be loaded as needed.')

    args = parser.parse_args()
    
    root = tk.Tk()
    root.title("Image Caption Editor:")
    image_extensions = (".jpg", ".png")
    image_directory = args.image_dir
    image_files = sorted([f for f in os.listdir(image_directory) if f.endswith(image_extensions)])
    image_files = [(os.path.join(image_directory, f), os.path.join(image_directory, os.path.splitext(f)[0] + args.caption_extension)) for f in image_files]

    # Split image list into chunks according to the grid size
    chunk_size = args.grid_size[0] * args.grid_size[1]
    image_file_chunks = [image_files[i:i+chunk_size] for i in range(0, len(image_files), chunk_size)]

    app = ScrollableFrame(root)
    app.pack(expand=True, fill='both')  # Using pack here

    editor = CaptionEditor(app.scrollable_frame, image_file_chunks, args.grid_size, args.preload_images)

    editor.pack(expand=True, fill='both')  # Using pack here as well

    root.mainloop()



