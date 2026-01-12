import sqlite3
import re
from datetime import datetime
import  mysql.connector
from salarymymodule import check_employee


conn =sqlite3.connect('emp_mngmnt.db')
cursor = conn.cursor()


    
def view_leave_by_employee(emp_id):
    # EMPLOYEE FUNCTION
    # TO VIEW LEAVES OF AN EMPLOYEE
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    cursor.execute('''SELECT * FROM leave_requests INNER JOIN employee
                   WHERE leave_requests.employee_id =? AND employee.Employee_ID = ?''',(emp_id,emp_id))
    employee_leave_list = cursor.fetchall()
    if employee_leave_list:
        for employee in employee_leave_list:
            print("YOUR LEAVE DETAILS -")
            print("EMPLOYEE ID: ", employee[1])
            print("EMPLOYEE NAME : ", employee[10])
            print("EMPLOYEE LEAVE ID : ", employee[0])
            print("LEAVE START DATE: ", employee[3])
            print("LEAVE END DATE : ", employee[4])
            print("STATUS OF YOUR LEAVE REQUEST: ", employee[6])
            print("REASON FOR YOUR LEAVE : ", employee[5])
            print("------------------------------------")
        
    else :
        print("NO LEAVE DETAILS AVAILABLE FOR YOU......")
    
    conn.close()

def view_leaves_of_employee():
    # ADMIN FUNCTION
    # FUNCTION TO VIEW LEAVES OF ALL EMPLOYEES
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    emp_id=0
    while emp_id == 0:
        
            emp_id = (input("ENTER THE EMPLOYEE ID TO VIEW LEAVES  : "))
            try :
                if emp_id == '' or emp_id.isdigit() == False :
                    raise ValueError("YOU MUST ENTER A VALID EMPLOYEE ID")
            except ValueError as error_message:
                print(f'Error Message - {error_message}') 
            if check_employee(emp_id)   :
                cursor.execute('''SELECT * FROM leave_requests INNER JOIN employee
                   WHERE leave_requests.employee_id =? AND employee.Employee_ID = ?''',(emp_id,emp_id)) 
                conn.commit()

                leave_data = cursor.fetchall()
    
                for employee in leave_data:
                    # PRINTING THE LEAVE DETAILS OF AN EMPLOYEE
                    print("EMPLOYEE ID : ", employee[1])
                    print("EMPLOYEE NAME : ", employee[11])
                    print("EMPLOYEE LEAVE ID : ", employee[0])
                    print("LEAVE START DATE : ", employee[3])
                    print("LEAVE END DATE : ", employee[4])
                    print("NUMBER OF DAYS OF LEAVE : ", employee[9])
                    print("LEAVE TYPE : ",employee[2])
                    print("REASON FOR LEAVE : ", employee[5])
                    print("STATUS OF LEAVE REQUEST",employee[6])
                    print("------------------------------------")
            else :
                print(f'EMPLOYEE ID {emp_id} DOES NOT EXISTS. PLEASE TRY ANOTHER ID')
        
    conn.close()

    

def calculate_leave_days(start_date_str, end_date_str, date_format='%Y-%m-%d'):
    """
    Calculates the number of full days of leave between a start and end date string.

    Args:
        start_date_str (str): The leave start date string (e.g., '2025-01-15').
        end_date_str (str): The leave end date string (e.g., '2025-01-20').
        date_format (str): The format of the date strings. Defaults to '%Y-%m-%d'.

    Returns:
        int: The number of days of leave.
    """
    # Convert string dates to datetime objects
    start_date = datetime.strptime(start_date_str, date_format)
    end_date = datetime.strptime(end_date_str, date_format)

    # Calculate the difference (timedelta object)
    duration = end_date - start_date

    # Return the number of days
    # This result represents the number of full 24-hour periods between the dates.
    return duration.days

