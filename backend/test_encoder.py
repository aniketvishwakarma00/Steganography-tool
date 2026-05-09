from encoder import encode_image

image_path = "test.png"
output_path = "encoded.png"

secret_message = "HELLO SIR 😈"

encode_image(
    image_path,
    secret_message,
    output_path
)

print("Message hidden successfully!")