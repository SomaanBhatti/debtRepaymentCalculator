from datetime import datetime
import json
from prettytable import PrettyTable


# initialises global variables
table = PrettyTable()
today = datetime.now().date()
menu = [
    "1. View existing debts",
    "2. Add a new credit card debt entry.",
    "3. Add payment to existing credit card.",
    "4. Add balance to existing credit card.",
    "5. Exit program.",
]


def main():
    # Prints welcome message.
    print("\n\nWelcome to the Debt Repayment Calculator!\n")
    print(f"Today's date: {today.strftime('%a %d %b %Y')}\n")

    while True:
        # Prints menu.
        for _ in menu:
            print(_)
        print()
        # Gets user choice and validates input.
        try:
            choice = int(input("Enter a number corresponding to a choice displayed: "))
            if choice in list(range(1, 6)):
                pass
            else:
                raise ValueError
        except ValueError:
            print("\n\nINVALID INPUT!\n\n")

        if choice == 1:
            # Views existing debts.
            print("\nYou've chosen option 1\n")
            view_extant_debts()
            break

        if choice == 2:
            print("\nYou've chosen option 2\n")

            # Gets and validates user input for variables needed to add new credit card debt entry using the add_new_cc function.
            while True:
                try:
                    four_digits = int(
                        input("Enter the last four digits of your card number: \n")
                    )
                    if four_digits >= 10000:
                        raise ValueError
                    remaining_balance = float(
                        input("Enter the remaining balance to 2 decimal places\n")
                    )
                    if remaining_balance != round(remaining_balance, 2):
                        raise ValueError
                    cleared_by = str(
                        input(
                            "Enter the date you wish to have this debt cleared by (DD/MM/YYYY): \n"
                        )
                    )
                    cleared_by = datetime.strptime(cleared_by, "%d/%m/%Y")
                    if cleared_by <= datetime.now():
                        raise ValueError
                    break
                except ValueError:
                    print("\n\nINVALID INPUT!\n\n")
            # Calls function to add new credit card debt entry.
            add_new_cc(four_digits, remaining_balance, cleared_by)
            break

        if choice == 3:
            print("\nYou've chosen option 3\n")

            # Gets and validates user input for variables needed to add payment to existing credit card using the add_payment function.
            while True:
                try:
                    four_digits = int(
                        input("Enter the last four digits of your card number: \n")
                    )
                    if four_digits >= 10000:
                        raise ValueError
                    amount_paid = float(
                        input("Enter the amount paid to 2 decimal places\n")
                    )
                    if amount_paid != round(amount_paid, 2):
                        raise ValueError
                    break
                except ValueError:
                    print("\n\nINVALID INPUT!\n\n")
            # Calls function to add payment to existing credit card.
            add_payment(four_digits, amount_paid)
            break

        if choice == 4:
            print("\nYou've chosen option 4\n")
            # Gets and validates user input for variables needed to add balance to existing credit card using the add_balance function.
            while True:
                try:
                    four_digits = int(
                        input("Enter the last four digits of your card number: \n")
                    )
                    if four_digits >= 10000:
                        raise ValueError
                    balance_added = float(
                        input(
                            "Enter the amount to be added to balance to 2 decimal places\n"
                        )
                    )
                    if balance_added != round(balance_added, 2):
                        raise ValueError
                    break
                except ValueError:
                    print("\n\nINVALID INPUT!\n\n")
            # Calls function to add balance to existing credit card.
            add_balance(four_digits, balance_added)
            break

        if choice == 5:
            # Exits program.
            print("\nYou've chosen option 5\n")
            break

    # Prints goodbye message.
    print("\nThank you for using this program. Goodbye!\n\n")


# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function definitions below
# --------------------------------------------------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------------------------------------------


