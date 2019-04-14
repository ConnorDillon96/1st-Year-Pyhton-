# created by B00355490 & B00346084


# Imported packages
import datetime
import easygui
import json
import os
import pickle
import shutil
import sys


# Note this may need to be installed > pip3 install matplotlib (in pycharm terminal)  Menu option relies on this library
try:
    import matplotlib.pyplot as plt  # makes it easier to reference in code
except ImportError and ModuleNotFoundError:  # if module is not found handle the error
    easygui.msgbox('Your computer is missing some dependencies \n Menu option 8 will not work as expected ')

# pip install PrettyTable
try:
    from prettytable import PrettyTable
except ModuleNotFoundError and ImportError:
    easygui.msgbox('Critical library not found!\nTerminating')
    exit()


class Component:
    # Class dedicated to Components
    def __init__(self, unique_sequential_serial, number_of_components):
        self.unique_sequential_serial = unique_sequential_serial
        self.number_of_components = number_of_components


class Batch:
    # Class dedicated to Batch
    def __init__(self, batch_number, manufacture_date, component_type, model, unique_sequential_serial,
                 number_of_components):
        self.batch_number = batch_number
        self.manufacture_date = manufacture_date
        self.component_type = component_type
        self.model = model
        self.unique_sequential_serial = unique_sequential_serial
        self.number_of_components = number_of_components

    def __str__(self):
        # if user wants to view batch gen
        # If user wants to view batch generation
        print('TYPE: ', self.component_type, '\t', 'MODEL: ', self.model, '\t')
        print('DATE: ', str(self.manufacture_date) + '\nBATCH: ',
              str(self.batch_number).zfill(4) + '\nSERIAL: ' + str(self.unique_sequential_serial) +
              '\nSTATUS: Manufactured-unfinished' + '\nALLOCATION: Factory Floor - Warehouse Not Allocated')

    def view_creation(self):
        easygui.msgbox('TYPE: ' + self.component_type + '\t' + 'MODEL: ' + self.model + '\n' +
                       'DATE: ' + str(self.manufacture_date) + '\nBATCH: ' + str(self.batch_number).zfill(4))

    def Objectdump(self):
        self.unique_sequential_serial = str(self.unique_sequential_serial).strip(
            '[]')  # removed [] from begging and end of str
        self.batch_number = str(self.batch_number).strip('[]').strip("''")  # removes characters
        batch = {'BATCH:' + str(self.batch_number).zfill(4): (str(self.manufacture_date) + str(self.batch_number).zfill(
            4) + '-' + self.unique_sequential_serial) + ' Manufactured-unfinished'}
        if not os.path.isfile('BatchIndex.json'):  # if file does not exist in path
            with open('BatchIndex.json', 'a+') as f:  # creates file
                f.write(json.dumps(batch, indent=4))  # writes data to file

        else:
            data = json.load(open('BatchIndex.json'))  # file exists, load data

            # convert data to list if file is a dict
            if type(data) is dict:
                data = [data]

            # append new item to data list
            data.append(batch)

            # write list to BathIndex.json
            with open('BatchIndex.json', 'w') as outfile:
                json.dump(data, outfile)

    def PickleBatch(self):
        batch_num = self.manufacture_date + self.batch_number.zfill(4)  # file name

        if os.path.isfile(batch_num + '.pickle'):
            data = [str(self.manufacture_date), str(self.batch_number).zfill(4), str(self.component_type), str(
                self.model), str(int(self.number_of_components)), 'Manufactured-unfinished',
                    'Factory Floor - Warehouse Not Allocated']
            with open(batch_num + '.pickle', 'ab') as file:  # add bytes - appending to pickle
                pickle.dump(data, file)  # dumps updated data
        else:  # File does not exist then
            with open(batch_num + '.pickle', "wb") as file:  # Creates file with batch as name
                pickle.dump([str(self.manufacture_date), str(self.batch_number).zfill(4), str(self.component_type), str(
                    self.model), str(int(self.number_of_components)), 'Manufactured-unfinished',
                             'Factory Floor - Warehouse Not Allocated'], file)

    def PickleCompnenet(self):
        name = str(self.manufacture_date) + str(self.batch_number).zfill(4) + '-' + self.unique_sequential_serial

        pickle_details_data = [str(self.manufacture_date), self.batch_number.zfill(4), self.unique_sequential_serial,
                               self.component_type,
                               self.model, 'Manufactured-unfinished', 'Factory Floor - Warehouse Not Allocated']

        if os.path.isfile(name + '.pickle'):
            with open(name + '.pickle', 'rb') as details:
                data = pickle.load(details) + pickle_details_data  # loads file and appends
            with open(name + '.pickle', 'wb') as file:
                pickle.dump(data, file)  # dumps updated data
        else:  # File does not exist then
            with open(name + '.pickle', "wb") as file:  # Creates file with batch as name
                pickle.dump(pickle_details_data, file)


