# AES-128 Encryption/Decryption Project

This project provides a complete implementation of the AES-128 encryption and decryption algorithm in Python. It includes detailed visualization of the entire process, showing the state after each transformation in every round.

## Features

- AES-128 encryption and decryption
- Support for text or hexadecimal input
- Detailed step-by-step visualization of the encryption/decryption process
- Display of all intermediate states and round keys
- Comprehensive comments explaining each part of the algorithm

## Files

- `main.py`: Main application with user interface
- `aes_core.py`: Core AES encryption and decryption functions
- `aes_utils.py`: Utility functions for data manipulation and display
- `aes_constants.py`: AES constants like S-box, inverse S-box, and round constants
- `aes_visualization.py`: Functions for visualizing the AES process (optional)
- `aes_debug.py`: Testing functions with standard test vectors

## AES-128 Algorithm Overview

AES (Advanced Encryption Standard) is a symmetric block cipher that processes data blocks of 128 bits using cipher keys of 128, 192, or 256 bits. This implementation focuses on AES-128, which uses a 128-bit key and 10 rounds.

### Key Transformations

1. **SubBytes (S-box)**: Substitutes each byte in the state with its corresponding value in the S-box
2. **ShiftRows**: Cyclically shifts the rows of the state to the left
3. **MixColumns**: Mixes data within each column through a linear transformation
4. **AddRoundKey**: Combines the state with a round key using XOR operation

### Encryption Process

1. **Initial Round**: AddRoundKey
2. **Main Rounds (1-9)**: SubBytes → ShiftRows → MixColumns → AddRoundKey
3. **Final Round (10)**: SubBytes → ShiftRows → AddRoundKey

### Decryption Process

1. **Initial Round**: AddRoundKey
2. **Main Rounds (1-9)**: InvShiftRows → InvSubBytes → AddRoundKey → InvMixColumns
3. **Final Round (10)**: InvShiftRows → InvSubBytes → AddRoundKey

## Usage

1. Run `main.py` to start the application
2. Choose between encryption or decryption
3. Enter the key (as text or hex)
4. Enter the plaintext/ciphertext (as text or hex)
5. View the detailed results of the process

## Requirements

- Python 3.6 or higher
- (Optional) Matplotlib for visualization features

## Example

```
python main.py
```

```
================================================
              AES-128 ENCRYPTION/DECRYPTION
================================================

Lựa chọn chức năng:
1. Mã hóa AES-128
2. Giải mã AES-128
3. Thoát

Lựa chọn của bạn (1-3): 1

--- MÃ HÓA AES-128 ---

Lựa chọn cách nhập khóa:
1. Nhập khóa dưới dạng chuỗi (sẽ được chuyển đổi sang 16 bytes)
2. Nhập khóa dưới dạng hex (phải đúng 32 ký tự hex)

Lựa chọn của bạn (1-2): 1

Nhập khóa (chuỗi): ThisIsTheKey123

Khóa đã được chuyển đổi thành: 54686973497354686554657931323300
(16 bytes - đủ 128 bit cho AES-128)

Lựa chọn cách nhập plaintext:
1. Nhập plaintext dưới dạng chuỗi
2. Nhập plaintext dưới dạng hex

Lựa chọn của bạn (1-2): 1

Nhập plaintext (chuỗi): Hello, AES!

plaintext đã được pad thành: 48656C6C6F2C2041455321050505050505
(16 bytes - đủ bội số của 16 bytes cho AES)

=== Xử lý block 1/1 ===

Plaintext block:
-----------------------------
| 48 | 65 | 6C | 6F |
| 2C | 20 | 41 | 45 |
| 53 | 21 | 05 | 05 |
| 05 | 05 | 05 | 05 |
-----------------------------

... [detailed round output would appear here] ...

Kết quả mã hóa block 1: 7BC5A08037AFA847F32EC28F3329D7FA

Nhấn Enter để tiếp tục...
```

## Implementation Notes

- The implementation follows the FIPS 197 specification for AES
- Verbose output is available to Sshow the state after each transformation
- The code is heavily commented to explain each step of the algorithm

1. aes_constants.py
File này chứa các hằng số cần thiết cho thuật toán AES:

sbox: Bảng thay thế S-box dùng trong phép biến đổi SubBytes
inv_sbox: Bảng thay thế ngược dùng trong phép biến đổi InvSubBytes (giải mã)
rcon: Hằng số Round Constant dùng trong quá trình mở rộng khóa
Các bảng này là cốt lõi của AES và được định nghĩa theo chuẩn, không thay đổi.
----------------------------------------------------------------------------------
2. aes_utils.py
File này chứa các hàm tiện ích để xử lý dữ liệu:

bytes_to_matrix(data): Chuyển đổi 16 bytes thành ma trận 4x4 theo thứ tự cột (column-major order). Đây là cách AES biểu diễn dữ liệu nội bộ.

matrix_to_bytes(matrix): Chuyển đổi ma trận 4x4 ngược lại thành chuỗi 16 bytes.

bytes_to_hex(data): Chuyển đổi bytes thành chuỗi hex để hiển thị.

hex_to_bytes(hex_str): Chuyển đổi chuỗi hex thành bytes.

display_state(state, title): Hiển thị ma trận trạng thái AES với định dạng đẹp.

