#! python3
#shebang line allows the program to be run from command line or by pressing WIN-R
"""This is part 5 of Group 5 programming project for Assessment 2.  The Project to create a blood donation signup,
and questionaire.  Donors can login and answer questions to donate and hospitals or clinics can request blood.  In this part of the program
hospitals create an account and or login, request blood product, type and quantity.  A confirmation email is then sent.  The program
has several features to ensure the correct responses otherwise the program will terminate"""
#importing modules sys, random, json, csv, getpass, stdiomask and smtplib
#sys is used in this program to exit the system at several points
#random is used to generate a 4 digit random number which is stored and could be used but is not as yet
#json module is used to load (call keys and values as Python dictionary) and dump data (convert Python objects to json string)
#csv module is currently not being used
#stdiomask and getpass are used to hide or mask the input password. This does not work in Windows as it cannot control whats called the echo.
#To make it work the python program must be converted to an executable file extension.exe which I have a copy on my machine
#It does however work in Repl.


import sys, random, getpass, stdiomask
import json, csv
import smtplib

# Select if you are a current registered user or a new user needing to create an account
attempts = 0

while True:
    print("Are you a registered user?")
    print("Please enter y or n or q to exit: ")
    signin = input() #input y for yes, n for no or q to exit system
    print()

    if attempts == 2:
        sys.exit("You have not made a valid input and need to restart")
        # if the user does not enter y,n or q on the 3rd attempt the program will end

#This section creates an account and saves the data to a users.json file
    if signin == "n":
        print("Please create an account")
        print()
        def create(user):
            user_id = input("Enter your name: ") # input name
            user_pass = input("Enter your password: ") # input password
            #user_pass = stdiomask.getpass("Enter you password") #not of windows unless converted to executable.exe
            initials = input("Enter your initials, first, last: ") #input
            hospital = input("Enter your Hospital or Clink name: ") #input
            user_no = random.randint(1000,9999) # creates a random 4 digit number
            print("your 4 digit User Id is: ", user_no)
            e_mail = input("Enter you email address: ") # input your email
            
# saves the keys and values
            user[user_id] = user_pass
            user[user_no] = e_mail
            user[initials] = hospital

            writeUsers(user)
            return True
#parse users to a dictionary with json.loads()      
        def readUsers():
            try:
                with open("users.json", "r") as f:
                    return json.load(f)
            except FileNotFoundError:
                return {}

        def writeUsers(user):
            with open("users.json", "w+") as f:
                json.dump(user, f)

        users = readUsers()
        success = create(users)

        while not success:
            success = create(users)
        break

        
# This section is for registered users to login
   
    elif signin == "y":
        break
# The next two elif statments exit the program using the sys module         
    elif signin == "q":
        sys.exit("You have entered \'q\' to exit the program, Goodbye") #exits the system

    elif attempts == 3:
        sys.exit("You have not made a valid input and need to restart")

# Else statment provides user with further oportunities before ending program      
    else:
        print("That is not a valid input, please enter 'y' or 'n' or 'q'")
        attempts += 1

# function for registered users and those just registered, requests name and password

def login(user):
    print("Please log in")
    user_id = input("Enter your name: ") #input
    user_pass = input("Confirm your password: ") #input
    #user_pass = stdiomask.getpass("Confirm you password")
    #password masking does not work on a windows machine unless the file is converted to an executable.exe

#checks user details in json file
    if user_id in user.keys():
        if user_pass == user[user_id]:
            print()
            print("Welcome back! ", user_id) # if user_id details correct
        else:
            print("Incorrect password.") #if details are not correct
            sys.exit("good bye") #exits the system using the sys module and exit() function
            return False
    else:
        print("Wrong user name or password")
        sys.exit("good bye") #exits the system

    user[user_id] = user_pass

    writeUsers(user)
    return True

    user_pass = input("Enter your password: ") # enter password
    user[user_id] = user_pass
#function reads json file
def readUsers():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
#function writes to json file
def writeUsers(user):
    with open("users.json", "w+") as f:
        json.dump(user, f)

users = readUsers()
success = login(users)

while not success:
    success = login(users)
    
print()

print("Thank you please continue")
print()
#In the following section the admin / user selects which type of blood product.  
blood_qty = 0
attempts3 = 3
remain = attempts3 - 1
while attempts3 > 0: #allows 3 attempts with while and if statements
    print("What blood product do you require, whole blood or plasma?: ")
    blood_prod = input().lower() #converts input to lower case
    print()
    if attempts3 == 1:
        print("you did not enter a vaild input")
        sys.exit("Good Bye")
    if blood_prod == "whole blood":
        break
    elif blood_prod == "plasma":
        break
    elif blood_prod != "whole blood" or "plasma":
        print("You must enter 'whole blood' or 'plasma' \n You have ", remain, " attempt(s) remaining")
        attempts3 = attempts3 - 1
        remain = attempts3 - 1
    else:
        sys.exit("Good Bye")
#In this section the user selects the blood group.   
bloodType = ""
attempts5 = 4
remain1 = 2
while attempts5 > 1: #allows 3 attempts to choose from all blood types
    if attempts5 == 1:
        sys.exit("Good Bye")
    print("What blood type do you need?: ")
    print("Please enter one of the following types: ")
    print("A, A-, A+, B, B-, B+, AB, AB-, AB+, O, O-, O+")
    bloodType = input().upper() #converts to upper
    group_list = ['A', 'A-', 'A+', 'B', 'B-', 'B+', 'AB', 'AB-', 'AB+', 'O', 'O-', 'O+'] #list of blood types

    if bloodType in group_list:
        print("You have selected ", bloodType)
        break
    elif bloodType not in group_list:
        attempts5 = attempts5 - 1
        print("You must enter a valid blood type.\n You have ", remain1, " attempt(s) remaining")
        
        if remain1 == 0:
            sys.exit("Good Bye")
        remain1 = remain1 - 1
    else:
        print("You must enter a valid blood type")
        
#This section asks user for input, how much blood must be between 200 and 5000
attempts4 = 0   
while True:
    if attempts4 == 3: #allows 3 attempts
        print("you did not enter a vaild input")
        sys.exit("Good Bye")

    try:
        print("You are required to enter a quantity, the minimun is 200ml and maximum is 5000ml")
        blood_qty = float(input("How much blood or plasma do you require in millilitres?: "))
        if blood_qty < 200 or blood_qty > 5000:
            print("Then quantity is not in the acceptable range")
            print("Please enter a quantity from 200 and 5000")
            continue
        
        if blood_qty == type(float) or type(int): #requires type int of float
            break
        else:
            print("please enter a number")

    except ValueError:
        print("Only numbers are allowed")
        attempts4 += 1
print()
#This section sends an email to the user
email = input("Please confirm your email: ")
#email must be a real email address otherwise the system will try to send the email and an error will be returned, program ends.
print()
#Message sent in email
print("""Thank you,\n
your order for {}ml of {}, type {} will be sent.\n
You will receive a confirmation email from fpbtheglen@gmail.com""".format(blood_qty, blood_prod, bloodType))
print()


smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login('fpbtheglen@gmail.com', 'ilhesmogxasqizge') #this email address is used to send the emails.

smtpObj.sendmail('fpbtheglen@gmail.com', email, 'Subject: Blood Product.\nThank you for your order.\n\nYour Blood Product, Quantity and Type has been dispatched.\n Sincerely,\n Blood Bank')
{}
smtpObj.quit()


    


print("Your session has ended, you may login again at any time")


#The system ends with the above message, however it crashes if the email is not a valid email.
    
