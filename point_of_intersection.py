from tkinter import *       # Library for GUI
import tkinter.messagebox
import main_classes
import matrix_arithmetics
import os       # Allows creating folders and deleting files

# Attributes starting with .__ are private and ._ are protected

# Global Variables for File Directory
STR_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STR_SUBDIR = 'Matrices'


# Class to display entry widgets to input a 2x2 arrangement
class PointOfIntersection2x2(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Point of Intersection - 2x2')
        self._window = windows
        self.__frame_equations = Frame(self._window, bg='#d6faff')
        self.register = self._window.register(self.correct_input_matrix)
        self.validate_commands = (self.register, '%S')

    # Method to print entry wigets to input equation
    def print_point_of_intersection(self):
        self.print_layout()
        self._window.configure(bg='#d6faff')
        self.__frame_equations.pack()
        # Dictionary used to identify each individual entry widget
        list_of_dictionarys = []
        for i in range(2):
            dictionary_entry_widgets = {}
            frame_equation = Frame(self.__frame_equations, bg='#d6faff')
            frame_equation.pack(padx=5, pady=5)
            entry_x = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=6, validate="key", validatecommand=self.validate_commands)
            entry_x.pack(side=LEFT)
            label_x = Label(frame_equation, text=' x ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_x.pack(side=LEFT)
            label_plus_sign_1 = Label(frame_equation, text=' + ', font='Times 12 bold', bg='#d6faff', fg='#000033')
            label_plus_sign_1.pack(side=LEFT)
            entry_y = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=6, validate="key", validatecommand=self.validate_commands)
            entry_y.pack(side=LEFT)
            label_y = Label(frame_equation, text=' y ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_y.pack(side=LEFT)
            label_equal_sign = Label(frame_equation, text='  =  ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_equal_sign.pack(side=LEFT)
            entry_answer = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=4, validate="key", validatecommand=self.validate_commands)
            entry_answer.pack(side=LEFT)
            dictionary_entry_widgets['x'] = entry_x
            dictionary_entry_widgets['y'] = entry_y
            dictionary_entry_widgets['answer'] = entry_answer
            list_of_dictionarys.append(dictionary_entry_widgets)
        button_submit = Button(self._window, fg='#d6faff', bg='#000033', font='Times 10 bold', text='Submit',
                               command=lambda: self.submit(list_of_dictionarys))
        button_submit.pack(side=RIGHT, padx=(0, 5), pady=5,)

    # Method to retrieve the values inputted in entry widgets
    def submit(self, list_of_dictionary):
        # Left side of equation is stored a 2x2 matrix
        matrix_equation = []
        # Right side of equation is stored a 2x1 matrix
        matrix_answers = []
        list_matrix_equation = []
        list_matrix_answer = []
        correct = True
        try:
            for i in range(2):
                # Find entry widget value using key and stores it in a 1d array
                equation_1 = list_of_dictionary[i]
                entry_x = equation_1['x']
                list_matrix_equation.append(float(entry_x.get()))
                entry_y = equation_1['y']
                list_matrix_equation.append(float(entry_y.get()))
                entry_answer = equation_1['answer']
                list_matrix_answer.append(float(entry_answer.get()))
        except ValueError:
            # Error Message if the values cannot be converted into a float
            msgbox_error = tkinter.messagebox.showerror('Not a valid number', 'Please Re Enter the Values')
            correct = False

        # converts 1d array into a 2d array (matrix)
        if correct == True:
            i = 0
            for row in range(2):
                current_row = []
                for column in range(2):
                    current_row.append(list_matrix_equation[i])
                    i = i + 1
                matrix_equation.append(current_row)

            i = 0
            for row in range(2):
                current_row = []
                for column in range(1):
                    current_row.append(list_matrix_answer[i])
                    i = i + 1
                matrix_answers.append(current_row)
            # Calculates the point of intersection
            object_coordinates = CalculatePointOfIntersection(matrix_answers, matrix_equation)
            answer, coordinates, inverse, matrix_equations, matrix_answers, determinant = \
                object_coordinates.calculate_point_of_intersection_result_2x2()
            # Opens the answer matrix
            self.open_result(answer, coordinates, inverse, matrix_equations, matrix_answers, determinant)

    # Method to open answer matrix and worked solutions
    @staticmethod
    def open_result(answer, result, inverse, matrix_equations, matrix_answers, determinant):
        object_row_column = main_classes.CheckMatrixRowColumn(matrix_equations)
        rows = object_row_column.get_rows()
        columns = object_row_column.get_columns()
        object_show_result = CalculatePointOfIntersection(matrix_equations, matrix_answers)
        # Checks determinant is not 0
        if answer == True:
            object_show_result.print_result(result)
            # Opens worked solutions
            object_show_solution = DisplayPointOfIntersectionSolution(result, inverse, matrix_equations,
                                                                      matrix_answers, determinant)
            object_show_solution.print_layout()
        else:
            pass

    # Method to validate user input as they input it live
    @staticmethod
    def correct_input_matrix(user_input):
        object_validation = main_classes.Validation
        if object_validation.float_active(user_input) == True:
            return True
        else:
            return False


# Class to display entry widgets to input a 3x3 arrangement
# Exactly the same as 2x2 but z values are considered
class PointOfIntersection3x3(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Point of Intersection - 3x3')
        self._window = windows
        self.__frame_equations = Frame(self._window, bg='#d6faff')
        self.register = self._window.register(self.correct_input_matrix)
        self.validate_commands = (self.register, '%S')

    def print_point_of_intersection(self):
        self.print_layout()
        self._window.configure(bg='#d6faff')
        self.__frame_equations.pack()
        list_of_dictionarys = []
        for i in range(3):
            dictionary_entry_widgets = {}
            frame_equation = Frame(self.__frame_equations, bg='#d6faff')
            frame_equation.pack(padx=5, pady=5)
            entry_x = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=6, validate="key",
                            validatecommand=self.validate_commands)
            entry_x.pack(side=LEFT)
            label_x = Label(frame_equation, text=' x ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_x.pack(side=LEFT)
            label_plus_sign_1 = Label(frame_equation, text=' + ', font='Times 12 bold', bg='#d6faff', fg='#000033')
            label_plus_sign_1.pack(side=LEFT)
            entry_y = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=6, validate="key",
                            validatecommand=self.validate_commands)
            entry_y.pack(side=LEFT)
            label_y = Label(frame_equation, text=' y ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_y.pack(side=LEFT)
            label_plus_sign_2 = Label(frame_equation, text=' + ', font='Times 12 bold', bg='#d6faff', fg='#000033')
            label_plus_sign_2.pack(side=LEFT)
            entry_z = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=6, validate="key", validatecommand=self.validate_commands)
            entry_z.pack(side=LEFT)
            label_z = Label(frame_equation, text=' z ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_z.pack(side=LEFT)
            label_equal_sign = Label(frame_equation, text='  =  ', font='Times 14 bold', bg='#d6faff', fg='#000033')
            label_equal_sign.pack(side=LEFT)
            entry_answer = Entry(frame_equation, font='Times 14 bold', fg='#000033', width=4, validate="key", validatecommand=self.validate_commands)
            entry_answer.pack(side=LEFT)
            dictionary_entry_widgets['x'] = entry_x
            dictionary_entry_widgets['y'] = entry_y
            dictionary_entry_widgets['z'] = entry_z
            dictionary_entry_widgets['answer'] = entry_answer
            list_of_dictionarys.append(dictionary_entry_widgets)
        button_submit = Button(self._window, fg='#d6faff', bg='#000033', font='Times 10 bold', text='Submit',
                               command=lambda: self.submit(list_of_dictionarys))
        button_submit.pack(side=RIGHT, padx=(0,5), pady=5)

    def submit(self, list_of_dictionary):
        matrix_equation = []
        matrix_answers = []
        list_matrix_equation = []
        list_matrix_answer = []
        correct = True
        try:
            for i in range(3):
                equation_1 = list_of_dictionary[i]
                entry_x = equation_1['x']
                list_matrix_equation.append(int(entry_x.get()))
                entry_y = equation_1['y']
                list_matrix_equation.append(int(entry_y.get()))
                entry_z = equation_1['z']
                list_matrix_equation.append(int(entry_z.get()))
                entry_answer = equation_1['answer']
                list_matrix_answer.append(int(entry_answer.get()))
        except ValueError:
            msgbox_error = tkinter.messagebox.showerror('Not a valid number', 'Please Re Enter the Values')
            correct = False

        if correct == True:
            i = 0
            for row in range(3):
                current_row = []
                for column in range(3):
                    current_row.append(list_matrix_equation[i])
                    i = i + 1
                matrix_equation.append(current_row)

            i = 0
            for row in range(3):
                current_row = []
                for column in range(1):
                    current_row.append(list_matrix_answer[i])
                    i = i + 1
                matrix_answers.append(current_row)
            object_coordinates = CalculatePointOfIntersection(matrix_answers, matrix_equation)
            answer, coordinates, inverse, matrix_equations, matrix_answers,  determinant = object_coordinates.calculate_point_of_intersection_result_3x3()
            self.open_result(answer, coordinates, inverse, matrix_equations, matrix_answers,  determinant)

    @staticmethod
    def open_result(answer, result, inverse, matrix_equations, matrix_answers, determinant):
        object_show_result = CalculatePointOfIntersection(matrix_equations, matrix_answers)
        if answer == True:
            object_show_result.print_result(result)
            object_show_solution = DisplayPointOfIntersectionSolution(result, inverse, matrix_equations, matrix_answers, determinant)
            object_show_solution.print_layout()
        else:
            pass


    @staticmethod
    def correct_input_matrix(user_input):
        object_validation = main_classes.Validation
        if object_validation.float_active(user_input) == True:
            return True
        else:
            return False


# Class to calculate the coordinates for point of intersection
class CalculatePointOfIntersection:
    def __init__(self, matrix_answers, matrix_equations):
        self.__matrix_answers = matrix_answers
        self.__matrix_equations = matrix_equations

    # Method to calculate point of intersection for a 3x3
    def calculate_point_of_intersection_result_3x3(self):
        # Calculates the determinant using CalculateDeterminant class
        object_get_determinant = matrix_arithmetics.CalculateDeterminant(self.__matrix_equations)
        determinant = object_get_determinant.calculate_determinant_result_3x3(self.__matrix_equations)
        # Checks to see if the determinant is not 0 before calculating
        if determinant == 0:
            self.no_inverse(3)
            return False, [], [], [], [], 0
        else:
            # Calculates the inverse for intersection formula
            object_get_inverse = matrix_arithmetics.CalculateInverse(self.__matrix_equations)
            answer, inverse, determinants, list_of_minors, matrix_of_cofactors, adjoint_matrix = \
                object_get_inverse.calculate_inverse_result_3x3(self.__matrix_equations, 3, 3)
            # Multiplies the inverse of the left and the right side (answer matrix)
            list_of_matrices = [inverse, self.__matrix_answers]
            object_multiply = matrix_arithmetics.CalculateMultiplication(list_of_matrices)
            object_multiply.calculate_multiplication_result(3, 1)
            # Coordinates is the result of the multiplication
            coordinates, boolean = object_multiply.get_result()
            return True, coordinates, inverse, self.__matrix_equations, self.__matrix_answers,  determinant

    # Method to calculate point of intersection for a 2x2
    # Same as 3x3
    def calculate_point_of_intersection_result_2x2(self):
        object_get_determinant = matrix_arithmetics.CalculateDeterminant(self.__matrix_equations)
        determinant = object_get_determinant.calculate_determinant_result_2x2()
        if determinant == 0:
            self.no_inverse(2)
            return False, [], [], [], [], 0
        else:
            object_get_inverse = matrix_arithmetics.CalculateInverse(self.__matrix_equations)
            answer, inverse, determinants, list_of_minors = object_get_inverse.calculate_inverse_result_2x2()
            list_of_matrices = [inverse, self.__matrix_answers]
            object_multiply = matrix_arithmetics.CalculateMultiplication(list_of_matrices)
            object_multiply.calculate_multiplication_result(2, 1)
            coordinates, boolean = object_multiply.get_result()
            return True, coordinates, inverse, self.__matrix_equations, self.__matrix_answers, determinant

    # Method to print the answer matrix
    def print_result(self, result):
        object_row_column = main_classes.CheckMatrixRowColumn(result)
        rows = object_row_column.get_rows()
        columns = object_row_column.get_columns()
        object_open_entry_matrix = main_classes.SaveMatrixResult(rows, columns, result)
        object_open_entry_matrix.print_layout()

    # Method to show error that there is no point of intersection
    def no_inverse(self, rows):
        # There maybe other forms of intersection for a 3x3
        if rows == 3:
            string = 'The determinant is 0 so there is no inverse meaning there is no singular point of intersection.' \
                     ' However you can use simultaneus equations to check if it forms a sheaf and if there is not' \
                     ' then it is a triangular prism '
            messagebox_determinat = tkinter.messagebox.showinfo(
                'No Inverse', string)
        if rows == 2:
            string = 'The determinant is 0 so there is no inverse meaning there is no singular point of intersection.'
            messagebox_determinat = tkinter.messagebox.showinfo(
                'No Inverse', string)


# Class to calculate the coordinates for point of intersection
class DisplayPointOfIntersectionSolution:
    def __init__(self, result, inverse, matrix_equations, matrix_answers, determinant ):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__equation_matrix = matrix_equations
        self.__answers_matrix = matrix_answers
        self.__inverse_matrix = inverse
        self.__result_matrix = result
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_1 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_2 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_3 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_4 = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033', bg='#d6faff')

    def print_layout(self):
        self.__label_solution.pack()
        self.__frame_matrices_sum.pack(pady=5)
        object_check_row_column = main_classes.CheckMatrixRowColumn(self.__equation_matrix)
        equation_rows = object_check_row_column.get_rows()
        equation_columns = object_check_row_column.get_columns()
        object_grids = main_classes.GetMatrixToTextFile(self.__equation_matrix, equation_rows, equation_columns)
        i = 0
        frame_matrices_equations = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices_equations.pack(side=LEFT)
        for row in range(equation_rows):
            for column in range(equation_columns):
                number = self.__equation_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_equations, number, row, column,
                                                        self.validate_commands)
                i = i + 1

        label_times_sign = Label(self.__frame_matrices_sum, text=' x ', font='Times 10 bold', bg='#d6faff')
        label_times_sign.pack(side=LEFT)

        xyz = []
        if equation_rows == 3:
            xyz = [['x'], ['y'], ['z']]
        elif equation_rows == 2:
            xyz = [['x'], ['y']]
        else:
            pass
        xyz_rows = len(xyz)
        xyz_columns = len(xyz[0])
        frame_matrices_xyz = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices_xyz.pack(side=LEFT, padx=(5, 2))
        for row in range(xyz_rows):
            for column in range(xyz_columns):
                number = xyz[row][column]
                text = StringVar(frame_matrices_xyz, value=number)
                label_sum = Label(frame_matrices_xyz, textvariable=text, font='Times 16 bold', bg='white')
                label_sum.grid(row=row, column=column, padx=5, pady=5)

        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)

        object_check_row_column = main_classes.CheckMatrixRowColumn(self.__answers_matrix)
        answers_rows = object_check_row_column.get_rows()
        answers_columns = object_check_row_column.get_columns()
        object_grids = main_classes.GetMatrixToTextFile(self.__answers_matrix, answers_rows, answers_columns)
        frame_matrices_answers = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices_answers.pack(side=LEFT)
        for row in range(answers_rows):
            for column in range(answers_columns):
                number = self.__answers_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_answers, number, row, column,
                                                        self.validate_commands)


        self.__frame_extra_solutions_1.pack(pady=(10, 10))
        object_check_row_column = main_classes.CheckMatrixRowColumn(self.__inverse_matrix)
        inverse_rows = object_check_row_column.get_rows()
        inverse_columns = object_check_row_column.get_columns()
        object_grids = main_classes.GetMatrixToTextFile(self.__inverse_matrix, inverse_rows, inverse_columns)
        i = 0
        frame_matrices_inverse = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
        frame_matrices_inverse.pack(side=LEFT)
        for row in range(equation_rows):
            for column in range(equation_columns):
                number = self.__inverse_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_inverse, number, row, column,
                                                        self.validate_commands)
                i = i + 1

        label_times_sign = Label(self.__frame_extra_solutions_1, text=' x ', font='Times 10 bold', bg='#d6faff')
        label_times_sign.pack(side=LEFT)
        object_grids = main_classes.GetMatrixToTextFile(self.__equation_matrix, equation_rows, equation_columns)
        i = 0
        frame_matrices_equations = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
        frame_matrices_equations.pack(side=LEFT)
        for row in range(equation_rows):
            for column in range(equation_columns):
                number = self.__equation_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_equations, number, row, column,
                                                        self.validate_commands)
                i = i + 1

        label_times_sign = Label(self.__frame_extra_solutions_1, text=' x ', font='Times 10 bold', bg='#d6faff')
        label_times_sign.pack(side=LEFT)

        frame_matrices_xyz = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
        frame_matrices_xyz.pack(side=LEFT, padx=(5, 2))
        for row in range(xyz_rows):
            for column in range(xyz_columns):
                number = xyz[row][column]
                text = StringVar(frame_matrices_xyz, value=number)
                label_sum = Label(frame_matrices_xyz, textvariable=text, font='Times 16 bold', bg='white')
                label_sum.grid(row=row, column=column, padx=5, pady=5)

        label_equal_sign = Label(self.__frame_extra_solutions_1, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)

        object_grids = main_classes.GetMatrixToTextFile(self.__inverse_matrix, inverse_rows, inverse_columns)
        i = 0
        frame_matrices_inverse = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
        frame_matrices_inverse.pack(side=LEFT)
        for row in range(equation_rows):
            for column in range(equation_columns):
                number = self.__inverse_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_inverse, number, row, column,
                                                        self.validate_commands)
                i = i + 1

        label_times_sign = Label(self.__frame_extra_solutions_1, text=' x ', font='Times 10 bold', bg='#d6faff')
        label_times_sign.pack(side=LEFT)

        object_grids = main_classes.GetMatrixToTextFile(self.__answers_matrix, answers_rows, answers_columns)
        frame_matrices_answers = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
        frame_matrices_answers.pack(side=LEFT)
        for row in range(answers_rows):
            for column in range(answers_columns):
                number = self.__answers_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_answers, number, row, column,
                                                        self.validate_commands)

        self.__frame_extra_solutions_2.pack(pady=10)
        frame_matrices_xyz = Frame(self.__frame_extra_solutions_2, bg='#d6faff')
        frame_matrices_xyz.pack(side=LEFT, padx=(5, 2))
        for row in range(xyz_rows):
            for column in range(xyz_columns):
                number = xyz[row][column]
                text = StringVar(frame_matrices_xyz, value=number)
                label_sum = Label(frame_matrices_xyz, textvariable=text, font='Times 16 bold', bg='white')
                label_sum.grid(row=row, column=column, padx=5, pady=5)

        label_equal_sign = Label(self.__frame_extra_solutions_2, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)

        object_check_row_column = main_classes.CheckMatrixRowColumn(self.__result_matrix)
        result_rows = object_check_row_column.get_rows()
        result_columns = object_check_row_column.get_columns()
        object_grids = main_classes.GetMatrixToTextFile(self.__result_matrix, result_rows, result_columns)
        frame_matrices_result = Frame(self.__frame_extra_solutions_2, bg='#d6faff')
        frame_matrices_result.pack(side=LEFT)
        for row in range(result_rows):
            for column in range(result_columns):
                number = self.__result_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices_result, number, row, column,
                                                        self.validate_commands)


    @staticmethod
    def validate_commands():
        return True


