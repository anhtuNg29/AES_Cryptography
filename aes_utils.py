#!/usr/bin/env python3
# AES-128 Encryption/Decryption Implementation
# Utility functions file

def bytes_to_matrix(data):
    """
    Chuyển đổi 16 bytes thành ma trận 4x4 theo thứ tự cột.
    data: 16 bytes
    return: ma trận 4x4
    """
    matrix = [[0 for _ in range(4)] for _ in range(4)]
    
    for i in range(4):
        for j in range(4):
            matrix[i][j] = data[i + 4*j]
    
    return matrix

def matrix_to_bytes(matrix):
    """
    Chuyển đổi ma trận 4x4 về 16 bytes theo thứ tự cột.
    matrix: ma trận 4x4
    return: 16 bytes
    """
    data = bytearray(16)
    
    for i in range(4):
        for j in range(4):
            data[i + 4*j] = matrix[i][j]
    
    return bytes(data)

def display_state(state):
    """
    Hiển thị ma trận state theo định dạng dễ đọc.
    """
    print("-" * 29)
    for i in range(4):
        row = " | ".join(f"{state[i][j]:02X}" for j in range(4))
        print(f"| {row} |")
    print("-" * 29)

def display_round_key(key):
    """
    Hiển thị khóa vòng theo định dạng dễ đọc.
    """
    # Hiển thị ma trận
    display_state(key)
    
    # Hiển thị dạng chuỗi hex liên tục
    flat_key = [key[i][j] for j in range(4) for i in range(4)]
    key_hex = ''.join(f"{b:02X}" for b in flat_key)
    print(f"Key (hex): {key_hex}")

def bytes_to_hex(data):
    """
    Chuyển đổi bytes thành chuỗi hex.
    """
    return ''.join(f"{b:02X}" for b in data)

def hex_to_bytes(hex_str):
    """
    Chuyển đổi chuỗi hex thành bytes.
    """
    return bytes.fromhex(hex_str)