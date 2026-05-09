from PIL import Image
from crypto_utils import decrypt_message

def decode_image(encoded_image_path, password):
    try:
        img = Image.open(encoded_image_path).convert('RGB')
    except Exception as e:
        print(f"[ERROR] Failed to open image: {e}")
        return "Error opening image."

    pixels = img.load()
    binary_data = ""
    extracted_text = ""

    print(f"[DEBUG - DECODER] Scanning {encoded_image_path} for hidden data...")

    # 1. Pixel Traversal and Bit Extraction
    for y in range(img.height):
        for x in range(img.width):
            r, g, b = pixels[x, y]

            # Extract the LSB from each channel using bitwise AND
            binary_data += str(r & 1)
            binary_data += str(g & 1)
            binary_data += str(b & 1)

    print(f"[DEBUG - DECODER] Extracted {len(binary_data)} total bits. Slicing into bytes...")

    # 2. Reconstruct characters and check for delimiter
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        if len(byte) == 8:
            extracted_char = chr(int(byte, 2))
            extracted_text += extracted_char

            # Check if the last 5 characters match our delimiter
            if extracted_text[-5:] == "#####":
                print(f"[SUCCESS] Delimiter found! Stopping extraction.")
                
                # We extracted the Base64 ciphertext. Strip the delimiter.
                extracted_b64 = extracted_text[:-5]
                
                # Decrypt it using your crypto_utils
                try:
                    decrypted_message = decrypt_message(extracted_b64, password)
                    return decrypted_message
                except Exception as e:
                    return f"[ERROR] Decryption failed! Wrong password or corrupted data. Details: {e}"

    # 3. Fallback / Failure analysis
    print("[DEBUG - DECODER] Delimiter '#####' was NEVER found.")
    return "No hidden message found."