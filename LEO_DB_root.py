#   Name: root
#   Description: This file contian all the basic function to be perform with data along with I/O operation.
#   Author: Malay Bhavsar
#   Year: 2020
#   Started: 07-09-2020 {This program & its design}
#   Older Version: 31-08-2020
#   First idea & version: 01-05-2020

# Importing the module & Defining the global variables.
import os
version = "0.1"
database_path = "./.leo_db_storage"

###################################################################################################
#                                       LEVEL 1 FUNCTION                                          #
###################################################################################################


def read_file(file_name):
    # This function is used to read data from the file.
    if os.path.exists(f"{database_path}/{file_name}"):
        file = open(f"{database_path}/{file_name}", "r")
        file_to_data = file.read()
        file.close()
        return (1, file_to_data)
    return (0, [])


def write_file(file_name, data_to_file=""):
    # This function is used to write data to the file.(Clearing all old data)
    file = open(f"{database_path}/{file_name}", "w")
    file_data = file.write(data_to_file)
    file.close()


def append_file(file_name, data_to_file=""):
    # This function is used to append data to the file.
    if os.path.exists(f"{database_path}/{file_name}"):
        file = open(f"{database_path}/{file_name}", "a")
        file_data = file.write(data_to_file)
        file.close()
        return 1
    return 0


def rename_file(old_file_name, new_file_name):
    # This function is used to rename the files.
    if os.path.exists(f"{database_path}/{old_file_name}"):
        os.rename(f"{database_path}/{old_file_name}",
                  f"{database_path}/{new_file_name}")
        return 1
    else:
        return 0


def list_to_string(data, join_with=""):
    # This function convert list to string with join_with variable.
    return join_with.join(element for element in data)


def string_to_list(data, split_with=" "):
    data_ls = data.split(split_with)
    return [element.strip() for element in data_ls]


def list_upper(list_data):
    # This function converts all the elements in the list to upper case.
    return [element.upper() for element in list_data]


def get_num_record(file_name):
    # This function provides number of records.
    success, data = read_file(file_name)
    if success == 1:
        data = string_to_list(data, "#END$")
        data.pop()
        return len(data)
    return -1


def export_table(table_name):
    # This function helps in exporting the table data to csv file.
    success1, data1 = read_file(f"{table_name}.db_leo")
    success2, data2 = read_file(f"{table_name}.meta_leo")
    if success1 == 1 and success2 == 1:
        # Writing column name.
        data2 = string_to_list(data2, "#NEXT$")
        data2 = list_to_string(data2, ",")
        data2 = string_to_list(data2, "#END$")
        data2 = list_to_string(data2, "\n")
        write_file(f"{table_name}.csv", data2)
        # Writing the records.
        data1 = string_to_list(data1, "#NEXT$")
        data1 = list_to_string(data1, ",")
        data1 = string_to_list(data1, "#END$")
        data1.pop()
        for data in data1:
            new_data = data + "\n"
            append_file(f"{table_name}.csv", new_data)
        return 1
    else:
        return 0


def import_table(table_name, path):
    # This function helps in importing the data from csv file to the database.
    path = list_to_string(path)
    file = open(f"{path}", "r")
    data = file.read()
    file.close()
    if data != "":
        data = string_to_list(data, "\n")
        data1 = data[0]
        data2 = data[1:]
        # Working on meta file.
        data1 = string_to_list(data1, ",")
        data1 = [sub.upper() for sub in data1]
        data1 = list_to_string(data1, "#NEXT$") + "#END$"
        write_file(f"{table_name}.meta_leo", data1)
        # Working on db file.
        data2 = list_to_string(data2, "#END$")
        data2 = string_to_list(data2, ",")
        data2 = list_to_string(data2, "#NEXT$")
        write_file(f"{table_name}.db_leo", data2)
        return 1
    else:
        return 0


###################################################################################################
#                                       LEVEL 2 FUNCTIONS                                         #
###################################################################################################


