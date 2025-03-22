import os

def delete_file(file_path):
    if os.path.exists(file_path):
        if os.access(file_path, os.W_OK):
            os.remove(file_path)
            print(f"{file_path} deleted.")
        else:
            print(f"No write access to {file_path}.")
    else:
        print(f"{file_path} does not exist.")

if __name__ == "__main__":
    file_path = input("Enter file path to delete: ")
    delete_file(file_path)