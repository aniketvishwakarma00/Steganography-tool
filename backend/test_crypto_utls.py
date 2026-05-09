from crypto_utils import encrypt_message, decrypt_message

message = "Hello Sir 😈"
password = "1234"

encrypted = encrypt_message(message, password)

print("Encrypted:")
print(encrypted)

decrypted = decrypt_message(encrypted, password)

print("\nDecrypted:")
print(decrypted)