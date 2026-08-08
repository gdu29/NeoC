# -*- coding: utf-8 -*-
"""
Protocol : NeoC (Autonomous Cognitive Architecture)
Module : IDENTITY (Cryptographic Sovereignty)
"""

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

class NeoCIdentity:
    def __init__(self):
        # Génération d'une nouvelle identité souveraine
        self.private_key = ed25519.Ed25519PrivateKey.generate()
        self.public_key = self.private_key.public_key()

    def get_public_key_bytes(self):
        return self.public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw
        ).hex()

    def sign_message(self, message: str) -> bytes:
        return self.private_key.sign(message.encode('utf-8'))

    @staticmethod
    def verify_signature(public_key_hex: str, message: str, signature: bytes) -> bool:
        try:
            pub_key_bytes = bytes.fromhex(public_key_hex)
            public_key = ed25519.Ed25519PublicKey.from_public_bytes(pub_key_bytes)
            public_key.verify(signature, message.encode('utf-8'))
            return True
        except Exception:
            return False
          
