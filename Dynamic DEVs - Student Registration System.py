import sqlite3
from os import system, name # os for clear function
from time import sleep
import getpass


# Connect to db
conn = sqlite3.connect('StudentInformation.db')

# Create cursor
c = conn.cursor()

# Create table
# Try except 
try:
    c.execute("""CREATE TABLE user (
            username text,
            fullname text,
            email text,
            passwd text
        )
        """)
except:
    pass

try:
    c.execute("""CREATE TABLE students (
            studentId text,
            name text,
            reg_status text,
            uId text
        )
        """)
except:
    pass

# Create another table for courses and section
try:
    c.execute("""CREATE TABLE courses (
            reg_id text,
            courses text,
            section text
        )
        """)
except:
    pass



  
  
# define our clear function 
def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 



def reg_status_fn():
    reg_input = int(input('\nRegistration Status: \n\t1. Completed  2. Partially Completed  3. Pending\nEnter 1, 2 or 3: '))
    
    if reg_input == 1:
        n = 'Completed'
    elif reg_input == 2:
        n = 'Partially Completed'
    else:
        n = 'Pending'
    
    return n




def search_print(id_input,uId):
    
    if id_input == 0:
        clear()
        print('\n\t-----------Searching (by Student ID)-----------\n\n')
        id_input = input('ID Number: ')
        print('Searching ',flush=True,end="")
        sleep(0.5)
        print('.',flush=True,end="")
        sleep(0.5)
        print('.',flush=True,end="")
        sleep(0.3)
        print('.',flush=True,end="")


    c.execute("SELECT rowid, * FROM students WHERE studentId = ? AND uId = ?",(id_input,uId))
    #c.execute("SELECT rowid, * FROM students WHERE uId = ?",(uId))
    infos = c.fetchall()
    #print(infos)
    if len(infos)>=1:
        c.execute("SELECT * FROM courses WHERE reg_id = ?",(str(infos[0][0]),))
        infos_course = c.fetchall()
        conn.commit()
        print('\nHere is the Student Information:\n')

        print(f'\tStudent ID: {id_input}')
        print(f'\tName: {infos[0][2]}\n')
        print('\t Courses      Section')
        for info in infos_course:
            print('\t',info[1],'\t',info[2])
        print(f'\n\tRegistration Status: {infos[0][3]}')

    else:
        print('\n\nNot found!!!')


    input('\nPress any key to continue...')




def update_student(uId):
    clear()
    print('\n\t-----------Update Student Information-----------\n')
    id_input = input("ID Number: ")
    c.execute("SELECT rowid, * FROM students WHERE studentId = ? AND uId = ?",(id_input,uId))
    infos = c.fetchall()
    if len(infos)>=1:
        print(f'\n\t-----------Update Information of ID: {id_input}------------\n\n')
        

        print('\t\t1. Update Name\n\t\t2. Update Courses\n\t\t3. Update Registration Status\n\t\t4. Show Updated Information\n\n')
        while True:
            n = input("Enter 1, 2, 3 or 4: ")
            if n =='1':
                name = input("Enter Updated Name: ")
                c.execute("UPDATE students SET name = ? WHERE studentId = ?",(name,id_input))
                conn.commit()

            elif n == '2':
                reg_id = str(infos[0][0])
                c.executemany("DELETE FROM courses WHERE reg_id = ?",reg_id)
                course_sec = [tuple(x.split(':')) for x in input('Courses and Section: Input Style "CSE231:C" \nEnter all courses: \n').split()]
                id_course_sec = [(reg_id,) + item for item in course_sec]
                c.executemany("INSERT INTO courses VALUES (?,?,?)",id_course_sec)
                conn.commit()

            elif n == '3':
                reg = reg_status_fn()
                c.execute("UPDATE students SET reg_status = ? WHERE studentId = ?",(reg,id_input))
                conn.commit()
                

            elif n == '4':
                search_print(id_input,uId)
                return
    else:
        print("\nNot Found!!!")

    input('\nPress any key to continue...')
    


