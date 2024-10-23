import hashlib
import base64

def verify_code_verifier(code_verifier, code_challenge):
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_challenge == code_challenge

