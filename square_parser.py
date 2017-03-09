"""
    Square Parser.py
        Written by John O'Hara
        March 9th, 2017 

        A small script for a bingo application. Coverts to/from CSV files representing possible square
        values from/to a more-readable text representation

        CSV input looks like this:

            $title=Test Card,Hello,Script

        Readable output looks like this:

            Test Card
            ---------

            00 - Hello
            01 - Script

        Line numbers are padded with zeros to the number of digits in the largest line number - i.e., 
        00, 01, 02 for a largest line number of 74.
"""


import re

div = "-------------------"

# probably shouldn't be changed
comma_replacement = "|"

if __name__ == "__main__":

    print()
    print("Bingo Square Parser")
    print(div)
    print()

    print("filename:", end=" ")

    filename = input()
    print()

    print("loading {}...".format(filename), end="")

    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print("aw, bummer. No file named '{}' exists.".format(filename))
        file_loaded = False
    else:
        print("success.")
        file_loaded = True

    while file_loaded:

        print("file option?", end=" ")
        file_option = input()
        print()

        if file_option == "c" or file_option == "csv":
            # go from squares format to csv
            file_output = open("{}_csv".format(filename.split(".")[0]),"w+")
            linecount = 0

            file.readline()

            for line in file.readlines():
                linecount += 1

            file.seek(0)

            pattern = r'\d+ - '

            title = file.readline().split("\n")[0]

            print("converting '{}' to csv format...".format(title))

            file_output.write("$title={},".format(title.replace(",",comma_replacement)))

            current_line = 0

            for line in file.readlines():
                match = re.match(pattern, line)
                current_line += 1

                if match:
                    parsed_line = line[match.span()[1]:].replace("\n", "")
                    print("adding '{}'...".format(parsed_line))
                    # commas in lines are replaced with pipes. Re-reading will eventually replace them.
                    formatted_line = "{}{}".format(parsed_line.replace(",",comma_replacement), "," if current_line != linecount else "")
                    file_output.write(formatted_line)

            file_output.close()
            break
        
        elif file_option == "s" or file_option == "squares":
            # go back from csv to squares
            file_output = open("{}_squares".format(filename.split(".")[0]),"w+")
            
            file_array = file.readline().split(",")

            linecount = len(file_array) - 1
            current_line = 0 

            title = file_array[0].split("$title=")[1]

            print("converting '{}' from csv format...".format(title))

            file_output.write("{}{}".format(title, "\n"))
            file_output.write("{}{}".format("-"*len(title), "\n"))
            file_output.write("\n")

            for line in file_array[1:]:
                formatted_line = "{} - {}".format(
                    format(
                        current_line, "".join(["0", len((linecount-1).__str__()).__str__()])), line.replace(comma_replacement, ","))
                print("adding '{}'...".format(formatted_line))
                file_output.write(formatted_line)
                current_line += 1

                if current_line != linecount:
                    file_output.write("\n")

            file_output.close()
            break

        elif file_option == "q" or file_option == "quit":
            print("exiting script...")
            break

    file.close()

    """
    if file_option == "a":
        print("read (a)ll:")
        print()
        print(file.read())
    elif file_option == "o":
        print("read (o)ne:")
        print()
        print(file.readline())
    elif file_option == "q":
        break
    else:
        print("Sorry, that's not a valid option - (a)ll/(o)ne/(q)uit")
    """