def batch_number():
    last_number = []
    batch = []

    if not os.path.isfile('BatchIndex.json'):  # if file is not in location then
        easygui.msgbox('CAUTION:Unable to locate  Data/BatchIndex.json\n'
              'Continuing will overwrite file\n'
              'or create new one if it does not exist')
        try:
            y_n = easygui.ynbox('Would you like to continue?', 'confirm', ['Yes', 'No'])
            if y_n is True:
                batch_num = 1
                return batch_num

            elif y_n is False:
                easygui.msgbox('Terminating, Returning to main menu')
                main()
            else:
                easygui.msgbox('Invalid option, please select Y or N')
                batch_number()

        except ValueError:
            easygui.msgbox('Invalid option, please select Y or N')
            batch_number()
    else:
        # reads from json and increment final by 1 and returns value
        with open('BatchIndex.json', 'r') as batch_id:
            used_numbers = batch_id.read()  # loads used numbers into a variable to manipulated
            target = len(used_numbers) - 1  # iterates from the end of list
            while target >= 0:
                if used_numbers[target] == '{':  # looks for this char as we use these to seperate our batch index
                    last_number.append(used_numbers[target:-5])  # this grabs the full batch info
                    break
                target -= 1
            # last_used = str(start + mid2 + mid + end)
            last_number = str(last_number).replace("'", '').replace('[', '')
            for characters in range(len(last_number[0:13])):
                batch.append(last_number[characters])
            number_found = (batch[-5:-1])  # this extracts the last used batch number
            # as our previous element is currently split by , we join all elemnts in the list to create one element
            number_found = ''.join(
                number_found)
            try:
                batch_num = (int(number_found) + 1)
                batch_num = str(batch_num).zfill(4)  # formats value (can only format string)
            # During testing an error was found due to the formatting of the first batch number
            # (we were unable to replicate the error) -
            # this will catch the specific error if bug is replicated and will correct it
            except ValueError:
                batch_num = str(2).zfill(
                    4)
            return batch_num


def date_input():
    when_made = easygui.ynbox('Was the batch made today?', 'Date', ['Yes', 'No'])
    date = datetime.datetime.now()  # sets current date and time to date module
    if when_made:
        date = date.strftime('%Y%m%d')  # Formats date as required, using datetime lib (Upper case Y for ful year)
        return date
    else:  # if user wants to input there own date then
        month = 0
        day = 0
        # limiting inputs to the present date and back to the year 2000
        year = easygui.integerbox('Please enter the year of manufacture', 'manual selection', lowerbound=2000,
                                  upperbound=int(datetime.datetime.now().year))

        # if the user clicks cancel return to main menu
        if year is None:
            main()

        month = easygui.integerbox('Please enter the month of manufacture as a number', lowerbound=1, upperbound=12)

        if month is None:
            main()

        # If user selects feb limits input to 1 > 28  +  Leap year Validation
        if month == 2:
            if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
                while day < 1 or day > 29:
                    day = easygui.integerbox('Please enter the day of manufacture:')
            else:
                while day < 1 or day > 28:
                    day = easygui.integerbox('Please enter the day of manufacture')
        else:
            while day < 1 or day > 31:
                day = easygui.integerbox('Please enter the day of manufacture')

        if day is None:
            main()

        # This will check user inputs and format using the built in python function zfill
        if day < 10 and month < 10:
            date = (str(year) + str(month).zfill(2) + str(day).zfill(2))
        elif day < 10:
            date = (str(year) + str(month) + str(day).zfill(2))
        elif month < 10:
            date = (str(year) + str(month).zfill(2) + str(day))
        else:
            date = (str(year) + str(month) + str(day))

    return date


def new_batch():

    number_of_components = easygui.integerbox('How many components in this batch? (1 to 9999)', lowerbound=1,
                                              upperbound=9999)
    # if the user selects cancel return home
    if number_of_components is None:
        main()

    component_type = easygui.choicebox('Select a component type', 'Type', ['Winglet strut', 'Door handle', 'Rudder pin'])
    if component_type is None:
        main()

    if component_type == 'Winglet strut':
            model = easygui.choicebox('Select Size/fitment type', 'Fitment', ['A320', 'A380'])

    if component_type == 'Rudder pin':
        model = easygui.choicebox('please select size', 'Size', ['10mmx75mm', '12mmx100mm', '16mmx150mm'])

    if component_type == 'Door handle':
        model = 'universal'

    if model is None:
        main()

    message = 'This batch contains ' + str(number_of_components) + ' ' + model + ' ' + component_type +\
              ' is this correct?'
    confirm = easygui.ynbox(message, 'Confirm', ['Yes', 'No'])
    if confirm is False:
        new_batch()
    else:
        return number_of_components, component_type, model


