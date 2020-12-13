import csv
import io
from datetime import datetime
from os import system

file = open("PB.csv", "r", encoding="UTF-8")
reader = csv.DictReader(file, delimiter=';')
data = list(reader)

running = True


def clear_screen():
    system('cls')


def generate_option_list():
    print("1. Generate average sum of all fines\n")
    print("2. Generate list of fines exceeding 100 euro's\n")
    print("3. Generate list of fines that were due to wrong parking\n")
    print("4. Generate top 10 of all outstanding fines\n")


def validate_input():
    while True:
        clear_screen()
        generate_option_list()
        selection = input("Please enter one of the options listen above in number form. \n"
                          "Alternatively, Press W to write all options to file \n"
                          "Press X to exit the program\n"
                          "Enter your option:  ")
        if selection.lower() not in ('1', '2', '3', '4', 'w', 'x'):
            print("Invalid option selected. Please try again\n")
        else:
            break

    if selection == "W":
        return 5
    if selection == "X":
        return 6

    try:
        if int(selection) == 1:
            return 1
        elif int(selection) == 2:
            return 2
        elif int(selection) == 3:
            return 3
        elif int(selection) == 4:
            return 4

    except ValueError:
        print("Invalid option selected. Please enter option in number form\n")


def select_option(selection):
    if selection == 1:
        clear_screen()
        total_sum, total_entries = generate_average_sum()
        print("Total Entries: " + str(total_entries))
        print("Total sum: €" + str(total_sum))
        print("Average sum: €" + str(int(total_sum / total_entries)) + "\n")
        input("Please press enter to continue\n")
    if selection == 2:
        clear_screen()
        amount = list_fines_over_100()
        print("There are " + str(amount) + " fines over €100 ")
        input("\nPlease press enter to continue\n")
    if selection == 3:
        clear_screen()
        amount = list_fines_for_wrong_parking()
        print("There are " + str(amount) + " fines for wrong parking")
        input("\nPlease press enter to continue\n")
    if selection == 4:
        clear_screen()
        entries = generate_top_10_overdue()
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
    return total_sum, total_entries


def list_fines_over_100():
    amount = 0
    for entries in data:
        if int(entries['bedrag']) >= 100:
            amount = amount + 1
    return amount


def list_fines_for_wrong_parking():
    amount = 0
    for entries in data:
        if str(entries['reden']) == "Invalideparkeerplek":
            amount = amount + 1
    return amount


def generate_top_10_overdue():
    collection = {}
    sortedlist = sorted([x for x in data if x['betaald'] == "Nee"],
                        key=lambda row: datetime.strptime(row["datum"], '%d-%m-%Y'))
    for i in range(10):
        collection[i] = f'{sortedlist[i]["datum"]}  Reden: {sortedlist[i]["reden"]} €{sortedlist[i]["bedrag"]}'
    return collection


def write_selection_to_file():
    filename = 'output.txt'
    encoding = 'utf-8'
    with io.open(filename, 'w+', encoding=encoding) as f:
        total_sum, total_entries = generate_average_sum()
        f.write("1. Average sum of fines: " + str(int(total_sum / total_entries)) + "\n")
        f.write("2. There are " + str(list_fines_over_100()) + " fines over €100 \n")
        f.write("3. There are " + str(list_fines_for_wrong_parking()) + " fines for wrong parking\n")

        entries = generate_top_10_overdue()
        f.write("4. Top 10 of longest outstanding unpaid fines: \n\n")
        for i in range(10):
            f.write(entries[i] + "\n")

        f.close()
    clear_screen()
    print("All available options have been written to a datafile named \"output.txt\"\n")
    input("Please press enter to continue\n")


def exit_program():
    print("Exiting program as requested")
    exit(0)


while running:
    select_option(validate_input())
