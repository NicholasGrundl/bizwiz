# BizWiz 

## Overview



## Getting Started with WSL (Windows Subsystem for Linux)

### Prerequisites

1. Install WSL if you haven't already. You can find instructions on the [Microsoft documentation](https://docs.microsoft.com/en-us/windows/wsl/install).

### Installing Make

1. Open your WSL terminal
2. Update your package list:
   ```
   sudo apt update
   ```
3. Install make:
   ```
   sudo apt install make
   ```

### Installing Miniconda

1. Download the latest Miniconda installer for Linux:
   ```
   wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```
2. Run the installer:
   ```
   bash Miniconda3-latest-Linux-x86_64.sh
   ```
3. Follow the prompts to complete the installation
4. Close and reopen your terminal to apply the changes

### Creating a new Conda environment

1. Create a new environment with Python (replace `3.10` with your desired version):
   ```
   conda create -n bizwiz python=3.10 pip
   ```
2. Activate the environment:
   ```
   conda activate bizwiz
   ```

### Installing Python packages/dependencies using the Makefile

The project includes a Makefile that simplifies the process of setting up the environment and installing dependencies.

1. Ensure you're in the project root directory
2. Install the required packages:
   ```
   make install
   ```

This command will install all the necessary dependencies listed in the `requirements.txt` and `requirements-dev.txt` files.

> **Important Note:** It's recommended to semi-regularly reinstall dependencies to ensure no dependencies are broken. You can do this by uninstalling all packages and then running the install command again.

To uninstall all packages:
```
make uninstall
```

After uninstalling, you can reinstall the packages:
```
make install
```

### Using the Makefile to run Streamlit or other code

The Makefile includes commands to run various parts of the project. Here are the available commands:


1. To start Jupyter Lab:
   ```
   make jupyter
   ```

2. To publish a new tag (for version control):
   ```
   make publish.tag
   ```

Always refer to the Makefile in the project root to see all available commands and their descriptions.

## Environment Variables and API Keys

This project uses environment variables to manage configuration and sensitive information such as API keys. We use two different methods for managing these variables:

1. `.env` files: Used for the package code

### Setting up .env file

1. Create a `.env` file in the root directory of the project.
2. Add your environment variables in the following format:

   ```
   VARIABLE_NAME=value
   API_KEY=your_api_key_here
   ```

3. Make sure to add `.env` to your `.gitignore` file to prevent sensitive information from being committed to version control.


### Using Environment Variables

- In Python code, you can access environment variables using the `os.environ` dictionary:

  ```python
  import os
  from dotenv import load_dotenv
  load_dotenv()

  api_key = os.environ.get('API_KEY')
  ```

Remember to never commit sensitive information like API keys to version control. Always use environment variables or secrets management for such data.


## Additional Information

For more detailed information about the project structure, available modules, and how to use them, please refer to the source code and any additional documentation in the repository.