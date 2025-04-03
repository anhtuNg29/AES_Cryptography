#!/usr/bin/env python3
# AES-128 Encryption/Decryption Implementation
# Testing and debugging file

from aes_core import encrypt, decrypt
from aes_utils import bytes_to_hex

def run_test_vectors():
    """
    Run some standard test vectors for AES-128 to verify implementation.
    """
    print("Running AES-128 test vectors...")
    
    test_vectors = [
        # (key, plaintext, expected_ciphertext)
        (
            bytes.fromhex("000102030405060708090a0b0c0d0e0f"), 
            bytes.fromhex("00112233445566778899aabbccddeeff"), 
            bytes.fromhex("69c4e0d86a7b0430d8cdb78070b4c55a")
        ),
        (
            bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c"), 
            bytes.fromhex("6bc1bee22e409f96e93d7e117393172a"), 
            bytes.fromhex("3ad77bb40d7a3660a89ecaf32466ef97")
        ),
        # Add more test vectors as needed
    ]
    
    for i, (key, plaintext, expected_ciphertext) in enumerate(test_vectors):
        print(f"\nTest Vector {i+1}:")
        print(f"Key:       {bytes_to_hex(key)}")
        print(f"Plaintext: {bytes_to_hex(plaintext)}")
        
        # Test encryption
        ciphertext = encrypt(plaintext, key)
        print(f"Ciphertext (calculated): {bytes_to_hex(ciphertext)}")
        print(f"Ciphertext (expected):   {bytes_to_hex(expected_ciphertext)}")
        print(f"Encryption {'PASSED' if ciphertext == expected_ciphertext else 'FAILED'}")
        
        # Test decryption
        decrypted = decrypt(ciphertext, key)
        print(f"Decrypted: {bytes_to_hex(decrypted)}")
        print(f"Decryption {'PASSED' if decrypted == plaintext else 'FAILED'}")

def test_round_trip():
    """
    Test encryption followed by decryption to verify correctness.
    """
    print("\nTesting round-trip encryption/decryption...")
    
    # Test with various inputs
    test_cases = [
        (b"This is a test.", bytes.fromhex("000102030405060708090a0b0c0d0e0f")),
        (b"AES-128 Algorithm", bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")),
        # Add more test cases as needed
    ]
    
    for i, (plaintext, key) in enumerate(test_cases):
        print(f"\nTest Case {i+1}:")
        print(f"Original: {plaintext}")
        
        # Pad plaintext if needed
        if len(plaintext) % 16 != 0:
            padding_length = 16 - (len(plaintext) % 16)
            padded_plaintext = plaintext + bytes([padding_length]) * padding_length
        else:
            padded_plaintext = plaintext
        
        print(f"Padded:   {bytes_to_hex(padded_plaintext)}")
        
        # Encrypt
        ciphertext = encrypt(padded_plaintext, key)
        print(f"Encrypted: {bytes_to_hex(ciphertext)}")
        
        # Decrypt
        decrypted = decrypt(ciphertext, key)
        print(f"Decrypted: {bytes_to_hex(decrypted)}")
        
        # Verify
        if decrypted == padded_plaintext:
            print("Round-trip test PASSED")
        else:
            print("Round-trip test FAILED")
            print(f"Original: {bytes_to_hex(padded_plaintext)}")
            print(f"Result:   {bytes_to_hex(decrypted)}")

if __name__ == "__main__":
    run_test_vectors()
    test_round_trip()