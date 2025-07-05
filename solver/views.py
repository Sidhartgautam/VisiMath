import cv2
import pytesseract
import re
from sympy import Eq, symbols, solve, N
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application, convert_xor
from django.shortcuts import render
from .forms import EquationImageForm
from .models import EquationImage # Make sure to import your model

# --- Tesseract Configuration (IMPORTANT!) ---
# You might need to set the path to your Tesseract executable.
# Uncomment and modify the line below if pytesseract cannot find tesseract.
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' # For Windows
# pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract' # For macOS/Linux (if installed via Homebrew/apt-get to a non-standard location)

def preprocess_image(image_path):
    """
    Applies image processing techniques to enhance readability for Tesseract.
    Converts to grayscale, applies Gaussian blur, and then Otsu's thresholding.
    Saves the processed image to a temporary path.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Image not found at {image_path}")

    # Apply Gaussian blur to reduce noise
    blur = cv2.GaussianBlur(img, (5, 5), 0)

    # Apply Otsu's thresholding to convert to binary image
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Create a new path for the processed image
    processed_path = image_path.replace(".png", "_processed.png").replace(".jpg", "_processed.jpg")
    cv2.imwrite(processed_path, thresh)
    return processed_path

def clean_ocr_output(text):
    """
    Cleans and normalizes the OCR output for SymPy parsing.
    Handles common OCR errors and applies mathematical syntax conventions.
    """
    # 1. Basic cleaning: strip whitespace, remove newlines, convert to lowercase
    # Removed .lower() for now to handle variables like 'X' or 'Y' if you intend them to be separate.
    # If you only expect 'x', then .lower() is fine. Let's keep it more flexible for now.
    cleaned_text = text.strip().replace('\n', '')

    # 2. Handle common OCR misinterpretations
    cleaned_text = cleaned_text.replace('O', '0').replace('o', '0') # 'O' (oh) to '0' (zero)
    cleaned_text = cleaned_text.replace('l', '1') # 'l' (el) to '1' (one) - common for '1'
    cleaned_text = cleaned_text.replace('s', '5') # 's' to '5' - less common but possible
    cleaned_text = cleaned_text.replace(' ', '') # Remove all spaces for initial parsing

    # 3. Replace common mathematical notation with SymPy-compatible syntax
    # Replace '^' with '**' for exponentiation
    cleaned_text = cleaned_text.replace('^', '**')

    # 4. Insert implicit multiplication
    # Regex to insert '*' between a digit and a letter (e.g., 3x -> 3*x)
    cleaned_text = re.sub(r'([0-9])([a-zA-Z])', r'\1*\2', cleaned_text)
    # Regex to insert '*' between a letter and a digit (e.g., x3 -> x*3)
    cleaned_text = re.sub(r'([a-zA-Z])([0-9])', r'\1*\2', cleaned_text)
    # Regex to insert '*' between two letters (e.g., xy -> x*y)
    cleaned_text = re.sub(r'([a-zA-Z])([a-zA-Z])', r'\1*\2', cleaned_text)
    # Regex to insert '*' before a parenthesis (e.g., 2(x+1) -> 2*(x+1))
    cleaned_text = re.sub(r'(\d)([([{])', r'\1*\2', cleaned_text)
    cleaned_text = re.sub(r'([a-zA-Z])([([{])', r'\1*\2', cleaned_text)

    # 5. Strip any remaining invalid characters that might confuse SymPy
    # Allow numbers, letters, +, -, *, /, =, ., (, ), [, ]
    cleaned_text = re.sub(r'[^0-9a-zA-Z\+\-\*/=\.()\[\]]', '', cleaned_text)

    return cleaned_text

def upload_image(request):
    result = None
    steps = []
    form = EquationImageForm() # Initialize form outside if/else for GET requests

    if request.method == 'POST':
        form = EquationImageForm(request.POST, request.FILES)
        manual_input = request.POST.get("manual_equation", "").strip()

        # Prioritize manual input if provided
        if manual_input:
            equations_to_process = [manual_input]
            steps.append("📝 Using Manual Input.")
        elif form.is_valid(): # Only process image if no manual input and form is valid
            obj = form.save()
            img_path = obj.image.path
            
            try:
                processed_path = preprocess_image(img_path)
                raw_text = pytesseract.image_to_string(processed_path)
                steps.append(f"📷 Raw OCR Output from Processed Image:\n`{raw_text.strip()}`")
                
                # Split raw OCR text by common delimiters (newline, semicolon, comma)
                equations_to_process = [eq.strip() for eq in re.split(r'\n|;|,', raw_text) if eq.strip()]
                if not equations_to_process:
                    steps.append("⚠️ OCR produced no recognizable equations.")
                    result = "No equations detected in the image."
                    return render(request, 'solver/upload.html', {'form': form, 'result': result, 'steps': steps})

            except FileNotFoundError as e:
                steps.append(f"❌ Error: {e}. Ensure image file exists.")
                result = "Error processing image: File not found."
                return render(request, 'solver/upload.html', {'form': form, 'result': result, 'steps': steps})
            except pytesseract.TesseractNotFoundError:
                steps.append("❌ Error: Tesseract is not installed or not in your PATH. Please see server logs.")
                result = "OCR engine (Tesseract) not found. Check server setup."
                return render(request, 'solver/upload.html', {'form': form, 'result': result, 'steps': steps})
            except Exception as e:
                steps.append(f"❌ Unexpected Error during image processing/OCR: {e}")
                result = f"An error occurred during image processing: {e}"
                return render(request, 'solver/upload.html', {'form': form, 'result': result, 'steps': steps})
        else:
            steps.append("⚠️ Please provide either an image or manual input.")
            result = "Invalid form submission. Please check your inputs."
            return render(request, 'solver/upload.html', {'form': form, 'result': result, 'steps': steps})
            
        # Define common symbols (can be expanded based on expected input)
        # It's better to define symbols dynamically based on what's in the equation
        # but for common cases like 'x', it's good to pre-define.
        x, y, z, a, b, c = symbols('x y z a b c')
        # Create a dictionary of available symbols for parse_expr
        local_vars = {s.name: s for s in [x, y, z, a, b, c]}

        # Define transformations for robust parsing with parse_expr
        # implicit_multiplication_application is crucial for '3x' -> '3*x'
        # convert_xor is useful if OCR outputs '^' instead of '**' (though you replace it too)
        transformations = (standard_transformations +
                           (implicit_multiplication_application, convert_xor,))

        results = []

        for raw_eq in equations_to_process:
            if not raw_eq.strip(): # Skip empty strings after splitting
                continue

            cleaned_eq = clean_ocr_output(raw_eq)
            
            # Add cleaned equation to steps before attempting SymPy parsing
            steps.append(f"🔄 Cleaned Text for Parsing: `{cleaned_eq}`")

            try:
                # Ensure '=' exists before splitting
                if '=' not in cleaned_eq:
                    # If no '=', assume it's an expression to be set to 0
                    parsed_expr = parse_expr(cleaned_eq, transformations=transformations, local_dict=local_vars)
                    sym_eq = Eq(parsed_expr, 0)
                    steps.append(f"➡️ Interpreted as: \\({parsed_expr}\\) = 0")
                else:
                    lhs_str, rhs_str = cleaned_eq.split('=', 1) # Split only on the first '='
                    parsed_lhs = parse_expr(lhs_str, transformations=transformations, local_dict=local_vars)
                    parsed_rhs = parse_expr(rhs_str, transformations=transformations, local_dict=local_vars)
                    sym_eq = Eq(parsed_lhs, parsed_rhs)
                    steps.append(f"➡️ Parsed Equation: \\({parsed_lhs}\\) = \\({parsed_rhs}\\)")

                # Identify symbols in the parsed equation to solve for
                # This makes it more flexible than just solving for 'x'
                symbols_in_eq = list(sym_eq.free_symbols)
                
                if not symbols_in_eq:
                    steps.append(f"🤷 No variables found in equation `{sym_eq}`. Cannot solve.")
                    results.append({str(sym_eq): "No variables to solve for."})
                    continue
                
                # For simplicity, if multiple symbols, we'll try to solve for the first one found
                # For complex systems, `solve` can take a list of variables or a system of equations
                variable_to_solve = symbols_in_eq[0] 
                steps.append(f"🔍 Attempting to solve for: \\({variable_to_solve}\\)")
                
                sol = solve(sym_eq, variable_to_solve)

                # Convert solutions to numerical approximations (N) for display, if they are not exact
                numerical_sol = [N(s, 4) for s in sol] # N(expression, number_of_digits)

                steps.append(f"✅ Solution found: \\({sol}\\) (Numerical: \\({numerical_sol}\\))")
                results.append({str(sym_eq): numerical_sol})

            except Exception as e:
                steps.append(f"❌ Error processing equation `{raw_eq}` (Cleaned: `{cleaned_eq}`): {type(e).__name__}: {e}")

        result = results if results else "No valid equations solved."

    return render(request, 'solver/upload.html', {
        'form': form,
        'result': result,
        'steps': steps,
    })
