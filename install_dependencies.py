import subprocess
import sys

def install_package(package):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}. Error: {e}")
        sys.exit(1)

def main():
    # Update pip and setuptools
    print("Updating pip and setuptools...")
    install_package("--upgrade pip setuptools")
    
    # Install dependencies
    dependencies = [
        "streamlit==1.24.0",
        "pillow==9.5.0"
    ]
    
    print("Installing dependencies...")
    for dep in dependencies:
        install_package(dep)
    
    print("All dependencies installed successfully!")

if __name__ == "__main__":
    main()
