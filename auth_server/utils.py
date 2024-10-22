import hashlib
import base64

def verify_code_verifier(code_verifier, code_challenge):
    # Calcola il code_challenge dal code_verifier usando S256
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')

    # Confronta il code_challenge calcolato con quello salvato
    return code_challenge == code_challenge

