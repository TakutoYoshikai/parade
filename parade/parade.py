from lina import lina
from PIL import Image
import argparse

DELIMETER = "#|#|#|#"

class DifferentSizeError(Exception):
    pass

class SizeOverError(Exception):
    pass

def write_data(data, outputpath):
    f = open(outputpath, "wb")
    f.write(data)

def capacity_of_image(image):
    width, height = image.size
    len_del = len(bytearray(DELIMETER.encode()))
    return width * height * 3 - len_del

def decode(imagepath, keypath, outputpath):
    image = Image.open(imagepath)
    key_image = Image.open(keypath)
    delimeter = DELIMETER.encode()
    delimeter = lina.message_to_binary(delimeter)
    delimeter = "".join(delimeter)
    width, height = image.size
    k_width, k_height = key_image.size
    if width * height != k_width * k_height:
        raise DifferentSizeError("size is different")
        return
    data_binary = ""
    buf = ""
    for pixel_i in range(width * height):
        row = pixel_i // width 
        col = pixel_i % width
        k_row = pixel_i // k_width
        k_col = pixel_i % k_width
        pixel = image.getpixel((col, row))
        key_pixel = key_image.getpixel((k_col, k_row))
        if image.mode == "RGBA":
            pixel = pixel[:3]
        rgb = []
        for i in range(3):
            color = pixel[i]
            k_color = key_pixel[i]
            byte = lina.message_to_binary(color)
            k_byte = lina.message_to_binary(k_color)
            for j in range(8):
                if len(buf) == len(delimeter):
                    buf = buf[1:len(delimeter)]
                if (byte[j] == "1" and k_byte[j] == "0") or (byte[j] == "0" and k_byte[j] == "1"):
                    buf += "1"
                    data_binary += "1"
                else:
                    buf += "0"
                    data_binary += "0"
            if buf == delimeter:
                image.close()
                write_data(lina.cut_bytes(lina.split(data_binary)), outputpath)
                return
    image.close()
    write_data(lina.cut_bytes(lina.split(data_binary)), outputpath)

def generate_key(imagepath, filepath, outputpath):
    f = open(filepath, "rb")
    data = f.read()
    f.close()
    delimeter = DELIMETER.encode()
    binary_content = lina.message_to_binary(data)
    binary_delimeter = lina.message_to_binary(delimeter)
    binary = "".join(binary_content) + "".join(binary_delimeter)
    image = Image.open(imagepath)
    key_image = image.copy()
    width, height = image.size
    capacity = capacity_of_image(image) * 8
    if capacity < len(binary):
        raise SizeOverError("size over")
        return
    i = 0
    for row in range(height):
        for col in range(width):
            pixel = image.getpixel((col, row))
            if image.mode == "RGBA":
                pixel = pixel[:3]
            rgb = []
            for color in pixel:
                byte = lina.message_to_binary(color)
                new_color_bits = ""
                for bit in byte:
                    if i >= len(binary):
                        new_color_bits += "0" * (8 - len(new_color_bits))
                        break
                    if (binary[i] == "0" and bit == "1") or (binary[i] == "1" and bit == "0"):
                        new_color_bits += "1"
                    else:
                        new_color_bits += "0"
                    i += 1
                new_color = int(new_color_bits, 2)
                rgb.append(new_color)
            if image.mode == "RGBA":
                key_image.putpixel((col, row), (rgb[0], rgb[1], rgb[2], 255))
            else:
                key_image.putpixel((col, row), (rgb[0], rgb[1], rgb[2]))
    key_image.save(outputpath)
    image.close()


def main():
    parser = argparse.ArgumentParser(description="parade is an encoder/decoder of data")
    parser.add_argument("mode", help="encode or decode")
    parser.add_argument("-k", "--key")
    parser.add_argument("-i", "--image")
    parser.add_argument("-o", "--output")
    parser.add_argument("-d", "--data")
    args = parser.parse_args()
    if args.mode == "encode":
        if args.image == None or args.data == None or args.output == None:
            parser.print_help()
            return
        generate_key(args.image, args.data, args.output)
    elif args.mode == "decode":
        if args.image == None or args.output == None or args.key == None:
            parser.print_help()
            return
        decode(args.image, args.key, args.output)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
