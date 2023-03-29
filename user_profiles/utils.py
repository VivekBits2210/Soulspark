from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from django.http import JsonResponse
from rest_framework import status

from mysecrets import SALT
from user_profiles.models import User


def decrypt_email(ciphertext, key=SALT):
    ciphertext = ciphertext.encode('utf-8')
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = cipher.decrypt(ciphertext)
    plaintext = unpad(padded_plaintext, AES.block_size).decode('utf-8')
    return plaintext

def fetch_user_or_error(request):
    encrypted_email = request.GET.get('email')
    if not encrypted_email:
        return JsonResponse({'error': 'email parameter missing'}, status=status.HTTP_404_NOT_FOUND)

    email = decrypt_email(encrypted_email)

    try:
        return User.objects.get(pk=email)
    except User.DoesNotExist:
        error_message = {'error': f'User {encrypted_email} not found'}
        return JsonResponse(error_message, status=status.HTTP_404_NOT_FOUND)