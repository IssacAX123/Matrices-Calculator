from tkinter import *
import tkinter.messagebox
import os

STR_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))  # Locates the users current directory
STR_SUBDIR = 'Matrices'
STR_FILEPATH = STR_CURRENT_DIR + '/' + STR_SUBDIR


# Class to print toolbar
class ToolbarLayout:
    def __init__(self, window):
        self._window = window
        self._frame_toolbar = Frame(self._window, bg='#000033')
        self._button_new_matrix = Button(self._frame_toolbar, text='New Matrix', command=self.open_get_row_column)
        self._button_delete_matrix = Button(self._frame_toolbar, text='Delete Matrix', command=self.open_delete_matrix)
        self._button_edit_matrix = Button(self._frame_toolbar, text='Edit Matrix', command=self.open_edit_matrix)
        self._button_home = Button(self._frame_toolbar, text='Home', command=self.home)
        self._button_exit = Button(self._frame_toolbar, text='Exit', command=exit)

    # Prints the toolbar in order defined
    def print_layout(self, window):
        window.configure(background='#d6faff')
        self._button_new_matrix.pack(side='left', padx=2, pady=2, expand=1)
        self._button_delete_matrix.pack(side='left', padx=2, pady=2, expand=1)
        self._button_edit_matrix.pack(side='left', padx=2, pady=2, expand=1)
        self._button_home.pack(side='left', padx=2, pady=2, expand=1)
        self._button_exit.pack(side='left', padx=2, pady=2, expand=1)
        self._frame_toolbar.pack(side='top', fill='x')

    # Methods below are ran when their respective buttons in the toolbar are pressed
    @staticmethod
    def open_get_row_column():
        object_open_get_row_column = GetRowColumn()
        object_open_get_row_column.print_layout()

    @staticmethod
    def open_delete_matrix():
        object_delete_matrix = DeleteMatrix()
        object_delete_matrix.print_layout()

    @staticmethod
    def open_edit_matrix():
        object_edit_matrix = EditMatrix()
        object_edit_matrix.print_layout()

    def home(self):
        self._window.destroy()
        import home
        home.run()


# Parent class for all forms to display the toolbar at the top
class App:
    def __init__(self, windows):
        self._windows = windows
        self.__object_toolbar = ToolbarLayout(self._windows)
        self._frame = Frame(self._windows)
        # Checks if the Matrices folder exists before creating one so windows won't give an error
        if os.path.exists(STR_SUBDIR) == False:
            os.mkdir(os.path.join(STR_CURRENT_DIR, STR_SUBDIR))

    # Method to print the toolbar
    def print_layout(self):
        self.__object_toolbar.print_layout(self._windows)


# Class to get the row and column of a new matrix to be created
class GetRowColumn:
    def __init__(self):
        self.__window_get_row_column = Tk()
        self.__window_get_row_column.title('Enter Row and Columns')
        self.__window_get_row_column.withdraw()
        self.__register = self.__window_get_row_column.register(self.correct_input_row_column)
        self.__rows = 0
        self.__label_rows = Label(self.__window_get_row_column, text='Enter the number of rows: ')
        self.__entry_rows = Entry(self.__window_get_row_column, validate="key", validatecommand=(self.__register, '%S'),
                                  width=5)
        self.__columns = 0
        self.__label_columns = Label(self.__window_get_row_column, text='Enter the number of columns: ')
        self.__entry_columns = Entry(self.__window_get_row_column, validate="key", validatecommand=(self.__register,
                                                                                                    '%S'),
                                     width=5)
        self.__button_submit_row_column = Button(self.__window_get_row_column, text='Submit',
                                                 command=lambda: self.submit_row_column(self.__window_get_row_column))

    # Method to: print the row & column entry widgets,text labels and submit buttons.
    def print_layout(self):
        self.__window_get_row_column.configure(background='#d6faff')
        self.__window_get_row_column.deiconify()
        self.__label_rows.grid(row=0, sticky='E')
        self.__entry_rows.grid(row=0, column=1)
        self.__label_columns.grid(row=1, sticky='E')
        self.__entry_columns.grid(row=1, column=1)
        self.__button_submit_row_column.grid(row=3, column=1)

    # Method to take input from entry widget when user clicks submit
    def submit_row_column(self, window_1):
        try:
            self.__rows = int(self.__entry_rows.get())
            self.__columns = int(self.__entry_columns.get())
            if self.__rows < 10 or self.__columns <= 10:
                # Instantiates GetMatrixName class for next step to create matrix
                object_get_matrix_name = GetMatrixName(self.__rows, self.__columns)
                object_get_matrix_name.print_layout()
                window_1.destroy()
            else:
                msgbox__matrix_exceeds_max_degree = tkinter.messagebox.showinfo(
                    'Invalid!', 'Make sure that matrices are less then 10x10')
        except:
            msgbox__matrix_exceeds_max_degree = tkinter.messagebox.showinfo(
                'Invalid!', 'Make sure that you enter a value')

    # Validation method to check live user input to only accept positive integers
    @staticmethod
    def correct_input_row_column(user_input):
        object_validation = Validation
        if object_validation.positive_integer_only(user_input) == True:
            return True
        else:
            return False


