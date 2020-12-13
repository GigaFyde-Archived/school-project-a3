import csv
import io
from datetime import datetime
from os import system

file = open("PB.csv", "r", encoding="UTF-8")
reader = csv.DictReader(file, delimiter=';')
data = list(reader)

running = True


def clear_screen():
    # Use system calls to clear the screen
    system('cls')


def generate_option_list():
    # List a selection of user options on the screen
    print("1. Generate average sum of all fines\n")
    print("2. Generate list of fines exceeding 100 euro's\n")
    print("3. Generate list of fines that were due to wrong parking\n")
    print("4. Generate top 10 of all outstanding fines\n")


def validate_input():
    # Start a loop
    while True:
        clear_screen()
        generate_option_list()
        selection = input("Please enter one of the options listen above in number form. \n"
                          "Alternatively, Press W to write all options to file \n"
                          "Press X to exit the program\n"
                          "Enter your option:  ")
        # input gets compared to selection below, if its not in that selection the input will be regarded as invalid
        if selection.lower() not in ('1', '2', '3', '4', 'w', 'x'):
            print("Invalid option selected. Please try again\n")
        else:
            break

    # Compare input to a few values
    if selection == "W":
        return 5
    if selection == "X":
        return 6

    # Check if the input is a number and if so, select the corresponding option
    try:
        if int(selection) == 1:
            return 1
        elif int(selection) == 2:
            return 2
        elif int(selection) == 3:
            return 3
        elif int(selection) == 4:
            return 4

    # In case the selection did still contain an invalid number, catch it and print an error
    except ValueError:
        print("Invalid option selected. Please enter option in number form\n")


def select_option(selection):
    # Start of if statement block
    if selection == 1:
        clear_screen()
        # Calculate average sum by dividing total_sum by total_entries
        total_sum, total_entries, average = generate_average_sum()
        print("Total Entries: " + str(total_entries))
        print("Total sum: €" + str(total_sum))
        print("Average sum: €" + str(average) + "\n")
        input("Please press enter to continue\n")
    if selection == 2:
        clear_screen()
        amount = list_fines_exceeding_100()
        # Print the total amount of fines that exceed 100 euros
        print("There are " + str(amount) + " fines over €100 ")
        input("\nPlease press enter to continue\n")
    if selection == 3:
        clear_screen()
        amount = list_fines_for_wrong_parking()
        # Print the total amount of fines found in the datafile that were for wrong parking
        print("There are " + str(amount) + " fines for wrong parking")
        input("\nPlease press enter to continue\n")
    if selection == 4:
        clear_screen()
        entries = generate_top_10_overdue()
        # Print a top 10 of all overdue fines found in the datafile by the function
        for i in range(10):
            print(entries[i])
        input("\nPlease press enter to continue\n")
    if selection == 5:
        write_selection_to_file()
    if selection == 6:
        exit_program()


def generate_average_sum():
    total_sum = 0
    total_entries = len(data)
    for entries in data:
        total_sum += int(entries['bedrag'])
    # Calculate average sum by dividing total_sum by total_entries
    return total_sum, total_entries, (total_sum / total_entries)


def list_fines_exceeding_100():
    # Count all entries that are over 100 euros and put the sum in a variable named amount
    amount = 0
    for entries in data:
        if int(entries['bedrag']) >= 100:
            amount = amount + 1
    return amount


def list_fines_for_wrong_parking():
    # Count all entries that are over for wrong parking and put the sum in a variable named amount
    amount = 0
    for entries in data:
        if str(entries['reden']) == "Invalideparkeerplek":
            amount = amount + 1
    return amount


def generate_top_10_overdue():
    # Sort all entries in the datafile that have the value of "Nee" for the key "betaald"
    # then sort them all by date from old to new
    collection = {}
    sortedlist = sorted([x for x in data if x['betaald'] == "Nee"],
                        key=lambda row: datetime.strptime(row["datum"], '%d-%m-%Y'))
    for i in range(10):
        collection[i] = f'{sortedlist[i]["datum"]}  Reden: {sortedlist[i]["reden"]} €{sortedlist[i]["bedrag"]}'
    return collection


def write_selection_to_file():
    filename = 'output.txt'
    encoding = 'utf-8'
    # Create a new file with utf-8 encoding, then write all values to it
    with io.open(filename, 'w+', encoding=encoding) as f:
        total_sum, total_entries, average = generate_average_sum()
        f.write("1. Average sum of fines: " + str(average) + "\n")
        f.write("2. There are " + str(list_fines_exceeding_100()) + " fines over €100 \n")
        f.write("3. There are " + str(list_fines_for_wrong_parking()) + " fines for wrong parking\n")

        entries = generate_top_10_overdue()
        f.write("4. Top 10 of longest outstanding unpaid fines: \n\n")
        # Iterate through all entries and write them all one by one on new lines
        for i in range(10):
            f.write(entries[i] + "\n")
        f.close()
    clear_screen()
    print("All available options have been written to a datafile named \"output.txt\"\n")
    input("Please press enter to continue\n")


def exit_program():
    print("Exiting program as requested")
    # Use system code 0 to indicate success, any value above 0 indicates an error
    exit(0)


while running:
    select_option(validate_input())
