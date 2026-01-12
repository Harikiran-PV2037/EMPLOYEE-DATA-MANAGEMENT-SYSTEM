import sqlite3
from salarymymodule import check_employee

conn =sqlite3.connect('emp_mngmnt.db')
cursor = conn.cursor()


def add_employee_department():
    # ADMIN FUNCTION
    # FUNCTION TO ADD A DEPARTMENT ID, DEPARTMENT NAME AND LOCATION FOR AN EMPLOYEE
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    print("ENTER THE DETAILS- EMPLOYEES DEPARTMENT ID, NAME AND LOCATION ")
    emp_id = 0 
    while emp_id == 0:
        
            emp_id = (input("ENTER THE EMPLOYEE ID : "))
            try :
                if emp_id == '' or emp_id.isdigit() == False :
                    raise ValueError("YOU MUST ENTER A VALID EMPLOYEE ID")
            except ValueError as error_message:
                print(f'Error Message - {error_message}') 
            if check_employee(emp_id)   :
                print(f'EMPLOYEE ID EXISTS')
                # TO CHECK IF AN EMPLOYEE WAS ALLOTTED A DEPARTMENT BEFORE
                cursor.execute('''SELECT * FROM department WHERE Employee_Id = ?''',(emp_id,))
                employee_data = cursor.fetchone()
                if employee_data :
                    print("EMPLOYEE DEPARTMENT ALREADY ADDED. PLEASE TRY OTHER ID")
                else:
                    # IF A DEPARTMENT WAS NOT ALLOTTED BEFORE ,PROVIDE THE DETAILS
                    print("CHOOSE THE DEPARTMENT ID FROM THE FOLLOWING")
                    print("1.FINANCE/ACCOUNTING\n2.HUMAN RESOURCE\n3.MARKETING\n4.SALES\n5.OPERATIONS/PRODUCTION")
                    print("6.IT\n7.CUSTOMER SERVICE SUPPORT\n8.FRESHER")
                    dep_dic = {1:'FINANCE/ACCOUNTING',2:'HR',3:'MARKETING',4:'SALES',5:'OPERATIONS/PRODUCTION',6:'IT',7:'CUSTOMER SERVICE SUPPORT',8:'FRESHER'}
                    default_value = 'Not Found'
                    department_id = int(input("ENTER THE DEPARTMENT ID :"))
                    
                    value = dep_dic.get(department_id,default_value)
                    if value != default_value:
                        department_name = value
                    else:
                        print(f"DEPARTMENT ID NOT FOUND")
                    department_location = ''
                    while department_location == '':    
                        department_location = input("ENTER THE LOCATION :")
                    try:
                        cursor.execute('''INSERT INTO department(Department_ID,Department_Name,Employee_Id,
                                Location) VALUES(?,?,?,?)''',(department_id,department_name,emp_id,department_location))
                        conn.commit()
                        print("EMPLOYEE DEPARTMENT DETAILS ADDED SUCCESSFULLY.....")
                    except sqlite3.Error as error_msg:
                        print(f'Error Message {error_msg}')
            else:
                print("EMPLOYEE ID DOES NOT EXIST. PLEASE TRY OTHER ID ")
    conn.close()  