def create_table(table_name, col_list):
    # This function creates a new table file along with it's meta file.
    t_string = f"{table_name}#END$"
    res = append_file(f"leo_list_db.meta_leo", t_string)
    if res == 0:
        return 0
    else:
        string = list_to_string(list_upper(col_list), "#NEXT$") + "#END$"
        write_file(f"{table_name}.meta_leo", string)
        write_file(f"{table_name}.db_leo", "")
        return 1


def rename_table(old_table_name, new_table_name):
    # This function helps in renaming the table.
    success, data = read_file("leo_list_db.meta_leo")
    if success == 1:
        data_ls = string_to_list(data, "#END$")
        for i in range(len(data_ls)):
            if data_ls[i] == old_table_name:
                data_ls[i] = new_table_name
        data = list_to_string(data_ls, "#END$")
        write_file("leo_list_db.meta_leo", data)
        rename_file(f"{old_table_name}.meta_leo", f"{new_table_name}.meta_leo")
        rename_file(f"{old_table_name}.db_leo", f"{new_table_name}.db_leo")
        print("[SUCCESS]: TABLE RENAMED SUCCESSFULLY")
    else:
        print("[ERROR]: NO SUCH TABLE FOUND")


def delete_table(table_name):
    # THis function deletes all the table associated entries and files.
    success, data = read_file("leo_list_db.meta_leo")
    if success == 1:
        data_ls = string_to_list(data, "#END$")
        index = -1
        for i in range(len(data_ls)):
            if data_ls[i] == table_name:
                index = i
        if index != -1:
            data_ls.pop(index)
            data = list_to_string(data_ls, "#END$")
            write_file("leo_list_db.meta_leo", data)
            os.remove(f"{database_path}/{table_name}.meta_leo")
            os.remove(f"{database_path}/{table_name}.db_leo")
            print("[SUCCESS]: TABLE DELETED SUCCESSFULLY")
        else:
            print("[ERROR]: NO TABLE FOUND!")
    else:
        print("[ERROR]: NO SUCH TABLE FOUND")


def insert_column_table(table_name, col_list):
    # This function is used to add a new column to the table.
    success, data = read_file(f"{table_name}.meta_leo")
    success_2, data_2 = read_file(f"{table_name}.db_leo")
    if success == 1 and success_2 == 1:
        # Updating meta file.
        data = string_to_list(data, "#END$")
        data = list_to_string(data)
        data = data.split("#NEXT$")
        for col in col_list:
            data.append(col.upper())
        data = list_to_string(data, "#NEXT$") + "#END$"
        write_file(f"{table_name}.meta_leo", data)
        # Updating db_file.
        data_2 = string_to_list(data_2, "#END$")
        new_ls = []
        for j in range(len(data_2)):
            for i in range(len(col_list)):
                data_2[j] += "#NEXT$NULL"
            new_ls.append(data_2[j])
        data_2 = list_to_string(new_ls, "#END$")
        write_file(f"{table_name}.db_leo", data_2)
        return 1
    else:
        return 0


def rename_column_table(table_name, old_col_name, new_col_name):
    old_col_name = old_col_name.upper()
    new_col_name = new_col_name.upper()
    # This function is used to rename column.
    success, data = read_file(f"{table_name}.meta_leo")
    if success == 1:
        # Updating meta file.
        data = string_to_list(data, "#END$")
        data = list_to_string(data)
        data = data.split("#NEXT$")
        print(data)
        print(old_col_name)
        if old_col_name in data:
            data = [sub.replace(old_col_name, new_col_name) for sub in data]
        else:
            return 0
        data = list_to_string(data, "#NEXT$") + "#END$"
        write_file(f"{table_name}.meta_leo", data)
        return 1
    else:
        return 0


