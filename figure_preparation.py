from PIL import Image


def concatenate_images_horizontally(image_path1, image_path2, output_path):
    # Open the images
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Ensure the images have the same height
    if img1.height != img2.height:
        raise ValueError("Images don't have the same height")

    # Create a new image with the combined width and the same height as the original images
    total_width = img1.width + img2.width
    new_image = Image.new('RGB', (total_width, img1.height))

    # Paste the images into the new image
    new_image.paste(img1, (0, 0))  # Paste img1 at the left edge
    new_image.paste(img2, (img1.width, 0))  # Paste img2 immediately to the right of img1

    # Save the new image
    new_image.save(output_path)


def concatenate_images_vertically(image_path1, image_path2, output_path):
    # Open the images
    img1 = Image.open(image_path1)
    img2 = Image.open(image_path2)

    # Ensure the images have the same width
    if img1.width != img2.width:
        raise ValueError("Images don't have the same width")

    # Create a new image with the same width and combined height of the original images
    total_height = img1.height + img2.height
    new_image = Image.new('RGB', (img1.width, total_height))

    # Paste the images into the new image
    new_image.paste(img1, (0, 0))  # Paste img1 at the top
    new_image.paste(img2, (0, img1.height))  # Paste img2 immediately below img1

    # Save the new image
    new_image.save(output_path)

if __name__ == "__main__":
    # Example usage
    figure_path = './results/'
    common_prefix = 'recall-'
    #common_prefix = 'performance-'
    problem_type = 'uf10'
    image_path1 = figure_path + common_prefix + problem_type + '-gpt3.5.png'
    image_path2 = figure_path + common_prefix + problem_type + '-gpt4.png'
    output_path = figure_path + common_prefix + problem_type + '-gpts.png'
    #concatenate_images_vertically(image_path1, image_path2, output_path)
    concatenate_images_horizontally(image_path1, image_path2, output_path)