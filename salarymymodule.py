import sqlite3


conn =sqlite3.connect('emp_mngmnt.db')
cursor = conn.cursor()


def check_employee(employee_id):
        #Function To check If an Employee_Id Exists
        conn = sqlite3.connect('emp_mngmnt.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT COUNT(*) FROM employee WHERE Employee_Id = ?
                              ''',(employee_id,))
        # print(employee_data)
        result = cursor.fetchone()
        count= result[0]  if result else 0
        
        return count > 0

def add_salary():
    # Function To Add Salary  For an Employee
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()

    print("ENTER THE EMPLOYEE DETAILS -")
    emp_id = 0 
    while emp_id == 0:
        
            emp_id = (input("ENTER THE EMPLOYEE ID : "))
            try :
                if emp_id == '' or emp_id.isdigit() == False :
                    raise ValueError("YOU MUST ENTER A VLID EMPLOYEE ID")
            except ValueError as error_message:
                print(f'Error Message - {error_message}') 
            if check_employee(emp_id)   :
                print(f'EMPLOYEE ID EXISTS')
                
                basic_pay = 0.0
                while basic_pay == 0.0:
                    basic_pay = float(input("ENTER THE BASIC SALARY :"))
                da = 0.0
                while da == 0.0 :
                    da = float(input("ENTER THE DA : "))
                hra = 0.0
                while hra == 0.0:
                    hra = float(input("ENTER THE HRA : "))
                medical_allow = 0.0
                while medical_allow == 0.0:
                    medical_allow = float(input("ENTER THE MEDICAL ALLOWANCES : "))
                net_salary = basic_pay+da+hra+medical_allow
                try:
                    cursor.execute('''INSERT INTO salary (Basic_Pay,DA,HRA,
                                Medical_Allowance,Net_Salary,Employee_Id) VALUES(?,?,?,?,?,?)
                                ''',(basic_pay,da,hra,medical_allow,net_salary,emp_id))
                    conn.commit()
                    print(f'SALARY OF EMPLOYEE ID -{emp_id} ADDED SUCCESSFULLY')
                except sqlite3.Error as error_msg:
                    print(f'Error Message {error_msg}')
            else:
                print("EMPLOYEE ID DOES NOT EXISTS. PLEASE TRY ANOTHER ID")
    conn.close()        
   
def view_salary_by_admin():
    # ADMIN FUNCTION
    # FUNCTION TO VIEW SALARY OF ALL EMPLOYEES 
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM salary INNER JOIN employee
                   WHERE salary.Employee_Id = employee.Employee_ID''')
    employeedata = cursor.fetchall()
    
    for employee in employeedata:
        
        print("Employee Id : ", employee[1])
        print("Employee Name : ", employee[8])
        print("Employee Salary Id : ", employee[0])
        print("Basic Pay : ", employee[2])
        print("D A : ", employee[3])
        print("H R A : ", employee[4])
        print("Medical Allowances : ", employee[5])
        print("NET Salary  : ",employee[6])
        print("------------------------------------")
  
    conn.close()

def view_salary_by_employee(emp_id):
    # EMPLOYEE FUNCTION
    # FUNCTION TO VIEW SALARY OF AN EMPLOYEE
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM salary INNER JOIN employee
                   WHERE salary.Employee_Id =? AND employee.Employee_ID = ?''',(emp_id,emp_id))
    employee = cursor.fetchone()
    
    if employee:
        print("SALARY DETAILS OF EMPLOYEE")
        print("-"*50)
        print("Employee Id : ", employee[1])
        print("Employee Name : ", employee[8])
        print("Employee Salary Id : ", employee[0])
        print("Basic Pay : ", employee[2])
        print("D A : ", employee[3])
        print("H R A : ", employee[4])
        print("Medical Allowances : ", employee[5])
        print("NET Salary  : ",employee[6])
        print("------------------------------------")

    else :
        print("YOUR SALARY DETAILS ARE NOT AVAILABLE NOW. PLEASE CONTACT ADMIN.")
    
    conn.close()

def edit_salary():
    # ADMIN FUNCTION
    # FUNCTION ALLOWS ADMIN TO EDIT THE SALARY OF AN EMPLOYEE 
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()

    while True:
        try:  
            # CHECKING IF THE ENTERED EMPLOYEE IS IS VALID
            emp_id = 0 
            while emp_id == 0:
                emp_id = (input("ENTER THE EMPLOYEE ID : "))
                try:
                    if emp_id == '' or emp_id.isdigit() == False :
                        raise ValueError("YOU MUST ENTER A VLID EMPLOYEE ID")
                  
                    else:
                        if check_employee(emp_id) == 0  :
                            print(f'EMPLOYEE ID {emp_id} DOES NOT EXISTS')
                            return
                            
                        else:
                            cursor.execute(''' SELECT Salary_Id FROM salary
                                            WHERE Employee_Id = ?''',(emp_id,))
                            print("ENTER THE NEW SALARY DETAILS :")
                  
                            try:    
                                basic_pay = float(input("Enter the New Basic Pay :"))
                                # raise TypeError("Invalid Values")
                                da = float(input("Enter the New DA : "))
                                # raise TypeError("Invalid Values")
                                hra = float(input("Enter the New HRA : "))
                                # raise TypeError("Invalid Values")
                                medical_allow = float(input("Enter the New Medical ALlowances : "))
                                net_salary = basic_pay+da+hra+medical_allow
                                # raise TypeError("Invalid Values")
                            except TypeError as error_message :
                                print(f'Error Message- {error_message}')
                               
                except ValueError as error_message :
                                print(f'Error Message- {error_message}')   
                try:
                    cursor.execute('''UPDATE salary SET Basic_Pay=?,DA=?,HRA=?,
                                Medical_Allowance=?,Net_Salary = ? WHERE Employee_Id = ?
                                ''',(basic_pay,da,hra,medical_allow,net_salary,emp_id))
                    conn.commit()
                    print(f'SALARY OF EMPLOYEE ID {emp_id}  UPDATED SUCCESSFULLY')
                except sqlite3.Error as error_msg:
                    print(f'Error Message {error_msg}')
            else:
                print("EMPLOYEE ID DOES NOT EXISTS. PLEASE TRY ANOTHER ID.")
        except ValueError as error_message:
            print(f'Error Message - {error_message}')
        finally :
            print("EMPLOYEE SALARY EDIT PROCESS FINISHED")        
    conn.close()    
           
def employee_salary():
    # ADMIN FUNCTION
    # MENU FOR CHOOSING THE SALARY ORIENTED OPERATIONS
    while True:
        try:
            print("------------SALARY OF EMPLOYEES-----------")
            print("1.SALARY ENTRY\n2.VIEW SALARY OF EMPLOYEES\n3.EDIT SALARY OF AN EMPLOYEE\n4.EXIT")
            admin_choice = input("ENTER YOUR CHOICE : ")
            if admin_choice == '1':
                # FUNCTION CALL TO ADD THE SALARY OF AN EMPLOYEE
                add_salary()

            elif admin_choice == '2':
                # FUNCTION CALL TO VIEW SALARY OF ALL EMPLOYEES
                view_salary_by_admin()

            elif admin_choice == '3':
                # FUNCTION CALL TO EDIT SALARY OF AN EMPLOYEE
                 edit_salary()

            elif admin_choice == '4' :
                # EXIT FROM LOOP
                break

            elif admin_choice == '':
                raise ValueError("YOU MUST ENTER A VALID CHOICE")
            else :
                print("INVALID CHOICE")
        except ValueError as error_message :
            print(f'Error Message - {error_message}')
                  
