import sqlite3
from employeemymodule import add_employee,view_details_by_employee,edit_employee,view_employees_by_admin,delete_employee,employee_data_crud
from salarymymodule import add_salary,view_salary_by_admin,view_salary_by_employee,edit_salary,employee_salary,check_employee
from leavemymodule import employee_leave_menu,request_leave,approve_reject_leave_requests,view_pending_leave_requests,view_leave_by_employee,view_leaves_of_employee,calculate_leave_days
from departmentmymodule import view_employee_department,department_menu,edit_employee_department,delete_employee_department,add_employee_department

from salarymymodule import check_employee
import time
import mysql.connector
conn =sqlite3.connect('emp_mngmnt.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee(
                                    Employee_Id  INTEGER PRIMARY KEY AUTOINCREMENT , 
                                    Employee_Name VARCHAR(75) NOT NULL,
                                    Gender CHAR(1) , Date_Of_Joining DATE(10),
                                    Employee_Address VARCHAR(200),
                                    Phone_Number VARCHAR(20), Email_Id VARCHAR (50)
                                        )
             ''')

cursor.execute ('''
                CREATE TABLE IF NOT EXISTS department(
                                    Department_Id INTEGER   NOT NULL, 
                                    Department_Name VARCHAR(100) NOT NULL,
                                    LOCATION VARCHAR(100),
                                    Employee_Id INTEGER, 
                                    FOREIGN KEY(Employee_Id) REFERENCES employee(Employee_Id)
                                        )
             ''')


cursor.execute('''
                CREATE TABLE IF NOT EXISTS salary(
                                    Salary_Id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                    Employee_Id INTEGER ,
                                    Basic_Pay DOUBLE(20) , 
                                    DA DOUBLE(20) ,
                                    HRA DOUBLE(20),
                                    Medical_Allowance DOUBLE(20),
                                    Net_Salary DOUBLE(20),
                                    FOREIGN KEY(Employee_Id) REFERENCES employee(Employee_Id)
                                             )
          ''')

cursor.execute('''
               CREATE TABLE IF NOT EXISTS leave_requests (
                                leave_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                employee_id INTEGER,
                                leave_type VARCHAR(50), 
                                start_date DATE,
                                end_date DATE,
                                reason TEXT,
                                status TEXT DEFAULT 'Pending', 
                                applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                                admin_remark TEXT, FOREIGN KEY (employee_id) REFERENCES employee(Employee_Id))
                
               ''')

          
cursor.execute('''
               CREATE TABLE IF NOT EXISTS user(     
                                id INTEGER PRIMARY KEY AUTOINCREMENT ,
                                username VARCHAR(15) UNIQUE,
                                 password  TEXT,
                                Emp_Id INTEGER, 
                                role TEXT,
                                access_control TEXT DEFAULT 'ACCESS GRANTED',
                                status_access_control TEXT,
                                logged_status TEXT DEFAULT 'LOGGED OUT',
                                FOREIGN KEY(Emp_Id) REFERENCES employee(Employee_Id)
                                )
            ''')


   
conn.commit()
conn.close()
import  mysql.connector

def request_access_grant(employee_id,status_access_control):
    """EMPLOYEE FUNCTION
       THIS FUNCTION ALLOWS EMPLOYEE TO REQUEST FOR ACCESS GRANT ,IF ADMIN ALREADY DENIED ACCESS.
    
    """
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    choice = ''
    while choice == '':

        choice = input("DO YOU WANT TO REQUEST ADMIN FOR GRANT OF ACCESS ?[Y/N] :")
        if status_access_control == 'PENDING':
            # USER ALREADY REQUESTED FOR ACCESS. BUT ADMIN HAS NOT GIVEN A REPLY .
            print("YOUR REQUEST HAVE BEEN SUBMITTED ALREADY. PLEASE WAIT FOR THE ADMIN TO REPLY.")
            break
        if choice.upper() == 'Y':
            # USER IS REQUESTING THE ADMIN TO GRANT ACCESS
            cursor.execute(''' UPDATE  user SET status_access_control= ?  WHERE Emp_Id = ?''',('PENDING',employee_id))
            print("REQUEST FOR ACCESS GRANT SUBMITTED SUCCESSFULLY....")
            conn.commit()
            return
            # request_flag = True
        elif choice.upper() == 'N':
            # USER IS NOT REQUESTING FTHE ADMIN TO GRANT ACCESS
            break
        else: 
            print("INVALID CHOICE")
    
    conn.commit()
    cursor.close()        
def login():
    """ ADMIN AND EMPLOYEE FUNCTIOM
        THIS FUNCTION IS USED TO LOGIN TO PROGRAM            """
    
    try:
        
        user_name = input("ENTER THE USERNAME : ")
        # VALIDATING USERNAME
        if user_name == '':
            raise ValueError("USERNAME ENTERED IS INVALID")  
        pass_word = input("ENTER THE PASSWORD : ")
        # VALIDATING PASSWORD
        if pass_word =='':
            raise ValueError("PASSWORD ENTERED IS INVALID")
        
        conn = sqlite3.connect('emp_mngmnt.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM user WHERE username = ? AND password = ?  ''', (user_name,pass_word))
        user_data = cursor.fetchone()
        """  ADMIN LOGIN DIRECTLY FROM HERE """
        if user_data:

            if user_data [3] == 0 :   #user_data[3]= Employee Id
                #user_data[1] = username user_data[4] = role[ADMIN/EMPLOYEE]
                print(f'USERNAME {user_data[1]} - LOGGED IN SUCCESSFULLY AS {user_data[4]}\n')
                cursor.execute('''UPDATE user SET logged_status = ?  WHERE Emp_Id = ?''',('LOGGED IN',user_data[3]))
                conn.commit()
                return user_data
            
        
                """ EMPLOYEE LOGIN FROM HERE"""
            else:   
                employee_id =user_data[3]
                logged_status = user_data[7]
                status_access_control = user_data[6]

                if logged_status == 'LOGGED IN' and status_access_control == 'APPROVED':
                    print("HI, YOU ARE LOGGED IN ALREADY.")
                    return user_data
                """ADMIN CAN DENY ACCESS TO A USER. HERE access_control is initialised to GRANTED. IF access control
                    is DENIED, USER CANNOT LOGIN. USER CAN REQUEST ADMIN TO GRANT ACCESS.

                """
                access_control = 'ACCESS GRANTED'
                while access_control == 'ACCESS GRANTED':
                    if user_data :
                        if user_data[5] == 'ACCESS DENIED':
                            
                            print("YOUR ACCESS IS DENIED!!!PLEASE CONTACT ADMIN")
                            access_control = user_data[5] 
                            status_access_control = user_data[6]
                            # EMPLOYEE CAN USE THIS FUNCTION TO REQUEST FOR ACCESS GRANT
                            request_access_grant(employee_id,status_access_control)
                            return
                        if user_data[7] == 'LOGGED OUT' :
                            print(f'USERNAME {user_data[1]} - LOGGED IN SUCCESSFULLY AS {user_data[4]}\n')
                            cursor.execute('''UPDATE user SET logged_status = ? ,status_access_control = ? WHERE Emp_Id = ?''',('LOGGED IN','APPROVED',employee_id))
                            conn.commit()
                            return user_data
                        
                        if user_data[7] =='LOGGED OUT' and user_data[6] == 'PENDING':
                            print("PLEASE WAIT FOR THE ADMIN TO GRANT PERMISSION")
                        
                    else:
                        print("NO USER EXISTS WITH THIS USERNAME....")
                        break
                conn.commit()    
            
        else :
            print("YOU HAVE ENTERED WRONG CREDENTIALS.TRY AGAIN")
            return
    except ValueError as error_message:
                    print(f'ERROR MESSAGE -{error_message}') 

