from PIL import Image


def change_image_size(image_path, output_path, new_width, new_height):
    image = Image.open(image_path)
    height_percent = new_height / image.size[1]
    width = int(image.size[0] * height_percent)

    new_image = image.resize((width, new_height))

    if width > new_width:
        left_and_right_difference = (width - new_width) // 2
        new_image = new_image.crop((left_and_right_difference, 0, width - left_and_right_difference, new_height))
    elif width < new_width:
        pixel_values = image.load()
        pixels_count = width * new_height

        total_red = total_green = total_blue = 0

        for i in range(width):
            for j in range(new_height):
                total_red += pixel_values[i, j][0]
                total_green += pixel_values[i, j][1]
                total_blue += pixel_values[i, j][2]

        avg_red = total_red // pixels_count
        avg_green = total_green // pixels_count
        avg_blue = total_blue // pixels_count
        average_color = (avg_red, avg_green, avg_blue)
        background_image = Image.new('RGB', (new_width, new_height), average_color)
        left_and_right_difference = (background_image.width - width) // 2

        background_image.paste(new_image, (left_and_right_difference, 0,
                                           new_image.width + left_and_right_difference,
                                           background_image.height))
        new_image = background_image

    new_image.save(output_path, "PNG")


for i in range(1, 10):
    change_image_size(f"../static/images/{i}.png", f"../static/images/{i}.png", 150, 215)