display_round_key(key, round_num): Hiển thị khóa vòng với định dạng đẹp.

Các hàm này giúp chuyển đổi giữa các định dạng dữ liệu và hiển thị trạng thái của thuật toán.
----------------------------------------------------------------------------------
3. aes_core.py
File này chứa các hàm cốt lõi của thuật toán AES:

Các phép biến đổi cơ bản:
sub_bytes(state, inverse=False): Thay thế mỗi byte trong ma trận trạng thái bằng giá trị tương ứng từ S-box (hoặc Inverse S-box khi giải mã).

shift_rows(state, inverse=False): Dịch chuyển các hàng của ma trận trạng thái:

Hàng 0: Không dịch
Hàng 1: Dịch 1 vị trí (trái khi mã hóa, phải khi giải mã)
Hàng 2: Dịch 2 vị trí
Hàng 3: Dịch 3 vị trí
mix_columns(state, inverse=False): Phép biến đổi MixColumns thực hiện phép nhân ma trận trong trường Galois GF(2^8). Mỗi cột của ma trận trạng thái được nhân với một ma trận cố định.

add_round_key(state, round_key): Thực hiện phép XOR giữa ma trận trạng thái và khóa vòng.

Phép nhân trong trường Galois:
galois_multiplication(a, b): Thực hiện phép nhân hai số trong trường Galois GF(2^8), cần thiết cho phép biến đổi MixColumns.
Mở rộng khóa:
expand_key(key): Mở rộng khóa 16 bytes ban đầu thành 11 khóa vòng (176 bytes).

generate_round_keys(key): Tạo ra các khóa vòng từ khóa chính và trả về dưới dạng danh sách các ma trận 4x4.

Mã hóa và giải mã:
encrypt_block(plaintext, key): Mã hóa một khối 16 bytes bằng thuật toán AES.

decrypt_block(ciphertext, key): Giải mã một khối 16 bytes đã mã hóa.

encrypt(plaintext, key, mode='ECB', iv=None): Mã hóa dữ liệu với các chế độ khác nhau (ECB, CBC).

decrypt(ciphertext, key, mode='ECB', iv=None): Giải mã dữ liệu với các chế độ khác nhau.
----------------------------------------------------------------------------------
4. aes_debug.py
File này chứa các hàm để kiểm tra và gỡ lỗi thuật toán AES:
----------------------------------------------------------------------------------
run_test_vectors(): Chạy các vector kiểm tra chuẩn cho AES-128 để xác minh triển khai.
File này giúp đảm bảo rằng thuật toán hoạt động đúng theo tiêu chuẩn AES.
----------------------------------------------------------------------------------
5. aes_visualization.py
File này có vẻ như chứa mã để trực quan hóa quá trình mã hóa/giải mã AES, nhưng nội dung không được cung cấp đầy đủ.
----------------------------------------------------------------------------------
6. main.py
File này là điểm vào chính của chương trình, cung cấp giao diện người dùng dòng lệnh:

clear_screen(): Xóa màn hình terminal.

get_key(): Lấy khóa AES từ người dùng, hỗ trợ nhập dưới dạng chuỗi hoặc hex.

pad_data(data): Thêm padding vào dữ liệu để đảm bảo độ dài là bội số của 16 bytes.

unpad_data(data): Loại bỏ padding sau khi giải mã.

encrypt_file(input_file, output_file, key, mode): Mã hóa nội dung của một file.

decrypt_file(input_file, output_file, key, mode): Giải mã nội dung của một file.

main(): Hàm chính điều khiển luồng chương trình, hiển thị menu và xử lý lựa chọn của người dùng.

Cách hoạt động của AES-128
--------------------------------------------
Quá trình mã hóa:
Khởi tạo: Chuyển đổi plaintext và key thành ma trận 4x4
AddRoundKey ban đầu: XOR ma trận trạng thái với khóa ban đầu
9 vòng chính:
SubBytes: Thay thế mỗi byte bằng giá trị từ S-box
ShiftRows: Dịch các hàng của ma trận
MixColumns: Trộn các cột của ma trận
AddRoundKey: XOR với khóa vòng
Vòng cuối:
SubBytes
ShiftRows
AddRoundKey (không có MixColumns)
Kết quả: Chuyển đổi ma trận trạng thái thành ciphertext
-----------------------------------------
Quá trình giải mã:
Quá trình giải mã thực hiện các phép biến đổi ngược lại theo thứ tự ngược:
Khởi tạo: Chuyển đổi ciphertext và key thành ma trận 4x4
AddRoundKey ban đầu: XOR với khóa vòng cuối
9 vòng chính:
InvShiftRows: Dịch các hàng ngược lại
InvSubBytes: Thay thế mỗi byte bằng giá trị từ Inverse S-box
AddRoundKey: XOR với khóa vòng
InvMixColumns: Trộn các cột ngược lại
Vòng cuối:
InvShiftRows
InvSubBytes
AddRoundKey (không có InvMixColumns)
Kết quả: Chuyển đổi ma trận trạng thái thành plaintext
Các chế độ mã hóa:
ECB (Electronic Codebook): Mỗi khối được mã hóa độc lập.
CBC (Cipher Block Chaining): Mỗi khối plaintext được XOR với khối ciphertext trước đó trước khi mã hóa.