# Class to get the name of a new matrix to be created
class GetMatrixName:
    def __init__(self, row, column):
        self.__window_get_matrix_name = Tk()
        self.__window_get_matrix_name.title('Enter Row and Columns')
        self.__window_get_matrix_name.withdraw()
        self.__label_matrix_name = Label(self.__window_get_matrix_name, text='Enter the name of your matrix: ')
        self.__register = self.__window_get_matrix_name.register(self.correct_matrix_name)
        self.__entry_matrix_name = Entry(self.__window_get_matrix_name, validate="key", validatecommand=(self.__register
                                                                                                         , '%S'))
        self.__button_submit_name = Button(self.__window_get_matrix_name, text='Submit',
                                           command=lambda: self.submit_matrix_name(self.__window_get_matrix_name, row,
                                                                                   column))

    # Method to print the entry widget and submit button
    def print_layout(self):
        self.__window_get_matrix_name.configure(background='#d6faff')
        self.__window_get_matrix_name.deiconify()
        self.__label_matrix_name.grid(row=0, sticky='E')
        self.__entry_matrix_name.grid(row=0, column=1)
        self.__button_submit_name.grid(row=1, column=1)

    # Method to take input from entry widget when user clicks submit
    def submit_matrix_name(self, window_2, row, column):
        matrix_name = str(self.__entry_matrix_name.get())
        # Validates the matrix name to see if it's allowed by windows or if nothing was entered
        object_validate = Validation
        if matrix_name == '' or object_validate.window_textfile_string(matrix_name) == False:
            msgbox__matrix_exceeds_max_degree = tkinter.messagebox.showinfo(
                'Invalid!', 'Make sure that you enter a valid name')
        else:
            window_2.destroy()
            object_matrix_text_file = GetMatrixToTextFile(matrix_name, row, column)
            object_matrix_text_file.print_layout('')

    # Validation method to check live user input to not accept banned filename characters
    @staticmethod
    def correct_matrix_name(user_input):
        object_validate = Validation
        if object_validate.window_textfile_string(user_input) == False:
            return False
        else:
            return True


