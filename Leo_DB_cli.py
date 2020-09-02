# This is a simple & minimal database with basic functionality.
# Name: LEO-DB
# Developed by Malay Bhavsar

# Importing the modules.
import os
database_path = "./.leo_storage"


def clear():
    os.system("cls")


def base_dir():
    # This function creates a sub-folder for storage of the data.
    if os.path.exists(f"{database_path}"):
        return 0
    else:
        os.mkdir(f'{database_path}')


def get_num_record(file_name):
    file_open = open(f"{database_path}/{file_name}", "r")
    file_data = file_open.read()
    list_data = []
    list_data = file_data.split("#END$")
    if '\n' in list_data:
        list_data.remove("\n")
    file_open.close()
    return len(list_data) - 1


def create_table(table_name, col_list):
    # This functions creates metafile for table.
    new_str = ''
    if os.path.exists(f"{database_path}/{table_name}.mdt"):
        print("[ERROR] : Table already exist! Try different name!")
    else:
        file_ls = open(f"{database_path}/{table_name}.mdt", "w")
        for m in range(len(col_list)):
            new_str += col_list[m].upper()
            if m != len(col_list) - 1:
                new_str += ","
        print(
            f"[SUCCESS] : Table Created! Number of columns: {len(col_list)}")
        file_ls.write(new_str)
        file_ls.close()
        db_file = open(f"{database_path}/{table_name}.leodb", "a")
        db_file.close()
        # Making entry of new tale created in list_table
        insert_list_table(table_name)


def insert_record(table_name, dt_list):
    db_file = open(f"{database_path}/{table_name}.leodb", "a")
    string = ''
    for i in range(len(dt_list)):
        string += dt_list[i]
        if i != len(dt_list) - 1:
            string += "#NXT$"
    string += "#END$"
    db_file.write(string)
    db_file.close()
    print(f"[SUCCESS] : Inserted Record!")


def insert_list_table(table_name):
    table_file = open(f"{database_path}/leodb_list.mdt", "a")
    string = ''
    ldb_id = get_num_record("leodb_list.mdt")
    string += f"{ldb_id}#NXT${table_name}#END$"
    table_file.write(string)
    table_file.close()


def list_table():
    table_file = open(f"{database_path}/leodb_list.mdt", "r")
    table_data = table_file.read()
    name_ls = []
    ls = []
    name_ls = table_data.split("#END$")
    for i in range(len(name_ls) - 1):
        ls = name_ls[i].split("#NXT$")
        table_name = f"{ls[1]}.leodb"
        print(f"{ls[0]}\t{ls[1]}\t Records: {get_num_record(table_name)}")
    table_file.close()


def display_table(table_name):
    if os.path.exists(f"{database_path}/{table_name}.leodb"):
        table_file = open(f"{database_path}/{table_name}.leodb", "r")
        table_data = table_file.read()
        name_ls = []
        main_ls = []
        name_ls = table_data.split("#END$")
        for i in range(len(name_ls) - 1):
            main_ls = name_ls[i].split("#NXT$")
            for j in range(len(main_ls)):
                print(f"{main_ls[j]}\t")
            print("\n")
        table_file.close()
    else:
        print("[ERROR] : No such table Exist.Try #> list to get a list of tables.")


def terminal():
    # This function must be run at start up.
    base_dir()
    clear()
    # Defining the variable.
    user_arg = ''
    database = ''
    # Start up Message.
    print("LEO-DB V1 --- Malay Bhavsar\nFor help type #> help")
    # Creating a loop for multiple operation.
    arg_ls = []
    while user_arg.lower() != 'exit':
        user_arg = input("\n#> ")
        arg_ls = user_arg.split(" ")
        # Running the if-else.
        if arg_ls[0].lower() == 'help':
            help_me()
        elif arg_ls[0].lower() == 'exit':
            print("Thank you for using me! :) Regards form Database Developer!")
        elif arg_ls[0].lower() == 'clear':
            clear()
        elif arg_ls[0].lower() == 'create':
            new_str = ''
            col_list = []
            for i in range(2, len(arg_ls)):
                new_str += arg_ls[i]
                if i != len(arg_ls) - 1:
                    new_str += ' '
            col_list = new_str.split(",")
            create_table(arg_ls[1], col_list)
        elif arg_ls[0].lower() == 'insert':
            if os.path.exists(f"{database_path}/{arg_ls[1]}.mdt") and os.path.exists(f"{database_path}/{arg_ls[1]}.leodb"):
                new_str = ''
                dt_list = []
                for i in range(2, len(arg_ls)):
                    new_str += arg_ls[i]
                    if i != len(arg_ls) - 1:
                        new_str += ' '
                dt_list = new_str.split(",")
                insert_record(arg_ls[1], dt_list)
            else:
                print("[ERROR] : No such Table Exist!")
        elif arg_ls[0].lower() == 'list':
            list_table()
        elif arg_ls[0].lower() == 'display':
            if len(arg_ls) == 2:
                display_table(arg_ls[1])
            else:
                print("[ERROR] : Please Enter proper Syntax. Type #> help")
        elif len(user_arg) == 0:
            pass
        else:
            print("[ERROR]: INVALID INPUT")


def help_me():
    print("\nWelcome to Help Me of LEO-DB V1\n")
    print("Here are some of the commands you can go with!\n")
    print("create table_name col_1,col_2,col_3...\t-->  To create a new database.")
    print("insert table_name value_1,value_2.....\t-->  To add a new entry")
    print("list\t\t\t\t\t-->  To Display names of table.")
    print("display table_name\t\t\t-->  To Display the table records.")
    print("clear\t\t\t\t\t-->  To clear the terminal screen")
    print("exit\t\t\t\t\t-->  To exit the program")
    print("More functionality will be added in te future! Stay tuned :)")


# Starting the program CLI-UI.
terminal()