# this loading bar was found on github > https://gist.github.com/vladignatyev/06860ec2040cb497f0f3
# Also was possible through external libraries, as this only uses built in libraries we opted to use this code snippet.
def progress(count, total, suffix=''):
    bar_len = 60
    try:
        filled_len = int(round(bar_len * count / float(total)))

        percents = round(100.0 * count / float(total), 1)
        bar = '=' * filled_len + '-' * (bar_len - filled_len)

        sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
        sys.stdout.flush()
    except ZeroDivisionError:
        print('********** 100% complete **********')


# Step 2 starts below

def show_batch():
    table = PrettyTable()
    batch_names = []
    sorted_batch = []
    details_print = []
    for filename in os.listdir():  # iterates through data folder listing dir and files
        batch_names.append(filename)
    for elements in batch_names:
        if '-' not in elements:  # if the file name does not contain - then add to the list
            if elements == 'BatchIndex.json' or elements == 'Backup':  # if name is batchindex/Backup then dont add list
                pass
            else:
                sorted_batch.append(elements)  # appends the batch files to sorted_batch to iterate through
    for files in sorted_batch:
        with (open(files, "rb")) as openfile:  # unpickles file until there is nothing left to unpickle(EOFError)
            while True:
                try:
                    details_print.append(pickle.load(openfile))
                except EOFError:
                    break
    table.field_names = ['Date', 'Batch', 'Model', 'Type', 'contain(s)', 'Status', 'Allocated']  # Titles for the output

    # function reads the highest batch number in the batch.pickle file
    # adds to table x axis
    # also avoids list in list formatting
    results = []
    for lists in details_print:
        try:
            if lists[1]:
                results.append(lists)
        except IndexError:
            for single in lists:
                try:
                    if single[1]:
                        results.append(single)
                except IndexError:
                    for one in single:
                        try:
                            if one[1]:
                                results.append(one)
                        except IndexError:
                                for uno in one:
                                    results.append(uno)
    previous = ''

    # formatting batch so not all components are shown
    # extracting nested lists
    for data in results:
        if (type(data[1])) == str:
            if previous == data[:2]:
                pass
            else:
                if 'Manufactured-unfinished' not in str(data):
                    data[-2] = 'Manufactured-finished'
                    table.add_row(data)
                    previous = data[:2]
                else:
                    table.add_row(data)
                    previous = data[:2]

        else:
            for nested_list in data:
                if previous == nested_list[:2]:
                    pass
                else:
                    if 'Manufactured-unfinished' not in str(nested_list):
                        nested_list[-2] = 'Manufactured-finished'
                        table.add_row(nested_list)
                        previous = nested_list[:2]
                    else:
                        table.add_row(nested_list)
                        previous = nested_list[:2]

    # easy-GUI does not support PrettyTable type
    print(table)
    easygui.msgbox('Please find information below')


def batch_detail():
    counter = 0
    focus_batch = easygui.enterbox('Enter batch number (YYYYMMDD0001)')
    if focus_batch is None:
        main()
    # checks  if the user is has included a '-' which is used in the component
    # search and warns the user that they might be searching in the wrong option
    if '-' in focus_batch:
        try:
            answer = easygui.ynbox(
                'It looks like you may be searching for a component, would you like to return to the main menu?',
                'Return Home?', ['Yes', 'No'])
            if answer is True:
                main()
            elif answer is False:
                easygui.msgbox('please try again')
                batch_detail()
            else:
                easygui.msgbox('selection not recognised')
                batch_detail()
        except ValueError:
            easygui.msgbox('Invalid option!')
            batch_detail()
    if os.path.isfile(focus_batch + '.pickle'):
        found_details = []
        with (open(focus_batch + '.pickle',
                   "rb")) as openfile:  # unpickles file until there is nothing left to unpickle(EOFError)
            while True:
                try:
                    found_details.append(pickle.load(openfile))
                except EOFError:
                    break
        with (open(focus_batch + '.pickle',
                   "rb")) as openfile:  # reading lines in file and incrementing counter to find out how many are in file
            for line in openfile:
                counter += 1

        table = PrettyTable()  # Assigns external library to the table variable
        table.field_names = ['Date', 'Batch', 'Model', 'Type', 'Component Number(s)', 'Status',
                             'Allocated']  # Titles for the output
        # adds to table x axis
        # also avoids list in list formatting
        # this is just a shortened version of the previous table creation, used in previous func
        for details in found_details:
            try:
                if type(details[1]) == list:
                    for lists in details:
                        if type(lists[1]) == list:
                            for data in found_details:
                                table.add_row(data)
                        else:
                            table.add_row(lists)
                else:
                    table.add_row(details)
            except IndexError:
                for singular in details:
                    try:
                        table.add_row(singular)
                    except:
                        for last in singular:
                            table.add_row(last)
        print(table)
        easygui.msgbox('Please find information below')

    else:
        error = easygui.ynbox('Batch number does not exists!\n would you like to return to main menu?','Home?',['Yes', 'No'])
        if error is True:
            main()
        else:
            batch_detail()