def request_leave(employee_id):
        # EMPLOYEE FUNCTION
        # TO REQUEST FOR LEAVE BY AN EMPLOYEE

    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
            
    
    print("EMPLOYEE MANAGEMENT SYSTEM -EMPLOYEE OPERATIONS")
    print("LEAVE APPLICATION SECTION")
    match = []
    while match == []:
        try:    
            # CHECKING THE VALIDITY OF LEAVE START DATE USING REGEX
            leave_start_date = input("ENTER THE LEAVE START DATE YOU WANT TO APPLY FOR (YYYY/MM/DD) : ")
            check_pattern_for_leave_start_date = r'^\d{4}[-/]\d{2}[-/]\d{2}$'
        
            match =re.findall(check_pattern_for_leave_start_date,leave_start_date)
            if match == []:
                raise ValueError("YOU MUST ENTER IN VALID DATE FORMAT [YYYY/MM/DD] -OK?")   
            
            else:
                # CHECKING THE VALIDITY OF LEAVE END DATE USING REGEX
                leave_end_date =input("ENTER THE LEAVE END DATE YOU WANT TO APPLY FOR (YYYY/MM/DD) : ")
                check_pattern_for_leave_start_date = r'^\d{4}[-/]\d{2}[-/]\d{2}$'
        
                match1 =re.findall(check_pattern_for_leave_start_date,leave_end_date)
                # CALCULATING THE NUMBER OF DAYS OF LEAVE
                number_of_days_leave = calculate_leave_days(leave_start_date,leave_end_date,date_format='%Y/%m/%d')
                if match1 == []:
                    raise ValueError("YOU MUST ENTER IN VALID DATE FORMAT [YYYY/MM/DD] -OK? ")   
                else:
                    try:
                        choice_leave_type = '' 
                        while choice_leave_type == '':
                            print("CHOOSE THE LEAVE TYPE-\n1.SICK\n2.CASUAL")
                            choice_leave_type =input("ENTER THE CHOICE : ")
                            if choice_leave_type == '1':
                                leave_type = 'SICK LEAVE'
                            elif choice_leave_type == '2':
                                leave_type = 'CASUAL LEAVE'
                            else :
                                print("INVALID LEAVE TYPE")
                            
                            # ENTER THE REASON OF LEAVE
                        reason_of_leave = input("\nENTER THE REASON FOR YOUR LEAVE : ")
                        if reason_of_leave == '':
                            raise ValueError("YOU MUST ENTER A REASON ")
                    except ValueError as errorr_message3 :
                        print(f'ERROR MESSAGE -{errorr_message3}')         

                    
                    cursor.execute('''INSERT INTO leave_requests (
                                    employee_id, leave_type,start_date, end_date,Number_Of_Days, reason, status) 
                                        VALUES (?,?,?,?,?,?,?)''',
                                        (employee_id,leave_type, leave_start_date, leave_end_date,number_of_days_leave, reason_of_leave, 'Pending'))
    

                    conn.commit()
                    print(f"LEAVE REQUEST SUBMITTED SUCCESSFULLY FOR EMPLOYEE ID - {employee_id}!")
                    
                    
        except ValueError as error_message2:
            print(f'Error Message -{error_message2}')

        finally:
            cursor.close()
            conn.close()


def view_pending_leave_requests():
    # ADMIN FUNCTION
    # ALLOWS ADMIN TO VIEW ALL PENDING LEAVE REQUESTS
    
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute('''SELECT * FROM leave_requests WHERE status = 'Pending' ''')
        
        conn.commit()
        requests = cursor.fetchall()
        if requests:
            for req in requests:
                print(f'PENDING REQUEST ID: {req[0]}, EMPLOYEE ID: {req[1]}, STATUS: {req[6]} , LEAVE START DATE:{req[3]}, LEAVE END DATE :{req[4]}, LEAVE TYPE :{req[2]} , LEAVE REASON :{req[5]}')
            return requests
        else:
            print("NO PENDING LEAVE REQUESTS.")
        
        
    except mysql.connector.Error as err:
        print(f"Error fetching requests: {err}")
        return []
    finally:
        cursor.close()
        conn.close()

def approve_reject_leave_requests():

    """ALLOWS THE ADMIN TO APPROVE OR REJECT LEAVE REQUESTS"""
    conn = sqlite3.connect('emp_mngmnt.db')
    cursor = conn.cursor()
    try:
        pending =view_pending_leave_requests()
        if pending :
            leave_to_approve_id = pending[0][0]
            
            print(f"\nADMIN PROCESSING REQUEST ID {leave_to_approve_id}...")
            status_choice = ''
            while status_choice == '':
                print(f'SELECT THE STATUS-\n1.APPROVED\n2.REJECTED')
                status_choice = input("ENTER THE OPTION - :")
                if status_choice == '1' :
                    status = 'APPROVED'
                    
                elif status_choice == '2' : 
                    status = 'REJECTED'  
                else :
                    print("YOU HAVE NOT CHOSEN AN  OPTION")
            admin_remark =input("ENTER THE REMARKS :")
            cursor.execute('''
                            UPDATE leave_requests 
                            SET status = ?, admin_remark = ?
                                WHERE leave_id = ?
                            ''', (status, admin_remark, leave_to_approve_id))
            conn.commit()
            print(f"LEAVE REQUEST {leave_to_approve_id} UPDATED TO {status}.")
            return True
        
    except mysql.connector.Error as err:
        print(f"Error updating request: {err}")
        conn.rollback()
        return False
    finally:
        cursor.close()
        conn.close()


def employee_leave_menu():
    # ADMIN FUNCTION
    # MENU TO SHOW THE EMPLOYEE LEAVE OPERATIONS
    while True:
        try:    
            print("1.VIEW LEAVE REQUESTS\n2.APPROVE OR REJECT LEAVES\n3.VIEW LEAVES OF AN EMPLOYEE\n4.EXIT")
            admin_choice_2 = input("Enter your choice : ")
            if admin_choice_2 == '1':
                # FUNCTION CALL TO VIEW PENDING LEAVE REQUESTS
                view_pending_leave_requests()
            elif admin_choice_2 == '2':
                # FUNCTION CALL TO APPROVE OR REJECT LEAVE REQUESTS
                approve_reject_leave_requests()
            elif admin_choice_2 == '3':
                # FUNCTION CALL TO VIEW LEAVES OF AN EMPLOYEE
                view_leaves_of_employee()
            elif admin_choice_2 == '4':
                # EXIT FROM LOOP
                break
            elif admin_choice_2 == '':
                raise ValueError("YOU MUST ENTER A VALID CHOICE")

            else:
                 print("INVALID CHOICE ")
        except ValueError as error_message:
            print(f'Error Message -{error_message}')

