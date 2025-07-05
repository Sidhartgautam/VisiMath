# 🧮 Math Solver (Handwritten & Manual Input)

## Project Overview

The Math Solver is a Django web application designed to solve mathematical equations. It provides two primary methods for equation input:

1.  **Image Upload (OCR-powered):** Users can upload images of handwritten or printed equations, which are then processed using Tesseract OCR (Optical Character Recognition) and OpenCV for image preprocessing.
2.  **Manual Text Input:** Users can directly type their equations into a text field.

The application uses the `SymPy` library in Python to parse, clean, and solve the equations, providing step-by-step insights into the process.

## Features

* **Image-to-Text Conversion:** Utilizes Tesseract OCR for robust text extraction from images.
* **Image Preprocessing:** Employs OpenCV to enhance image quality (grayscale, blur, thresholding) for better OCR accuracy.
* **Robust Equation Parsing:** Intelligently handles implicit multiplications (e.g., `3x` becomes `3*x`), common OCR errors (e.g., `O` to `0`), and standard mathematical syntax.
* **Equation Solving:** Leverages the powerful SymPy library to solve algebraic equations.
* **Flexible Input:** Supports both image uploads and direct text input, with manual input taking precedence if both are provided.
* **Step-by-Step Breakdown:** Provides detailed processing steps, from raw OCR output to the final solution, aiding in debugging and understanding.
* **User-Friendly Interface:** A clean web interface allows easy interaction.

## Technologies Used

