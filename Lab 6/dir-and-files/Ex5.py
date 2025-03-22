import os

def write_list_to_file(file_path, my_list):
    with open(file_path, 'w') as file:
        for item in my_list:
            file.write(f"{item}\n")
    print(f"List written to {file_path}")

if __name__ == "__main__":
    my_list = ["PP2","Discrete","Calculus2","SPK","English"]

    write_list_to_file('output.txt', my_list)