def component_detail():
    focus_component = easygui.enterbox('Enter component number (YYYYMMDD0001-0001):')
    if focus_component is None:
        main()
    # checks  if the user does not included a '-'  warns the user that they might be searching in the wrong option
    if '-' not in focus_component:
        answer = easygui.ynbox(
            'It looks like you may be searching for a batch, would you like to return to the main menu?', 'Home?', ['Yes', 'No'])
        if answer is True:
            main()
        elif answer is False:
            component_detail()

    if os.path.isfile(focus_component + '.pickle'):
        found_details = []
        with (open(focus_component + '.pickle',
                   "rb")) as openfile:  # unpickles file until there is nothing left to unpickle(EOFError)
            while True:
                try:
                    found_details.append(pickle.load(openfile))
                except EOFError:
                    break

        table = PrettyTable()  # Assigns external library to the table variable
        table.field_names = ['Date', 'Batch', 'Sequential-Serial', 'Type', 'Model', 'Status',
                             'Allocated']  # Titles for the output

        try:
            table.add_row(found_details)
        except:
            try:
                for data in found_details:
                        table.add_row(data)  # selecting last item in list, being the requested details
                        # except with no parameters is used as we are not able to catch PrettyTable exceptions directly
            except:
                for data in found_details:
                    for single in data:
                        table.add_row(single)

        print(table)
        easygui.msgbox('\n Details for: {}  displayed below'.format(focus_component))

    else:
        error = easygui.ynbox('Component number does not exists!\n would you like to return to main menu?', 'Home?', ['Yes', 'No'])
        if error is True:
            main()
        else:
            component_detail()


# step 3
def allocate_stock():
    warehouse = 0
    target_batch = easygui.enterbox('Enter batch number (YYYYMMDD0001)')
    if target_batch is None:
        main()
    if '-' in target_batch:  # making sure the user is not trying to assign an individual batch
        easygui.msgbox('you can only allocate batches not components!, Returning to main menu')
        main()

    if os.path.isfile(target_batch + '.pickle'):  # look for the user specified batch file
        found_details = []
        with (open(target_batch + '.pickle',
                   "rb")) as batch:  # unpickles file until there is nothing left to unpickle(EOFError) readbytes
            while True:
                try:
                    found_details.append(pickle.load(batch))  # append data to list
                except EOFError:
                    break

        # also avoids list in list formatting
        # reduces our nested lists after a finish is assigned
        results = []

        for lists in found_details:
            try:
                if lists[1]:
                    results.append(lists)
            except IndexError:
                for single in lists:
                    try:
                        if single[1]:
                            results.append(single)
                    except IndexError:
                        for one in single:
                            results.append(one)

        for one in results:
            str_one = str(one)
            if 'Factory Floor - Warehouse Not Allocated' not in str_one:
                try:
                    # temp is only used to tempt a Index error, meaning we have a nested list
                    temp = one[1]
                    easygui.msgbox('This batch is already assigned\nReturning to menu')
                    main()
                except IndexError:
                    for nest in one:
                        str_nest = str(nest)
                        if 'Factory Floor - Warehouse Not Allocated' not in str_nest:
                            easygui.msgbox('This batch is already assigned\nReturning to menu')
                            main()

        else:  # if unassigned then
            while warehouse == 0:
                warehouse = easygui.choicebox('Select warehouse', 'Location', ['Paisley', 'Dubai'])
                if warehouse is None:
                    main()

        # Function will iterate and update list as selected above
        for_dump = []
        for lists in results:
            # checking for nested lists
            if type(lists[1]) == list:
                for nested in lists:
                    # updates factory floor with the ware house
                    if 'Factory Floor - Warehouse Not Allocated' in str(nested):
                        nested[-1] = warehouse
                        for_dump.append(nested)
            else:
                if 'Factory Floor - Warehouse Not Allocated' in str(lists):
                    lists[-1] = warehouse
                    for_dump.append(lists)

        # overwriting pickle file
        with (open(target_batch + '.pickle', "wb")) as updating_batch:
            pickle.dump(for_dump, updating_batch)

            easygui.msgbox('{} batch will now be allocated and shipped to {}'.format(target_batch, warehouse))

            batch_index(target_batch, warehouse)  # calling our function to update batch-index

            component_allocation(target_batch, warehouse)  # calling our function to update components

    else:
        easygui.msgbox('Batch not found, returning to main menu')
        main()


