from PIL import Image
from crypto_utils import encrypt_message

def text_to_binary(text):
    """Converts a string to a continuous stream of 8-bit binary."""
    return ''.join(format(ord(char), '08b') for char in text)

def encode_image(input_image_path, secret_data, password, output_image_path):
    # 1. Encrypt the data first using your crypto_utils
    encrypted_b64 = encrypt_message(secret_data, password)
    
    # 2. Append the delimiter to the ENCRYPTED string
    encrypted_b64 += "#####"
    
    # 3. Convert to binary
    binary_data = text_to_binary(encrypted_b64)
    data_length = len(binary_data)
    data_index = 0

    print(f"[DEBUG - ENCODER] Total bits to hide: {data_length}")

    # 4. Open image and ensure it's in RGB mode
    try:
        img = Image.open(input_image_path).convert('RGB')
    except Exception as e:
        print(f"[ERROR] Failed to open image: {e}")
        return False

    # Check if image has enough pixels to hold the data
    if data_length > img.width * img.height * 3:
        print("[ERROR] Image is too small to hold this much data.")
        return False

    pixels = img.load()

    # 5. Pixel Traversal and Bit Modification
    for y in range(img.height):
        for x in range(img.width):
            if data_index < data_length:
                r, g, b = pixels[x, y]

                # Modify Red channel
                if data_index < data_length:
                    r = (r & ~1) | int(binary_data[data_index]) 
                    data_index += 1
                
                # Modify Green channel
                if data_index < data_length:
                    g = (g & ~1) | int(binary_data[data_index])
                    data_index += 1
                
                # Modify Blue channel
                if data_index < data_length:
                    b = (b & ~1) | int(binary_data[data_index])
                    data_index += 1

                # Write modified pixel back to the image
                pixels[x, y] = (r, g, b)
            else:
                break
        if data_index >= data_length:
            break

    # 6. Save as PNG (CRITICAL: Lossless format)
    img.save(output_image_path, "PNG")
    print(f"[SUCCESS] Data encoded and saved to {output_image_path}")
    return True