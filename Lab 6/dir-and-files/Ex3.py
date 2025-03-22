import os

def check_path_and_split(path):
    if os.path.exists(path):
        print(f"The path exists.")
        print(f"Directory: {os.path.dirname(path)}")
        print(f"Filename: {os.path.basename(path)}")
    else:
        print("The path does not exist.")

if __name__ == "__main__":
    path = input("Enter a path: ")
    check_path_and_split(path)