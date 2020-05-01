# This is a simple offline database for local level storage and without any security.
# Must have python installed.
# By Malay @ 2020

# Importing the modules.
import os


def new_db():
    name = input("Enter name of Database: ")
    if os.path.exists(f"./{name}"):
        return 0
    else:
        os.mkdir(f'./{name}')
    create_info(name)


def add_entry(database):
    # Declaring the variables.
    data_value = []
    data_name = get_info(database)
    print(f"Last entry was of :: {get_last_id(database)}")
    # Checking if the database exists.(Return of 0 => Failure && 1 => Sucess)
    if os.path.exists(f"./{database}"):
        pass
    else:
        return 0
    # As per given list of data to be entered.
    print(data_name)
    for j in range(len(data_name)):
        data = input(f"{data_name[j]}: ")
        if data == '':
            data_value.append("0")
        else:
            data_value.append(data)

    # Generating the output.
    data_file = open(f"./{database}/{data_value[0]}.dbmb", "w")
    data_file.write("{")
    for i in range(len(data_name)):
        string = f"'{data_name[i].upper()}':'{data_value[i]}',"
        data_file.write(string)
    data_file.write("}")
    data_file.close()
    return 1


def add_entry_api(database, data_list):
    data_file = open(f"./{database}/{data_list[1]}.dbmb", "w")
    data_file.write("{")
    for i in range(int(len(data_list)/2)):
        string = f"'{data_list[(2 * i)]}':'{data_list[(2 * i) + 1]}',"
        data_file.write(string)
    data_file.write("}")
    data_file.close()


def read_entry(database, id_num):
    # Declaring the variable.
    is_valid = False
    data_list = []
    new_str = ''
    i = 0
    # Opening the file to read the data.
    if os.path.exists(f"./{database}/{id_num}.dbmb"):
        data_file = open(f"./{database}/{id_num}.dbmb", 'r')
        data = data_file.read()
        data_file.close()
    else:
        return 0
    # collecting the dat from the read data.
    while i < len(data):
        if data[i] == "'":
            if is_valid == True:
                is_valid = False
            else:
                is_valid = True
                i += 1
        if is_valid == True:
            new_str += data[i]
        else:
            if new_str != '':
                data_list.append(new_str)
                new_str = ''
        i += 1
    return data_list


def get_info(database):
    # Reads README.txt and returns the data_name list.
    if os.path.exists(f"./{database}/README.TXT"):
        file_ls = open(f"./{database}/README.TXT", "r")
        data_name = file_ls.read()
        file_ls.close()
        data_name = list(data_name.split(' '))
        if '' in data_name:
            data_name.remove('')
        return data_name


def create_info(database):
    # This functions creates README.txt file in the database.
    new_str = ''
    data_name = []
    if os.path.exists(f"./{database}"):
        num = int(input("Enter number of entrie:"))
        for s in range(num):
            dataname = input(f"Data_name[{s}]: ")
            data_name.append(dataname.upper())
        file_ls = open(f"./{database}/README.txt", "w")
        for m in range(len(data_name)):
            new_str += data_name[m].upper() + ' '
        file_ls.write(new_str)
        file_ls.close()


def get_last_id(database):
    # This function returns the last id.
    new_list = []
    characters = ['.', 'd', 'b', 'm']
    list_file = os.listdir(f'./{database}')
    list_file.remove('README.txt')
    for file in list_file:
        for character in characters:
            file = file.replace(character, "")
        new_list.append(int(file))
    if len(new_list) == 0:
        return -1
    else:
        return max(new_list)


def search_entry(database):
    # This function search for a specific type of entries.
    characters = ['.', 'd', 'b', 'm']
    count = 0
    data_name_ls = get_info(database)
    print(f"Search from => {data_name_ls}")
    data_name = input("Enter the parameter to be searched: ")
    data_name = data_name.upper()
    data_value = input("Entered the value to be searched: ")
    data_index = data_name_ls.index(data_name)
    list_file = os.listdir(f'./{database}')
    list_file.remove('README.txt')
    for file in list_file:
        for character in characters:
            file = file.replace(character, "")
        file_data = read_entry(database, file)
        if file_data[2 * data_index] == data_name:
            if file_data[(2*data_index) + 1] == data_value:
                display_entry(file_data)
                count += 1
    if count == 0:
        print("No such record found!")