def batch_index(target_batch, warehouse):
    target_batch = target_batch[-4:]  # this will extract the batch number we are looking to update
    all_batch = []
    with open('BatchIndex.json', 'r') as index:  # open json file as index
        index_dict = json.load(index)
    for batch in index_dict:
        all_batch.append(batch)  # iterated through index and appends to all batches
    for keys in all_batch:
        for key in keys:
            if key == 'BATCH:' + target_batch:  # compares target key against existing keys
                for items in all_batch:
                    if key == 'BATCH:' + target_batch:
                        data = ([
                            'all ' + target_batch + ' batches are assigned to ' + warehouse]) + all_batch  # updating batchindex with location
                        with open('BatchIndex.json', 'w') as index:  # open json file as index
                            json.dump(data, index)


# if a batch is allocated to a site eg Dubai or Paisley we need to reflect this in all child components
def component_allocation(target_batch, warehouse):
    files = []
    target_files = []
    data_list = []
    for oslist_files in os.listdir():  # iterates through data folder listing dir and files and adding them to files []
        files.append(oslist_files)

    for file in files:
        if target_batch + '-' in file:  # iterating through our file list looking for user specified component files
            target_files.append(file)

    update = []

    for file in target_files:  # this will read through the files we need to check
        with open(file, 'rb') as file_found:  # read bytes assigned to file
            data_list.append(pickle.load(file_found))
            # Function will iterate and update list as selected above
            data_list = (data_list[-1])

            # if our lists is finished we have nested lists
            # this will extract nested lists into flat lists
            try:
                temp = (data_list[1])
                if type(temp) is str:
                    pass
                else:
                    for nested in data_list:
                        data_list = nested
            except IndexError:
                for nested in data_list:
                    data_list = nested

            for index, element in enumerate(data_list):
                if 'Factory Floor - Warehouse Not Allocated' in element:
                    data_list[index] = warehouse
                    update.append(data_list)

            # updating the file
            with open(file, 'wb') as updates:
                pickle.dump(data_list, updates)  # replaces old data with new


# step 4
def search_type():

    component_type = easygui.choicebox('Select a component type:', 'type', ['Winglet Strut', 'Door Handle', 'Rudder Pin'])
    if component_type is None:
        main()

    if component_type == 'Winglet Strut':
            model = easygui.choicebox('Select Size/fitment type', 'model', ['A320', 'A380'])

    elif component_type == 'Rudder Pin':
            model = easygui.choicebox('please select size', 'size', ['10mmx75mm', '12mmx100mm', '16mmx150mm'])

    else:
        model = 'universal'

    confirm = easygui.ynbox('You selected ' + model + ' ' + component_type + ' is this correct?', 'confirm', ['Yes', 'No'])
    if confirm is False:
        search_type()

    files_available = []
    component_files = []
    all = []
    results = []

    for oslist_files in os.listdir():  # iterates through data folder listing dir and files
        files_available.append(oslist_files)
    for files in files_available:
        if '-' in files and 'pickle' in files:  # this will add component file names to list
            component_files.append(files)
        else:
            pass
    for filenames in component_files:  # iterate through the component files
        with (open(filenames, "rb")) as search:  # unpickles files
            file = pickle.load(search)
            all.append(file)
    # function converts to flat list (find nested)
    for details in all:
        try:
            if type(details[1]) == list:
                for lists in details:
                    if type(lists[1]) == list:
                        for data in lists:
                            results.append(data)
                    else:
                        results.append(lists)
            else:
                results.append(details)
        except IndexError:
            results.append(details)
    # results = empty, no stock found
    if not results:
        easygui.msgbox('Not in stock')
        main()

    # creates tables preparing for output
    table_finished = PrettyTable()
    table_unfinished = PrettyTable()
    table_finished.field_names = ('Date', 'Batch', 'Serial', 'Model', 'Type', 'Status', 'Allocation')
    table_unfinished.field_names = ('Date', 'Batch', 'Serial', 'Model', 'Type', 'Status', 'Allocation')

    all = []

    # extracting nested lists
    for lists in results:
        try:
            temp = (type(lists[1]))
            all.append(lists)
        except IndexError:
            for nested in lists:
                all.append(nested)

    no_results = 0
    try:
        for found in all:
            str_found = str(found)
            if component_type and model in str_found:
                # separating finished from unfinished
                if 'Manufactured-unfinished' in str_found:
                    table_unfinished.add_row(found)
                    no_results += 1
                else:
                    table_finished.add_row(found)  # adding all found data to table rows
                    no_results += 1
            else:
                pass
    except:
        easygui.msgbox('Something unexpected has happened please refer to backup')

    if no_results == 0:  # counter will = 0 if no results are found
        easygui.msgbox('none found!\nReturning to menu')
        main()
    else:
        print('\t\tFINISHED')
        print(table_finished)
        print('\n')
        print('\t\tUNFINISHED')
        print(table_unfinished)
        easygui.msgbox('Results for your search: ' + model + ' ' + component_type + ' View below')


