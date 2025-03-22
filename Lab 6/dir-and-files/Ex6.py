def generate_alphabet_files():
    for letter in range(ord('A'), ord('Z') + 1):
        file_name = f"{chr(letter)}.txt"
        with open(file_name, 'w') as file:
            file.write(f"This is file {chr(letter)}.txt")
    print("26 files generated from A.txt to Z.txt")

if __name__ == "__main__":
    generate_alphabet_files()