def delete_column_table(table_name, col_list):
    # This function is used to delete columns from the table.
    success, data = read_file(f"{table_name}.meta_leo")
    success_2, data_2 = read_file(f"{table_name}.db_leo")
    if success == 1 and success_2 == 1:
        # Updating meta file.
        for col_name in col_list:
            print(col_name)
            data = string_to_list(data, "#END$")
            data = list_to_string(data)
            data = data.split("#NEXT$")
            index = -1
            if col_name.upper() in data:
                index = data.index(col_name.upper())
                data.pop(index)
            data = list_to_string(data, "#NEXT$") + "#END$"
            write_file(f"{table_name}.meta_leo", data)
            # Updating db_file.
            if index != -1:
                data_2 = string_to_list(data_2, "#END$")
                data_2.pop()
                for i in range(len(data_2)):
                    data_2[i] = string_to_list(data_2[i], "#NEXT$")
                    data_2[i].pop(index)
                    data_2[i] = list_to_string(data_2[i], "#NEXT$")
                data_2 = list_to_string(data_2, "#END$") + "#END$"
                write_file(f"{table_name}.db_leo", data_2)
            else:
                print("[ERROR]: NO SUCH COLUMN NAME EXIST")
        return 1
    else:
        return 0


def display_table(table_name):
    # This function helps in displaying the table in the terminal.
    success_1, data = read_file(f"{table_name}.db_leo")
    success_2, col_list = read_file(f"{table_name}.meta_leo")
    if success_1 == 1 and success_2 == 1:
        data = string_to_list(data, "#END$")
        col_list = string_to_list(col_list, "#END$")
        data.pop()
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = col_list.split("#NEXT$")
        # print("\nIndex", end="\t")
        print("{:^6}".format("Index"), end="\t")
        for element in col_list:
            if len(element) > 15:
                element = element[:10] + "[..]"
            print("{:^15}".format(element), end="\t")
            # print(f"\t{element}", end="\t")
        for i in range(len(data)):
            print("")
            new_data = data[i].split("#NEXT$")
            # print(f"{i+1}", end="\t")
            print("{:^6}".format(i+1), end="\t")
            for element in new_data:
                # print(f"\t{element}", end="\t")
                if len(element) > 15:
                    element = element[:10] + "[..]"
                print("{:^15}".format(element), end="\t")
        print("\n")
    else:
        print("[ERROR]: SOME FILES WERE NOT FOUND!")


def define_struct(table_name):
    # This functions displays a list of column name.
    success, col_list = read_file(f"{table_name}.meta_leo")
    if success == 1:
        col_list = string_to_list(col_list, "#END$")
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = col_list.split("#NEXT$")
        print(f"COLUMN LIST: {col_list}")
    else:
        print("[ERROR]: SOME FILES WERE NOT FOUND!")


def define_table(table_name):
    # This function describes the table.
    success_1, data = read_file(f"{table_name}.db_leo")
    success_2, col_list = read_file(f"{table_name}.meta_leo")
    if success_1 == 1 and success_2 == 1:
        data = string_to_list(data, "#END$")
        data.pop()
        col_list = string_to_list(col_list, "#END$")
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = string_to_list(col_list, "#NEXT$")
        total_size = os.path.getsize(f"{database_path}/{table_name}.db_leo") + \
            os.path.getsize(f"{database_path}/{table_name}.meta_leo")
        total_size = total_size / 1000
        size_type = "KB"
        if total_size > 1000:
            total_size = total_size / 1000
            size_type = "MB"
        print(f"\nNAME OF TABLE : {table_name}")
        print(f"SIZE ON DISK : {total_size} {size_type}")
        print(f"NUMBER OF COLUMN : {len(col_list)}")
        print(f"LIST OF COLUMN : {col_list}")
        print(f"NUMBER OF RECORD : {len(data)}")
    else:
        print("[ERROR]: SOME FILES WERE NOT FOUND!")


###################################################################################################
#                                       LEVEL 3 FUNCTIONS                                         #
###################################################################################################
# Level 3 allows user to group data by recurring search and make it more operable.


def insert_record(table_name, record_ls):
    # Thi function is used to insert record in a particular table
    success, data = read_file(f"{table_name}.meta_leo")
    if success == 1:
        col_list = data.split("#END$")
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = col_list.split("#NEXT$")
        if len(col_list) == len(record_ls):
            record_string = list_to_string(record_ls, "#NEXT$") + "#END$"
            append_file(f"{table_name}.db_leo", record_string)
            return 1
        else:
            print(
                "[ERROR]: SOME FIELDS WERE MISSING! IF LEFT BY PURPOSE FILL IT BY 'NULL' or ''")
            return 0
    else:
        print("[ERROR]: NO SUCH TABLE WAS FOUND!")
        return 0


