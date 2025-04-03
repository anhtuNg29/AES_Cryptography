#!/usr/bin/env python3
# AES-128 Encryption/Decryption Implementation
# Main application file

import os
from aes_core import encrypt, decrypt, generate_round_keys
from aes_utils import bytes_to_matrix, matrix_to_bytes, display_state, hex_to_bytes, bytes_to_hex

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_key():
    """Get the AES key from user input."""
    while True:
        print("\nLựa chọn cách nhập khóa:")
        print("1. Nhập khóa dưới dạng chuỗi (sẽ được chuyển đổi sang 16 bytes)")
        print("2. Nhập khóa dưới dạng hex (phải đúng 32 ký tự hex)")
        
        choice = input("\nLựa chọn của bạn (1-2): ")
        
        if choice == '1':
            key_str = input("\nNhập khóa (chuỗi): ")
            # Convert string to bytes and ensure it's 16 bytes by padding or truncating
            key_bytes = key_str.encode('utf-8')
            if len(key_bytes) < 16:
                key_bytes = key_bytes.ljust(16, b'\x00')  # Padding with null bytes
            else:
                key_bytes = key_bytes[:16]  # Truncate to 16 bytes
            
            print(f"\nKhóa đã được chuyển đổi thành: {bytes_to_hex(key_bytes)}")
            print(f"(16 bytes - đủ 128 bit cho AES-128)")
            return key_bytes
            
        elif choice == '2':
            key_hex = input("\nNhập khóa (hex, 32 ký tự): ")
            key_hex = key_hex.replace(" ", "")  # Remove any spaces
            
            if len(key_hex) != 32 or not all(c in '0123456789ABCDEFabcdef' for c in key_hex):
                print("Lỗi: Khóa phải có đúng 32 ký tự hex (0-9, A-F).")
                continue
                
            key_bytes = hex_to_bytes(key_hex)
            return key_bytes
        
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

def get_input_data(mode):
    """Get the input data (plaintext/ciphertext) from user input."""
    while True:
        input_type = "plaintext" if mode == "encrypt" else "ciphertext"
        
        print(f"\nLựa chọn cách nhập {input_type}:")
        print(f"1. Nhập {input_type} dưới dạng chuỗi")
        print(f"2. Nhập {input_type} dưới dạng hex")
        
        choice = input("\nLựa chọn của bạn (1-2): ")
        
        if choice == '1':
            data_str = input(f"\nNhập {input_type} (chuỗi): ")
            # Convert string to bytes
            data_bytes = data_str.encode('utf-8')
            
            # For encryption, we need to ensure the input is a multiple of 16 bytes
            if mode == "encrypt" and len(data_bytes) % 16 != 0:
                padding_length = 16 - (len(data_bytes) % 16)
                data_bytes += bytes([padding_length]) * padding_length
                print(f"\n{input_type} đã được pad thành: {bytes_to_hex(data_bytes)}")
                print(f"({len(data_bytes)} bytes - đủ bội số của 16 bytes cho AES)")
            
            return data_bytes
            
        elif choice == '2':
            data_hex = input(f"\nNhập {input_type} (hex): ")
            data_hex = data_hex.replace(" ", "")  # Remove any spaces
            
            if len(data_hex) % 32 != 0 or not all(c in '0123456789ABCDEFabcdef' for c in data_hex):
                print("Lỗi: Input phải có số ký tự hex là bội số của 32 (0-9, A-F).")
                continue
                
            data_bytes = hex_to_bytes(data_hex)
            return data_bytes
        
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")

def main():
    while True:
        clear_screen()
        print("=" * 60)
        print("              AES-128 ENCRYPTION/DECRYPTION")
        print("=" * 60)
        print("\nLựa chọn chức năng:")
        print("1. Mã hóa AES-128")
        print("2. Giải mã AES-128")
        print("3. Thoát")
        
        choice = input("\nLựa chọn của bạn (1-3): ")
        
        if choice == '1':
            # Encryption mode
            print("\n--- MÃ HÓA AES-128 ---")
            key = get_key()
            plaintext = get_input_data("encrypt")
            
            # Process each 16-byte block separately
            for block_num in range(0, len(plaintext), 16):
                block = plaintext[block_num:block_num+16]
                print(f"\n=== Xử lý block {block_num//16 + 1}/{len(plaintext)//16} ===")
                
                # Generate round keys
                round_keys = generate_round_keys(key)
                
                # Display the original block
                print("\nPlaintext block:")
                display_state(bytes_to_matrix(block))
                
                # Encrypt and show detailed process
                ciphertext_block = encrypt(block, key, verbose=True)
                
                print(f"\nKết quả mã hóa block {block_num//16 + 1}: {bytes_to_hex(ciphertext_block)}")
            
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == '2':
            # Decryption mode
            print("\n--- GIẢI MÃ AES-128 ---")
            key = get_key()
            ciphertext = get_input_data("decrypt")
            
            if len(ciphertext) % 16 != 0:
                print("Lỗi: Ciphertext phải có độ dài là bội số của 16 bytes.")
                input("\nNhấn Enter để tiếp tục...")
                continue
            
            # Process each 16-byte block separately
            for block_num in range(0, len(ciphertext), 16):
                block = ciphertext[block_num:block_num+16]
                print(f"\n=== Xử lý block {block_num//16 + 1}/{len(ciphertext)//16} ===")
                
                # Generate round keys
                round_keys = generate_round_keys(key)
                
                # Display the original block
                print("\nCiphertext block:")
                display_state(bytes_to_matrix(block))
                
                # Decrypt and show detailed process
                plaintext_block = decrypt(block, key, verbose=True)
                
                print(f"\nKết quả giải mã block {block_num//16 + 1}: {bytes_to_hex(plaintext_block)}")
                
                # Try to interpret as utf-8 if possible
                try:
                    text = plaintext_block.decode('utf-8')
                    print(f"Giải mã thành văn bản: {text}")
                except UnicodeDecodeError:
                    pass
            
            input("\nNhấn Enter để tiếp tục...")
            
        elif choice == '3':
            print("\nĐã thoát chương trình.")
            break
            
        else:
            print("Lựa chọn không hợp lệ. Vui lòng chọn lại.")
            input("\nNhấn Enter để tiếp tục...")

if __name__ == "__main__":
    main()