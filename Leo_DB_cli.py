# This is a simple & minimal database with basic functionality.
# Name: LEO-DB
# Developed by Malay Bhavsar

# Importing the modules.
import os
database_path = "./.leo_storage"
version = '3.0'


def clear():
    # This function helps in clearing the screen.
    os.system("cls")


def base_dir():
    # This function creates a sub-folder for storage of the data.
    if os.path.exists(f"{database_path}"):
        return 0
    else:
        os.mkdir(f'{database_path}')
        list_file = open(f"{database_path}/leodb_list.mdt", "w")
        list_file.close()


def get_num_record(file_name):
    # It returns number of records in the given file_name.
    if os.path.exists(f"{database_path}/{file_name}"):
        file_open = open(f"{database_path}/{file_name}", "r")
        file_data = file_open.read()
        list_data = []
        list_data = file_data.split("#END$")
        if '\n' in list_data:
            list_data.remove("\n")
        file_open.close()
        return len(list_data) - 1
    else:
        return -1


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
        db_file = open(f"{database_path}/{table_name}.leodb", "w")
        db_file.close()
        # Making entry of new tale created in list_table
        insert_list_table(table_name)


def delete_table(table_name):
    # Removes all files asscoiated with table_name.
    table_path = f"{database_path}/{table_name}.leodb"
    table_meta = f"{database_path}/{table_name}.mdt"
    count = 0
    if os.path.exists(table_path) and os.path.exists(table_meta):
        os.remove(table_path)
        os.remove(table_meta)
        print("[SUCCESS] : Table Deleted Successfully!")
        delete_list_table(table_name)
    else:
        print("[ERROR] : Table Not Found!")


def insert_record(table_name, dt_list):
    # To insert a record inside the given table.
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
    # Inserts entry in the main table list.
    table_file = open(f"{database_path}/leodb_list.mdt", "a")
    string = ''
    string += f"{table_name}#END$"
    table_file.write(string)
    table_file.close()


def delete_list_table(table_name):
    # Removes ebtry from the main table list.
    table_file = open(f"{database_path}/leodb_list.mdt", "r")
    table_data = table_file.read()
    table_file.close()
    os.remove(f"{database_path}/leodb_list.mdt")
    table_ls = table_data.split("#END$")
    table_ls.pop()
    if table_name in table_ls:
        table_index = table_ls.index(table_name)
        table_ls.pop(table_index)
    table_file = open(f"{database_path}/leodb_list.mdt", "w")
    string = ''
    for i in range(len(table_ls)):
        string += f"{table_ls[i]}#END$"
    table_file.write(string)
    table_file.close()


def list_table():
    # Gives a list of table.
    table_file = open(f"{database_path}/leodb_list.mdt", "r")
    table_data = table_file.read()
    table_file.close()
    name_ls = table_data.split("#END$")
    if len(name_ls) - 1 == 0:
        print("[ALERT] : Table list empty! Try creating a table.")
    else:
        print(f"Index\tTable_name\tRecords\n")
        for i in range(len(name_ls) - 1):
            table_name = f"{name_ls[i]}.leodb"
            num_record = get_num_record(table_name)
            print(f"{i}\t{name_ls[i]}\t\t{num_record}")


def display_table(table_name):
    # Display the entire records of the given table name.
    if os.path.exists(f"{database_path}/{table_name}.leodb"):
        table_file = open(f"{database_path}/{table_name}.leodb", "r")
        table_data = table_file.read()
        table_file.close()
        table_info_file = open(f"{database_path}/{table_name}.mdt", "r")
        table_info = table_info_file.read()
        table_info_file.close()
        col_list = []
        col_list = table_info.split(",")
        print(f"Index\t", end='')
        for column in col_list:
            print(f"{column}\t", end='')
        print("\n")
        name_ls = []
        main_ls = []
        name_ls = table_data.split("#END$")
        for i in range(len(name_ls) - 1):
            main_ls = name_ls[i].split("#NXT$")
            print(f"{i}\t", end='')
            for j in range(len(main_ls)):
                print(f"{main_ls[j]}\t", end='')
            print("")
    else:
        print("[ERROR] : No such table Exist.Try #> list to get a list of tables.")


def search_record(table_name, col_name, value):
    # Searchs the table for given column name with the value.
    if os.path.exists(f"{database_path}/{table_name}.leodb"):
        table_info_file = open(f"{database_path}/{table_name}.mdt", "r")
        table_info = table_info_file.read()
        table_info_file.close()
        col_list = []
        col_list = table_info.split(",")
        if col_name.upper() in col_list:
            col_index = col_list.index(col_name.upper())
            table_file = open(f"{database_path}/{table_name}.leodb", "r")
            table_data = table_file.read()
            table_file.close()
            data_ls = []
            data_ls = table_data.split("#END$")
            data_ls.pop()
            count = 0
            print(f"Index\t", end='')
            for column in col_list:
                print(f"{column}\t", end='')
            print("\n")
            for data in data_ls:
                val_ls = []
                val_ls = data.split("#NXT$")
                if value in val_ls[col_index]:
                    count += 1
                    print(f"{data_ls.index(data)}", end='\t')
                    for val in val_ls:
                        print(f"{val}", end='\t')
                    print("")
            if count == 0:
                print("No record with given data found")
        else:
            print("[ERROR] : No Such Table column exists!")
    else:
        print("[ERROR] : No such table Exist.Try #> list to get a list of tables.")