def delete_record(table_name, col_name, value_ls):
    # This function deletes all the records containing values of particular columngiven by the user.
    success1, data1 = read_file(f"{table_name}.db_leo")
    success2, data2 = read_file(f"{table_name}.meta_leo")
    if success1 == 1 and success2 == 1:
        col_list = string_to_list(data2, "#END$")
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = string_to_list(col_list, "#NEXT$")
        index = -1
        if col_name.upper() in col_list:
            index = col_list.index(col_name.upper())
        if index != -1:
            data1 = string_to_list(data1, "#END$")
            data1.pop()
            pop_ls = []
            for i in range(len(data1)):
                data_ls = string_to_list(data1[i], "#NEXT$")
                for value in value_ls:
                    if value == data_ls[index]:
                        pop_ls.append(i)
                        break
            count = 0
            for num in pop_ls:
                data1.pop(num-count)
                count += 1
            data1 = list_to_string(data1, "#END$") + "#END$"
            write_file(f"{table_name}.db_leo", data1)
            return 1
        else:
            print("[ERROR]: NO SUCH COLUMN FOUND")
            return 0
    else:
        print("[ERROR]: NO SUCH TABLE FOUND")
        return 0


def edit_record(table_name, find_ls, new_data_ls):
    pass


def search_record(table_name, col_ls, value_ls):
    success1, data1 = read_file(f"{table_name}.db_leo")
    success2, data2 = read_file(f"{table_name}.meta_leo")
    if success1 == 1 and success2 == 1:
        col_list = string_to_list(data2, "#END$")
        col_list.pop()
        col_list = list_to_string(col_list)
        col_list = string_to_list(col_list, "#NEXT$")
        index_ls = []
        for col_name in col_ls:
            index = -1
            if col_name.upper() in col_list:
                index = col_list.index(col_name.upper())
                index_ls.append(index)
            else:
                print("[ERROR]: INDEX NOT IN LIST")
                return 0
        data1 = string_to_list(data1, "#END$")
        data1.pop()
        new_display_list = []
        for i in range(len(data1)):
            data_ls = string_to_list(data1[i], "#NEXT$")
            count = 0
            for j in range(len(index_ls)):
                if data_ls[index_ls[j]] == value_ls[j]:
                    count += 1
            if count == len(col_ls):
                new_display_list.append(i)
        # Now displaying the search result.
        if len(new_display_list) != 0:
            print("")
            print("{:^6}".format("Index"), end="\t")
            for element in col_list:
                if len(element) > 15:
                    element = element[:10] + "[..]"
                print("{:^15}".format(element), end="\t")
                # print(f"\t{element}", end="\t")
            for i in range(len(new_display_list)):
                print("")
                new_data = data1[new_display_list[i]].split("#NEXT$")
                # print(f"{i+1}", end="\t")
                print("{:^6}".format(i+1), end="\t")
                for element in new_data:
                    # print(f"\t{element}", end="\t")
                    if len(element) > 15:
                        element = element[:10] + "[..]"
                    print("{:^15}".format(element), end="\t")
            print("\n")
            return 1
        else:
            return 0
    else:
        return 0


###################################################################################################
#                                     BOOT UP LEVEL FUNCTIONS                                     #
###################################################################################################


def create_base():
    # This function creates the base directory used for storing data.
    if os.path.exists(f"{database_path}"):
        pass
    else:
        os.mkdir(f"{database_path}")
        write_file("leo_list_db.meta_leo")


def clear_screen():
    # This function clears the screen.
    os.system("CLS")


def greet_message():
    print(f"LEO-DB --- (Malay Bhavsar) --- (VERSION: {version})")
    print("Type #> help if you get lost..  :)")

###################################################################################################
#                                       UI LEVEL FUNCTIONS                                         #
###################################################################################################