def logout():
    """ ADMIN AND EMPLOYEE FUNCTION
     THIS FUNCTION IS USED TO LOGOUT FROM THE PROGRAM """
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute(''' SELECT * FROM user WHERE logged_status = 'LOGGED IN' ''')
    user_data = cursor.fetchone()
        
    if user_data :
    # IF A USER IS STILL LOGGED IN, user_data HAS A VALUE    
        id = user_data[0]
        username = user_data[1]
        
        choice = input("DO YOU WANT TO LOGOUT ? [Y/N] :")
        if choice.upper() == 'Y' or choice.upper() == 'YES': 
            # SETTING THE LOGGED STATUS AS LOGGED OUT 
            cursor.execute('''UPDATE user SET logged_status = ? WHERE id = ? ''',('LOGGED OUT',id))
            print(f'USERNAME - {username} LOGGED OUT SUCCESSFULLY.....')
            conn.commit()
            return

        elif choice.upper() == 'N' or choice == 'NO' :
            print("USER NOT LOGGED OUT")
       
        else:
            print("INVALID CHOICE")
    

    
   

def register():
    # USER REGISTERS USING EMPLOYEE ID,USERNAME AND PASSWORD
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    while True:
        try:
            print("WELCOME TO USER REGISTERATION PROFILE")
            cursor.execute('''SELECT * FROM user ''')
            emp_data = cursor.fetchone()

            if emp_data :
                print("FIRST YOU MUST ENTER THE COMPANY PROVIDED EMPLOYEE ID FOR REGISTERATION")
                emp_id = (input("ENTER YOUR VALID IMPLOYEE ID :"))
                if str(emp_id) == '' or emp_id.isdigit() == False :
                    raise ValueError("YOU MUST ENTER A NUMERIC EMPLOYEE ID")
                
                if check_employee(emp_id) :
                # CASE OF AN EMPLOYEE ID EXISTS 
                
                    print("PLEASE CREATE A VALID USERNAME(A-Z,0-9,NO BLANK SPACES)")
                    user_name = input("ENTER THE USERNAME : ")
                    if user_name == '':
                                # VALIDATING THE USERNAME
                                raise ValueError("USERNAME YOU HAVE ENTERED IS INVALID")  
                    pass_word = input("ENTER THE PASSWORD : ")
                    if pass_word =='':
                                # VALIDATING THE PASSWORD
                                raise ValueError("PASSWORD YOU HAVE ENTERED IS INVALID")
                    cursor.execute('''INSERT INTO user (Emp_id,username,password,role,status_access_control) VALUES(?,?,?,?,?)
                                            ''',(emp_id,user_name,pass_word,'EMPLOYEE','APPROVED'))
                    print("YOUR REGISTERATION IS SUCCESSFUL.")
                    print("NOW YOU CAN LOGIN USING USER LOGIN OPTION. IF YOU CANNOT LOGIN, YOUR DETAILS ARE YET TO BE UPLOADED.WAIT FOR THE ADMIN TO COMPLETE IT.")
                    print("AFTER YOUR ACCESS, YOU MUST LOGOUT")
                    conn.commit()
                    break
                else:
                    print("YOU CANNOT REGISTER NOW AS YOUR DETAILS YET TO BE UPLOADED. PLEASE CONTACT ADMIN ")
                    break   
                
            else:
                
                    try:
                        print("ADMIN REGISTERATION PORTAL")
                        print("YOU CAN GIVE USERNAME AND PASSWORD AS YOU WISH. SUGGESTION IS USERNAME:ADMIN AND PASSWORD:ADMIN")
                        print("ENTER THE USERNAME (A-Z,0-9,NO BLANK SPACES)")
                        user_name = input("ENTER THE USERNAME :")
                        if user_name == '':
                                    # VALIDATING THE USERNAME
                                    raise ValueError("USERNAME YOU HAVE ENTERED IS INVALID")  
                        pass_word = input("ENTER THE PASSWORD :")
                        if pass_word =='':
                                    # VALIDATING THE PASSWORD
                                    raise ValueError("PASSWORD YOU HAVE ENTERED IS INVALID")
                                # INSERTING THE ADMIN DETAILS TO user TABLE WITH EMPLYEE ID AS ZERO
                        cursor.execute('''INSERT INTO user (Emp_id,username,password,role) VALUES(?,?,?,?)
                                                ''',(0,user_name,pass_word,'ADMIN'))
                        conn.commit()
                        print(f"USER '{user_name}' REGISTRATION SUCCESSFULL")
                        print("AFTER REGISTERATION, ADMIN HAVE TO DO LOGIN WITH USERNAME AND PASSWORD")
                        print("AFTER SUCCESSFUL LOGIN, ADMIN CAN CHOOSE VARIOUS OPTIONS.")
                        return True
                    except ValueError as error_message:
                        print (f'ERROR MESSAGE -{error_message}')    

        except sqlite3.IntegrityError as e:
                        # Catch the specific IntegrityError
            print(f"Error: {e}")
            print(f"USRENAME '{user_name}' ALREADY EXISTS. PLEASE CHOOSE ANOTHER USERNAME.")
            # Roll back the transaction in case of an error
            conn.rollback() 
            return False    
            