def edit_employee_department():
    #  ADMIN FUNCTION
    # TO EDIT THE DEPARTMENT OF AN EMPLOYEE
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    print("ENTRY FORM FOR THE DETAILS OF EMPLOYEE DEPARTMENT AND LOCATION")
    emp_id = 0 
    while emp_id == 0:
        
            emp_id = (input("ENTER THE EMPLOYEE ID : "))
            try :
                if emp_id == '' or emp_id.isdigit() == False :
                    raise ValueError("YOU ,UST ENTER A VALID EMPLOYEE ID")
            except ValueError as error_message:
                print(f'Error Message - {error_message}') 
            if check_employee(emp_id)   :
                print(f'Employee Id EXISTS')
                cursor.execute('''SELECT * FROM department WHERE Employee_Id = ?''',(emp_id,) )
                department_data = cursor.fetchone()
                print(f'Previous Department Id -{department_data[0]}\n{' '*10} Department Name -{department_data[1]}\n{' '*10}Location -{department_data[2]}')
                print("-"*50)
                print("CHOOSE THE DEPARTMENT ID TO EDIT FROM THE FOLLOWING")
                print("1.FINANCE/ACCOUNTING\n2.HR\n3.MARKETING\n4.SALES\n5.OPERATIONS/PRODUCTION")
                print("6.IT\n7.CUSTOMER SERVICE SUPPORT\n8.FRESHER")
                dep_dic = {1:'FINANCE/ACCOUNTING',2:'HR',3:'MARKETING',4:'SALES',5:'OPERATIONS/PRODUCTION',6:'IT',7:'CUSTOMER SERVICE SUPPORT',8:'FRESHER'}
                default_value = 'NOT FOUND'
                department_id = 0
                while department_id == 0:
                    try :
                        department_id = int(input("ENTER THE DEPARTMENT ID :"))
                        if str(department_id) == '':
                            raise ValueError("YOU MUST ENTER NUMERIC VALUE")
                    except ValueError as error_message:
                        print(f'Error Message -{error_message}')
                        return
                value = dep_dic.get(department_id,default_value)
                if value != default_value:
                     department_name = value
                else:
                    print(f"NOT FOUND")
                department_location = input("ENTER THE LOCATION :")
                try:
                    cursor.execute('''UPDATE department SET Department_ID= ?,Department_Name = ?,Employee_Id =?,
                               Location =? ''',(department_id,department_name,emp_id,department_location))
                    conn.commit()
                    print("EMPLOYEE DEPARTMENT DETAILS UPDATED SUCCESSFULLY.....")
                except sqlite3.Error as error_msg:
                    print(f'Error Message {error_msg}')
            else:
                print("EMPLOYEE ID DOES NOT EXISTS. PLEASE TRY ANOTHER ID.")
    conn.close()      

def view_employee_department_by_admin():
    # ADMIN FUNCTION
    # FUNCTION TO VIEW A PARTICULAR EMPLOYEE OR ALL EMPLOYEES DEPARTMENTS
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    while True:
        print("*********DEPARTMENT DETAILS OF EMPLOYEES********")
        print("1.VIEW AN EMPLOYEE DEPARTMENT DETAILS\n2.VIEW ALL EMPLOYEES DEPARTMENT DETAILS\n3.EXIT")
        choice = input("ENTER THE CHOICE : ")
        if choice == '1':
            emp_id = 0 
            while emp_id == 0:
                emp_id = (input("ENTER THE EMPLOYEE ID : "))
                try :
                    if emp_id == '' or emp_id.isdigit() == False :
                        raise ValueError("YOU MUST ENTER A VALID EMPLOYEE ID")
                    else:
                        if check_employee(emp_id)   :
                            
                            cursor.execute('''SELECT * FROM department 
                                           WHERE department.Employee_Id =? ''',(emp_id,))
                            employee_data = cursor.fetchone()
                            if employee_data:
                                print(f'\nDEPARTMENT DETAILS OF EMPLOYEE ID -  {emp_id}')
                                print(f'EMPLOYEE ID -{employee_data[3]}')
                                print(f'EMPLOYEE DEPARTMENT ID  -{employee_data[0]}')
                                print(f'EMPLOYEE DEPARTMENT NAME -{employee_data[1]}')
                                print(f'EMPLOYEE LOCATION -{employee_data[2]}')
                            else :
                                print(f'EMPLOYEE ID {emp_id} NOT POSTED TO A DEPARTMENT. YOU HAVE TO ADD THE DETAILS')    
                        else :
                            print(f' EMPLOYEE WITH EMPLOYEE ID {emp_id} DOED NOT EXISTS. TRY ANOTHER ID.')    
                except ValueError as error_message:
                    print(f'Error Message - {error_message}') 
        elif choice == '2':
            # VIEW THE DEPARTMENTS OF ALL EMPLOYEES
            try:
                cursor.execute('''SELECT * FROM department  ''')
                department_data = cursor.fetchall()
                num_employees = len(department_data)
                print(f"NUMBER OF EMPLOYEES : {num_employees}") 
                emp_number = 1
                if department_data :
                    for employee in department_data:
                        print(f'SERIAL NUMBER {emp_number}')
                        print(f'EMPLOYEE ID -{employee[3]}')
                        print(f'EMPLOYEE DEPARTMENT ID  -{employee[0]}')
                        print(f'EMPLOYEE DEPARTMENT NAME -{employee[1]}')
                        print(f'EMPLOYEE LOCATION -{employee[2]}')
                        print('-'*50)
                        emp_number += 1
            except sqlite3.Error as error_msg:
                    print(f'Error Message {error_msg}')
        elif choice =='3':
            break
        else:
            print("INVALID CHOICE")

    conn.close()

