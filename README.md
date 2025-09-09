# debtRepaymentCalculator
Program to calculate average repayments of your interest free credit card debts and how long it will take to clear your debt.

Add the program to your computer and you can use it straight away. Just download the src folder and add it to your desired folder.

WARNING!
THIS PROGRAM IS NOT PASSWORD PROTECTED AND DOES NOT INCLUDE ANY SECURITY FEATURES.

Use at your own risk. I am not liable for any information leaked from your device.

## Purpose and Problem Definition

I have created this program as an easy way to view any credit card debt I have and work out easily what my average outgoings per card would be, in order to pay off my balance in full before the promotional rate ends.

Currently, banking applications do not easily show when your promotional rate ends. Some people may lose track of this and when planning or making financial decisions, or just for visibility of cash flow, this fact may be lost upon them.

I wanted to make sure that I can easily calculate how much time I have before the promotional rates of each of my cards end, and what the average monthly repayment would be. Hence, the debtRepaymentCalculator was born.

## Step by Step Process

This program took me approximately 5 hours to complete from start to finish, including:
1. Problem definition.
2. Drafting software requirements. (see SRS_debtRepaymentCalculator in the root directory of this repository) 
3. Development of program.
4. Testing the program.
5. Launching the program here on github.com

## Debugging Process

Through the development of this program, there were some bugs I found which had to be squashed.
The most annoying one of which was the extra indentation within the while loop for option 2. This went unnoticed for a while and I was confused. What would happen is I would be able to add information about the card as planned, but the txt file would not be written to.
This is all because the add_payment() function was called INSIDE the while loop itself. All I did was undo that extra indentation and everything worked as planned.

Another Problem was initially using PrettyTable to print the lines in the txt file in a nice ASCII format to the terminal.
I have never used PrettyTable before and while reading their official documentation, I found that there is a function in their library which can add rows to a predefined table using the function, "add_rows()".
I assumed it would take a list and to test if my function was working correctly, I added a list in line 1 of the existing_debts.txt file which included dummy values.
The table would not print and an error was thrown.

After some research I found that my code was reading the line in the txt file as a single string. Not what the function add_rows would take as an input. The simple solution to this was to import the "json" library.
Using this library I was able to read from and write to the txt file using json.loads and json.dumps.

I have also reformatted the file using the "black" python library for easy viewing of the code.

## Evaluation

Overall, a fun little weekend project which doesn't take long but helps me practice what I've learned.
In the future, would be nice to implement the following features:

1. Include functionality that would allow me to calculate repayments for debt which is not interest free.
2. Ability to remove entire rows from the table.
3. Any other recommendations or feedback implemented. 