def terminal():
    # Running the basic functions.
    create_base()
    clear_screen()
    greet_message()
    # Defining the variable.
    user_arg = ''
    arg_ls = []
    # Creating a loop for multiple operation.
    while user_arg.upper() != 'EXIT':
        user_arg = input("\n#> ")
        arg_ls = user_arg.split(" ")
        # Starting the if-else.
        if arg_ls[0].upper() == "EXIT":
            # To display exit message.
            print("[SUCCESS]: THANK YOU FOR USING MY SERVICE")
        elif arg_ls[0].upper() == "CLEAR":
            # To clear screen.
            clear_screen()
        elif arg_ls[0].upper() == "HELP":
            # To display help function.
            help_me()
        elif arg_ls[0].upper() == "CREATE":
            # Creating a table.
            if arg_ls[1] != " ":
                col_list = list_to_string(arg_ls[2:], " ")
                col_list = string_to_list(col_list, ",")
                success = create_table(arg_ls[1], col_list)
                if success == 0:
                    print("[ERROR]: UNABLE TO CREATE A TABLE")
                elif success == 1:
                    print("[SUCCESS]: TABLE CREATED SUCCESSFULLY")
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "RENAME":
            # Renaming a table.
            if arg_ls[1] != "" and arg_ls != "":
                rename_table(arg_ls[1], arg_ls[2])
            else:
                print("[ERROR]: NO NAME GIVEN")
        elif arg_ls[0].upper() == "DELETE":
            # To delete a table.
            if arg_ls[1] != "":
                confirm = input("Please Renter Table Name: ")
                if confirm == arg_ls[1]:
                    delete_table(arg_ls[1])
                else:
                    print("[ERROR]: TABLE NOT DELETED")
            else:
                print("[ERROR]: NO TABLE NAME GIVEN")
        elif arg_ls[0].upper() == "INSERT_COL":
            # Add multiple column name.
            if arg_ls[1] != " ":
                col_list = list_to_string(arg_ls[2:], " ")
                col_list = string_to_list(col_list, ",")
                success = insert_column_table(arg_ls[1], col_list)
                if success == 0:
                    print("[ERROR]: UNABLE TO ADD COLUMN")
                elif success == 1:
                    print("[SUCCESS]: COLUMN ADDED SUCCESSFULLY")
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "RENAME_COL":
            # To delete a table.
            if arg_ls[1] != "":
                success = rename_column_table(arg_ls[1], arg_ls[2], arg_ls[3])
                if success == 1:
                    print("[SUCCESS]: COLUMN RENAMED SUCCESSFUL")
                else:
                    print("[ERROR]: UNABLE TO RENAME COLUMN")
            else:
                print("[ERROR]: NO TABLE NAME GIVEN")
        elif arg_ls[0].upper() == "DELETE_COL":
            # To delete a table.
            if arg_ls[1] != "":
                confirm = input("Please Renter Table Name: ")
                if confirm == arg_ls[1]:
                    col_list = list_to_string(arg_ls[2:], " ")
                    col_list = string_to_list(col_list, ",")
                    success = delete_column_table(arg_ls[1], col_list)
                    if success == 1:
                        print("[SUCCESS]: COLUMN DELETED SUCCESSFUL")
                    else:
                        print("[ERROR]: UNABLE TO DELETE COLUMN")
            else:
                print("[ERROR]: NO TABLE NAME GIVEN")
        elif arg_ls[0].upper() == "DISPLAY":
            # This function displays the table.
            if arg_ls[1] != " ":
                display_table(arg_ls[1])
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "DEFINE_TABLE":
            # This function describes the table.
            if arg_ls[1] != " ":
                define_table(arg_ls[1])
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "DEFINE_STRUCT":
            # This function describes the structure of table.
            if arg_ls[1] != " ":
                define_struct(arg_ls[1])
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "INSERT_RECORD":
            if arg_ls[1] != "":
                records = list_to_string(arg_ls[2:], " ")
                records = string_to_list(records, ",")
                success = insert_record(arg_ls[1], records)
                if success == 1:
                    print("[SUCCESS]: RECORD INSERTED SUCCESSFULLY")
                else:
                    print("[ERROR]: UNABLE TO INSERT RECORD")
            else:
                print("[ERROR]: IMPROPER SYNTAX TYPE #>HELP FOR SYNTAX")
        elif arg_ls[0].upper() == "EDIT_RECORD":
            pass
        elif arg_ls[0].upper() == "DELETE_RECORD":
            # To delete record.
            if arg_ls[1] != "":
                values = list_to_string(arg_ls[3:], " ")
                values = string_to_list(values, ",")
                success = delete_record(arg_ls[1], arg_ls[2], values)
                if success == 1:
                    print("[SUCCESS]: RECORD INSERTED SUCCESSFULLY")
                else:
                    print("[ERROR]: UNABLE TO INSERT RECORD")
            else:
                print("[ERROR]: IMPROPER SYNTAX TYPE #>HELP FOR SYNTAX")
        elif arg_ls[0].upper() == "SEARCH_RECORD":
            # To search record.
            if arg_ls[1] != "":
                values = list_to_string(arg_ls[2:], " ")
                values = string_to_list(values, ":")
                col_ls = string_to_list(values[0], ",")
                value_ls = string_to_list(values[1], ",")
                success = search_record(arg_ls[1], col_ls, value_ls)
                if success == 1:
                    print("[SUCCESS]: RECORDS FOUND")
                else:
                    print("[ERROR]: RECORDS NOT FOUND")
            else:
                print("[ERROR]: IMPROPER SYNTAX TYPE #>HELP FOR SYNTAX")
        elif arg_ls[0].upper() == "DISPLAY_RECORD":
            pass
        elif arg_ls[0].upper() == "EXPORT":
            # To export table into CSV.
            if arg_ls[1] != " ":
                success = export_table(arg_ls[1])
                if success == 1:
                    print("[SUCCESS]: FILE EXPORTED SUCCESSFULLY")
                else:
                    print("[ERROR]: SOME ERROR OCCOURED")
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "IMPORT":
            # To import CSV file to leo_table.
            if arg_ls[1] != " ":
                path = arg_ls[2:]
                success = import_table(arg_ls[1], path)
                if success == 1:
                    print("[SUCCESS]: FILE IMPORTED SUCCESSFULLY")
                else:
                    print("[ERROR]: FILE NOT FOUND")
            else:
                print("[ERROR]: UNIDENTIFED TABLE NAME")
        elif arg_ls[0].upper() == "":
            pass
        else:
            print("[ERROR]: INVALID SYNTAX")


