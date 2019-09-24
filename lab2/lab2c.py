#!/usr/bin/python
import pgdb
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from sys import argv

class Program:
    def __init__(self): #PG-connection setup
        # local server:
        params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':'Kth_derp667'}
        # kth server:
        # params = {'host':'nestor2.csc.kth.se', 'user': 'yourkthusername', 'database':'', 'password':'yournestorpassword'}
        self.conn = pgdb.Connection(**params)
        self.conn.autocommit=False
        # specify the command line menu here
        self.actions = [self.population_query, self.exit]
        # menu text for each of the actions above
        self.menu = ["Population Query", "Exit"]
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
        city = input("City name: ")
        country = input("Country code: ")
        query ="""SELECT citypops.year, citypops.population, regr_slope(popdata.population,popdata.year),
        regr_intercept(popdata.population,popdata.year), regr_r2(popdata.population,popdata.year), COUNT(popdata.population)
        FROM PopData, citypops WHERE popdata.city LIKE '%s' AND citypops.country LIKE '%s'
        GROUP BY (citypops.year, citypops.population)""" % (city, country) #yields None when year, popul included
        print("Will execute: ", query)

        self.cur.execute(query)
        self.print_answer()

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
    db = Program()
    db.run()