def display_entry(data_list):
    # It takes list as input and displays it in the terminl.
    print("\n")
    for i in range(int(len(data_list)/2)):
        print(f"{data_list[(2 * i)]} : {data_list[(2 * i) + 1]}")
    print("\n")


def delete_entry(database):
    print("Search for database entries:-")
    search_entry(database)
    _id_num = int(input("Enter the ID to be Deleted: "))
    if os.path.exists(f"./{database}/{_id_num}.dbmb"):
        os.remove(f"./{database}/{_id_num}.dbmb")
        print("Task Sucessful!")
    else:
        print("No such ID found!")


def edit_entry(database):
    search_entry(database)
    entry_id = input("Enter the entry Id: ")
    data_name = input("Enter the parameter to be changed: ")
    data_name = data_name.upper()
    data_name_ls = get_info(database)
    data_index = data_name_ls.index(data_name)
    data_ls = read_entry(database, entry_id)
    data_value = data_ls[(2 * data_index) + 1]
    print(f"The parameter you are going to change has value {data_value}")
    data_value = input("Enter the new Parameter value: ")
    data_ls[(2 * data_index) + 1] = data_value
    print("New entry is...")
    display_entry(data_ls)
    add_entry_api(database, data_ls)


def terminal():
    # This function must be run at start up.
    os.system("cls")
    # Defining the variable.
    user_arg = ''
    database = ''
    is_db_open = False
    # Start up Message.
    print("Database V1 +> By Malay Bhavsar\nFor help type #>help!")
    # Creating a loop for multiple operation.
    while user_arg != 'exit':
        user_arg = input("\n#> ")
        if user_arg == 'help!':
            help_me()
        elif user_arg == 'exit':
            print("Thank you for using me! :) Regards form Database Developer!")
        elif user_arg == 'clear':
            # This is for the purpose of cleaning the screen.
            os.system("cls")
        elif user_arg == 'create_db':
            new_db()
        elif user_arg == 'add_entry':
            if is_db_open == True:
                add_entry(database)
            else:
                print("[ERROR] : OPEN A DATABASE FIRST!")
        elif user_arg == 'delete_entry':
            if is_db_open == True:
                delete_entry(database)
            else:
                print("[ERROR] : OPEN A DATABASE FIRST!")
        elif user_arg == 'open_db':
            if is_db_open == True:
                answer = input(
                    f"Already database {database} is open.Still want to continue? (Y/N) >")
                if answer == 'y' or answer == 'Y':
                    pass
                else:
                    print("ok")
            database = input("Enter the name of database: ")
            if os.path.exists(f"./{database}"):
                is_db_open = True
            else:
                print("[ERROR] : TRY AGAIN (NO SUCH DATABASE FOUND!)")
                is_db_open = False
        elif user_arg == 'search_entry':
            if is_db_open == True:
                search_entry(database)
            else:
                print("[ERROR] : OPEN A DATABASE FIRST!")
        elif user_arg == 'edit_entry':
            if is_db_open == True:
                edit_entry(database)
            else:
                print("[ERROR] : OPEN A DATABASE FIRST!")
        else:
            print("[ERROR]: INVALID INPUT")


def help_me():
    print("\nWelcome to Help Me of Database\n")
    print("Here are some of the commands you can go with!")
    print("create_db\t-->  To create a new database.")
    print("open_db \t-->  To open a existing database")
    print("add_entry\t-->  To add a new entry")
    print("delete_entry\t-->  To delete a specific entry")
    print("search_entry\t-->  To search a specific entry")
    print("clear  \t-->  To clear the terminal screen")
    print("exit  \t-->  To exit the program")


# Directing the program to main()
terminal()
