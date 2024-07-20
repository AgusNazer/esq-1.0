# Login System Created with Python-Flask Using JWT (JSON Web Token)

This project is a login system developed with **Python** and **Flask**, utilizing the **JWT (JSON Web Token)** library for secure authentication. The system is designed to provide a template for various web applications, and it can be adapted and scaled according to specific needs and requirements.

## Features

- **User Registration**: Allows new users to create an account.
- **Login**: Authenticate users and generate JWT tokens.
- **Password Hashing**: Ensures passwords are securely hashed before storage.
- **Error Handling**: Provides appropriate error messages for various authentication issues.
- **Redirections**: Manages user redirections post-login and logout.

## Installation

To run this project, you need **Python 3.x** installed. Follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/your-repository.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd your-repository
    ```

3. **Create a virtual environment and activate it:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables:**

    Create a `.env` file in the root directory of the project and add the following variable:

    ```
    SECRET_KEY=your_secret_key
    ```

6. **Run the application:**

    ```bash
    python app.py
    ```

    The application will be available at `http://127.0.0.1:5000`.

## Usage

- **User Registration**: Send a POST request to `/auth/register` with `username`, `password`, and `email`.
- **Login**: Send a POST request to `/auth/login` with `username` and `password`.

## Overview

The system serves as a general-purpose authentication framework and can be customized for different web applications. It provides a solid foundation for handling user authentication, including secure password management and efficient error handling. Adapt and scale it to fit specific application requirements.

---

For further details, feel free to check the code and modify it according to your needs.