def delete_record(table_name, col_name, value):
    if os.path.exists(f"{database_path}/{table_name}.leodb"):
        table_detail_file = open(f"{database_path}/{table_name}.mdt", "r")
        table_detail = table_detail_file.read()
        table_detail_file.close()
        table_detail_ls = table_detail.split(",")
        if col_name.upper() in table_detail_ls:
            col_index = table_detail_ls.index(col_name.upper())
            table_data_file = open(f"{database_path}/{table_name}.leodb", "r")
            table_data = table_data_file.read()
            table_data_file.close()
            table_data_ls = table_data.split("#END$")
            table_data_ls.pop()
            data_string = ''
            count = 0
            value = ''.join([str(elem) for elem in value])
            for record in table_data_ls:
                record_ls = record.split("#NXT$")
                if value == record_ls[col_index]:
                    count += 1
                else:
                    data_string += record + "#END$"
            table_data_file = open(
                f"{database_path}/{table_name}.leodb", "w")
            table_data_file.write(data_string)
            table_data_file.close()
            if count != 0:
                print(f"[SUCCESS] : {count} records deleted!")
            else:
                print(f"[SUCCESS : No such record found!")
        else:
            print("[ERROR] : No such column exist!")
    else:
        print("[ERROR] : No such table exist!")


def terminal():
    # This function must be run at start up.
    base_dir()
    clear()
    # Defining the variable.
    user_arg = ''
    database = ''
    # Start up Message.
    print(f"LEO-DB Version:{version} --- Malay Bhavsar\nFor help type #> help")
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
        elif arg_ls[0].lower() == 'remove':
            if os.path.exists(f"{database_path}/{arg_ls[1]}.mdt") and os.path.exists(f"{database_path}/{arg_ls[1]}.leodb"):
                new_str = ''
                dt_list = []
                for i in range(3, len(arg_ls)):
                    new_str += arg_ls[i]
                    if i != len(arg_ls) - 1:
                        new_str += ' '
                dt_list = new_str.split(",")
                delete_record(arg_ls[1], arg_ls[2], dt_list)
            else:
                print("[ERROR] : No such Table Exist!")
        elif arg_ls[0].lower() == 'list':
            list_table()
        elif arg_ls[0].lower() == 'display':
            if len(arg_ls) == 2:
                display_table(arg_ls[1])
            else:
                print("[ERROR] : Please Enter proper Syntax. Type #> help")
        elif arg_ls[0].lower() == 'search':
            if len(arg_ls) >= 4:
                new_str = ''
                for i in range(3, len(arg_ls)):
                    new_str += arg_ls[i]
                    if i != len(arg_ls) - 1:
                        new_str += ' '
                search_record(arg_ls[1], arg_ls[2], new_str)
            else:
                print("[ERROR] : Please Enter proper Syntax. Type #> help")
        elif arg_ls[0].lower() == 'delete':
            if os.path.exists(f"{database_path}/{arg_ls[1]}.leodb"):
                confirm = input("Re-enter Table name for Confirmation: ")
                if confirm == arg_ls[1]:
                    delete_table(arg_ls[1])
                else:
                    print("[ABORT] : Table deletion aborted!")
            else:
                print("[ERROR] : No such table Exist.")
        elif len(user_arg) == 0:
            pass
        else:
            print("[ERROR]: INVALID INPUT")


def help_me():
    # THis function helps the user with the syntax and this database.
    print(f"\nWelcome to Help Me of LEO-DB Version:{version}")
    print("Here are some of the commands you can go with!\n")
    print("create table_name col_1,col_2,col_3...\t-->  To create a new database.")
    print("insert table_name value_1,value_2.....\t-->  To add a new entry")
    print("list\t\t\t\t\t-->  To Display names of table.")
    print("display table_name\t\t\t-->  To Display the table records.")
    print("delete table_name\t\t\t-->  To Delete the entire table.")
    print("search table_name col_name value\t-->  To Display the specifictable records.")
    print("clear\t\t\t\t\t-->  To clear the terminal screen")
    print("exit\t\t\t\t\t-->  To exit the program")
    print("\nMore functionality will be added in te future! Stay tuned :)")


# Starting the program CLI-UI.
terminal()
