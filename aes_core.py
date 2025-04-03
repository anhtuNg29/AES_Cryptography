#!/usr/bin/env python3
# AES-128 Encryption/Decryption Implementation
# Core functionality file

from aes_utils import bytes_to_matrix, matrix_to_bytes, display_state, display_round_key
from aes_constants import sbox, inv_sbox, rcon

def sub_bytes(state, inverse=False):
    """
    Thay thế mỗi byte trong state bằng giá trị tương ứng từ S-box.
    SubBytes transformation hoạt động độc lập trên mỗi byte của state.
    """
    box = inv_sbox if inverse else sbox
    
    for i in range(4):
        for j in range(4):
            state[i][j] = box[state[i][j]]
    
    return state

def shift_rows(state, inverse=False):
    """
    Dịch chuyển các hàng của ma trận state:
    - Hàng 0: Không dịch
    - Hàng 1: Dịch 1 vị trí (sang trái khi mã hóa, phải khi giải mã)
    - Hàng 2: Dịch 2 vị trí
    - Hàng 3: Dịch 3 vị trí
    """
    # Tạo một bản sao của state để không thay đổi trực tiếp
    result = [row[:] for row in state]
    
    for i in range(1, 4):
        # Số vị trí cần dịch chuyển cho mỗi hàng
        shift = i
        if inverse:
            shift = 4 - i
            
        # Dịch chuyển hàng i
        result[i] = state[i][shift:] + state[i][:shift]
    
    return result

def galois_multiplication(a, b):
    """Nhân hai số trong trường Galois GF(2^8)."""
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi_bit_set = a & 0x80
        a <<= 1
        if hi_bit_set:
            a ^= 0x1B  # AES's irreducible polynomial x^8 + x^4 + x^3 + x + 1 (0x11b)
        b >>= 1
    return p & 0xFF

def mix_columns(state, inverse=False):
    """
    Mix Columns transformation hoạt động trên mỗi cột của state.
    Mỗi cột được coi như một đa thức trong GF(2^8) và được nhân với
    một đa thức cố định: a(x) = {03}x^3 + {01}x^2 + {01}x + {02} (mã hóa)
    hoặc nghịch đảo của nó (giải mã).
    """
    for i in range(4):
        # Lưu cột hiện tại
        col = [state[j][i] for j in range(4)]
        
        if not inverse:
            # MixColumns transformation cho mã hóa
            state[0][i] = galois_multiplication(0x02, col[0]) ^ \
                          galois_multiplication(0x03, col[1]) ^ \
                          col[2] ^ col[3]
            state[1][i] = col[0] ^ \
                          galois_multiplication(0x02, col[1]) ^ \
                          galois_multiplication(0x03, col[2]) ^ \
                          col[3]
            state[2][i] = col[0] ^ col[1] ^ \
                          galois_multiplication(0x02, col[2]) ^ \
                          galois_multiplication(0x03, col[3])
            state[3][i] = galois_multiplication(0x03, col[0]) ^ \
                          col[1] ^ col[2] ^ \
                          galois_multiplication(0x02, col[3])
        else:
            # InvMixColumns transformation cho giải mã
            state[0][i] = galois_multiplication(0x0E, col[0]) ^ \
                          galois_multiplication(0x0B, col[1]) ^ \
                          galois_multiplication(0x0D, col[2]) ^ \
                          galois_multiplication(0x09, col[3])
            state[1][i] = galois_multiplication(0x09, col[0]) ^ \
                          galois_multiplication(0x0E, col[1]) ^ \
                          galois_multiplication(0x0B, col[2]) ^ \
                          galois_multiplication(0x0D, col[3])
            state[2][i] = galois_multiplication(0x0D, col[0]) ^ \
                          galois_multiplication(0x09, col[1]) ^ \
                          galois_multiplication(0x0E, col[2]) ^ \
                          galois_multiplication(0x0B, col[3])
            state[3][i] = galois_multiplication(0x0B, col[0]) ^ \
                          galois_multiplication(0x0D, col[1]) ^ \
                          galois_multiplication(0x09, col[2]) ^ \
                          galois_multiplication(0x0E, col[3])
    
    return state

def add_round_key(state, round_key):
    """
    AddRoundKey transformation kết hợp mỗi byte của state với
    byte tương ứng trong round key bằng phép XOR.
    """
    for i in range(4):
        for j in range(4):
            state[i][j] ^= round_key[i][j]
    
    return state

def generate_round_keys(key):
    """
    Sinh các khóa con từ khóa chính key.
    """
    key_schedule = []
    key_matrix = bytes_to_matrix(key)
    key_schedule.append(key_matrix)
    
    for i in range(10):  # AES-128 có 10 vòng, nên cần 11 khóa con (khóa ban đầu + 10 khóa vòng)
        # Lấy khóa của vòng trước
        prev_key = key_schedule[-1]
        new_key = [row[:] for row in prev_key]  # Tạo bản sao
        
        # RotWord: Dịch vòng cột cuối
        temp = [prev_key[1][3], prev_key[2][3], prev_key[3][3], prev_key[0][3]]
        
        # SubWord: Thay thế bằng giá trị từ S-box
        for j in range(4):
            temp[j] = sbox[temp[j]]
        
        # XOR với cột đầu của khóa trước và với Rcon
        for j in range(4):
            new_key[j][0] = prev_key[j][0] ^ temp[j] ^ (rcon[i] if j == 0 else 0)
        
        # Tính các cột còn lại
        for j in range(1, 4):
            for k in range(4):
                new_key[k][j] = new_key[k][j-1] ^ prev_key[k][j]
        
        key_schedule.append(new_key)
    
    return key_schedule

