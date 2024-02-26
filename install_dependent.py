import os

def install_dependencies_from_file(filename):
    with open(filename, 'r') as file:
        dependencies = file.read().splitlines()
        for dependency in dependencies:
            os.system(f"pip install {dependency}")

if __name__ == "__main__":
    dependencies_file = "dependent.txt"
    install_dependencies_from_file(dependencies_file)