# Class to get the values of the matrix and then save it as a text file
class GetMatrixToTextFile:
    def __init__(self, matrix_name, rows, columns):
        self.__window_get_matrix_input = Tk()
        self.__window_get_matrix_input.title('Enter matrix values')
        self.__window_get_matrix_input.withdraw()
        self.__rows = rows
        self.__columns = columns
        self.__frame_window_get_matrix_input = Frame(self.__window_get_matrix_input)
        self.register = self.__window_get_matrix_input.register(self.correct_input_matrix)
        self.validate_commands = (self.register, '%S')
        self.__dictionary_for_row_column_of_entry_widgets = {}
        self.__submit__matrix_of_entry = Button(self.__frame_window_get_matrix_input, text='Submit',
                                                command=lambda: self.submit_matrix(rows, columns, matrix_name,
                                                                self.__window_get_matrix_input,
                                                                self.__dictionary_for_row_column_of_entry_widgets))

    # Prints a matrix of entry widgets and then a submit button
    # Each entry widget has coordinates stored as a tuple in a hashtable/dictionary ...
    # ... allowing access for each individual values
    def print_layout(self, text):
        self.__window_get_matrix_input.configure(background='#d6faff')
        self.__window_get_matrix_input.deiconify()
        self.__frame_window_get_matrix_input.grid()
        for row in range(self.__rows):
            for column in range(self.__columns):
                location = (row, column)
                entry_matrix_input = self.grids(self.__frame_window_get_matrix_input, text, row, column, self.validate_commands)
                self.__dictionary_for_row_column_of_entry_widgets[location] = entry_matrix_input
        self.__submit__matrix_of_entry.grid(row=self.__rows + 1, column=self.__columns - 1)

    # Creates individual entry widgets that can have values pre-written or left empty
    def grids(self, frame, text, row, column, validate_commands):
        string = StringVar(frame, value=text)
        entry_matrix_input = Entry(frame, validate="key", validatecommand=validate_commands,
                                   width=10, textvariable=string)
        entry_matrix_input.grid(stick="e", row=row, column=column, padx=2, pady=2)
        return entry_matrix_input

    def submit_matrix(self, rows, columns, matrix_name, window_3, dictionary):
        list_full_matrix = []
        correct = True
        # reads each entry widgets and stores them in the array
        try:
            for row in range(rows):
                current_row = []
                for column in range(columns):
                    location = (row, column)
                    float(dictionary[location].get())
                    # If value cannot convert to float then it is invalid
                    current_row.append(dictionary[location].get())
                list_full_matrix.append(current_row)
        except ValueError:
            msgbox_error = tkinter.messagebox.showerror('Not a valid number', 'Please Re Enter the Matrix')
            correct = False
        # Creates the matrix text file
        if correct == True:
            filename_matrix_text_file_name = (matrix_name + '.txt')
            filepath_matrix_text_file_name = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix_text_file_name)
            try:
                matrix_text_file = open(filepath_matrix_text_file_name, 'w+')
                for row in list_full_matrix:
                    for column in row:
                        matrix_text_file.write(column)  # Writes matrix values line by line
                        matrix_text_file.write("\n")
                matrix_text_file.write(str(rows))       # Writes matrix rows in 2nd last line
                matrix_text_file.write("\n")
                matrix_text_file.write(str(columns))    # Writes matrix columns in 2nd last line
                matrix_text_file.close()
            except OSError:
                msgbox_error = tkinter.messagebox.showerror('Windows Error', 'Windows cannot create file. please choose another matrix name ')
            self.__frame_window_get_matrix_input.destroy()
            window_3.destroy()

    # Validation method to check live user input to only accept real values
    @staticmethod
    def correct_input_matrix(user_input):
        object_validation = Validation
        if object_validation.float_active(user_input) == True:
            return True
        else:
            return False


# Class to return the row or column of a matrix
class CheckMatrixRowColumn:
    def __init__(self, matrix):
        try:
            # Initially it will try to open the corresponding matrix text file
            self.__filename_matrix = matrix + '.txt'
            self.__filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, self.__filename_matrix)
            self.__text_file_matrix = open(self.__filepath_matrix, 'r')
            self.__lines = self.__text_file_matrix.readlines()
            # It will read the last two lines and assigns the numbers to row and column
            self.__rows = int(self.__lines[-2])
            self.__columns = int(self.__lines[-1])
        except:
            # If the program can't open a text file then an actual matrix array has been passed through
            self.__rows = len(matrix)
            self.__columns = len(matrix[0])

    # Method to return rows
    def get_rows(self):
        return self.__rows

    # Method to return columns
    def get_columns(self):
        return self.__columns