def view_pending_access_requests():
    """ ADMIN FUNCTION
        THIS ALLOWS THE ADMIN TO VIEW THE ACCESS GRANT REQUESTS SENT BY EMPLOYEE USERS  """
                                        
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT * FROM user WHERE status_access_control = 'PENDING' ''')
        requests = cursor.fetchall() 
        if requests:
            for req in requests:
                # SHOWS THE REQUESTS OF USERS FOR ACCESS GRANT
                print(f'PENDING REQUEST FOR ACCESS GRANT OF EMPLOYEE ID: {req[3]}, STATUS OF REQUEST: {req[6]}')
            return requests
        else:
            print("NO PENDING REQUESTS FOUND")
    except mysql.connector.Error as err:
        print(f"Error fetching requests: {err}")
        return []
    cursor.close()

def user_access_control():
    """ ADMIN FUNCTION
        THIS FUNCTION ALLOWS THE ADMIN TO DENY ACCESS TO A USER FROM USING THE PROGRAM.
        ALSO ADMIN CAN VIEW PENDING REQUSTS FOR ACCESS GRANT FROM DENIED USERS AND 
        ALSO APPROVE OR REJECT THE REQUETS    
                                                        """
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    while True:
        print("ACCESS CONTROL SYSTEM")
        print("1.ACCESS GRANT OR DENY\n2.VIEW PENDING ACCESS REQUETS\n3.APPROVE OR REJECT REQUESTS\n4.EXIT")
        choice = input("ENTER YOUR CHOICE : ")
        if choice == '1':
            # ADMIN CAN DENY OR GRANT LOGIN ACCESS TO PROGRAM FOR A USER 
            employee_id = 0
            while employee_id == 0:
                employee_id = int(input("ENTER THE EMPLOYEE ID TO CONTROL ACCESS TO PROGRAM : "))
            if check_employee(employee_id) == 0:
                print("EMPLOYEE ID DOES NOT EXISTS. PLEASE TRY ANOTHER ID.")
                return
            
            cursor.execute('''SELECT * FROM user WHERE Emp_Id = ?''',(employee_id,))
            employee_data = cursor.fetchone()
            print(f'ACCESS STATUS GIVEN TO EMPLOYEE ID {employee_id} is {employee_data[5]}')
            # choice = ''
            # while choice == '':
            print("ACCESS CONTROL SYSTEM->ACCESS GRANT OR DENY->")
            print("1.ACCESS GRANTED\n2.ACCESS DENIED")
            emp_access_control = input("Enter your option :")
            if emp_access_control == '1' :
                # IF A USER'S ACCESS WAS DENIED BEFORE, ADMIN CAN GRANT ACCESS TO USER HERE
                access_control = 'ACCESS GRANTED'
                cursor.execute(''' UPDATE user SET access_control = ? WHERE Emp_Id = ?''',(access_control,employee_id))
                print(f'USER WITH EMPLOYEE ID {employee_id} ACCES SET TO GRANTED')
                
            elif emp_access_control == '2':
                # HERE ADMIN CANDENY ACCESS TO A USER 
                access_control = 'ACCESS DENIED'
                cursor.execute(''' UPDATE user SET access_control = ? WHERE Emp_Id = ?''',(access_control,employee_id))
                print(f'USER WITH EMPLOYEE ID {employee_id} ACCES SET TO DENIED')

            else :
                print("INVALID CHOICE")

        elif choice == '2':
           # FUNCTION CALL TO VIEW PENDING ACCESS REQUESTS
           view_pending_access_requests()
           
        elif choice =='3':
            # FOR PERFORMING THE APPROVE OR REJECT PENDING REQUESTS
            conn = sqlite3.connect('emp_mngmnt.db')
            cursor = conn.cursor()
    
            try:
                pending =view_pending_access_requests()
                if pending :
                    
                    request_for_access_id = pending[0][0]
                    print(f"\nADMIN PROCESSING THE REQUEST...")
                   
                    # status_choice = ''
                    # while status_choice == '':
                    print("SELECT A STATUS YOU WANT TO GIVE TO THE REQUEST --\n1.APPROVED\n2.REJECTED\n ")
                    status_choice = input("ENTER YOUR CHOICE :-")
                    if status_choice == '1' :
                        """ IF ADMIN SELECTS STATUS AS APPROVED , USER access control SET TO ACCESS GRANTED.
                        NOW USER CAN LOG IN USING LOGIN FUNCTION    """
                        status = 'APPROVED'
                        access_control = 'ACCESS GRANTED'

                    elif status_choice == '2' : 
                        """ IF ADMIN SELECTS STATUS AS REJECTED , USER access control SET TO ACCESS DENIED.
                        NOW USER CANNOT LOG IN USING LOGIN FUNCTION    """
                        status = 'REJECTED'  
                        access_control = 'ACCESS DENIED'

                    else :
                        print("INVALID CHOICE")
                    
                    cursor.execute('''UPDATE user SET status_access_control = ?,access_control = ?
                                   WHERE  id = ?''', (status,access_control,request_for_access_id))
                    conn.commit()
                    print(f"CONTROL ACCESS REQUEST UPDATED TO {status}.")
                    return True
            except mysql.connector.Error as err:
                print(f"ERROE UPDATING REQUEST: {err}")
                conn.rollback()
                return False
            
        elif choice == '4':
            break
        else :
            print("INVALID CHOICE")    
           
        
    conn.commit()
    cursor.close()

def admin_able():
    """ ADMIN FUNCTION
           THIS FUNCTION ALLOWS ADMIN TO DO VARIOUS OPERATIONS
           EMPLOYEE DETAILS CRUD , DEPARTMENT CRUD,SALARY HANDLING,LEAVE HANDLING, USER ACCESS CONTROL
              FOR LOGGING TO PROGRAM   """
    while True: 
        try:
            print("\nEMPLOYEE MANAGEMENT SYSTEM - ADMIN OPERATIONS")
            print('-'*60)
            print("1.EMPLOYEE CRUD OPERATIONS\n2.DEPARTMENT OF EMPLOYEE CRUD\n3.SALARY OF EMPLOYEE\n4.LEAVE OF EMPLOYEE\n5.USER ACCESS CONTROL TO PROGRAM\n6.EXIT")
            admin_choice_1 = input("ENTER YOUR CHOICE : ")
            if admin_choice_1 == '1':
                # EMPLOYEE CRUD OPERATIONS
                employee_data_crud()

            elif admin_choice_1 == '2':
                # Employee Department Operations
                department_menu()
                
            elif admin_choice_1 == '3':
                # FUNCTION CALL TO EMPLOYEE SALARY OPERATIONS
                employee_salary()
                    
            elif admin_choice_1 == '4':
                # FUNCTION CALL TO EMPLOYEE LEAVE OPERATIONS
                employee_leave_menu()

            elif admin_choice_1 == '5':
                """ FUNCTION IS USED BY ADMIN TO DENY ACCESS TO USER,VIEW PENDING ACCESS GRANT 
                 REQUESTS AND APPROVE OR REJECT PENDING REQUESTS"""
                user_access_control()    

            elif admin_choice_1 == '6':
                # EXIT FROM LOOP
                break

            elif admin_choice_1 == '':
                raise ValueError("YOU MUST ENTER A VALID CHOICE")
            else :
                print("INVALID CHOICE ")
        except ValueError as error_message:
            print(f'ERROR MESSAGE -{error_message}')        
        finally :
            print("ADMIN OPERATIONS FINISHED\n")

def employee_able(employee_id):
    """ EMPLOYEE FUNCTION
           THIS FUNCTION ALLOWS EMPLOYEE TO VIEW PROFILE, VIEW DEPARTMENT AND LOCATION, VIEW SALARY,
           VIEW LEAVES AND STATUS OF LEAVES APPLIED, REQUEST FOR LEAVES   """
    try:
        while True:
            print("\nEMPLOYEE MANAGEMENT SYSTEM - EMPLOYEE OPERAIONS")
            print('-'*60)
            print("1.VIEW PROFILE\n2.VIEW DEPARTMENT\n3.VIEW SALARY\n4.VIEW LEAVES -STATUS OF LEAVES APPLIED\n5.REQUEST FOR NEW LEAVE\n6.EXIT")
            employee_choice = (input("ENTER YOUR CHOICE : "))
            if employee_choice == '1':
                # VIEW DETAILS OF EMPLOYEE
                view_details_by_employee(employee_id)

            elif employee_choice == '2':
                # VIEW DEPARTMENT DETAILS OF EMPLOYEE
                view_employee_department(employee_id)

            elif employee_choice == '3' :
                # VIEW SALARY DETAILS OF EMPLOYEE
                view_salary_by_employee(employee_id)

            elif employee_choice == '4' :
                # VIEW LEAVES TAKEN, STATUS OF NEW LEAVES APPLIED
                view_leave_by_employee(employee_id)
                
            elif employee_choice == '5':
                # REQUEST FOR NEW LEAVES
                request_leave(employee_id)

            elif employee_choice == '6':
                # EXIT FROM LOOP
                break
            elif employee_choice == '':
                raise ValueError("YOU MUST ENTER A VLID CHOICE")
            else :
                print("INVALID CHOICE")
    except ValueError as error_message:
            print(f'Error Message -{error_message}')        
    finally :
            print("EMPLOYEE OPERATIONS FINISHED")

def main():
    #  DEFINING MAIN FUNCTION
    while True:
        
        try:    
            # INITIAL MENU 
            print("WELCOME TO EMPLOYEE MANAGEMENT SYSTEM")
            print('-'*50)
            print("1.USER REGISTERATION\n2.USER LOGIN\n3.USER LOGOUT\n4.EXIT")
            choice = (input("ENTER YOUR CHOICE : "))
            if choice == '1':
                # FUNCTION CALL TO REGISTER USER
                register()
            elif choice == '2':
                # FUNCTION CALL TO LOGIN USING USERNAME AND PASSWORD
                user_val = login()
                if user_val:
                    # IF LOGGED IN AS ADMIN , ADMIN_ABLE FUNCTION IS CALLED
                    if user_val[4] == 'ADMIN':
                        admin_able() 
                     # IF LOGGED IN AS EMPLOYEE ,EMPLOYEE_ABLE FUNCTION IS CALLED   
                    elif user_val[4] =='EMPLOYEE':
                        employee_able(user_val[3])
                # FUNCTION CALL TO LOGOUT
            elif choice == '3':
                 # FUNCTION CALL FOR USER LOGOUT
                 logout()

            elif choice == '4':
                # EXIT FROM LOOP
                break

            elif choice == '':
                raise ValueError("YOU MUST ENTER A VALID CHOICE...")
            else:
                print("INVALID CHOICE")
        except ValueError as error_message:
            print(f'Error Message - {error_message}')            


# CALLING THE MAIN FUNCTION
main()
