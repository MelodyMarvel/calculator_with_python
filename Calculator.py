import tkinter as tk
import math

LARGE_FONT_STYLE = ("Ariel", 40, "bold")
SMALL_FONT_STYLE = ("Ariel", 16)
DIGITS_FONT_STYLE = ("Ariel", 24, "bold")
DEFAULT_FONT_STYLE = ("Ariel", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


def log_function_call(func):
    def wrapper(*args, **kwargs):
        print(f'calling function: {func.__name__}')
        return func(*args, **kwargs)
    return wrapper

class Calculator:
    current_operator = None

    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(0,0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            ")": (4, 2), "(": (4, 1), 0: (4, 3), '.': (5, 3)
        }

        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+", "%": "%"} #unique code for the operator symbols
        self.buttons_frame = self.create_buttons_frame()

        for x in range(1, 5): #This loop helps our rows and columns to expand
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digits_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.current_num = None

    @log_function_call
    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_log_button()

    @log_function_call
    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E,
                               bg=LIGHT_BLUE, fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E,
                               bg=LIGHT_GRAY, fg=LABEL_COLOR, padx=4, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    @log_function_call
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    @log_function_call
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    @log_function_call
    def create_digits_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    @log_function_call
    def append_operator(self, operator):
        if operator == "log":
            try:
                result = math.log10(float(self.current_expression))
                self.current_expression = str(result)
                # self.total_expression += self.current_expression
                # self.current_expression = ""
                self.update_total_label()
                self.update_label()
            except ValueError:
                self.current_expression = "Error"
                self.update_label()
        else:
            self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression = ""
            self.update_total_label()
            self.update_label()

    @log_function_call
    def create_operator_buttons(self):
        i=0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    @log_function_call
    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    @log_function_call
    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    @log_function_call
    def sqrt(self):
        self.current_expression = str(eval(self.current_expression) ** 0.5)
        self.update_label()

    @log_function_call
    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    @log_function_call
    def square(self):
        self.current_expression = str(eval(self.current_expression)**2)
        self.update_label()

    @log_function_call
    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    @log_function_call
    def create_log_button(self):
        button = tk.Button(self.buttons_frame, text="log", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=lambda: self.append_operator("log"))
        button.grid(row=5, column=4, sticky=tk.NSEW)

    @log_function_call
    def evaluate(self):
        try:
            if self.current_operator == "log":
                result = math.log10(float(self.current_num))
                self.current_expression = str(result)
            else:
                expression = self.total_expression + self.current_expression
                result = eval(expression)
                self.current_expression = str(result)
                self.total_expression = ""  # Clear the total_expression for continuous calculations
        except Exception as e:
            self.current_expression = "Error"
            result = None
        finally:
            self.update_total_label()
            self.update_label()

    @log_function_call
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, height=2,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=5, column=1, columnspan=2, sticky=tk.NSEW)


    @log_function_call
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    @log_function_call
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    @log_function_call
    def update_label(self):
        self.label.config(text=self.current_expression[:9])

    def run(self): # Creating a function to start te calculator app
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()  # Creates an instance of the Calculator class
    calc.run()  # Run the calculator application logic