# Class to edit a chosen matrix and re-save it
class EditMatrix:
    def __init__(self):
        self.__window_select_matrix = Tk()
        self.__window_select_matrix.title('Select a Matrix to Edit')
        self.__window_edit_matrix = Tk()
        self.__window_edit_matrix.title('Edit matrix')
        self.__window_edit_matrix.withdraw()
        self.__frame_edit_matrix = Frame(self.__window_edit_matrix)
        self.__frame_select_matrix = Frame(self.__window_select_matrix)
        self.__frame_list_of_matrix = Frame(self.__frame_select_matrix)
        self.__register = self.__window_edit_matrix.register(self.correct_input_matrix)
        self.__validate_commands = (self.__register, '%S')
        self.__dictionary_for_row_column_of_entry_widgets = {}
        self.__label_title = Label(self.__frame_select_matrix, text='Select a matrix to edit', font='Times 18 bold',
                                   fg='white', bg='#000033')
        self.__listbox_files = Listbox(self.__frame_list_of_matrix, selectmode=SINGLE, font='Times 18 bold',
                                       bg='#d6faff')
        self.__scrollbar = Scrollbar(self.__frame_list_of_matrix)
        self.__object_scan_files = ScanFiles()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    # Prints a matrix of entry widgets and then a submit button
    def print_layout(self):
        self.__frame_select_matrix.configure(background='#000033')
        self.__frame_select_matrix.pack()
        self.__label_title.pack()
        self.__frame_list_of_matrix.pack()
        i = 0
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            self.__listbox_files.insert(i, matrix_name)
            i = i + 1
        button_submit = Button(self.__frame_select_matrix, text='Submit',
                               command=lambda: self.open_matrix())
        self.__scrollbar.pack(side=RIGHT, fill=Y)
        self.__listbox_files.pack(pady=2)
        self.__listbox_files.config(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__listbox_files.yview)
        button_submit.pack()

    # Opens the matrix text file and reads the rows and columns
    # Reads each matrix value line by line
    # Creates individual entry widgets that can have  pre-written matrix values
    def open_matrix(self):
        chosen_matrix = self.__listbox_files.curselection()
        for matrix_index in chosen_matrix:
            matrix_name = self.__listbox_files.get(matrix_index)
            filename_matrix = matrix_name + '.txt'
            filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
            text_file_matrix = open(filepath_matrix, 'r')
            lines = text_file_matrix.readlines()
            self.__window_select_matrix.destroy()
            self.__window_edit_matrix.deiconify()
            object_get_rows_colums = CheckMatrixRowColumn(matrix_name)
            rows = object_get_rows_colums.get_rows()
            columns = object_get_rows_colums.get_columns()
            __submit__matrix_of_entry = Button(self.__frame_edit_matrix, text='Submit', command=lambda: self.submit_matrix(rows, columns, matrix_name, self.__window_edit_matrix))
            self.__frame_edit_matrix.grid()
            i = 0
            object_grids = GetMatrixToTextFile(matrix_name, rows, columns)
            for row in range(rows):
                for column in range(columns):
                    number = float(lines[i])
                    location = (row, column)
                    entry_matrix_input = object_grids.grids(self.__frame_edit_matrix, number, row, column, self.__validate_commands)
                    self.__dictionary_for_row_column_of_entry_widgets[location] = entry_matrix_input
                    i = i + 1
            __submit__matrix_of_entry.grid(row=rows + 1, column=columns - 1)

    # Method to re-save matrix
    def submit_matrix(self, rows, columns, matrix_name, window_3):
        object_matrix_text_file = GetMatrixToTextFile(matrix_name, rows, columns)
        object_matrix_text_file.submit_matrix(rows, columns, matrix_name, window_3, self.__dictionary_for_row_column_of_entry_widgets)

    # Validation method to check live user input to only accept real values
    @staticmethod
    def correct_input_matrix(user_input):
        object_validation = Validation
        if object_validation.float_active(user_input) == True:
            return True
        else:
            return False


