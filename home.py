from tkinter import *
import main_classes


class HomeLayout(main_classes.App):
    def __init__(self, windows):
        super().__init__(windows)
        self._window = windows
        self.__button_option_matrices_arithmetic = Button(self._windows,
                                                          text='Matrix Arithmetic ',
                                                          font='Times 18 bold',
                                                          fg='#000033', bg='#d6faff',
                                                          command=self.matrix_arithmetics)  # runs method when clicked
        self.__button_option_geometric_arrangement = Button(self._windows,
                                                            text='Point Of Intersection ',
                                                            font='Times 18 bold',
                                                            fg='#000033', bg='#d6faff',
                                                            command=self.point_of_intersection)

    # print_home method places the buttons and the toolbars on the screen for the homepage
    def print_home(self):
        self._window.title('Home')
        self.__button_option_matrices_arithmetic.pack(side=LEFT, expand=True)
        self.__button_option_geometric_arrangement.pack(side=RIGHT, expand=True)

    # The two methods below are called when their respected buttons are pressed.
    # e.g. If the 'Matrix Arithmetic' button is pressed then matrix_arithmetics.py module is ran
    def matrix_arithmetics(self):
        self._window.destroy()
        import matrix_arithmetics as ma
        ma.run()

    def point_of_intersection(self):
        self._window.destroy()
        import point_of_intersection as poi
        poi.run()

# Instantiates the HomeLayout class
# It then runs the 'print_layout' method for the parent class which prints the toolbar
# It then runs the 'print_home' method for the homepage
def run():
    root = Tk()
    object_main_program = HomeLayout(root)
    object_main_program.print_layout()
    object_main_program.print_home()
    root.mainloop()


