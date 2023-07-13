import os
import random

# Define the folder path where the images are located
folder_path = "./"

# Get the list of image files in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(".jpg")]

# Generate a .caption file for each image
for image_file in image_files:
    # Generate a random caption
    random_caption = " ".join([
            random.choice(["word1", "hhh", "wjisdjw", "emndien", "word2", "word3"])
            for _ in range(5)
        ]
    )  # Modify the word choices as per your requirement

    # Create the .caption file name by replacing the file extension
    caption_file = os.path.splitext(image_file)[0] + ".caption"

    # Create the full path for the .caption file
    caption_path = os.path.join(folder_path, caption_file)

    # Write the random caption to the .caption file
    with open(caption_path, "w", encoding="utf-8") as file:
        file.write(random_caption)

    print(f"Generated caption file: {caption_path}")