# Class to delete chosen matrices
class DeleteMatrix:
    def __init__(self):
        self.__window_delete_matrix = Tk()
        self.__window_delete_matrix.title('Select matrices to delete')
        self.__frame_delete_matrix = Frame(self.__window_delete_matrix)
        self.__frame_list_of_matrix = Frame(self.__frame_delete_matrix)
        self.__label_title = Label(self.__frame_delete_matrix, text='Select matrices to delete', font='Times 18 bold',
                                   fg='white', bg='#000033')
        self.__listbox_files = Listbox(self.__frame_list_of_matrix, selectmode=MULTIPLE, font='Times 18 bold',
                                       bg='#d6faff')
        self.__scrollbar = Scrollbar(self.__frame_list_of_matrix)
        self.__object_scan_files = ScanFiles()
        self.__matrix_list = self.__object_scan_files.get_matrix_list()

    def print_layout(self):
        self.__frame_delete_matrix.configure(background='#000033')
        self.__frame_delete_matrix.pack()
        self.__label_title.pack()
        self.__frame_list_of_matrix.pack()
        i = 0
        for line in self.__matrix_list:
            matrix_name = line[:-4]
            self.__listbox_files.insert(i, matrix_name)
            i = i + 1
        button_submit = Button(self.__frame_delete_matrix, text='Submit',
                               command=lambda: self.confirmation_message_box(matrix_name))
        self.__scrollbar.pack(side=RIGHT, fill=Y)
        self.__listbox_files.pack(pady=2)
        self.__listbox_files.config(yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.config(command=self.__listbox_files.yview)
        button_submit.pack()


    def delete_chosen_file(self):
        chosen_matrix = self.__listbox_files.curselection()
        for matrix_index in chosen_matrix:
            matrix_name = self.__listbox_files.get(matrix_index)
            filename_matrix = matrix_name + '.txt'
            filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, filename_matrix)
            os.remove(filepath_matrix)
            self.__matrix_list.remove(filename_matrix)
        self.__window_delete_matrix.destroy()

    def confirmation_message_box(self, matrix_name):
        msgbox_confirm_delete = tkinter.messagebox.askquestion('Delete File',
                                                               'Are you sure you want to delete these files')
        if msgbox_confirm_delete == 'yes':
            self.delete_chosen_file()
        else:
            pass


# Class to scan textfiles in Matrices Folder
class ScanFiles:
    def __init__(self):
        self._matrix_list = []
        for file in os.listdir(STR_FILEPATH):
            if file.endswith(".txt"):
                self._matrix_list.append(file)

    # Method to return an array of all the matrix filenames
    def get_matrix_list(self):
        return self._matrix_list


# Class to scan textfiles then filters out only square matrices.
class ScanFilesForSquareMatrix(ScanFiles):
    def __init__(self):
        super().__init__()
        self.__squarematrix_list = []
        for i in range(len(self._matrix_list)):
            current_matrix = self._matrix_list[i]
            matrix_name = current_matrix[:-4]
            object_check_matrix1 = CheckMatrixRowColumn(matrix_name)
            matrix_row = object_check_matrix1.get_rows()
            matrix_columns = object_check_matrix1.get_columns()
            if matrix_row == matrix_columns and matrix_row <= 3:
                self.__squarematrix_list.append(current_matrix)

    # Same method name as parent class but only returns square matrices
    def get_matrix_list(self):
        return self.__squarematrix_list


# Class to convert a textfile to a 2d matrix array
class TextTo2dArray:
    def __init__(self, matrix_name):
        self.__matrix_name = matrix_name
        self.__filename_matrix = self.__matrix_name + '.txt'
        self.__filepath_matrix = os.path.join(STR_CURRENT_DIR, STR_SUBDIR, self.__filename_matrix)
        self.__text_file_matrix = open(self.__filepath_matrix, 'r')
        self._lines = self.__text_file_matrix.readlines()
        self.__rows = int(self._lines[-2])
        self.__columns = int(self._lines[-1])

    # Method to convert matrix textfile to a 2d array that can be manipulated
    def convert(self):
        try:
            text_matrix = []
            full_matrix = []
            for line in range(self.__rows * self.__columns):
                x = float(self._lines[line])
                text_matrix.append(x)
            i = 0
            for row in range(self.__rows):
                current_row = []
                for column in range(self.__columns):
                    current_row.append(float(self._lines[i]))
                    i = i + 1
                full_matrix.append(current_row)
        except TypeError:
            full_matrix = self.__matrix_name
        return full_matrix


