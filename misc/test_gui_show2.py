import os
import argparse
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

class ScrollableFrame(tk.Frame):
    def __init__(self, container, **kwargs):
        super().__init__(container, **kwargs)

        canvas = tk.Canvas(self, highlightthickness=0)
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

        canvas.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        
class ImageLabel(tk.Label):
    def __init__(self, master=None, image_file=None, caption_file=None, **kw):
        super().__init__(master, **kw)
        self.image_file = image_file
        self.caption_file = caption_file
        self.bind("<Button-1>", self.handle_click)

    def handle_click(self, event):
        if self.master.current_selected is not None:
            self.master.current_selected.configure(relief="flat")  # Remove border from the previously selected image
        self.configure(relief="solid", bd=2)  # Add border to the newly selected image
        self.master.current_selected = self
     #  self.master.master.focus_set()  # Set focus back to the root window

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
        self.current_selected = None
        self.bind("<Delete>", self.handle_delete)
        self.bind("<BackSpace>", self.handle_delete)
        self.focus_set()
     
        if self.preload_images:
            self.load_all_images(image_file_chunks)

        self.show_grid(self.image_file_chunks[self.current_chunk_index])

    def load_image(self, image_file, caption_file):
        with Image.open(image_file) as img:
            img.thumbnail((200, 200), Image.Resampling.LANCZOS)
            original_photo = ImageTk.PhotoImage(img)
            filled_photo = original_photo

            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                filled_img = img.convert("RGBA")
                base = Image.new("RGBA", filled_img.size, (255, 255, 255, 255))
                filled_img = Image.alpha_composite(base, filled_img)
                filled_img.thumbnail((200, 200), Image.Resampling.LANCZOS)
                filled_photo = ImageTk.PhotoImage(filled_img)

        caption_text = open(caption_file).read()
        return original_photo, filled_photo, caption_text

    def load_all_images(self, image_file_chunks):
        for chunk in image_file_chunks:
            chunk_images = [self.load_image(image_file, caption_file) for image_file, caption_file in chunk]
            self.images.append(chunk_images)

    def handle_delete(self, event):
        if isinstance(self.focus_get(), tk.Text):  # Add this line to ignore <Delete> when a text widget has focus
            return
        
        label = self.current_selected
        if label and messagebox.askokcancel("Delete", "Do you want to delete this image and its caption?"):
            # Remove the image file and the caption file
            os.remove(label.image_file)
            os.remove(label.caption_file)
            # Find and destroy the associated caption text field and remove it from the CaptionEditor's list
            associated_caption = self.associated_captions[label]
            self.associated_captions.pop(label)
            self.caption_texts.remove(associated_caption)
            associated_caption.destroy()
            # Remove the image from the CaptionEditor's list
            self.image_labels.remove(label)
            # Remove the image and the caption from the UI
            label.destroy()

            # Remove the image from the chunk and preloaded list
            removed_index = self.image_file_chunks[self.current_chunk_index].index((label.image_file, label.caption_file))
            self.image_file_chunks[self.current_chunk_index].remove((label.image_file, label.caption_file))
            self.images[self.current_chunk_index].pop(removed_index)

            # Reset the currently selected image
            self.current_selected = None
        self.focus_set()  # Set focus back to CaptionEditor


    def show_grid(self, image_files):
        for widget in self.winfo_children():
            widget.destroy()

        self.current_selected = None  # Reset the currently selected image

        self.image_labels = []
        self.caption_texts = []
        self.associated_captions = {}  # New dictionary to hold associated captions

        for i in range(self.grid_size[0]):
            for j in range(self.grid_size[1]):
                if self.grid_size[1]*i+j < len(image_files):
                    image_file, caption_file = image_files[self.grid_size[1]*i+j]

                    # Check whether images are preloaded
                    if self.preload_images:
                        original_photo, filled_photo, caption_text = self.images[self.current_chunk_index][self.grid_size[1]*i+j]
                    else:
                        original_photo, filled_photo, caption_text = self.load_image(image_file, caption_file)

                    label = ImageLabel(self, image=original_photo, image_file=image_file, caption_file=caption_file)
                    label.image = original_photo  # Keep a reference to the image object to prevent garbage collection
                    label.grid(row=2*i, column=j)
                    label.bind('<Double-1>', lambda e, l=label, o=original_photo, f=filled_photo: self.switch_image(l, o, f))  # Bind a double-click to the switch_image method

                    text = tk.Text(self, height=4, width=30)
                    text.insert('1.0', caption_text)
                    text.config(state='disabled')  # Make it read-only by default
                    text.bind('<Double-1>', self.enable_editing)  # Bind a double-click to the enable_editing method
                    text.grid(row=2*i+1, column=j)

                    self.image_labels.append(label)
                    self.caption_texts.append(text)
                    self.associated_captions[label] = text  # Store the associated caption

        self.prev_button = tk.Button(self, text="Prev", command=self.prev)
        self.next_button = tk.Button(self, text="Next", command=self.next)

        self.prev_button.grid(row=2*self.grid_size[0], column=0, sticky='ew')
        self.next_button.grid(row=2*self.grid_size[0], column=self.grid_size[1]-1, sticky='ew')
        # Bind the <ButtonRelease> event to the prev and next buttons
        self.prev_button.bind("<ButtonRelease>", lambda e: self.parent.focus_set())
        self.next_button.bind("<ButtonRelease>", lambda e: self.parent.focus_set())

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
        text_widget.focus_set()  # Set focus to the text box

    def disable_editing(self, event):
        text_widget = event.widget
        text_widget.config(state='disabled')  # Remove the highlight after editing
        index = self.caption_texts.index(text_widget)
        caption_file = self.image_file_chunks[self.current_chunk_index][index][1]  # Get the corresponding caption file
        with open(caption_file, 'w') as f:
            f.write(text_widget.get('1.0', 'end').strip())  # Write the text to the caption file
        self.focus_set()

    def next(self):
        if self.current_chunk_index < len(self.image_file_chunks) - 1:
            self.current_chunk_index += 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])
        self.parent.focus_set()

    def prev(self):
        if self.current_chunk_index > 0:
            self.current_chunk_index -= 1
            self.show_grid(self.image_file_chunks[self.current_chunk_index])
        self.parent.focus_set()

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
    root.focus_set()  # Set initial focus to root window

    root.mainloop()