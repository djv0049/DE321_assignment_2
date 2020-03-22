
"""
cli will have the cmd interface
"""
from cmd import Cmd
from classes import Doctor, Nurse


class CommandLineInterface(Cmd):
    intro = 'Simple Cli for Assessment2. Please type help or ? for command list.\n'
    prompt = '>>>'
    file = None

    def __init__(self):
        Cmd.__init__(self)
        self.name = 'unknown'
        self.id = "unknown"
        self.salary = ''

    def do_employee_name(self, employee_name):
        if employee_name:
            self.name = employee_name
        print(self.name)

    def do_employee_id(self, employee_id):
        if employee_id:
            self.id = employee_id
        print(self.id)

    def do_employee_salary(self, employee_salary):
        if employee_salary:
            self.salary = employee_salary
        print(self.salary)

    def do_introduce(self, employee_name):
        """
        Syntax: introduce 'me'
                [type your name]
        """
        # if employee_name:
        #     print('Hello ' + employee_name)
        # else:
        #     print('Hello ' + self.name)
        if employee_name != '':
            try:
                print('Welcome')
                employee_name = (input("Please enter you employee_name: "))
                print('Hello ' + employee_name)
            except ValueError as e:
                print(f'The exception is: {e}')
            except KeyError as e:
                print(f'{e}: Not a command')

    def do_calculate(self, employee_id, arg):
        """
        syntax: payroll [employee_id]
        """
        # if employee_id == 'Doctor':
        #     print(Doctor.calculate_payroll)
        # if employee_id == 'Nurse':
        #     print(Nurse.calculate_payroll)
        # else:
        #     print('error')
        try:
            if employee_id == 'Doctor':
                print(Doctor.calculate_payroll())
            if employee_id == 'Nurse':
                print(Nurse.calculate_payroll())
        except ValueError as err:
            print('The exception is: ', err)
        else:
            print('Everything went fine.')
        finally:
            print('The End')

    def do_exit(self, line):
        """
        Stop the program
        syntax: exit
        """
        print('Thank you for visiting.')
        return True


if __name__ == '__main__':
    cmd = CommandLineInterface()
    cmd.cmdloop()
