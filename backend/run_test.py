from encoder import encode_image
from decoder import decode_image

print("--- STARTING TEST ---")
# 1. Encode
encode_image("test.png", "This is a top secret payload!", "MyStrongPassword123", "encoded_output.png")

# 2. Decode
print("\n--- DECODING ---")
result = decode_image("encoded_output.png", "MyStrongPassword123")
print(f"Final Extracted Message: {result}")