def finish_comp():
    component_to_finish = []
    component_selected = []
    serial = easygui.enterbox('enter serial of the component to complete YYYYMMDD0001-0001')
    if serial is None:
        main()
    if '-' not in serial:
        easygui.msgbox('looks like you have tried to update a full batch, this option is only for components'
              '\n returning to main menu')
        main()
    else:
        serial = serial + '.pickle'  # file is named batch.pickle, file wont be located without this
    for oslist_files in os.listdir():  # iterates through data folder listing dir and files
        if oslist_files == serial:  # if the file matches the users choice append to list
            component_to_finish.append(oslist_files)
    for component_file in component_to_finish:
        with open(component_file, 'rb') as component_finish:  # opens the file to change the status
            component_selected.append(pickle.load(component_finish))

    # if list is empty then return home
    if not component_to_finish:
        easygui.msgbox('Component not found\nReturning to main menu')
        main()

    # function converts multi-dimensional list to one list in list
    results = []
    for details in component_selected:
        try:
            if type(details[1]) == list:
                for lists in details:
                    if type(lists[1]) == list:
                        for data in lists:
                            results.append(data)
                    else:
                        results.append(lists)
            else:
                results.append(details)
        except IndexError:
            results.append(details)

    updated = []
    try:
        for component_details in results:
            try:
                if (type(component_details[1])) == str:
                    if 'Manufactured-unfinished' not in str(component_details):  # ensures that the component is not finished
                        easygui.msgbox('This component is already complete\nreturning to main menu')
                        main()
                    else:
                        # formatting table for output
                        table = PrettyTable()
                        table.field_names = ('Date', 'Batch', 'Serial', 'Model', 'Type', 'Status', 'Allocation')
                        table.add_row(component_details)
                        updated.append(component_details)
            except IndexError:
                for lists in component_details:
                    if 'Manufactured-unfinished' not in str(lists):
                        easygui.msgbox('This component is already complete\nreturning to main menu')
                        main()
                    else:
                        # formatting table for output
                        table = PrettyTable()
                        table.field_names = ('Date', 'Batch', 'Serial', 'Model', 'Type', 'Status', 'Allocation')
                        table.add_row(lists)
                        updated.append(lists)
    except:  # pretty table error meaning that batch is already assigned (cannot target specific error)
        easygui.msgbox('Batch already allocated\nReturning to menu')
        main()

    print(table)
    # confirmation yes no box
    update = easygui.ynbox('Are you sure you want to update the following\n Viewed below?', 'Update', ['Yes', 'No'])

    if update is True:
        finish = easygui.choicebox('Select your finish', 'finish', ['Polished', 'Painted'])
        if finish is None:
            main()
        if finish == 'Painted':
            paint_code = easygui.enterbox('please enter 4 digit paint code')
            if paint_code is None:
                main()
            while len(paint_code) != 4:  # makes sure user input is equal to 4 in character length
                paint_code = easygui.enterbox('invalid option! \nplease enter 4 digit paint code')
                if paint_code is None:
                    main()

        else:
            # polish selected then :
            paint_code = ''

        # update component in list with finish
        for items in updated:
            for index, elements in enumerate(items):
                if 'Manufactured-unfinished' in elements:
                    items[index] = finish + paint_code
                else:
                    pass

        for component_file in component_to_finish:
            with open(component_file, 'wb') as completing_update:
                pickle.dump(updated, completing_update)  # update component pickle file
        serial = serial.replace('.pickle', '')  # Removes the .pickle to display below
        easygui.msgbox('Component number {} will be finished using: {} {}'.format(serial, paint_code, finish))

        # update batch.pickle
        batch_file_update(serial, finish, paint_code)
        # will check all components and check if batch needs updated
        all_components_finished(serial, finish, paint_code)
    else:
        easygui.msgbox('Returning to main menu')
        main()