def help_me():
    # THis function helps the user with the syntax and this database.
    print(f"\nWelcome to Help Me of LEO-DB Version:{version}")
    print("Here are some of the commands you can go with!\n")
    print("#> CREATE table_name col_name1,col_name2,... \t\t--> Create new table")
    print("#> RENAME old_table_name new_table_name \t\t--> Rename an old table")
    print("#> DELETE table_name\t\t\t\t\t--> Delete a table")
    print("#> INSERT_COL table_name col_name1,col_name2,... \t--> Insert Multiple/Single column to existing table")
    print("#> RENAME_COL table_name old_col_name,new_col_name\t--> Rename an existing column")
    print("#> DELETE_COL table_name col_name1,col_name2,...\t--> Delete Multiple/Single column")
    print("#> DISPLAY table_name\t\t\t\t\t--> Display all records of the table")
    print("#> DEFINE_TABLE table_name\t\t\t\t--> Give brief description of the table")
    print("#> DEFINE_STRUCT table_name\t\t\t\t--> Give list of column in order")
    print("#> INSERT_RECORD table_name value1,value2,value3..\t--> To insert record into the table")
    print("#> DELETE_RECORD table_name col_name value1,value2..\t--> To insert record into the table")
    print("#> SEARCH_RECORD table_name col_name1,col_name2..:value1,value2.. --> To search record into the table")
    print("\nMore functionality will be added in te future! Stay tuned :)")


terminal()
