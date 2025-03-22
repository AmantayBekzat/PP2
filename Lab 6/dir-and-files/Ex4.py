def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            print(f"Number of lines: {len(lines)}")
    except FileNotFoundError:
        print("File not found!")

if __name__ == "__main__":
    file_path = input("Enter file path to count lines: ")
    count_lines_in_file(file_path)