def delete_student(uId):
    clear()
    print('\n\t-----------Deleting (by Student ID)-----------\n')
    id_input = input('ID Number: ')
    c.execute("SELECT rowid, * FROM students WHERE studentId = ? AND uId = ?",(id_input,uId))
    infos = c.fetchall()
    if len(infos)>=1:
        c.execute("DELETE FROM students WHERE studentId = ?",(id_input,))
        c.executemany("DELETE FROM courses WHERE reg_id = ?",(str(infos[0][0]),))
        conn.commit()
        print('Deleting ',flush=True,end="")
        sleep(0.3)
        print('.',flush=True,end="")
        sleep(0.3)
        print('.',flush=True,end="")
        sleep(0.2)
        print('.',flush=True,end="")
        print('\nDeleted!!!')
        #print('\nRegistration Deleted successfully of ID',id_input)
    else:
        print("Not Found!!!")
    
    input('\nPress any key to continue...')




def add_student(uId):
    clear()
    # Inputing data
    print('\n\t-----------Add Student (Enter these information Properly)-----------\n')
    id_input = input('ID number: ')
    name = input('\nName: ')
    #print('Courses and Section: Input Style "CSE231:C" \nEnter all courses: ')
    print()
    course_sec = [tuple(x.split(':')) for x in input('Courses and Section: Input Style "CSE231:C" \nEnter all courses: \n\n').split()]
    reg = reg_status_fn()


    c.execute("INSERT INTO students VALUES (?,?,?,?)",(id_input,name,reg,uId))
    reg_id = c.lastrowid
    id_course_sec = [(reg_id,) + item for item in course_sec]
    c.executemany("INSERT INTO courses VALUES (?,?,?)",id_course_sec)

    conn.commit()
    
    print('Registration Recorded of ID',id_input)
    search_print(id_input,uId)



def menu(uId):
    while True:
        clear()
        print('\n\t----------------Semester Registration System----------------\n\t\t\t     By The Dynamic DEVs\n\n')
        print('\t\t\t1. Add a New Student\n\t\t\t2. Search by Student ID\n\t\t\t3. Update Student Information\n\t\t\t4. Delete Registration Record\n\n')
        n = input("Enter 1, 2, 3, 4 and 'e' for exit: ")
        if n =='1': add_student(uId)
        elif n == '2': search_print(0,uId)
        elif n == '3': update_student(uId)
        elif n == '4': delete_student(uId)
        elif n == 'e': exit()



def login():
    print('\n\n\t\t--------------Login--------------\n\n')
    login_uname = input('\tUsername: ')
    login_pass = getpass.getpass('\tPassword: ')
    c.execute("SELECT rowid, * FROM user WHERE username = ? AND passwd = ?",(login_uname,login_pass))
    info = c.fetchall()
    if len(info)>=1:
        menu(str(info[0][0]))
    else:
        print('\n\nYour Username or Password are incorrect! Please Try again!')
        n = input("Press 1. Register or 2. Login: ")
        if n=='1':
            register()
        else:
            login()


def register():
    print('\n\n\t\t--------------Create an Account--------------\n\n')
    reg_uname = input('\tUsername: ')
    reg_name = input('\tFull Name: ')
    reg_email = input('\tEmail: ')
    reg_pass = input('\tPassword: ')
    reg_conf_pass = input('\tConfirm Password: ')
    if reg_pass == reg_conf_pass:
        c.execute("INSERT INTO user VALUES (?,?,?,?)",(reg_uname,reg_name,reg_email,reg_pass))
        conn.commit()
        print("Successfully Registered!!! Now Login!\n\n")
        login()
    else:
        print("Password does not match! Try again!")
        input("Press any key for try again! ")
        register()
    




# Login Screen
clear()
print('\n\t----------------Semester Registration System----------------\n\t\t\t     By The Dynamic DEVs\n\n')
print('\t\t\t1. Login     2. Register\n\n')
choose = input('Enter 1 or 2: ')
if choose == '1': login()
elif choose == '2': register()
else: exit()