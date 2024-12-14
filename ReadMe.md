# Project Overview

=====================================

This project is a graphical user interface (GUI) application built using Python and the CTk library for creating modern and visually appealing interfaces. The code provides functionality for users to log in, view home section content, and update book data.

## Table of Contents

---

1. [Project Structure](#project-structure)
2. [Features](#features)
3. [Getting Started](#getting-started)
4. [Dependencies](#dependencies)
5. [Installation Instructions](#installation-instructions)
6. [Running the Application](#running-the-applicaion)

## Project Structure

---

The project is structured into the following files and directories:

- `interface.py`: Contains the main GUI application code.
- `library.py`: Handles book data operations, including reading and updating data.

## Features

---

### 1. ISBN Search

- Implement a feature to search for books by their ISBN (International Standard Book Number).
- The search functionality should be able to handle both exact matches and partial searches (e.g., searching for "978-3-16" instead of the full ISBN "978-3-16-148410-0").

### 2. Password Hashing

- Implement a password hashing mechanism using a secure library such as `bcrypt` or `argon2c`.
- This ensures that passwords are stored securely and cannot be retrieved in plaintext.
- Modify the login functionality to use the hashed passwords for authentication.

### 3. Logging Mechanism

- Configure the logging settings to track user interactions and errors in the application.
- Use a simple logging fucntion to log meesages to a log file for later review.
- Modify the `interface.py` file to include logging statements for important events.

### 4. Different Authentication Levels

- A multiple authentication levels, allowing administrators and regular users to access different features and data.
- Create roles or permissions for each level of access (e.g., "admin", "Librarian") and modify the login functionality to assign these roles based on user input.

### 5. Database Management

- The application stores book data in a CSV file located at `./Books.csv`.
- This provied a way to enable data storage that can be easily adapted for a database.
- Also this provides a way to ealisy manipulate data or segemnt data for a larger scale system

## Getting Started

---

To run the application, navigate to the project directory in your terminal/command prompt and execute the following command:

```bash
python interface.py
```

This will launch the GUI application. You can log in using the provided username and password, and access the home section content.

## Dependencies

---

- Python 3.x (recommended: 3.10)
- customtkinter library for GUI creation
- NumPy and Pandas libraries for data manipulation

### Installation Instructions

To install the required dependencies, run the following command in your terminal/command prompt:

```bash
pip install -r requirements.txt
```

### Running the Application

Run the application using the following command:

```bash
python interface.py
```

This will launch the GUI application.