def encrypt(plaintext, key, verbose=False):
    """
    Mã hóa plaintext với khóa key sử dụng AES-128.
    Nếu verbose=True, hiển thị thông tin chi tiết qua mỗi vòng.
    """
    state = bytes_to_matrix(plaintext)
    round_keys = generate_round_keys(key)
    
    if verbose:
        print("\nKhóa chính:")
        display_round_key(round_keys[0])
        print("\nCác khóa vòng:")
        for i in range(1, 11):
            print(f"\nKhóa vòng {i}:")
            display_round_key(round_keys[i])
    
    # Initial round
    if verbose:
        print("\n--- Vòng ban đầu ---")
        print("Trước AddRoundKey:")
        display_state(state)
    
    state = add_round_key(state, round_keys[0])
    
    if verbose:
        print("Sau AddRoundKey:")
        display_state(state)
    
    # Main rounds
    for i in range(1, 10):
        if verbose:
            print(f"\n--- Vòng {i} ---")
        
        if verbose:
            print("Trước SubBytes:")
            display_state(state)
        
        state = sub_bytes(state)
        
        if verbose:
            print("Sau SubBytes:")
            display_state(state)
            print("Trước ShiftRows:")
            display_state(state)
        
        state = shift_rows(state)
        
        if verbose:
            print("Sau ShiftRows:")
            display_state(state)
            print("Trước MixColumns:")
            display_state(state)
        
        state = mix_columns(state)
        
        if verbose:
            print("Sau MixColumns:")
            display_state(state)
            print("Trước AddRoundKey:")
            display_state(state)
        
        state = add_round_key(state, round_keys[i])
        
        if verbose:
            print("Sau AddRoundKey:")
            display_state(state)
    
    # Final round (no MixColumns)
    if verbose:
        print("\n--- Vòng cuối (10) ---")
        print("Trước SubBytes:")
        display_state(state)
    
    state = sub_bytes(state)
    
    if verbose:
        print("Sau SubBytes:")
        display_state(state)
        print("Trước ShiftRows:")
        display_state(state)
    
    state = shift_rows(state)
    
    if verbose:
        print("Sau ShiftRows:")
        display_state(state)
        print("Trước AddRoundKey:")
        display_state(state)
    
    state = add_round_key(state, round_keys[10])
    
    if verbose:
        print("Sau AddRoundKey (Ciphertext):")
        display_state(state)
    
    return matrix_to_bytes(state)

def decrypt(ciphertext, key, verbose=False):
    """
    Giải mã ciphertext với khóa key sử dụng AES-128.
    Nếu verbose=True, hiển thị thông tin chi tiết qua mỗi vòng.
    """
    state = bytes_to_matrix(ciphertext)
    round_keys = generate_round_keys(key)
    
    if verbose:
        print("\nKhóa chính:")
        display_round_key(round_keys[0])
        print("\nCác khóa vòng:")
        for i in range(1, 11):
            print(f"\nKhóa vòng {i}:")
            display_round_key(round_keys[i])
    
    # Initial round
    if verbose:
        print("\n--- Vòng ban đầu ---")
        print("Trước AddRoundKey:")
        display_state(state)
    
    state = add_round_key(state, round_keys[10])
    
    if verbose:
        print("Sau AddRoundKey:")
        display_state(state)
    
    # Main rounds
    for i in range(9, 0, -1):
        if verbose:
            print(f"\n--- Vòng {10-i} ---")
        
        if verbose:
            print("Trước InvShiftRows:")
            display_state(state)
        
        state = shift_rows(state, inverse=True)
        
        if verbose:
            print("Sau InvShiftRows:")
            display_state(state)
            print("Trước InvSubBytes:")
            display_state(state)
        
        state = sub_bytes(state, inverse=True)
        
        if verbose:
            print("Sau InvSubBytes:")
            display_state(state)
            print("Trước AddRoundKey:")
            display_state(state)
        
        state = add_round_key(state, round_keys[i])
        
        if verbose:
            print("Sau AddRoundKey:")
            display_state(state)
            print("Trước InvMixColumns:")
            display_state(state)
        
        state = mix_columns(state, inverse=True)
        
        if verbose:
            print("Sau InvMixColumns:")
            display_state(state)
    
    # Final round (no InvMixColumns)
    if verbose:
        print("\n--- Vòng cuối (10) ---")
        print("Trước InvShiftRows:")
        display_state(state)
    
    state = shift_rows(state, inverse=True)
    
    if verbose:
        print("Sau InvShiftRows:")
        display_state(state)
        print("Trước InvSubBytes:")
        display_state(state)
    
    state = sub_bytes(state, inverse=True)
    
    if verbose:
        print("Sau InvSubBytes:")
        display_state(state)
        print("Trước AddRoundKey:")
        display_state(state)
    
    state = add_round_key(state, round_keys[0])
    
    if verbose:
        print("Sau AddRoundKey (Plaintext):")
        display_state(state)
    
    return matrix_to_bytes(state)