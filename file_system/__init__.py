import os

# from Crypto.PublicKey import RSA
# from Crypto.Random import get_random_bytes
# from Crypto.Cipher import AES, PKCS1_OAEP

UPLOAD_FOLDER = "/uploads"


class FileSystem:
    uploadfolder, encryption = None, None

    def __init__(self):
        self.encryption = self.Encryption()

    def setup_file_system(self, app):
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        return app

    def save_file(self, file, extra):
        file.save(os.path.join(UPLOAD_FOLDER, extra['filename'] if ('filename' in extra) else 'file'))

    class Encryption:
        key, nonce = "", None

        def __init__(self, key="DEFAULT KEY COMES HERE"):
            self.key = key
            self.nonce = None

        def encrypt(self, text):  # FIND OUT THE KEY YOU'RE USING TO ENCRYPT THE PINS
            try:
                """
                code = 'nooneknows'
                with open('/path/to/encrypted_data.bin', 'wb') as out_file:
                    recipient_key = RSA.import_key(
                        open('/path_to_public_key/my_rsa_public.pem').read())
                    session_key = get_random_bytes(16)
                 
                    cipher_rsa = PKCS1_OAEP.new(recipient_key)
                    out_file.write(cipher_rsa.encrypt(session_key))
                 
                    cipher_aes = AES.new(session_key, AES.MODE_EAX)
                    data = b'blah blah blah Python blah blah'
                    ciphertext, tag = cipher_aes.encrypt_and_digest(data)
                 
                    out_file.write(cipher_aes.nonce)
                    out_file.write(tag)
                    out_file.write(ciphertext)
                """
                
                pass
                
                # self.cipher = AES.new(self.key, AES.MODE_EAX)
                # self.nonce = self.cipher.nonce
                # ciphertext, self.tag = self.cipher.encrypt_and_digest(text)
                # return ciphertext
            except ValueError:
                print("Key incorrect or message corrupted")
                print("Returning Ciphertext back")
            return text

        def decrypt(self, ciphertext):
            try:
                """
                code = 'nooneknows'
                with open('/path/to/encrypted_data.bin', 'rb') as fobj:
                    private_key = RSA.import_key(
                        open('/path_to_private_key/my_rsa_key.pem').read(),
                        passphrase=code)
                 
                    enc_session_key, nonce, tag, ciphertext = [ fobj.read(x) 
                                                                for x in (private_key.size_in_bytes(), 
                                                                16, 16, -1) ]
                 
                    cipher_rsa = PKCS1_OAEP.new(private_key)
                    session_key = cipher_rsa.decrypt(enc_session_key)
                 
                    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
                    data = cipher_aes.decrypt_and_verify(ciphertext, tag)
                 
                print(data)
                """
                # self.cipher = AES.new(self.key, AES.MODE_EAX, nonce=self.nonce)
                # plaintext = self.cipher.decrypt(ciphertext)
                # self.cipher.verify(self.tag)
                # print("The message is authentic:", plaintext)
                # return plaintext
            except ValueError:
                print("Key incorrect or message corrupted")
                print("Returning Ciphertext back")
            return ciphertext