# class to save result matrices from calculations
class SaveMatrixResult:
    def __init__(self, rows, columns, result):
        self.__window_display_result = Tk()
        self.__window_display_result.title('Result')
        self.__label_answer = Label(self.__window_display_result, text='Answer', font='Times 16 bold',
                                      fg='#000033', bg='#d6faff')
        self.__bottomframe_result = Frame(self.__window_display_result, bg='#d6faff')
        self.__rows = rows
        self.__columns = columns
        self.__result_matrix = result
        self.__frame_window_display_result = Frame(self.__window_display_result)
        self.register = self.__window_display_result.register(self.correct_input_matrix)
        self.validate_commands = (self.register, '%S')
        self.__window_2 = Tk()
        self.__window_2.withdraw()
        self.__label_matrix_name = Label(self.__window_2, text='Enter the name of your matrix: ')
        self.__entry_matrix_name = Entry(self.__window_2)
        self.dictionary_for_row_column_of_entry_widgets = {}

    def print_layout(self):
        self.__label_answer.grid()
        rows = self.__rows
        columns = self.__columns
        __button_save_result = Button(self.__frame_window_display_result, text='Save', fg='#d6faff', bg='#000033',
                                      font='Times 10 bold', command=self.submit)
        self.__frame_window_display_result.grid()
        i = 0
        matrix_name = ''
        object_grids = GetMatrixToTextFile(matrix_name, rows, columns)
        for row in range(rows):
            for column in range(columns):
                number = self.__result_matrix[row][column]
                location = (row, column)
                entry_matrix_input = object_grids.grids(self.__frame_window_display_result, number, row, column,
                                                        self.validate_commands)
                self.dictionary_for_row_column_of_entry_widgets[location] = entry_matrix_input
                i = i + 1
        __button_save_result.grid(row=rows + 1, column=columns - 1)

    def print_name_layout(self):
        button_submit_name = Button(self.__window_2, text='Submit',
                                    command=lambda: self.submit_matrix_name(self.__window_2,
                                                                            self.__window_display_result,
                                                                            self.__rows, self.__columns))
        self.__window_2.configure(background='#d6faff')
        self.__window_2.deiconify()
        self.__label_matrix_name.grid(row=0, sticky='E')
        self.__entry_matrix_name.grid(row=0, column=1)
        button_submit_name.grid(row=1, column=1)

    def submit(self):
        self.print_name_layout()

    def submit_matrix_name(self, window_2, window_3, rows, columns):
        matrix_name = str(self.__entry_matrix_name.get())
        self.submit_matrix(matrix_name,rows,columns,window_2, window_3)

    def submit_matrix(self, matrix_name, rows, columns, window_3, window_2):
        object_matrix_text_file = GetMatrixToTextFile(matrix_name, rows, columns)
        object_matrix_text_file.submit_matrix(rows, columns, matrix_name, window_3,
                                              self.dictionary_for_row_column_of_entry_widgets)

    @staticmethod
    def correct_input_matrix(user_input):
        object_validation = Validation
        if object_validation.float_active(user_input) == True:
            return True
        else:
            return False

# Class with methods to validate inputs as they are being entered live
class Validation:
    def __init__(self):
        pass

    @staticmethod
    def positive_integer_only(user_input):
        if user_input.isdigit():
            return True
        else:
            return False

    @staticmethod
    def float_active(user_input):
        if user_input == '-' or user_input in '1234567890' or user_input == '.':
            return True
        else:
            return False

    @staticmethod
    def window_textfile_string(user_input):
        if user_input in ['<', '>', ':', '"', '/', '|', '?', '*', '!', "'", u'0x005C']:
            return False
        else:
            return True


class Queue:
    def __init__(self, queue):
        self.queue = queue

    def dequeue(self):
        element = self.queue[0]
        self.queue.pop(0)
        return element

    def enqueue(self, element):
        size = self.size()
        self.queue.insert(size + 1, element)

    def size(self):
        size = len(self.queue)
        return size

    def peek(self):
        element = self.queue[0]
        return element

