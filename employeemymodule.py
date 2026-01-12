import sqlite3
import re
from salarymymodule import check_employee

conn =sqlite3.connect('emp_mngmnt.db')
cursor = conn.cursor()

def add_employee():
        # ADMIN FUNCTION
        # FUNCTION TO ADD AN EMPLOYEE RECORD
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    choice = 'Y'
    while choice.upper() == 'Y' or choice.upper() == 'YES':
        print("Enter the Employee Details -")
        try:
            # ENTERING THE EMPLOYEE NAME
            emp_name = ''
            while emp_name == '':
                emp_name= input("Enter the Employee Name : ")
                #ENTERING THE GENDER OF EMPLOYEE
            gender = ''
            while gender == '':
                gender = input("Enter the Gender [M/F]: ")
                # ENTERING THE DATE OF JOINING
                # CHECKING THE DATE OF JOINING ENTERED IS VALID USING REGEX
            match1 =[]
            while match1 == [] :
                date_of_join = input("Enter the date of joining [YYYY/MM/DD] : ")
                check_pattern_for_date_of_join = r'^\d{4}[-/]\d{2}[-/]\d{2}$'
                match1 =re.findall(check_pattern_for_date_of_join,date_of_join)
                if match1 == []:
                    raise ValueError("You must enter a valid date  ")   
              # ENTERING THE EMPLOYEE ADDRESS
            emp_address = ''
            while emp_address == '':
                emp_address = input("Enter the Employee Address : ")
                # CHECKING THE PHONE NUMBER ENTERED IS VALID 
            match2 = []
            while match2 == []:
                phone_num = input("Enter the contact number : ")
                mobile_num_pattern =  r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                match2 = re.findall(mobile_num_pattern,phone_num)
                if match2 == [] :
                    raise ValueError("Enter a valid Phone Number")
                # CHECKING THE EMAIL ID ENTERED IS VALID
            match3 = []
            while match3 == []:
                email_id = input("Enter the email address : ")  
                email_addr_pattern = r'([a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-z]+)'
                match3 =re.findall(email_addr_pattern,email_id)
        
                if match3 == [] :
                    raise ValueError("Enter a valid email id")
                
                    
        except ValueError as e:
                print(f"Error :{e}")

        # FINDING THE EMPLOYEE DATA DUPLICATION
        # ALL DETAILS ARE CROSS CHECKED TO FIND AN ALREADY ENTERED EMPLOYEE RECORD   

        cursor.execute('''SELECT * FROM employee WHERE Employee_Name = ? AND Gender = ? AND Date_Of_Joining = ? AND
                        Employee_Address = ? AND Phone_Number = ? AND Email_Id = ?
                        ''',(emp_name,gender,date_of_join,emp_address,phone_num,email_id))
        employee_data = cursor.fetchone()
        if employee_data :
            print("Employee Data Duplication Noticed. Please add next employee ")
        else:
            # IF NO DUPLICATION IS FOUND, EMPLOYEE DATA IS INSERTED IN THE EMPLOYEE TABLE
            try:
                cursor.execute('''INSERT INTO employee (Employee_Name,Gender,Date_Of_Joining,
                            Employee_Address,Phone_Number,Email_Id) VALUES(?,?,?,?,?,?)
                            ''',(emp_name,gender,date_of_join,emp_address,phone_num,email_id))
                conn.commit()
                print("Employee Added Successfully")
                
            except sqlite3.Error as error_msg:
                print(f'Error Message {error_msg}')
        print("Do You Want To Add Another Employee")
        choice = input("Enter the choice [Y/N] :")
                
    conn.close()
                
