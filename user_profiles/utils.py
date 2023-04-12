import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import unpad, pad
from django.http import JsonResponse
from rest_framework import status

# from mysecrets import SALT
from user_profiles.models import User
from dotenv import dotenv_values

SALT = dotenv_values(".env")['SALT']


def encrypt_email(data, key):
    key = key.encode("utf-8")
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    return base64.b64encode(encrypted_data).decode('utf-8')


def decrypt_email(email, key):
    key = key.encode("utf-8")
    encrypted_data = base64.b64decode(email)
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted_data.decode('utf-8')

    # key = key.encode("utf-8") if isinstance(key, str) else key
    # ciphertext = base64.b64decode(ciphertext)
    # iv = ciphertext[: AES.block_size]
    # ciphertext = ciphertext[AES.block_size:]
    # cipher = AES.new(key, AES.MODE_CBC, iv)
    # padded_plaintext = cipher.decrypt(ciphertext)
    # plaintext = unpad(padded_plaintext, AES.block_size).decode("utf-8")
    # return plaintext


def fetch_user_or_error(request):
    try:
        encrypted_email = (
            request.GET.get("email")
            if request.method == "GET"
            else request.data["email"]
        )
    except KeyError:
        return JsonResponse(
            {"error": "email parameter missing"}, status=status.HTTP_400_BAD_REQUEST
        )
    if not encrypted_email:
        return JsonResponse(
            {"error": "email parameter missing"}, status=status.HTTP_400_BAD_REQUEST
        )

    try:
        email = decrypt_email(encrypted_email)
    except ValueError as e:
        return JsonResponse({"error": repr(e)}, status=status.HTTP_400_BAD_REQUEST)

    try:
        return User.objects.get(pk=email)
    except User.DoesNotExist:
        error_message = {
            "error": f"User with email {email} not found"
        }  # TODO: Do not return email
        return JsonResponse(error_message, status=status.HTTP_400_BAD_REQUEST)