# Class to display Point of Intersection Layout
class PointOfIntersectionLayout(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Point of Intersection')
        self._window = windows
        self.__button_2x2 = Button(self._window, text='2x2', font='Times 18 bold',
                                       fg='#d6faff', bg='#000033', width=8, command=self.open_2x2)
        self.__button_3x3 = Button(self._window, text='3x3', font='Times 18 bold',
                                           fg='#d6faff', bg='#000033', width=8, command=self.open_3x3)

    # Prints layout of points of intersection menu
    def print_geometrical_arrangement(self):
        self.__button_2x2.pack(side=LEFT, expand=1, padx=(0,2), pady=3)
        self.__button_3x3.pack(side=RIGHT, expand=1, padx=(2,0), pady=3)

    # Method to open 2x2 arrangement
    def open_2x2(self):
        self._window.destroy()
        window_2x2 = Tk()
        object_2x2 = PointOfIntersection2x2(window_2x2)
        object_2x2.print_point_of_intersection()

    # Method to open 3x3 arrangement
    def open_3x3(self):
        self._window.destroy()
        window_3x3 = Tk()
        object_3x3 = PointOfIntersection3x3(window_3x3)
        object_3x3.print_point_of_intersection()


def run():
    root = Tk()
    object_main_program = PointOfIntersectionLayout(root)
    object_main_program.print_layout()
    object_main_program.print_geometrical_arrangement()
    root.mainloop()
    return root