def batch_file_update(serial, finish_set, paint_code):
    # change component name to batch name
    # extract serial and remove zfill 0's
    count = -4
    sequential_serial = serial[-4:]
    for numbers in sequential_serial:
        if numbers == '0':
            count = count + 1
        else:
            sequential_serial = sequential_serial[count:]
            break

    # extracting batch file name
    serial = serial[:-5] + '.pickle'
    batch_data = []
    with open(serial, 'rb') as batch:
        while True:
            try:
                # loading data into list for manipulation
                batch_data.append(pickle.load(batch))
            except EOFError:
                break

    results = []
    # flatten list
    for details in batch_data:
        try:
            if type(details[1]) == list:
                for lists in details:
                    if type(lists[1]) == list:
                        for data in lists:
                            results.append(data)
                    else:
                        results.append(lists)
            else:
                results.append(details)
        except IndexError:
            results.append(details)

    # find list object which needs updating
    # update target list using index
    final = []
    for data in results:
        if sequential_serial in data:
            pos = data.index(sequential_serial)
            pos += 1
            data[pos] = finish_set + paint_code
            final.append(data)
        else:
            final.append(data)

    # rewrite batch file
    with open(serial, 'wb') as batch:
        pickle.dump(final, batch)


# if all components are finished individually batch needs to reflect this in menu option 2()
def all_components_finished(serial, finish_set, paint_code):
    files = []
    data_list = []
    data_update = []
    serial_sepcific = serial[:12]  # key file(s) contain name, file wont be located without this
    for oslist_files in os.listdir():  # iterates through data folder listing dir and files
        if serial_sepcific in oslist_files:  # if the file matches make list of file
            files.append(oslist_files)
        else:
            pass
    for file in files:  # this will read through the files we need to check
        if '-' in file:
            with open(file, 'rb') as file_found:  # read bytes assigned to file
                while True:  # this avoids out ran out of input error
                    try:
                        data_list.append(pickle.load(file_found))
                    except EOFError:
                        break
        else:
            pass
    data_list_string = str(data_list)  # to make the in function available
    if 'Manufactured-unfinished' in data_list_string:  # searches through all component files string looking all are finished
        main()
    else:
        with open(serial_sepcific + '.pickle', 'rb') as update:
            while True:  # this avoids out ran out of input error
                try:
                    data_update.append(pickle.load(update))
                except EOFError:
                    break
    results = []
    # flatten lists
    for lists in data_update:
        try:
            if lists[1]:
                results.append(lists)
        except IndexError:
            for single in lists:
                try:
                    if single[1]:
                        results.append(single)
                except IndexError:
                    for one in single:
                        results.append(one)

        # replace unfinished element with finish

        for lists in results:
            for index, element in enumerate(lists):
                if 'Manufactured-unfinished' in element:
                    lists[index] = finish_set + paint_code

        with open(serial_sepcific + '.pickle', 'wb') as update:
            pickle.dump(results, update)  # replaces old data with new
    batch_index_finish(serial, finish_set + paint_code)


# this function will change batchindex manufacture finish
def batch_index_finish(serial, finish):
    serial = serial[:]  # removes .pickle
    list_for_update = []
    final_list = []
    if finish == 1:
        finish = 'Polished'
    else:
        finish = 'Painted'
    data = json.load(open('BatchIndex.json'))  # file exists, load data
    list_for_update.append(data)
    list_for_update = str(list_for_update).split(',')  # seperating our list at commas and converting into string
    for batch in list_for_update:
        if serial in batch:  # if the serial is found during iteration updates it and appends to list
            batch = batch.replace('Manufactured-unfinished', finish)
            final_list.append(batch)
        else:
            final_list.append(batch)

    with open('BatchIndex.json', 'w+') as index:
        json.dump(final_list, index)  # write to file


def graph():
    try:
        amount_of_components = 0
        amount_of_batches = 0
        for oslist_files in os.listdir():  # iterates through data folder ( files )
            if '-' in oslist_files:
                amount_of_components += 1  # increments our amount of components counter
            elif '-' not in oslist_files:  # increments our amount of batch counter
                amount_of_batches += 1
        amount_of_batches = amount_of_batches - 1  # removes json file from the counter

        types = ['Batch(s)', 'Component(s)']  # creates our bar labels
        amount = [amount_of_batches, amount_of_components]  # the amount of each type
        position = [0, 1]  # moves bar position
        plt.bar(position, amount, width=0.7)  # plots bars and selects width
        plt.xticks(position, types)  # using our position and types generates the two bars
        plt.ylabel('Amount Created')  # Label for y axis
        plt.xlabel('')  # no label for x axis
        plt.show()  # finally shows the user the generated graph
        average = amount_of_components / amount_of_batches  # this calculates the average amount of components per batch
        easygui.msgbox('On average {} components, are made per batch'.format(average))
    except ZeroDivisionError:
        easygui.msgbox('No current components files were detected returning to main menu')
        main()
    except ImportError and ImportWarning:  # If the user does not have the lib installed, error message
        easygui.msgbox('Your computer is missing the required dependencies\n Returning to main menu')
        main()