# Views existing debts in a table format.
def view_extant_debts():
    with open("existing_debts.txt", "r") as file:
        # adds headers and rows to table from PrettyTable.
        table.field_names = [
            "Last Updated",
            "Card ending in ...",
            "Remaining Balance",
            "Avg Monthly Repayment",
            "No. Payments Remaining",
            "Debt cleared by",
        ]
        # reads each line from the txt file and adds to table and prints it.
        for line in file:
            table.add_row(json.loads(line))
        print(table)


def add_new_cc(four_digits: int, remaining_balance: float, cleared_by: str) -> None:
    # calculates average monthly repayment and number of repayments needed.
    num_of_repayments = 12 * (cleared_by.year - today.year) + (
        cleared_by.month - today.month
    )
    avg_repayment = round(remaining_balance / num_of_repayments, 2)

    # writes updated information to txt file.
    with open("existing_debts.txt", "a") as file:
        entry = [
            today.strftime("%a %d %b %Y"),
            four_digits,
            f"£{remaining_balance:.2f}",
            f"£{avg_repayment:.2f}",
            num_of_repayments,
            cleared_by.strftime("%a %d %b %Y"),
        ]
        file.write(json.dumps(entry) + "\n")
        file.close()
    print("\nNew Card added successfully!\n")


def add_payment(four_digits: int, amount_paid: float) -> None:
    # initialises list to hold all lines from txt file for processing.
    lines = []

    # reads each line from txt file and adds to list.
    with open("existing_debts.txt", "r") as file:
        for line in file:
            lines.append(json.loads(line))

    # processes each line/entry in the "lines" list taken from the txt tile to find matching card and update relevant information.
    for entry in lines:
        if entry[1] == four_digits:
            # finds current balance and calculates new balance after payment.
            current_balance = float(entry[2].replace("£", ""))
            new_balance = current_balance - amount_paid
            if new_balance < 0:
                print("\n\nPayment exceeds remaining balance. Please try again.\n\n")
                return
            entry[2] = f"£{new_balance:.2f}"
            # recalculates average repayment and number of repayments needed.
            num_of_repayments = entry[4]
            if num_of_repayments > 1:
                avg_repayment = round(new_balance / num_of_repayments, 2)
            else:
                avg_repayment = new_balance
                num_of_repayments = 1
            # updates average repayment and last updated date in the list "lines".
            entry[3] = f"£{avg_repayment:.2f}"
            entry[0] = today.strftime("%a %d %b %Y")
            break
    # if no matching card found, prints error message and exits function.
    else:
        print("\n\nCard not found. Please try again.\n\n")
        return

    # writes updated information from list "lines" back to the txt file.
    with open("existing_debts.txt", "w") as file:
        for entry in lines:
            file.write(json.dumps(entry) + "\n")
        file.close()

    print("\nPayment added successfully!\n")


def add_balance(four_digits: int, balance_added: float) -> None:
    # initialises list to hold all lines from txt file for processing.
    lines = []
    with open("existing_debts.txt", "r") as file:
        # reads each line from txt file and adds to list.
        for line in file:
            lines.append(json.loads(line))
    # processes each line/entry in the "lines" list taken from the txt tile to find matching card and update relevant information.
    for entry in lines:
        if entry[1] == four_digits:
            # finds current balance and calculates new balance after payment.
            current_balance = float(entry[2].replace("£", ""))
            new_balance = current_balance + balance_added
            entry[2] = f"£{new_balance:.2f}"
            num_of_repayments = entry[4]
            # recalculates average repayment and number of repayments needed.
            avg_repayment = round(new_balance / num_of_repayments, 2)

            # updates average repayment and last updated date in the list "lines".
            entry[3] = f"£{avg_repayment:.2f}"
            entry[0] = today.strftime("%a %d %b %Y")
            break
    # if no matching card found, prints error message and exits function.
    else:
        print("\n\nCard not found. Please try again.\n\n")
        return
    # writes updated information from list "lines" back to the txt file.
    with open("existing_debts.txt", "w") as file:
        for entry in lines:
            file.write(json.dumps(entry) + "\n")
        file.close()
    print("\nBalance added successfully!\n")


if __name__ == "__main__":
    main()
