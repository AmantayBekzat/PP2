import shutil

def copy_file(source, destination):
    try:
        shutil.copyfile(source, destination)
        print(f"Contents of {source} copied to {destination}")
    except FileNotFoundError:
        print("Source file not found!")

if __name__ == "__main__":
    source = input("Enter source file to copy: ")
    destination = input("Enter destination file: ")
    copy_file(source, destination)