def view_employees_by_admin():
    # ADMIN FUNCTION
    # FUNCTION TO VIEW ALL EMPLOYEE RECORDS BY ADMIN
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM employee  
                   ''')
    employeedata = cursor.fetchall()
    num_employees = len(employeedata)
    print(f"The number of employees is: {num_employees}")
    emp_number = 1
    for employee in employeedata:    
        print(f'Employee Number {emp_number}')
        print("Employee Id :",employee[0])
        print("Employee Name :",employee[1])
        print("Employee Gender : ", employee[2])
        print("Employee Date Of Joining : ", employee[3])
        print("Employee Address : ", employee[4])
        print("Employee Phone Number : ", employee[5])
        print("Employee Email : ", employee[6])
        print("------------------------------------")
        emp_number += 1
    conn.close()

def edit_employee():
    # ADMIN FUNCTION
    # FUNCTION TO EDIT AN EMPLOYEE RECORD
    conn =sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    while True :
        try:   
            # CHECKING IF THE ENTERED EMPLOYEE IS IS VALID
            emp_id = 0 
            while emp_id == 0:
                emp_id = (input("Enter the Employee ID : "))
                try :
                    if emp_id == '' or emp_id.isdigit() == False :
                        raise ValueError("You must enter a valid Employee Id")
                    else:
                        if check_employee(emp_id) == 0   :
                            print(f'Employee Id {emp_id} Does Not Exists.Please Try Another')
                            return
                        
                except ValueError as error_message:
                             print(f'Error Message - {error_message}')
            
            admin_choice = 0
            while admin_choice == 0 :  
                  
                print("What do you want to edit ?")
                print("1.Employee Address\n2.Employee Phone Number\n3.Employee Email Id\n4.Exit")
                admin_choice = input("Enter your choice : ")
        
                if admin_choice == '1' :
                    
                    # EDITING EMPLOYEE ADDRESS
                        
                        cursor .execute(''' SELECT Employee_Address FROM employee where Employee_Id = ?
                                        ''',(emp_id,))
                        data = cursor.fetchone()
                        print(f'Previous Employee Address is : {data}')
                        emp_address = input("Enter the employee address to update :")
                        cursor.execute('''UPDATE employee SET Employee_Address=? WHERE Employee_Id = ?
                                    ''',(emp_address,emp_id))
                        conn.commit()
                        print("Employee Address successfully updated.......")
                        
                    
                elif admin_choice == '2' :
                    # EDITING THE EMPLOYEE PHONE NUMBER
                    
                    cursor .execute(''' SELECT Phone_Number FROM employee where Employee_Id = ?
                                    ''',(emp_id,))
                    data = cursor.fetchone()
                    print(f'Previous Phone Number is : {data}')
                    # CHECKING THE PHONE NUMBER FORMAT REGEX
                    match2 = []
                    while match2 == []:
                        emp_phone_number = input("Enter the employee phone number :")
                        mobile_num_pattern =  r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
                        match2 = re.findall(mobile_num_pattern,emp_phone_number)
                        if match2 == [] :
                            raise ValueError("Enter a valid Phone Number")
                    
                    cursor.execute('''UPDATE employee SET Phone_Number =? WHERE Employee_Id = ?
                                ''',(emp_phone_number,emp_id))
                    conn.commit()
                    print("Employee Phone Number successfully updated......")
                    
                    
                elif admin_choice == '3' :
                    # EDITING THE EMPLOYEE EMAIL ID
                    
                    cursor .execute(''' SELECT Email_Id FROM employee where Employee_Id = ?
                                    ''',(emp_id,))
                    data = cursor.fetchone()
                    print(f'Previous Email Id is : {data}')
                    # CHECKING THE EMAIL ID FORMAT REGEX
                    match3 = []
                    while match3 == []:
                        emp_email_id = input("Enter the Email Id to update :")
                        email_addr_pattern = r'([a-zA-Z0-9.]+@[a-zA-Z0-9]+.[a-z]+)'
                        match3 =re.findall(email_addr_pattern,emp_email_id)
                
                        if match3 == [] :
                            raise ValueError("Enter a valid email id")
                   
                    cursor.execute('''UPDATE employee SET Email_Id =? WHERE Employee_Id = ?
                                ''',(emp_email_id,emp_id))
                    conn.commit()
                    print("Employee Email Id successfully updated ......")
                    
                    break
                elif admin_choice == '4':
                    break
                elif admin_choice == '':
                    raise ValueError("You must enter a valid choice")
                else:
                    print("Invalid choice")
            break        
        except ValueError as error_message:
            print(f'Error Message - {error_message}')
        finally :
            print("EMPLOYEE EDIT PROCESS FINISHED")
    conn.close()

def delete_employee():
    #Function To Delete an Employee
    employee_id = int(input("Enter the Employee Id to delete :"))
    if check_employee(employee_id) == 0:
        print(f'Employee Id {employee_id} Does Not Exist .Please Try Another Id')
        return
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    try:
        #ADDITIONAL CONFIRMATION QUESTION TP DELETE EMPLOYEE DATA
        delete_question = input("Are You Sure That You Want To Delete The Employee [Y/N]?")
        if delete_question.upper() == 'Y' or delete_question.upper() == 'YES':
            confirm_qn =int(input("If YES - Give the Answer For SUM OF  55 AND 45 :"))
            if confirm_qn == 100:
                cursor.execute('''DELETE  FROM employee WHERE Employee_Id = ?
                          ''',(employee_id,))
                conn.commit()
                print(f"Employee Id {employee_id} Deleted Successfully.....")
            else:
                print("YOUR ANSWER IS WRONG. PLEASE TRY AGAIN")
        else :
            print(f"Employee Id {employee_id} Not Deleted.....")
    except sqlite3.Error as error_msg:
        print(f'Error Message - {error_msg}')  

def view_details_by_employee(employee_id):      
    # FUNCTION TO VIEW EMPLOYEE OWN DETAILS
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM employee INNER JOIN department WHERE employee.Employee_Id = ? AND 
            department.Employee_Id = ?      ''',(employee_id,employee_id))
    employee_data = cursor.fetchone()
    
    print("Employee Id : ", employee_data[0])
    print("Employee Name : ", employee_data[1])
    print("Employee Gender : ", employee_data[2])
    print("Employee Date Of Joining : ", employee_data[3])
    print("Employee Department Name  : ", employee_data[8])
    print("Employee Address : ", employee_data[4])
    print("Employee Phone Number : ", employee_data[5])
    print("Employee Email : ", employee_data[6])
    print("------------------------------------")    
    conn.close()   

def employee_data_crud():
    # ADMIN FUNCTION
    #  MENU TO CHOOSE EMPLOYEE CRUD OPERATIONS
    while True:
        try:    
            print("\nEMPLOYEE DATA CRUD OPERATION MENU")
            print("1.ADD EMPLOYEE\n2.VIEW EMPLOYEE\n3.EDIT EMPLOYEE\n4.DELETE EMPLOYEE\n5.EXIT")
            admin_choice_2 = input("Enter your choice : ")
            if admin_choice_2 == '1':
                # FUNCTION CALL TO ADD AN EMPLOYEE
                add_employee()
            elif admin_choice_2 == '2':
                #FUNCTION CALL TO VIEW EMPLOYEE RECORDS
                view_employees_by_admin()
            elif admin_choice_2 == '3':
                #FUNCTION CALL TO EDIT AN EMPLOYEE
                edit_employee()
            elif admin_choice_2 == '4':
                #FUNCTION CALL TO DELETE AN EMPLOYEE
                delete_employee()
            elif admin_choice_2 == '5':
                 break
            elif admin_choice_2 == '':
                raise ValueError("You must enter a valid choice")
            else:
                 print("Invalid Choice ")
        except ValueError as error_message:
            print(f'Error Message -{error_message}')
