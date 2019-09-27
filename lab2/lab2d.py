# HYPOTHESIS:
# The higher elevation, the lower population
# The higher values (both +/-) latitude, the lower population

# A menu where the user can choose on different factors that they can
# then compare a potential correlation to population

#!/usr/bin/python
import pgdb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sys import argv

class Program:
    def __init__(self): #PG-connection setup
        # local server:
        params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':''}
        self.conn = pgdb.Connection(**params)
        self.conn.autocommit=False
        # specify the command line menu here
        self.actions = [self.population_query, self.exit]
        # menu text for each of the actions above
        self.menu = ["Test hypotheses 🤔", "Exit"]
        self.cur = self.conn.cursor()
    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()
    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not valid, baka.... :(")

    def population_query(self):
        city = input("\nWhat's the name of the city you want to check out: ")
        country = input("\n%s lies in which country (type country code): " % city)
        query ="SELECT population, latitude, elevation FORM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (city, country)
        print("Will execute: ", query)

        self.cur.execute(query)
        self.print_answer()


        print("\nExplore population of %s, %s by:" % city, country)
        try:
            factors = int(input("1. Latitude\n2. Elevation\nChoose: "))
        except ValueError:
            print("Please choose between the given options, 1 or 2")
            return

    def exit(self):
        self.cur.close()
        self.conn.close()
        print("Buh-bye")
        exit()

    def print_answer(self):
        print("-----------------------------------")
        year_data = []
        pop_data = []
        result = []
        for r in self.cur.fetchall():
            if (r[0] != None and r[0] != None):
                year_data.append(float(r[0]))
                pop_data.append(float(r[1]))
                result.append(r)
            else:
                print("Dropped tuple ", r)
        print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        print("-----------------------------------")

        plt.scatter(year_data, pop_data)
        (m, b) = np.polyfit(year_data, pop_data, 1)
        print("TEST", m, b)
        yp = np.polyval([m, b], year_data)
        plt.plot(year_data, yp)
        plt.xlabel("year")
        plt.ylabel("population")
        plt.grid(True)
        plt.show()

    def run(self):
        while True:
            try:
                self.actions[self.print_menu()-1]()
            except IndexError:
                print("Bad choice")
                continue

if __name__ == "__main__":
    print("========================================================================\nWE PRESENT TO YOU OUR HYPOTHESES FOR CITIES AROUND THE 🌍:\n\nThe higher elevation, the lower population\nThe higher latitude (both +/- values), the lower population\n")
    db = Program()
    db.run()