# Main menu accepting user input
def main():
    done = False
    # Until condition is True menu will run
    while not done:
        user_selection = easygui.choicebox('Choose an option', 'Menu', ['Create New Batch','List All Batches',
                                       'View Details Of A Batch', 'View Details Of A Component',
                                       'Allocate stock', 'Search by product type', 'Finish Component',
                                       'Graph Data(Batches & Components)', 'Quit'])
        if user_selection == 'Quit':
            done = True
            easygui.msgbox('Thank you Goodbye')
            quit()
        elif user_selection == 'Create New Batch':
            (number_of_components, component_type, model) = new_batch()  # unpack data and assign variable names
            manufacture_date = date_input()
            number = batch_number()
            view = easygui.ynbox('view batch?', 'View', ['Yes', 'No'])
            if view is True:
                serials = 0
                # if user wants to print sequential serials then
                while number_of_components != 0:
                    progress_count = 0  # this is for the progress bar
                    batch_details = Batch(number, manufacture_date, component_type, model,
                                          str(number_of_components).zfill(4),
                                          number_of_components)  # calls function and assigns variable
                    print('\nNumber of components to go {}'.format(number_of_components))
                    Batch.__str__(batch_details)
                    Batch.Objectdump(batch_details)
                    Batch.PickleBatch(batch_details)
                    Batch.PickleCompnenet(batch_details)
                    number_of_components -= 1
                    progress_count += 1
                    serials += 1
                    progress(progress_count, number_of_components)
                Batch.view_creation(batch_details)
                serials = str(serials).zfill(4)
                easygui.msgbox('Serials 0001 to ' + serials + ' created!')
                easygui.msgbox('please find more details below')

            else:
                # if user does not want to print sequential serials then
                while number_of_components != 0:
                    progress_count = 0  # this is for the progress bar
                    batch_details = Batch(number, manufacture_date, component_type, model,
                                          str(number_of_components).zfill(4),
                                          number_of_components)  # calls function and assigns variable
                    Batch.Objectdump(batch_details)
                    Batch.PickleBatch(batch_details)
                    Batch.PickleCompnenet(batch_details)
                    number_of_components -= 1
                    progress_count += 1
                    progress(progress_count, number_of_components)

        elif user_selection == 'List All Batches':
            # list all batches
            show_batch()
        elif user_selection == 'View Details Of A Batch':
            # Details of Batch
            batch_detail()
        elif user_selection == 'View Details Of A Component':
            # Details of Component
            component_detail()
        elif user_selection == 'Allocate stock':
            # Allocate stock
            allocate_stock()
        elif user_selection == 'Search by product type':
            # Search by product type
            search_type()
        elif user_selection == 'Finish Component':
            # Finish Component
            finish_comp()
        elif user_selection == 'Graph Data(Batches & Components)':
            # this function has dependence noted at top of code under imports
            try:
                graph()
            except NameError:
                easygui.msgbox('Your computer is missing some dependencies for this option please refer to documentation\n'
                      'returning to main menu')
                main()
        elif user_selection is None:
            easygui.msgbox('Thank you Goodbye')
            quit()


if __name__ == '__main__':
    try:
        os.mkdir('../Data/Backup')  # creates backup folder
    except FileExistsError:  # if file exists then ignore create folder
        pass
    for files in os.listdir('../Data'):
        try:
            # this copies all files in the folder through iteration to the backup folder with the shutil library
            shutil.copy('../Data/' + files,
                        '../Data/Backup')
        except PermissionError:
            pass
    easygui.msgbox('backup created')
    os.chdir('../Data')  # returns to regular folder for normal use
    easygui.msgbox('\n\nWelcome to the PPEC inventory system\n\n')
    if not os.path.isfile('BatchIndex.json'):  # checks for batch index file
        proceed = easygui.ynbox('Unable to Locate BatchIndex.json\nContinuing will create a new file', 'Warning',
                                ['Yes', 'No'])
        if proceed is True:
            main()
        else:
            easygui.msgbox('Terminating')
            quit()
    else:
        main()