def view_employee_department(emp_id):
    # EMPLOYEE FUNCTION
    # FUNCTION TO VIEW AN EMPLOYEE HIS OWN DEPARTMENT DETAILS
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM department INNER JOIN employee
                   WHERE department.Employee_Id =? AND employee.Employee_ID = ?''',(emp_id,emp_id))
    employee_data = cursor.fetchone()

    if employee_data:
        print("DEPARTMENT AND LOCATION DETAILS")
        print('-'*50)
        print(f'EMPLOYEE ID - {employee_data[3]}')
        print(f'EMPLOYEE NAME  - {employee_data[5]}')
        print(f'EMPLOYEE DEPARTMENT ID - {employee_data[0]}')
        print(f'EMPLOYEE DEPARTMENT NAME - {employee_data[1]}')
        print(f'EMPLOYEE LOCATION -{employee_data[2]}')
    else :
        print("YOUR DEPARTMENT DETAILS ARE NOT AVAILABLE NOW. PLEASE CONTACT ADMIN.")
    conn.close()

def delete_employee_department():
    # FUNCTION TO DELETE AN EMPLOYEE DEPARTMENT
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    emp_id = int(input("ENTER THE EMPLOYEE ID TO DELETE :"))
    if check_employee(emp_id) == 0:
        print("EMPLOYEE ID DOES NOT EXISTS. PLEASE TRY ANOTHER ID.")
        return
    
    try:

        delete_question = input("ARE YOU SURE THAT YOU WANT TO DELETE THE DEPARTMENT OFEMPLOYEE [Y/N] ? :")
        if delete_question.upper() == 'Y' or delete_question.upper() == 'YES':
            # ADDITIONAL SAFETY MEASURE TO DELETE A DEPARTMENT OF AN EMPLOYEE
            confirm_question = int(input("IF YES - GIVE THE ANSWER FOR SUM OF 55AND 45 : "))
            if confirm_question == '':
                raise ValueError("YOU MUST ENTER A NUMERIC VALU AS ANSWER")
            if confirm_question == 100:
                cursor.execute('''DELETE  FROM department 
                   WHERE Employee_Id =? ''',(emp_id,))
                conn.commit()
                print("EMPLOYEE DEPARTMENT REMOVED SUCCESSFULLY")
            else :
                print("YOUR ANSWER IS WRONG. PLEASE TRY AGAIN.....")
        else:
            print(f"EMPLOYEE ID {emp_id} DEPARTMENT NOT DELETED ")

    except sqlite3.Error as error_msg:
        print(f'Error Message - {error_msg}')     
    conn.close()

def department_menu():
    # MENU TO CHOOSE EMPLOYEE DEPARTMENT OPTIONS
    while True:
        try:
            print("------------DEPARTMENT MENU-----------")
            print("1.ADD EMPLOYEE DEPARTMENT\n2.VIEW EMPLOYEE DEPARTMENT\n3.EDIT EMPLOYEE DEPARTMENTt\n4.DELETE EMPLOYEE DEPARTMENT\n5.EXIT")
            admin_choice = input("Enter your choice : ")
            if admin_choice == '1':
                # FUNCTION CALL TO ADD AN EMPLOYEE TO A DEPARTMENT
                add_employee_department()
            elif admin_choice == '2':
                # FUNCTION CALL TO VIEW AN EMPLOYEE DEPARTMENT BY ADMIN
                view_employee_department_by_admin()
            elif admin_choice == '3':
                # FUNCTION CALL TO EDIT AN EMPLOYEE DEPARTMENT
                edit_employee_department()
            elif admin_choice == '4':
                # FUNCTION CALL TO DELETE AN EMPLOYEE DEPARTMENT
                delete_employee_department()    
            elif admin_choice == '5':
                # EXIT FROM LOOP
                break                
            elif admin_choice == '':
                raise ValueError("YOU MUST ENTER A VALID CHOICE")
            else :
                print("INVALID CHOICE ")
        except ValueError as error_message :
            print(f'Error Message - {error_message}')
