from tkinter import *       # Library for GUI
import tkinter.messagebox
import main_classes
import os       # Allows creating folders and deleting files

# Attributes starting with .__ are private and ._ are protected

# Global Variables for File Directory
STR_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
STR_SUBDIR = 'Matrices'


# Class to display the addition menu when chosen in matrix arithmetic
# Inherits parent class App from main_classes
class Addition(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Addition')
        self.__matrix_chosen_files = []
        self._window_addition = windows
        self.__frame_messagebox = Frame(self._window_addition, height=10, width=500,)
        self._messagebox_addition_sum = Message(self._window_addition,  text='',  font='Times 14 bold', width=500)
        self.__bottomframe = Frame(self._window_addition, bg='#d6faff')
        self.__button_submit_sum = Button(self.__bottomframe, text='Submit', fg='#d6faff', bg='#000033',
                                          font='Times 10 bold', command=self.submit)
        self.__button_clear_sum = Button(self.__bottomframe, text='Clear', fg='#d6faff', bg='#000033',
                                         font='Times 10 bold', command=self.clear)
        self.__object_scan_files = main_classes.ScanFiles()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    # Method to print the addition menu
    def print_addition(self):
        #initializes the parent class method
        super().print_layout()
        self.__frame_messagebox.pack(fill=X)
        self._messagebox_addition_sum.pack(fill=BOTH)
        self.__bottomframe.pack(side=BOTTOM, pady=2)
        self.__button_clear_sum.pack(side=LEFT, padx=4, expand=1)
        self.__button_submit_sum.pack(side=LEFT, padx=4, expand=1)
        i = 0
        # prints matrix names as buttons
        for line in self.__matrix_list:
            # Removes the .txt from the matrix name
            matrix_name = line[:-4]
            text = StringVar(self._window_addition, value=matrix_name)
            button_matrix = Button(self._window_addition, textvariable=text, font='Times 18 bold',
                                   command=lambda matrix=matrix_name: self.add_chosen_matrix(matrix))
            button_matrix.pack(side=LEFT, padx=2, pady=2, expand=1)
            i = i + 1

    # method to add matrix when pressed to an array of all the matrices in the sum
    def add_chosen_matrix(self, matrix_name):
        text = ''
        # instantiates queue data structure from main_classes
        object_queue = main_classes.Queue(self.__matrix_chosen_files)
        # Adds each chosen matrix to the end of the queue
        object_queue.enqueue(matrix_name)
        for matrix in self.__matrix_chosen_files:
            text = text + ' ' + matrix + ' + '
        self._messagebox_addition_sum['text'] = text

    # method to clear the sum and empty the array
    def clear(self):
        self.__matrix_chosen_files =[]
        self._messagebox_addition_sum['text'] = ''

    def submit(self):
        try:
            # checks to see if all the matrices are the same size before calculating
            answer, rows, columns = self.check_sum_validity()
            if answer  == False:
                pass
            else:
                chosen_matrix = []
                object_queue = main_classes.Queue(chosen_matrix)
                for i in range(len(self.__matrix_chosen_files)):
                    object_queue.enqueue(self.__matrix_chosen_files[i])
                self.open_result(chosen_matrix, rows, columns)
        except TypeError:
            msgbox_error = tkinter.messagebox.showerror('Not a valid sum', 'Please try again')

    def check_sum_validity(self):
        rows = 0
        columns = 0
        valid_matrix = []
        chosen_matrix = []
        matrix_degree = 0
        for i in range(len(self.__matrix_chosen_files)):
            object_queue = main_classes.Queue(self.__matrix_chosen_files)
            # peeks the first matrix in the queue
            matrix = object_queue.peek()
            # instantiates object to retrieve row and column of a matrix
            object_check = main_classes.CheckMatrixRowColumn(matrix)
            rows = object_check.get_rows()
            columns = object_check.get_columns()
            # Matrix degree is the row x column
            # This is done for all matrices and compared with the original degree to see if they match
            matrix_degree = rows * columns
            valid_matrix.append(matrix_degree)
            chosen_matrix.append(matrix)
        for matrix in valid_matrix:
            if matrix_degree != matrix:
                msgbox_confirm_delete = tkinter.messagebox.showinfo(
                    'Invalid!', 'Make sure that all matrix have the same rows and columns')
                # calls clear method to reset sum
                self.clear()
                return False, rows, columns
            else:
                return True, rows, columns

    # Method to calculate sum, display the answer and display the worked solutions
    @staticmethod
    def open_result(matrix_list, rows, columns):
        object_show_result = CalculateAddition(matrix_list)
        object_show_result.calculate_addition_result(rows, columns)
        result = object_show_result.get_result()
        object_show_result.print_result(rows, columns, result)
        object_show_solution = DisplayAdditionSolution(matrix_list, rows, columns, result)
        object_show_solution.print_layout()


# Class to calculate addition of chosen matrices
class CalculateAddition:
    def __init__(self, matrix_list):
        self.__matrix_list = matrix_list
        self.__result = []

    def calculate_addition_result(self, rows, columns):
        # initializes 2d array for answer
        list_full_matrix = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                # Creates an answer matrix which is initialized with zero
                current_row.append(0.0)
            list_full_matrix.append(current_row)
        # copys the matrix sum queue as a list
        matrix_list_new = self.__matrix_list.copy()
        object_queue = main_classes.Queue(matrix_list_new)
        for i in range(len(self.__matrix_list)):
            # dequeues the queue which also returns the element
            matrix = object_queue.dequeue()
            # Instanciates class to convert text file to a 2d array
            object_array = main_classes.TextTo2dArray(matrix)
            next_matrix = object_array.convert()
            for row in range(rows):
                for column in range(columns):
                    # Converts current matrix and next matrix in the sums values to float
                    int1 = float(list_full_matrix[row][column])
                    int2 = float(next_matrix[row][column])
                    # Replaces the current matrices value with the sum
                    list_full_matrix[row][column] = int1 + int2
        self.__result = list_full_matrix

    # Method to get the result
    def get_result(self):
        return self.__result

    # Method to display the answer matrix
    def print_result(self,rows,columns,result):
        object_open_entry_matrix = main_classes.SaveMatrixResult(rows, columns, result)
        object_open_entry_matrix.print_layout()


# Class to display worked solutions for Matrix Addition
class DisplayAdditionSolution:
    def __init__(self, matrix_list, rows, columns, result):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__matrix_list = matrix_list
        self.__rows = rows
        self.__columns = columns
        self.__result = result
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033', bg='#d6faff')

    def print_layout(self):
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        for matrix_name in self.__matrix_list:
            filename_matrix = matrix_name + '.txt'
            filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
            text_file_matrix = open(filepath_matrix, 'r')
            lines = text_file_matrix.readlines()
            object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
            i = 0
            # Creates a frame for each matrix and covers it with entry widgets
            frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
            frame_matrices.pack(side=LEFT)
            for row in range(self.__rows):
                for column in range(self.__columns):
                    number = float(lines[i])
                    entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                            self.validate_commands)
                    i = i + 1
            label_plus_sign = Label(self.__frame_matrices_sum, text=' + ', font='Times 14 bold', bg='#d6faff')
            label_plus_sign.pack(side=LEFT)
        i = 0
        matrix_name = ''
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack()
        for row in range(self.__rows):
            for column in range(self.__columns):
                number = self.__result[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1

    @staticmethod
    def validate_commands():
        return True


# Class to display the subtraction menu when chosen in matrix arithmetic
# Similar to Addition class
class Subtraction(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Subtraction')
        self.__matrix_chosen_files = []
        self._window_subtraction = windows
        self.__frame_messagebox = Frame(self._window_subtraction, height=10, width=500, )
        self._messagebox_addition_sum = Message(self._window_subtraction, text='', font='Times 14 bold', width=500)
        self.__bottomframe = Frame(self._window_subtraction, bg='#d6faff')
        self.__button_submit_sum = Button(self.__bottomframe, text='Submit', fg='#d6faff', bg='#000033', font='Times 10 bold', command=self.submit)
        self.__button_clear_sum = Button(self.__bottomframe, text='Clear', fg='#d6faff', bg='#000033', font='Times 10 bold', command=self.clear)
        self.__object_scan_files = main_classes.ScanFiles()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    def print_subtraction(self):
        super().print_layout()
        self.__frame_messagebox.pack(fill=X)
        self._messagebox_addition_sum.pack(fill=BOTH)
        self.__bottomframe.pack(side=BOTTOM, pady=2)
        self.__button_clear_sum.pack(side=LEFT, padx=4, expand=1)
        self.__button_submit_sum.pack(side=LEFT, padx=4, expand=1)
        i = 0
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            text = StringVar(self._window_subtraction, value=matrix_name)
            button_matrix = Button(self._window_subtraction, textvariable=text, font='Times 18 bold', command=lambda matrix=matrix_name: self.add_chosen_matrix(matrix))
            button_matrix.pack(side=LEFT, padx=2, pady=2, expand=1)
            i = i + 1

    def add_chosen_matrix(self, matrix_name):
        text = ''
        self.__matrix_chosen_files.append(matrix_name)
        for matrix in self.__matrix_chosen_files:
            text = text + ' ' + matrix + ' - '
        self._messagebox_addition_sum['text'] = text

    def clear(self):
        self.__matrix_chosen_files =[]
        self._messagebox_addition_sum['text'] = ''

    def submit(self):
        try:
            answer, rows, columns = self.check_sum_validity()
            if answer  == False:
                pass
            else:
                chosen_matrix = []
                object_queue = main_classes.Queue(chosen_matrix)
                for i in range(len(self.__matrix_chosen_files)):
                    object_queue.enqueue(self.__matrix_chosen_files[i])
                self.open_result(chosen_matrix, rows, columns)
        except TypeError:
            msgbox_error = tkinter.messagebox.showerror('Not a valid sum', 'Please try again')

    def check_sum_validity(self):
        rows = 0
        columns = 0
        valid_matrix = []
        chosen_matrix = []
        matrix_degree = 0
        for i in range(len(self.__matrix_chosen_files)):
            object_queue = main_classes.Queue(self.__matrix_chosen_files)
            matrix = object_queue.peek()
            object_check = main_classes.CheckMatrixRowColumn(matrix)
            rows = object_check.get_rows()
            columns = object_check.get_columns()
            matrix_degree = rows * columns
            valid_matrix.append(matrix_degree)
            chosen_matrix.append(matrix)
        for matrix in valid_matrix:
            if matrix_degree != matrix:
                msgbox_confirm_delete = tkinter.messagebox.showinfo(
                    'Invalid!', 'Make sure that all matrix have the same rows and columns')
                self.clear()
                return False, rows, columns
            else:
                return True, rows, columns

    @staticmethod
    def open_result(matrix_list, rows, columns):
        object_show_result = CalculateSubtraction(matrix_list)
        object_show_result.calculate_subtraction_result(rows, columns)
        result = object_show_result.get_result()
        object_show_result.print_result(rows, columns, result)
        object_show_solution = DisplaySubtractionSolution(matrix_list, rows, columns, result)
        object_show_solution.print_layout()


# Class to calculate subtraction of chosen matrices
# Similar to CalculateAddition class
class CalculateSubtraction:
    def __init__(self, matrix_list):
        self.__matrix_list = matrix_list
        self.__result = []

    def calculate_subtraction_result(self, rows, columns):
        list_full_matrix = []
        list_start_matrix_name = self.__matrix_list[0]
        object_array = main_classes.TextTo2dArray(list_start_matrix_name)
        list_start_matrix = object_array.convert()
        for row in range(rows):
            current_row = []
            for column in range(columns):
                current_row.append(0.0)
            list_full_matrix.append(current_row)
        for row in range(rows):
            for column in range(columns):
                # Replaces the answer matrix with the first matrix
                list_full_matrix[row][column] = list_start_matrix[row][column]
        # Queue now starts from second element
        self.__matrix_list = self.__matrix_list[1:]
        matrix_list_new = self.__matrix_list.copy()
        object_queue = main_classes.Queue(matrix_list_new)
        # Removes the first matrix before subtractions
        for i in range(len(self.__matrix_list)):
            matrix = object_queue.dequeue()
            object_array = main_classes.TextTo2dArray(matrix)
            next_matrix = object_array.convert()
            for row in range(rows):
                for column in range(columns):
                    int1 = float(list_full_matrix[row][column])
                    int2 = float(next_matrix[row][column])
                    list_full_matrix[row][column] = int1 - int2
        self.__result = list_full_matrix

    def get_result(self):
        return self.__result

    def print_result(self,rows,columns, result):
        object_open_entry_matrix = main_classes.SaveMatrixResult(rows, columns, result)
        object_open_entry_matrix.print_layout()


# Class to display worked solutions for Matrix Subtraction
# Similar to DisplayAdditionSolution class
class DisplaySubtractionSolution:
    def __init__(self, matrix_list, rows, columns, result):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__matrix_list = matrix_list
        self.__rows = rows
        self.__columns = columns
        self.__result = result
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033', bg='#d6faff')

    def print_layout(self):
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        for matrix_name in self.__matrix_list:
            filename_matrix = matrix_name + '.txt'
            filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
            text_file_matrix = open(filepath_matrix, 'r')
            lines = text_file_matrix.readlines()
            object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
            i = 0
            frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
            frame_matrices.pack(side=LEFT)
            for row in range(self.__rows):
                for column in range(self.__columns):
                    number = float(lines[i])
                    entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                            self.validate_commands)
                    i = i + 1
            label_plus_sign = Label(self.__frame_matrices_sum, text=' - ', font='Times 14 bold', bg='#d6faff')
            label_plus_sign.pack(side=LEFT)
        i = 0
        matrix_name = ''
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack()
        for row in range(self.__rows):
            for column in range(self.__columns):
                number = self.__result[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1

    @staticmethod
    def validate_commands():
        return True


# Class to display the subtraction menu when chosen in matrix arithmetic
# Similar to Addition class but has extra functionality
class Multiplication(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Multiplication')
        self.__matrix_chosen_files = []
        self._window_multiplication = windows
        self.__frame_messagebox = Frame(self._window_multiplication, height=10, width=500, )
        self._messagebox_multiplication_sum = Message(self._window_multiplication, text='', font='Times 14 bold', width=500)
        self.__bottomframe = Frame(self._window_multiplication, bg='#d6faff')
        self.__button_submit_sum = Button(self.__bottomframe, text='Submit', fg='#d6faff', bg='#000033',
                                          font='Times 10 bold', command=self.submit)
        self.__button_clear_sum = Button(self.__bottomframe, text='Clear', fg='#d6faff', bg='#000033',
                                         font='Times 10 bold', command=self.clear)
        self.__object_scan_files = main_classes.ScanFiles()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    def print_multiplication(self):
        super().print_layout()
        self.__frame_messagebox.pack(fill=X)
        self._messagebox_multiplication_sum.pack(fill=BOTH)
        self.__bottomframe.pack(side=BOTTOM, pady=2)
        self.__button_clear_sum.pack(side=LEFT, padx=4, expand=1)
        self.__button_submit_sum.pack(side=LEFT, padx=4, expand=1)
        i = 0
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            text = StringVar(self._window_multiplication, value=matrix_name)
            button_matrix = Button(self._window_multiplication, textvariable=text, font='Times 18 bold',
                                   command=lambda matrix=matrix_name: self.add_chosen_matrix(matrix))
            button_matrix.pack(side=LEFT, padx=2, pady=2, expand=1)
            i = i + 1

    def add_chosen_matrix(self, matrix_name):
        text = ''
        self.__matrix_chosen_files.append(matrix_name)
        for matrix in self.__matrix_chosen_files:
            text = text + ' ' + matrix + ' x '
        self._messagebox_multiplication_sum['text'] = text

    def clear(self):
        self.__matrix_chosen_files =[]
        self._messagebox_multiplication_sum['text'] = ''

    # Method to submit chosen matrices to be calculated
    def submit(self):
        try:
            chosen_matrix = []
            for matrix in self.__matrix_chosen_files:
                chosen_matrix.append(matrix)
            # Checks the first matrix's rows and last matrix's columns as the rows and columns for the answer matrix
            object_check_matrix1 = main_classes.CheckMatrixRowColumn(self.__matrix_chosen_files[0])
            rows = object_check_matrix1.get_rows()
            object_check_matrix2 = main_classes.CheckMatrixRowColumn(self.__matrix_chosen_files[-1])
            columns = object_check_matrix2.get_columns()
            self.open_result(chosen_matrix, rows, columns)
        except IndexError:
            # Error message if the user dosen't choose any matrices
            msgbox_error = tkinter.messagebox.showerror('Not a valid operation', 'Please try again')


    @staticmethod
    def open_result(matrix_list, result_rows, result_columns):
        # backup of chosen matrix list created as elements will be popped off when calculating
        matrix_list_bckup = matrix_list.copy()
        object_show_result = CalculateMultiplication(matrix_list)
        # Checks to see if the rows and columns of the first two matrices match before calculating
        answer, rows, columns = object_show_result.check_sum_validity(matrix_list)
        if answer == True:
            object_show_result.calculate_multiplication_result(rows, columns)
            result, second_answer = object_show_result.get_result()
            if second_answer == True:
                object_show_result.print_result(result_rows, result_columns, result)
                result_matrix = object_show_result.get_result_matrix()
                object_show_solution = DisplayMultiplicationSolution(matrix_list_bckup, result_rows, result_columns, result_matrix, result)
                object_show_solution.print_layout()


# Class to calculate subtraction of chosen matrices
class CalculateMultiplication:
    def __init__(self, matrix_list):
        self.__queue_matrices = matrix_list
        self.__matrix_chosen_files = []
        self.__result_matrix = []
        self.__count = len(self.__queue_matrices)
        self.__result = []
        self.__answer = True

    def check_sum_validity(self, matrix_list):
        valid_matrix_row = []
        valid_matrix_column = []
        chosen_matrix = []
        rows = 0
        columns = 0
        # Checks to see if the list is greater than one to prevent index errors
        if len(matrix_list) > 1:
            object_check_matrix1 = main_classes.CheckMatrixRowColumn(matrix_list[0])
            matrix1_column = object_check_matrix1.get_columns()
            object_check_matrix2 = main_classes.CheckMatrixRowColumn(matrix_list[1])
            matrix2_row = object_check_matrix2.get_rows()
            valid_matrix_row.append(matrix2_row)
            valid_matrix_column.append(matrix1_column)
            chosen_matrix.append(matrix_list[0])
            chosen_matrix.append(matrix_list[1])
            correct = True
            # For each two matrix pairs they need to have the same value for matrix1 rows and matrix2 columns
            if matrix1_column != matrix2_row:
                correct = False
                msgbox_confirm_delete = tkinter.messagebox.showinfo(
                    'Invalid!', 'Make sure that matrices dimensions are compatible for multiplication')
                self.__matrix_chosen_files.clear()
                return False, rows, columns
            if correct == True:
                object_check_matrix1 = main_classes.CheckMatrixRowColumn(matrix_list[0])
                rows = object_check_matrix1.get_rows()
                object_check_matrix2 = main_classes.CheckMatrixRowColumn(matrix_list[1])
                columns = object_check_matrix2.get_columns()
                return True, rows, columns
        return True, rows, columns

    def calculate_multiplication_result(self, rows, columns):
        list_full_matrix = []
        for row in range(rows):
            current_row = []
            for column in range(columns):
                # Creates initial 0 matrix
                current_row.append(0.0)
            list_full_matrix.append(current_row)
        # Converts both matrices text files to a 2d array
        try:
            object_array = main_classes.TextTo2dArray(self.__queue_matrices[0])
            first_matrix = object_array.convert()
        except TypeError:
            # Exception for if the matrix is already of an array and doesn't need to be converted
            first_matrix = self.__queue_matrices[0]
        try:
            object_array = main_classes.TextTo2dArray(self.__queue_matrices[1])
            second_matrix = object_array.convert()
        except TypeError:
            # Exception for if the matrix is already of an array and doesn't need to be converted
            second_matrix = self.__queue_matrices[1]
        # 3 for loops so program can pivot through a certain column and row rather than going from each row to column
        for row in range(rows):
            for column in range(columns):
                for i in range(len(second_matrix)):
                    # Calculates the value
                    sum_of_horizontal_and_vertical = (first_matrix[row][i] * second_matrix[i][column])
                    # Replaces the value in the answer Matrix
                    list_full_matrix[row][column] = round(list_full_matrix[row][column], 5)\
                        + round(sum_of_horizontal_and_vertical, 5)
        self.__result_matrix.append(list_full_matrix)
        # Initializes the queue
        next_list_for_queue = []
        object_queue = main_classes.Queue(self.__queue_matrices)
        # check to see the queue has more than 2 elements as recursion will fail
        if len(self.__queue_matrices) != 2:
            # DeQueues the first elements of the queue
            object_queue.dequeue()
            object_queue.dequeue()
            matrix_array_calculated_answer = list_full_matrix
            # high priority matrix that's added to the queue
            object_next_queue = main_classes.Queue(next_list_for_queue)
            # order for queue defined with matrix ordered in terms of priority
            object_next_queue.enqueue(matrix_array_calculated_answer)
            next_list_for_queue = next_list_for_queue + self.__queue_matrices
            self.__queue_matrices = next_list_for_queue
            # Checks matrix validity before attempting recursion
            self.__answer, rows, columns = self.check_sum_validity(next_list_for_queue)
            if self.__answer == True:
                if self.__count != 1:
                    # Recursion occurs
                    list_full_matrix = self.calculate_multiplication_result(rows, columns)
                self.__result = list_full_matrix
                self.__count = self.__count - 1
        self.__result = list_full_matrix
        return list_full_matrix

    # Method to return matrix answer
    def get_result_matrix(self):
        return self.__result_matrix

    # Method to get each specific answers for worked solutions
    def get_result(self):
        return self.__result, self.__answer

    # Method to open the reuslt matrix
    def print_result(self, rows, columns, result):
        object_open_entry_matrix = main_classes.SaveMatrixResult(rows, columns, result)
        object_open_entry_matrix.print_layout()


# Class to display worked solutions for Matrix Multiplication
# Small similarities to DisplayAdditionSolution class
class DisplayMultiplicationSolution:
    def __init__(self, matrix_list, result_rows, result_columns, result_matrix, result):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__matrix_list = matrix_list
        self.__new_list = []
        self.__rows = result_rows
        self.__columns = result_columns
        self.__result = result
        self.__result_matrix = result_matrix
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033'
                                      , bg='#d6faff')
        self.__label_no_solution = Label(self.__window_solution,
                                         text='**Worked solution below are only for the first two matrices**',
                                         font='Times 16 bold', fg='#ff0000', bg='#d6faff')

    def print_layout(self):
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        for matrix_name in self.__matrix_list:
            filename_matrix = matrix_name + '.txt'
            filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
            text_file_matrix = open(filepath_matrix, 'r')
            lines = text_file_matrix.readlines()
            object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
            i = 0
            frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
            frame_matrices.pack(side=LEFT)
            object_check = main_classes.CheckMatrixRowColumn(matrix_name)
            rows = object_check.get_rows()
            columns = object_check.get_columns()
            for row in range(rows):
                for column in range(columns):
                    number = float(lines[i])
                    entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                            self.validate_commands)
                    i = i + 1
            label_plus_sign = Label(self.__frame_matrices_sum, text=' x ', font='Times 14 bold', bg='#d6faff')
            label_plus_sign.pack(side=LEFT)
        i = 0
        matrix_name = ''
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack()
        for row in range(self.__rows):
            for column in range(self.__columns):
                number = self.__result[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1
        self.__new_list.append(self.__matrix_list[0])
        self.__new_list.append(self.__matrix_list[1])
        for k in range(len(self.__matrix_list) -2):
            self.__new_list.append(self.__result_matrix[k])
            self.__new_list.append(self.__matrix_list[k+2])
        if len(self.__matrix_list) > 2:
            self.__label_no_solution.pack()

        self.__frame_extra_solutions.pack(pady=15)
        object_check_matrix1 = main_classes.CheckMatrixRowColumn(self.__matrix_list[0])
        rows = object_check_matrix1.get_rows()
        object_check_matrix2 = main_classes.CheckMatrixRowColumn(self.__matrix_list[1])
        columns = object_check_matrix2.get_columns()
        object_array = main_classes.TextTo2dArray(self.__matrix_list[0])
        first_matrix = object_array.convert()
        object_array = main_classes.TextTo2dArray(self.__matrix_list[1])
        second_matrix = object_array.convert()

        list_times_across = []
        list_answer = []
        for row in range(rows):
            for column in range(columns):
                for i in range(len(second_matrix)):
                    list_answer.append((first_matrix[row][i] * second_matrix[i][column]))
                    #list_full_matrix[row][column] = list_full_matrix[row][column] + sum_of_horizontal_and_vertical
                    multiply = (' (' + str(first_matrix[row][i]) + ' x ' + str(second_matrix[i][column]) + ')')
                    list_times_across.append(multiply)

        list_sum_horizontal_vertical = []
        length = len(second_matrix)
        x = True
        text = ''
        while x == True:
            for i in range(length):
                text = text + str(list_times_across[i]) + ' + '
            text = text[1:-3]
            list_sum_horizontal_vertical.append(text)
            text = ''
            del list_times_across[:length]
            if len(list_times_across) == 0:
                x = False

        i = 0
        for row in range(rows):
            for column in range(columns):
                text = StringVar(self.__frame_extra_solutions, value=list_sum_horizontal_vertical[i])
                label_sum = Label(self.__frame_extra_solutions, textvariable=text, font='Times 14 bold', bg='white')
                label_sum.grid(row=row, column=column, padx=5, pady=5)
                i = i + 1
        

    @staticmethod
    def validate_commands():
        return True


# Class to display the determinant menu when chosen in matrix arithmetic
class Determinant(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Determinant')
        self.__matrix_chosen_files = []
        self._window_determinant = windows
        self.__label_prompt = Label(self._window_determinant, text='Select a Matrix', fg='#000033', bg='#d6faff', font='Times 18 bold')
        # Only displays square matrices upto 3x3
        self.__object_scan_files = main_classes.ScanFilesForSquareMatrix()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    def print_determinant(self):
        super().print_layout()
        self.__label_prompt.pack(side=TOP, pady=2)
        i = 0
        # for loop to print each matrix as a button
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            text = StringVar(self._window_determinant, value=matrix_name)
            button_matrix = Button(self._window_determinant, textvariable=text, font='Times 18 bold', command=lambda matrix=matrix_name: self.submit(matrix))
            button_matrix.pack(side=LEFT, padx=2, pady=2, expand=1)
            i = i + 1

    def submit(self, matrix_name):
        self.__matrix_chosen_files.append(matrix_name)
        self.open_result(matrix_name)

    @staticmethod
    def open_result(matrix_name):
        object_row_column = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_row_column.get_rows()
        columns = object_row_column.get_columns()
        object_show_result = CalculateDeterminant(matrix_name)
        # If statements for different calculations for 2x2 or 3x3
        if rows == 2:
            # Calculates determinant
            result = object_show_result.calculate_determinant_result_2x2()
            # Displays the answer
            object_show_result.print_result(result)
            # Displays the worked solutions
            object_show_solution = DisplayDeterminantSolution(matrix_name, rows, columns, result)
            object_show_solution.print_layout_2x2()
        elif rows == 3:
            result = object_show_result.calculate_determinant_result_3x3(matrix_name)
            object_show_result.print_result(result)
            object_show_solution = DisplayDeterminantSolution(matrix_name, rows, columns, result)
            object_show_solution.print_layout_3x3()


# Class to calculate subtraction of chosen matrices
class CalculateDeterminant:
    def __init__(self, matrix):
        self.__matrix = matrix

    # Method to calculate determinant for a 2x2 matrix
    def calculate_determinant_result_2x2(self):
        try:
            object_array = main_classes.TextTo2dArray(self.__matrix)
            list_matrix = object_array.convert()
        except TypeError:
            list_matrix = self.__matrix
        # Formula for 2x2 determinant
        neg_diagonal = (list_matrix[0][1] * list_matrix[1][0])
        pos_diagonal = (list_matrix[0][0] * list_matrix[1][1])
        determinant = pos_diagonal - neg_diagonal
        return determinant

    def calculate_determinant_result_3x3(self, matrix):
        try:
            object_array = main_classes.TextTo2dArray(matrix)
            matrix = object_array.convert()
        except TypeError:
            matrix = self.__matrix
        # Formula for 3x3 determinant
        list_coffactor_1 = matrix[0][0] * ((matrix[1][1] * matrix[2][2]) - (matrix[1][2] * matrix[2][1]))
        list_coffactor_2 = -1*(matrix[0][1] * ((matrix[1][0] * matrix[2][2]) - (matrix[2][0] * matrix[1][2])))
        list_coffactor_3 = matrix[0][2] * ((matrix[1][0] * matrix[2][1]) - (matrix[1][1] * matrix[2][0]))
        determinant = list_coffactor_1 + list_coffactor_2 + list_coffactor_3
        return determinant


    # Method to print the answer message
    def print_result(self, result):
        window = Toplevel
        string = 'answer is ' + str(result)
        messagebox_determinat = tkinter.messagebox.showinfo(
                    'Determinant', string)


# Class to display worked solutions for Matrix Determinant
class DisplayDeterminantSolution:
    def __init__(self, matrix_name, result_rows, result_columns, result):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__matrix_name = matrix_name
        self.__rows = result_rows
        self.__columns = result_columns
        self.__result = result
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_1 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_2 = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033', bg='#d6faff')

    def print_layout_2x2(self):
        matrix_name = self.__matrix_name
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        filename_matrix = matrix_name + '.txt'
        filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
        text_file_matrix = open(filepath_matrix, 'r')
        lines = text_file_matrix.readlines()

        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        i = 0
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        object_check = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_check.get_rows()
        columns = object_check.get_columns()
        for row in range(rows):
            for column in range(columns):
                number = float(lines[i])
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        number = self.__result
        text = StringVar(self.__frame_matrices_sum, value=number)
        label_sum = Label(self.__frame_matrices_sum, textvariable=text, font='Times 14 bold', bg='white')
        label_sum.pack(side=LEFT)

        object_array = main_classes.TextTo2dArray(matrix_name)
        matrix = object_array.convert()
        text = '(' + str(matrix[0][0]) + ' x ' + str(matrix[1][1]) + ') -' + '(' + str(matrix[0][1]) + ' x ' + str(matrix[1][0]) + ')' + ' = ' + str(self.__result)
        self.__frame_extra_solutions_1.pack(side=BOTTOM, pady=15)
        label_sum = Label(self.__frame_extra_solutions_1, text=text, font='Times 14 bold', bg='white')
        label_sum.pack(side=LEFT)

    def print_layout_3x3(self):
        matrix_name = self.__matrix_name
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        filename_matrix = matrix_name + '.txt'
        filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
        text_file_matrix = open(filepath_matrix, 'r')
        lines = text_file_matrix.readlines()

        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        i = 0
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        object_check = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_check.get_rows()
        columns = object_check.get_columns()
        for row in range(rows):
            for column in range(columns):
                number = float(lines[i])
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        number = self.__result
        text = StringVar(self.__frame_matrices_sum, value=number)
        label_sum = Label(self.__frame_matrices_sum, textvariable=text, font='Times 18 bold', bg='white')
        label_sum.pack(side=LEFT)

        object_array = main_classes.TextTo2dArray(matrix_name)
        matrix = object_array.convert()
        list_pivot_element = [matrix[0][0], matrix[0][1], matrix[0][2]]
        list_minor_1 = [[matrix[1][1], matrix[1][2]], [matrix[2][1], matrix[2][2]]]
        list_minor_2 = [[matrix[1][0], matrix[1][2]], [matrix[2][0], matrix[2][2]]]
        list_minor_3 = [[matrix[1][0], matrix[1][1]], [matrix[2][0], matrix[2][1]]]
        list_all_minors = [list_minor_1, list_minor_2, list_minor_3]
        self.__frame_extra_solutions_1.pack(pady=25)
        i = 0
        for minor in list_all_minors:
            label_det_sign = Label(self.__frame_extra_solutions_1, text=list_pivot_element[i], font='Times 14 bold', bg='#d6faff')
            label_det_sign.pack(side=LEFT, padx=(20,0))
            label_times_sign = Label(self.__frame_extra_solutions_1, text=' x ', font='Times 12', bg='#d6faff')
            label_times_sign.pack(side=LEFT)
            if i == 1:
                label_minus_sign = Label(self.__frame_extra_solutions_1, text=' - ', font='Times 12', bg='#d6faff')
                label_minus_sign.pack(side=LEFT)
            label_det_sign = Label(self.__frame_extra_solutions_1, text=' Det ', font='Times 14 bold', bg='#d6faff')
            label_det_sign.pack(side=LEFT)
            frame_minors = Frame(self.__frame_extra_solutions_1, bg='#d6faff')
            frame_minors.pack(side=LEFT)
            for row in range(2):
                for column in range(2):
                    number = minor[row][column]
                    entry_matrix_input = object_grids.grids(frame_minors, number, row, column,
                                                    self.validate_commands)
            label_plus_sign = Label(self.__frame_extra_solutions_1, text=' + ', font='Times 14', bg='#d6faff')
            label_plus_sign.pack(side=LEFT, padx=(10,0))
            i = i + 1
        label_plus_sign = Label(self.__frame_extra_solutions_1, text=' = ', font='Times 18 bold', bg='#d6faff')
        label_plus_sign.pack(side=LEFT)
        number = self.__result
        text = StringVar(self.__frame_extra_solutions_1, value=number)
        label_sum = Label(self.__frame_extra_solutions_1, textvariable=text, font='Times 18 bold', bg='white')
        label_sum.pack(side=LEFT)

        list_dets = []
        for minor in list_all_minors:
            object_determinent = CalculateDeterminant(minor)
            det = object_determinent.calculate_determinant_result_2x2()
            list_dets.append(det)
        self.__frame_extra_solutions_2.pack(side=BOTTOM, pady=15)
        string_extra_solution = '(' + str(list_pivot_element[0]) + ' x ' + str(list_dets[0]) + ')' + ' + ' + '(' + str(list_pivot_element[1]) + ' x -' + str(list_dets[1]) + ')' + ' + ' + '(' + str(list_pivot_element[2]) + ' x ' + str(list_dets[2]) + ')' + ' = ' + str(self.__result)
        label_sum = Label(self.__frame_extra_solutions_2, text=string_extra_solution, font='Times 18 bold', bg='white')
        label_sum.pack(side=LEFT)

    @staticmethod
    def validate_commands():
        return True


# Class to display the inverse menu when chosen in matrix arithmetic
# Similar to Determinant class
class Inverse(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        windows.title('Inverse')
        self.__matrix_chosen_files = []
        self._window_inverse = windows
        self.__label_prompt = Label(self._window_inverse, text='Select a Matrix', fg='#000033', bg='#d6faff', font='Times 18 bold')
        self.__object_scan_files = main_classes.ScanFilesForSquareMatrix()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    # Method to print Inverse menu
    def print_inverse(self):
        super().print_layout()
        self.__label_prompt.pack(side=TOP, pady=2)
        i = 0
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            text = StringVar(self._window_inverse, value=matrix_name)
            button_matrix = Button(self._window_inverse, textvariable=text, font='Times 18 bold', command=lambda matrix=matrix_name: self.submit(matrix))
            button_matrix.pack(side=LEFT, padx=2, pady=2, expand=1)
            i = i + 1

    def submit(self, matrix_name):
        self.__matrix_chosen_files.append(matrix_name)
        self.open_result(matrix_name)

    @staticmethod
    def open_result(matrix_name):
        object_row_column = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_row_column.get_rows()
        columns = object_row_column.get_columns()
        object_show_result = CalculateInverse(matrix_name)
        # If statement for different inverse calculations
        if rows == 2:
            # gets the determinant, answer and a rearranged matrix used for the calculations
            answer, result, determinant, new_matrix = object_show_result.calculate_inverse_result_2x2()
            # Checks to see if a matrix exist before printing answer and worked solutions
            if answer == True:
                object_show_result.print_result(result)
                object_show_solution = DisplayInverseSolution(matrix_name, rows, columns, result)
                object_show_solution.print_layout_2x2(determinant, new_matrix)
            else:
                pass
        elif rows == 3:
            # If statement same as 2x2 but also gets the matrix of cofactors and adjoint matrix for worked solutions
            answer, result, determinant, list_of_minors, matrix_of_cofactors, adjoint_matrix = \
                object_show_result.calculate_inverse_result_3x3(matrix_name, rows, columns)
            if answer == True:
                object_show_result.print_result(result)
                object_show_solution = DisplayInverseSolution(matrix_name, rows, columns, result)
                object_show_solution.print_layout_3x3(determinant, list_of_minors, matrix_of_cofactors, adjoint_matrix)
            else:
                pass


# Class to calculate subtraction of chosen matrices
class CalculateInverse:
    def __init__(self, matrix):
        self.__matrix = matrix

    # Method to calculate inverse for a 2x2
    def calculate_inverse_result_2x2(self):
        # Calculates determinant using CalculateDeterminant class
        object_get_determinant = CalculateDeterminant(self.__matrix)
        determinant = object_get_determinant.calculate_determinant_result_2x2()
        if determinant == 0:
            # No inverse exists if the determinant is 0
            self.no_inverse()
            return False, 0, [], []
        else:
            # Creates a matrix for (1/determinant) thus allowing multiplication
            determinant_matrix = []
            for row in range(2):
                current_row = []
                for column in range(2):
                    # Creates a 0 matrix
                    current_row.append(0.0)
                determinant_matrix.append(current_row)
            # replaces positive diagonal with values
            determinant_matrix[0][0] = float(1/determinant)
            determinant_matrix[1][1] = float(1/determinant)
            # Converts matrix text file to matrix array
            try:
                object_get_matrix = main_classes.TextTo2dArray(self.__matrix)
                matrix = object_get_matrix.convert()
            except TypeError:
                matrix = self.__matrix
            # Rearranges matrix to be used in inverse formula
            a = matrix[0][0]
            d = matrix[1][1]
            matrix[0][0] = d
            matrix[0][1] = matrix[0][1] * -1.0
            matrix[1][1] = a
            matrix[1][0] = matrix[1][0] * -1.0
            #  Multiplies (1/determinant) and the rearranged matrix using CalculateMultiplication class
            matrix_list = [determinant_matrix, matrix]
            object_multiply_matrix = CalculateMultiplication(matrix_list)
            object_multiply_matrix.calculate_multiplication_result(2, 2)
            # Inverse result is the result of the multiplication
            inverse, boolean = object_multiply_matrix.get_result()
            return True, inverse, determinant, matrix

    # Method to calculate inverse for a 3x3
    def calculate_inverse_result_3x3(self, matrix, rows, columns):
        # Calculates determinant using CalculateDeterminant class
        object_get_determinant = CalculateDeterminant(self.__matrix)
        determinant = object_get_determinant.calculate_determinant_result_3x3(matrix)
        if determinant == 0:
            # No inverse exists if the determinant is 0
            self.no_inverse()
            return False, 0, [], [], [], []
        else:
            # Creates a matrix for (1/determinant) thus allowing multiplication
            determinant_matrix = []
            for row in range(3):
                current_row = []
                for column in range(3):
                    current_row.append(0.0)
                determinant_matrix.append(current_row)
            # Replaces positive diagonal with values
            determinant_matrix[0][0] = float(1 / determinant)
            determinant_matrix[1][1] = float(1 / determinant)
            determinant_matrix[2][2] = float(1 / determinant)
            # Converts matrix text file to matrix array
            try:
                object_get_matrix = main_classes.TextTo2dArray(self.__matrix)
                matrix = object_get_matrix.convert()
            except TypeError:
                matrix = self.__matrix
            # all 9 minors of a 3x3 matrix
            # minors are a 2x2 matrix composed of certain locations of a 3x3
            minor_1 = [[matrix[1][1], matrix[1][2]], [matrix[2][1], matrix[2][2]]]
            minor_2 = [[matrix[1][0], matrix[1][2]], [matrix[2][0], matrix[2][2]]]
            minor_3 = [[matrix[1][0], matrix[1][1]], [matrix[2][0], matrix[2][1]]]
            minor_4 = [[matrix[0][1], matrix[0][2]], [matrix[2][1], matrix[2][2]]]
            minor_5 = [[matrix[0][0], matrix[0][2]], [matrix[2][0], matrix[2][2]]]
            minor_6 = [[matrix[0][0], matrix[0][1]], [matrix[2][0], matrix[2][1]]]
            minor_7 = [[matrix[0][1], matrix[0][2]], [matrix[1][1], matrix[1][2]]]
            minor_8 = [[matrix[0][0], matrix[0][2]], [matrix[1][0], matrix[1][2]]]
            minor_9 = [[matrix[0][0], matrix[0][1]], [matrix[1][0], matrix[1][1]]]
            # creates a list of all minors
            list_of_minors = [minor_1, minor_2, minor_3, minor_4, minor_5, minor_6, minor_7, minor_8, minor_9]
            # Calculates the determinant of each minor using CalculateDeterminant class
            list_of_dets = []
            for minor in list_of_minors:
                object_get_determinant = CalculateDeterminant(minor)
                minor_determinants = object_get_determinant.calculate_determinant_result_2x2()
                list_of_dets.append(minor_determinants)
            i = 0
            # Cofactors are 3x3 matrix of the determinants from before but every two values are negated
            matrix_of_cofactors = []
            for row in range(3):
                current_row = []
                for column in range(3):
                    # every 2nd element negated
                    if i in (1, 3, 5, 7):
                        current_row.append(-1.0 * list_of_dets[i])
                    else:
                        current_row.append(list_of_dets[i])
                    i = i + 1
                matrix_of_cofactors.append(current_row)

            # An adjoint Matrix is the 3x3 matrix but the rows and columns are replaced
            adjoint_matrix = []
            i = 0
            for row in range(3):
                current_row = []
                for column in range(3):
                    current_row.append(matrix_of_cofactors[column][row])
                    i = i + 1
                adjoint_matrix.append(current_row)
            #  Multiplies (1/determinant) and the adjoint matrix using CalculateMultiplication class
            matrix_list = [determinant_matrix, adjoint_matrix]
            object_multiply_matrix = CalculateMultiplication(matrix_list)
            object_multiply_matrix.calculate_multiplication_result(3, 3)
            # Inverse result is the result of the multiplication
            inverse, boolean = object_multiply_matrix.get_result()
            return True, inverse, determinant, list_of_minors, matrix_of_cofactors, adjoint_matrix

    # Method to print answer matrix
    def print_result(self, result):
        object_row_column = main_classes.CheckMatrixRowColumn(result)
        rows = object_row_column.get_rows()
        columns = object_row_column.get_columns()
        object_open_entry_matrix = main_classes.SaveMatrixResult(rows, columns, result)
        object_open_entry_matrix.print_layout()

    # Method to print error message saying there is no inverse
    def no_inverse(self):
        string = 'The determinant is 0 so there is no inverse'
        messagebox_determinat = tkinter.messagebox.showinfo(
            'No Inverse', string)


# Class to display worked solutions for Matrix Inverse
class DisplayInverseSolution:
    def __init__(self, matrix_name, result_rows, result_columns, result):
        self.__window_solution = Tk()
        self.__window_solution.configure(bg='#d6faff')
        self.__matrix_name = matrix_name
        self.__rows = result_rows
        self.__columns = result_columns
        self.__result = result
        self.__frame_matrices_sum = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_1 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_2 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_3 = Frame(self.__window_solution, bg='#d6faff')
        self.__frame_extra_solutions_4 = Frame(self.__window_solution, bg='#d6faff')
        self.__label_solution = Label(self.__window_solution, text='Worked Solution', font='Times 20 bold', fg='#000033', bg='#d6faff')

    def print_layout_2x2(self, determinant, new_matrix):
        matrix_name = self.__matrix_name
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        filename_matrix = matrix_name + '.txt'
        filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
        text_file_matrix = open(filepath_matrix, 'r')
        lines = text_file_matrix.readlines()

        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        i = 0
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        object_check = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_check.get_rows()
        columns = object_check.get_columns()
        for row in range(rows):
            for column in range(columns):
                number = float(lines[i])
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        for row in range(self.__rows):
            for column in range(self.__columns):
                number = self.__result[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)

        self.__frame_extra_solutions_1.pack(pady=(25,0))
        text = ' Determinant = ' + str(determinant)
        label_determinant = Label(self.__frame_extra_solutions_1, text=text, font='Times 16 bold', bg='#d6faff')
        label_determinant.pack(side=LEFT)

        self.__frame_extra_solutions_2.pack(side=BOTTOM, pady=10)
        text = '(1/' + str(determinant) + ') x '
        label_det_inverse = Label(self.__frame_extra_solutions_2, text=text, font='Times 16 bold', bg='#d6faff')
        label_det_inverse.pack(side=LEFT)
        frame_new_matrix = Frame(self.__frame_extra_solutions_2, bg='#d6faff')
        frame_new_matrix.pack(side=LEFT)
        for row in range(2):
            for column in range(2):
                number = new_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_new_matrix, number, row, column,
                                                        self.validate_commands)

    def print_layout_3x3(self, determinant, list_of_minors, matrix_of_cofactors, adjoint_matrix):
        matrix_name = self.__matrix_name
        self.__label_solution.pack(side=TOP)
        self.__frame_matrices_sum.pack()
        filename_matrix = matrix_name + '.txt'
        filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
        text_file_matrix = open(filepath_matrix, 'r')
        lines = text_file_matrix.readlines()

        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        i = 0
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        object_check = main_classes.CheckMatrixRowColumn(matrix_name)
        rows = object_check.get_rows()
        columns = object_check.get_columns()
        for row in range(rows):
            for column in range(columns):
                number = float(lines[i])
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)
                i = i + 1
        object_grids = main_classes.GetMatrixToTextFile(matrix_name, self.__rows, self.__columns)
        label_equal_sign = Label(self.__frame_matrices_sum, text=' = ', font='Times 20 bold', bg='#d6faff')
        label_equal_sign.pack(side=LEFT)
        frame_matrices = Frame(self.__frame_matrices_sum, bg='#d6faff')
        frame_matrices.pack(side=LEFT)
        for row in range(self.__rows):
            for column in range(self.__columns):
                number = self.__result[row][column]
                entry_matrix_input = object_grids.grids(frame_matrices, number, row, column,
                                                        self.validate_commands)

        self.__frame_extra_solutions_1.pack(pady=(10, 10))
        text = ' Determinant = ' + str(determinant)
        label_determinant = Label(self.__frame_extra_solutions_1, text=text, font='Times 14 bold', bg='#d6faff')
        label_determinant.pack(side=TOP)

        self.__frame_extra_solutions_2.pack()
        label_matrix_of_coffactors = Label(self.__frame_extra_solutions_2, text='Matrix of Cofactors: ',
                                           font='Times 12 bold', bg='#d6faff')
        label_matrix_of_coffactors.pack(side=TOP)
        frame_left_matrix_of_cofactors = Frame(self.__frame_extra_solutions_2, bg='#d6faff')
        frame_left_matrix_of_cofactors.pack(side=LEFT, padx=10)
        frame_minors_r1 = Frame(frame_left_matrix_of_cofactors, bg='#d6faff')
        frame_minors_r1.pack()
        frame_minors_r2 = Frame(frame_left_matrix_of_cofactors, bg='#d6faff')
        frame_minors_r2.pack()
        frame_minors_r3 = Frame(frame_left_matrix_of_cofactors, bg='#d6faff')
        frame_minors_r3.pack()

        frame_right_matrix_of_cofactors = Frame(self.__frame_extra_solutions_2, bg='#d6faff')
        frame_right_matrix_of_cofactors.pack(side=LEFT, padx=10)
        frame_label_minors_r1 = Frame(frame_right_matrix_of_cofactors, bg='#d6faff')
        frame_label_minors_r1.pack()
        frame_label_minors_r2 = Frame(frame_right_matrix_of_cofactors, bg='#d6faff')
        frame_label_minors_r2.pack()
        frame_label_minors_r3 = Frame(frame_right_matrix_of_cofactors, bg='#d6faff')
        frame_label_minors_r3.pack()
        i = 0
        for minor in list_of_minors:
            if i <= 2:
                frame_minors1 = Frame(frame_minors_r1, bg='#d6faff')
                frame_minors1.pack(side=LEFT, padx=10, pady=10)
                for row in range(2):
                    for column in range(2):
                        number = minor[row][column]
                        entry_matrix_input = object_grids.grids(frame_minors1, number, row, column,
                                                        self.validate_commands)

                if i == 2:
                    for column in range(3):
                        text = StringVar(frame_label_minors_r1, value=matrix_of_cofactors[0][column])
                        label_sum = Label(frame_label_minors_r1, textvariable=text, font='Times 14 bold', bg='white')
                        label_sum.pack(side=LEFT, padx=5, pady=5)

            if i <= 5 and i > 2 :
                frame_minors2 = Frame(frame_minors_r2, bg='#d6faff')
                frame_minors2.pack(side=LEFT, padx=10, pady=10)
                for row in range(2):
                    for column in range(2):
                        number = minor[row][column]
                        entry_matrix_input = object_grids.grids(frame_minors2, number, row, column,
                                                        self.validate_commands)

                if i == 5:
                    for column in range(3):
                        text = StringVar(frame_label_minors_r2, value=matrix_of_cofactors[1][column])
                        label_sum = Label(frame_label_minors_r2, textvariable=text, font='Times 14 bold', bg='white')
                        label_sum.pack(side=LEFT, padx=5, pady=5)

            if i <= 8 and i > 5:
                frame_minors3 = Frame(frame_minors_r3, bg='#d6faff')
                frame_minors3.pack(side=LEFT, padx=10, pady=10)
                for row in range(2):
                    for column in range(2):
                        number = minor[row][column]
                        entry_matrix_input = object_grids.grids(frame_minors3, number, row, column,
                                                        self.validate_commands)
                if i ==8:
                    for column in range(3):
                        text = StringVar(frame_label_minors_r3, value=matrix_of_cofactors[2][column])
                        label_sum = Label(frame_label_minors_r3, textvariable=text, font='Times 14 bold', bg='white')
                        label_sum.pack(side=LEFT, padx=5, pady=5)
            i = i + 1

        self.__frame_extra_solutions_3.pack()
        label_adjoint_matrix = Label(self.__frame_extra_solutions_3, text='Adjoint Matrix: ',
                                           font='Times 12 bold', bg='#d6faff')
        label_adjoint_matrix.pack(side=TOP)
        frame_adjoint_matrix = Frame(self.__frame_extra_solutions_3, bg='#d6faff')
        frame_adjoint_matrix.pack()
        for row in range(3):
            for column in range(3):
                number = adjoint_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_adjoint_matrix, number, row, column,
                                                        self.validate_commands)

        label_inverse = Label(self.__frame_extra_solutions_4, text='Inverse: ',
                                           font='Times 12 bold', bg='#d6faff')
        label_inverse.pack(side=TOP)
        self.__frame_extra_solutions_4.pack(side=BOTTOM, pady=10)
        text = '(1/' + str(determinant) + ') x '
        label_det_inverse = Label(self.__frame_extra_solutions_4, text=text, font='Times 14 bold', bg='#d6faff')
        label_det_inverse.pack(side=LEFT)
        frame_adjoint_matrix = Frame(self.__frame_extra_solutions_4, bg='#d6faff')
        frame_adjoint_matrix.pack(side=LEFT)
        for row in range(3):
            for column in range(3):
                number = adjoint_matrix[row][column]
                entry_matrix_input = object_grids.grids(frame_adjoint_matrix, number, row, column,
                                                        self.validate_commands)

    @staticmethod
    def validate_commands():
        return True

# Class to display matrix arithmetic menu
class MatrixArithmeticsLayout(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        self._window = windows
        self.__button_addition = Button(self._window, text='Addition ', font='Times 18 bold',
                                       fg='#000033', bg='#d6faff', command=lambda: self.open_addition())
        self.__button_subtraction = Button(self._window, text='Subtraction ', font='Times 18 bold',
                                           fg='#000033', bg='#d6faff', command=lambda: self.open_subtraction())
        self.__button_multiplication = Button(self._window, text='Multiplication ',
                                              font='Times 18 bold',
                                              fg='#000033', bg='#d6faff', command=lambda: self.open_multiplication())
        self.__button_determinant = Button(self._window, text='Determinant ',
                                           font='Times 18 bold',
                                           fg='#000033', bg='#d6faff', command=lambda: self.open_determinant())
        self.__button_inverse = Button(self._window, text='Inverse ',
                                       font='Times 18 bold',
                                       fg='#000033', bg='#d6faff', command=lambda: self.open_inverse())

    # Method to print menu
    def print_matrix_arithmetics(self):
        self.__button_addition.pack(side=LEFT)
        self.__button_subtraction.pack(side=LEFT)
        self.__button_multiplication.pack(side=LEFT)
        self.__button_determinant.pack(side=LEFT)
        self.__button_inverse.pack(side=LEFT)

# Methods to open corresponding button option
    def open_addition(self):
        self._window.destroy()
        window_addition = Tk()
        object_addition = Addition(window_addition)
        object_addition.print_addition()

    def open_subtraction(self):
        self._window.destroy()
        window_subtraction = Tk()
        object_subtraction = Subtraction(window_subtraction)
        object_subtraction.print_subtraction()

    def open_multiplication(self):
        self._window.destroy()
        window_multiplication = Tk()
        object_multiplication = Multiplication(window_multiplication)
        object_multiplication.print_multiplication()

    def open_determinant(self):
        self._window.destroy()
        window_determinant = Tk()
        object_determinant = Determinant(window_determinant)
        object_determinant.print_determinant()

    def open_inverse(self):
        self._window.destroy()
        window_inverse = Tk()
        object_inverse = Inverse(window_inverse)
        object_inverse.print_inverse()


def run():
    root = Tk()
    root.title(' Matrix Arithmetics')
    object_main_program = MatrixArithmeticsLayout(root)
    object_main_program.print_layout()
    object_main_program.print_matrix_arithmetics()
    root.mainloop()
    return root
