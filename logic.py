from PyQt6.QtWidgets import *
from bank_app import *
import csv


class Logic(QMainWindow, Ui_Bank_App):
    def __init__(self) -> None:
        '''
        Sets up the screen and hiding majority of inputs until the login is complete.
        Also connects the buttons to their functions
        '''
        super().__init__()
        self.setupUi(self)
        self.Welcome_Label.hide()
        self.Welcome_Text.hide()
        self.Withdraw_Button.hide()
        self.Deposit_Button.hide()
        self.Submit_Button.hide()
        self.Balance_Label.hide()
        self.Amount_Label.hide()
        self.Amount_Input.hide()

        self.Login_Button.clicked.connect(lambda : self.account_check())
        self.Submit_Button.clicked.connect(lambda : self.transfer())


    def account_check(self) -> None:
        '''
        This function covers over the login button which allows the user to access their file information in info.csv
        first : String value that holds the first name of the user
        second : String value that holds the last name of the user
        password : holds the pin for the user account which needs to match for the user to login in
        user_found : value that's True or False that confirms if the user account was found or not
        '''
        self.first = self.First_Name_Input.text()
        self.last = self.Last_Name_Input.text()
        password = self.Pin_Input.text()
        user_found = False
        with open('info.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:
                if (row['first_name'].strip() == self.first) and (row['last_name'].strip() == self.last):
                    if row['password'].strip() == password:
                        first_name = self.First_Name_Input.text()
                        last_name = self.Last_Name_Input.text()
                        self.Welcome_Label.setText(f'Welcome {first_name} {last_name}!')
                        user_found = True
                        self.Welcome_Label.show()
                        self.Welcome_Text.show()
                        self.Withdraw_Button.show()
                        self.Deposit_Button.show()
                        self.Submit_Button.show()
                        self.Balance_Label.show()
                        self.Amount_Label.show()
                        self.Amount_Input.show()
                        self.Balance_input.setText(f'${row['balance']}')

                    elif row['password'].strip() != password:
                        self.Welcome_Label.setText(f'Incorrect Password Please Try Again')
                        user_found = True

            if user_found == False:
                with open('info.csv', 'a') as csv_file:
                    field_names = ['first_name', 'last_name', 'password', 'balance']
                    writer = csv.DictWriter(csv_file, fieldnames = field_names)
                    writer.writerow({'first_name' : self.first, 'last_name' : self.last, 'password' : password, 'balance' : '0.00'})
                    self.Welcome_Label.setText(f'Creating a new account, Welcome New User!')
                    self.Welcome_Label.show()
                    self.Welcome_Text.show()
                    self.Withdraw_Button.show()
                    self.Deposit_Button.show()
                    self.Submit_Button.show()
                    self.Balance_Label.show()
                    self.Amount_Label.show()
                    self.Amount_Input.show()
                    self.Balance_input.setText(f'$0.00')

    def transfer(self) -> None:
        '''
        The function that controls over the transfer of money to accounts which allows you to eithr deposit or withdraw
        The change in function is then submitted to info.csv which holds account infomation
        first : String value that holds the first name of the user
        second : String value that holds the last name of the user
        num : String value of the current balance
        rows : List created to hold the rows in info so it could be changed
        balance: a float value of the account balance
        amount : a float value of the amount being changed

        '''
        first = self.first
        last = self.last
        num = self.Amount_Input.text()

        try:
            amount = float(num)
            if amount <= 0:
                raise ValueError('Amount must be positive')
        except (ValueError, TypeError):
            self.Amount_Label.setText('Please enter a valid positive number')
            return

        rows = []
        balance = 0

        with open('info.csv', 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                if (row['first_name'].strip() == first) and (row['last_name'].strip() == last):
                    balance = float(row['balance'])

                    if self.Withdraw_Button.isChecked():
                        if amount > balance:
                            self.Amount_Label.setText('Insufficient funds')
                            return
                        balance -= amount

                    elif self.Deposit_Button.isChecked():
                        balance += amount

                    else:
                        self.Amount_Label.setText('Please choose either withdraw or deposit')
                        return

                    row['balance'] = f'{balance:.2f}'
                    self.Balance_input.setText(f'${balance}')

                rows.append(row)

        with open('info.csv', 'w', newline='') as csv_file:
            field_names = ['first_name', 'last_name', 'password', 'balance']
            writer = csv.DictWriter(csv_file, fieldnames=field_names)
            writer.writeheader()
            writer.writerows(rows)
