* **Backend:**
    * Python 3.x
    * Django (Web Framework)
    * SymPy (Symbolic Mathematics Library)
    * Pillow (Python Imaging Library - Django's default for ImageField)
    * `opencv-python-headless` (OpenCV for image processing)
    * `pytesseract` (Python wrapper for Tesseract OCR)
* **Frontend:**
    * HTML5, CSS3
    * JavaScript (for dynamic form interactions)
    * MathJax (for rendering mathematical equations beautifully in the browser)
* **OCR Engine:**
    * Tesseract OCR (External system dependency)

## Setup Instructions

Follow these steps to get the Math Solver running on your local machine.

### 1. Prerequisites

* **Python 3.8+:** Download and install from [python.org](https://www.python.org/downloads/).
* **Tesseract OCR:** This is a crucial external dependency.
    * **Windows:** Download the installer from [Tesseract-OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki). **During installation, ensure "Add to PATH" is selected.**
    * **macOS:** Install via Homebrew:
        ```bash
        brew install tesseract
        ```
    * **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update
        sudo apt install tesseract-ocr
        sudo apt install libtesseract-dev # Often needed for pytesseract to work correctly
        ```
    * **Verify Installation:** Open a new terminal/command prompt and run:
        ```bash
        tesseract --version
        ```
        You should see version information. If not, ensure Tesseract is correctly installed and its executable directory is added to your system's PATH environment variable.

### 2. Project Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/math-solver.git](https://github.com/your-username/math-solver.git)
    cd math-solver
    ```
    (Replace `your-username/math-solver.git` with your actual repository URL)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Python dependencies:**
    ```bash
    pip install django pillow opencv-python-headless pytesseract sympy
    ```
    * **Note:** If `opencv-python-headless` causes issues on your specific system, try `pip install opencv-python`.

5.  **Configure Django:**
    * Navigate into the Django project root (where `manage.py` is located):
        ```bash
        cd mathsolver # If your main project folder is named mathsolver inside the clone
        ```
    * Apply database migrations:
        ```bash
        python manage.py makemigrations solver
        python manage.py migrate
        ```

### 3. Run the Application

1.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

1.  **Upload Image:** Click "Choose File" and select an image file (`.png`, `.jpg`, etc.) containing a handwritten or printed mathematical equation.
2.  **Manual Input:** Type your equation directly into the "Manual Input" text box (e.g., `x**2 + 3*x - 4 = 0`).
    * **Note:** If you provide both an image and manual input, the manual input will be prioritized.
3.  Click the "Solve" button.
4.  The application will display the processing steps, including raw OCR output, cleaned text, parsed equation, and the final solution(s).

### Equation Syntax Tips

* **Multiplication:** While the solver attempts to handle implicit multiplication (e.g., `3x`), it's safest to use `*` for clarity (e.g., `3*x`).
* **Exponentiation:** Use `**` (double asterisk) for powers (e.g., `x**2` for $x^2$).
* **Variables:** The solver primarily looks for `x`, `y`, `z`, `a`, `b`, `c`.
* **Equality:** Use `=` for equations (e.g., `x + 5 = 10`). If no `=` is present, the expression is assumed to be equal to zero.

## Project Structure
Got it! A good README.md is essential for any GitHub project. It helps others (and your future self!) understand what the project is, how to set it up, and how to use it.

Here's a comprehensive README.md for your Math Solver project, incorporating all the features and setup steps we've discussed.

Markdown

# 🧮 Math Solver (Handwritten & Manual Input)

## Project Overview

The Math Solver is a Django web application designed to solve mathematical equations. It provides two primary methods for equation input:

1.  **Image Upload (OCR-powered):** Users can upload images of handwritten or printed equations, which are then processed using Tesseract OCR (Optical Character Recognition) and OpenCV for image preprocessing.
2.  **Manual Text Input:** Users can directly type their equations into a text field.

The application uses the `SymPy` library in Python to parse, clean, and solve the equations, providing step-by-step insights into the process.

## Features

* **Image-to-Text Conversion:** Utilizes Tesseract OCR for robust text extraction from images.
* **Image Preprocessing:** Employs OpenCV to enhance image quality (grayscale, blur, thresholding) for better OCR accuracy.
* **Robust Equation Parsing:** Intelligently handles implicit multiplications (e.g., `3x` becomes `3*x`), common OCR errors (e.g., `O` to `0`), and standard mathematical syntax.
* **Equation Solving:** Leverages the powerful SymPy library to solve algebraic equations.
* **Flexible Input:** Supports both image uploads and direct text input, with manual input taking precedence if both are provided.
* **Step-by-Step Breakdown:** Provides detailed processing steps, from raw OCR output to the final solution, aiding in debugging and understanding.
* **User-Friendly Interface:** A clean web interface allows easy interaction.

## Technologies Used

* **Backend:**
    * Python 3.x
    * Django (Web Framework)
    * SymPy (Symbolic Mathematics Library)
    * Pillow (Python Imaging Library - Django's default for ImageField)
    * `opencv-python-headless` (OpenCV for image processing)
    * `pytesseract` (Python wrapper for Tesseract OCR)
* **Frontend:**
    * HTML5, CSS3
    * JavaScript (for dynamic form interactions)
    * MathJax (for rendering mathematical equations beautifully in the browser)
* **OCR Engine:**
    * Tesseract OCR (External system dependency)

## Setup Instructions

Follow these steps to get the Math Solver running on your local machine.

### 1. Prerequisites

* **Python 3.8+:** Download and install from [python.org](https://www.python.org/downloads/).
* **Tesseract OCR:** This is a crucial external dependency.
    * **Windows:** Download the installer from [Tesseract-OCR for Windows](https://github.com/UB-Mannheim/tesseract/wiki). **During installation, ensure "Add to PATH" is selected.**
    * **macOS:** Install via Homebrew:
        ```bash
        brew install tesseract
        ```
    * **Linux (Debian/Ubuntu):**
        ```bash
        sudo apt update
        sudo apt install tesseract-ocr
        sudo apt install libtesseract-dev # Often needed for pytesseract to work correctly
        ```
    * **Verify Installation:** Open a new terminal/command prompt and run:
        ```bash
        tesseract --version
        ```
        You should see version information. If not, ensure Tesseract is correctly installed and its executable directory is added to your system's PATH environment variable.

### 2. Project Setup

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/math-solver.git](https://github.com/your-username/math-solver.git)
    cd math-solver
    ```
    (Replace `your-username/math-solver.git` with your actual repository URL)

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    * **Windows:**
        ```bash
        .\venv\Scripts\activate
        ```
    * **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install Python dependencies:**
    ```bash
    pip install django pillow opencv-python-headless pytesseract sympy
    ```
    * **Note:** If `opencv-python-headless` causes issues on your specific system, try `pip install opencv-python`.

5.  **Configure Django:**
    * Navigate into the Django project root (where `manage.py` is located):
        ```bash
        cd mathsolver # If your main project folder is named mathsolver inside the clone
        ```
    * Apply database migrations:
        ```bash
        python manage.py makemigrations solver
        python manage.py migrate
        ```

### 3. Run the Application

1.  **Start the Django development server:**
    ```bash
    python manage.py runserver
    ```

2.  **Access the application:**
    Open your web browser and go to `http://127.0.0.1:8000/`.

## Usage

1.  **Upload Image:** Click "Choose File" and select an image file (`.png`, `.jpg`, etc.) containing a handwritten or printed mathematical equation.
2.  **Manual Input:** Type your equation directly into the "Manual Input" text box (e.g., `x**2 + 3*x - 4 = 0`).
    * **Note:** If you provide both an image and manual input, the manual input will be prioritized.
3.  Click the "Solve" button.
4.  The application will display the processing steps, including raw OCR output, cleaned text, parsed equation, and the final solution(s).

### Equation Syntax Tips

* **Multiplication:** While the solver attempts to handle implicit multiplication (e.g., `3x`), it's safest to use `*` for clarity (e.g., `3*x`).
* **Exponentiation:** Use `**` (double asterisk) for powers (e.g., `x**2` for $x^2$).
* **Variables:** The solver primarily looks for `x`, `y`, `z`, `a`, `b`, `c`.
* **Equality:** Use `=` for equations (e.g., `x + 5 = 10`). If no `=` is present, the expression is assumed to be equal to zero.

## Project Structure

.
├── mathsolver/                   # Django project root
│   ├── settings.py               # Django settings
│   ├── urls.py                   # Project-level URL configurations
│   └── wsgi.py
│   ├── asgi.py
│   └── solver/                   # Django app
│       ├── migrations/
│       ├── templates/
│       │   └── solver/
│       │       └── upload.html   # Frontend template
│       ├── init.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py              # Django forms for image upload
│       ├── models.py             # Database models for storing images
│       ├── tests.py
│       └── views.py              # Core logic: image processing, OCR, SymPy solving
├── manage.py                     # Django management script
└── README.md                     # This file