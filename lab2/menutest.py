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
        self.explore_menu = ["Latitute", "Elevation"]
        self.cur = self.conn.cursor()

    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i,x in enumerate(self.menu):
            print("%i. %s"%(i+1,x))
        return self.get_int()

    def print_explore_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
        for i,x in enumerate(self.explore_menu):
            print("%i. %s"%(i+1,x))
        return self.get_explore_int()

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
                print("That was not a number...")

    def get_explore_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.explore_menu):
                    return choice
                print("Invalid choice.")
            except (NameError,ValueError, TypeError,SyntaxError):
                print("That was not a number...")

    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    def run(self):
        while True:
            try:
                self.actions[self.print_menu()-1]()
                #self.actions[self.print_explore_menu()-1]()
            except IndexError:
                print("Bad choice")
                continue

    def population_query(self):
        print("\nExplore population by:")
        print("TEST", self.print_explore_menu())
        if self.print_explore_menu() == 1:
            self.latitude_program()
            # return or continue?
        if self.print_explore_menu() == 2:
            self.elevation_program()
            # return or continue?
        else:
            print("OPSI, fix error sutff")

        # while True:
        #     try:

        #         factors = int(input("Choose: "))
        #         if 1 <= choice <= len(self.explore_menu):
        #             return choice
        #         print("Invalid choice.")
        #     except (NameError,ValueError, TypeError,SyntaxError):
        #         print("That was not a number...")

        # def population_query(self):
        #     print("\nExplore population by:")
        #     while True:
        #         try:
        #             factors = int(input("1. Latitude\n2. Elevation\nChoose: "))
        #             if factors == 1:
        #                 self.latitude_program()
        #             if factors == 2:
        #                 self.elevation_program()
        #         except ValueError:
        #             print("Please choose between the given options, 1 or 2")
        #             return

    '''Elevation functions'''

    def elevation_program(self):
        minelv = input("\nChoose the minimum elevation for a city to explore: ")
        maxelv = input("Choose the maximum elevation for a city to explore: ")
        query ="SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <= %s ORDER BY elevation" % (minelv, maxelv)
        self.cur.execute(query)
        self.print_elevation_options()
        [pop_data1, elv_data1, chosen_city1] = self.choose_city1_elevation()
        print("\nNow find a second city with")
        minelv = input("Minimum elevation: ")
        maxelv = input("Maximum elevation: ")
        query ="SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minelv, maxelv)
        self.cur.execute(query)
        self.print_elevation_options()
        [pop_data2, elv_data2, chosen_city2] = self.choose_city2_elevation(chosen_city1)
        print("\nPlotting data...\n")
        self.print_elv_plot(pop_data1, elv_data1, pop_data2, elv_data2, chosen_city1, chosen_city2)

    def print_elevation_options(self):
        print("-----------------------------------")
        city_data = []
        country_data = []
        elevation_data = []
        result = []
        for r in self.cur.fetchall():
            if (r[0] != None and r[0] != None):                 # ADD ERROR HANDLIN
                city_data.append(r[0])
                country_data.append(r[1])
                elevation_data.append(float(r[2]))
                result.append(r)
            else:
                print("ERR", r)
        print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        print("-----------------------------------")

    def choose_city1_elevation(self):
        pop_data1 = []
        elv_data1 = []
        print("\nNow pick one of these cities to compare to another")                # ERROR HANDLIN
        if len(pop_data1) == 0:
            chosen_city1 = input("Type the name of the city: ")
            chosen_country1 = input("Type the country code for %s: " % chosen_city1)
            query = "SELECT city, country, year, population, elevation FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data1.append(float(r[3]))
                    elv_data1.append(float(r[4]))
                    print("\nYou chose %s, %s at elevation %s" % (chosen_city1, chosen_country1, elv_data1))  # elevation TO STRINg??
                    return [pop_data1, elv_data1, chosen_city1]
                else:
                    print("Dropped tuple ", r)
        else:           # NOT IN USE
            [pop_data2, elv_data2] = self.choose_city2_elevation(chosen_city1)

    def choose_city2_elevation(self, chosen_city1):
        pop_data2 = []
        elv_data2 = []
        print("\nNow pick one of these cities to compare to %s" % (chosen_city1))
        chosen_city2 = input("\nType the name of the city: ")
        chosen_country2 = input("Type the country code for %s: " % chosen_city2)
        if len(pop_data2) == 0:
            query = "SELECT city, country, year, population, elevation FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city2, chosen_country2)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data2.append(float(r[3]))
                    elv_data2.append(float(r[4]))
                    print("\nYou chose %s, %s at elevation %s" % (chosen_city2, chosen_country2, elv_data2))     # elv TO STRINg??
                    return [pop_data2, elv_data2, chosen_city2]
                else:
                    print("Dropped tuple ", r)
        else:
            print("OJ something went wrong. FIX ERROr")

    def print_elv_plot(self, pop_data1, elv_data1, pop_data2, elv_data2, chosen_city1, chosen_city2):
        plt.scatter(elv_data1, pop_data1, label=chosen_city1)
        plt.scatter(elv_data2, pop_data2, label=chosen_city2)
        plt.ylabel("POPULATION")
        plt.xlabel("ELEVATION")
        plt.legend(loc='best')
        plt.title("HYPOTHESIS: The higher the elevation, the lower the population")
        plt.show()

    '''Latitude functions'''

    def latitude_program(self):             # VERY UglY
        minlat = input("\nChoose the minimum latitude (-90 <= latitude => 90) for a city to explore: ")
        maxlat = input("Choose the maximum latitude for a city to explore: ")
        query ="SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minlat, maxlat)
        self.cur.execute(query)
        self.print_latitude_options()
        [pop_data1, lat_data1, chosen_city1] = self.choose_city1_latitude()
        print("\nNow find a second city with")
        minlat = input("Minimum latitude: ")
        maxlat = input("Maximum latitude: ")
        query ="SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minlat, maxlat)
        self.cur.execute(query)
        self.print_latitude_options()
        [pop_data2, lat_data2, chosen_city2] = self.choose_city2_latitude(chosen_city1)
        print("\nPlotting data...\n")
        self.print_lat_plot(pop_data1, lat_data1, pop_data2, lat_data2, chosen_city1, chosen_city2)

    def print_latitude_options(self):
        print("-----------------------------------")
        city_data = []
        country_data = []
        latitude_data = []
        result = []
        for r in self.cur.fetchall():
            if (r[0] != None and r[0] != None):                 # ADD ERROR HANDLIN
                city_data.append(r[0])
                country_data.append(r[1])
                latitude_data.append(float(r[2]))
                result.append(r)
            else:
                print("ERR", r)
        print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        print("-----------------------------------")

    def choose_city1_latitude(self):
        pop_data1 = []
        lat_data1 = []
        print("\nNow pick one of these cities to compare to another")                # ERROR HANDLIN
        if len(pop_data1) == 0:
            chosen_city1 = input("Type the name of the city: ")
            chosen_country1 = input("Type the country code for %s: " % chosen_city1)
            query = "SELECT city, country, year, population, latitude FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data1.append(float(r[3]))
                    lat_data1.append(float(r[4]))
                    print("\nYou chose %s, %s at latitude %s" % (chosen_city1, chosen_country1, lat_data1))  # LATITUDE TO STRIN??
                    return [pop_data1, lat_data1, chosen_city1]
                else:
                    print("Dropped tuple ", r)
        else:           # NOT IN USE
            [pop_data2, lat_data2] = self.choose_city2_latitude(chosen_city1)

    def choose_city2_latitude(self, chosen_city1):
        pop_data2 = []
        lat_data2 = []
        print("\nNow pick one of these cities to compare to %s" % (chosen_city1))
        chosen_city2 = input("\nType the name of the city: ")
        chosen_country2 = input("Type the country code for %s: " % chosen_city2)
        if len(pop_data2) == 0:
            query = "SELECT city, country, year, population, latitude FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city2, chosen_country2)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data2.append(float(r[3]))
                    lat_data2.append(float(r[4]))
                    print("\nYou chose %s, %s at latitude %s" % (chosen_city2, chosen_country2, lat_data2))     # LATITUDE TO STRIN??
                    return [pop_data2, lat_data2, chosen_city2]
                else:
                    print("Dropped tuple ", r)
        else:
            print("OJ something went wrong. FIX ERROr")

    def print_lat_plot(self, pop_data1, lat_data1, pop_data2, lat_data2, chosen_city1, chosen_city2):
        plt.scatter(lat_data1, pop_data1, label=chosen_city1)
        plt.scatter(lat_data2, pop_data2, label=chosen_city2)
        plt.ylabel("POPULATION")
        plt.xlabel("LATITUDE (°)")
        plt.legend(loc='best')
        plt.title("HYPOTHESIS: The higher the latitude, the lower the population")
        plt.show()


if __name__ == "__main__":
    print("========================================================================\nWE PRESENT TO YOU OUR HYPOTHESES FOR CITIES AROUND THE 🌍:\n\nThe higher the elevation, the lower the population\nThe higher the latitude (both +/- values), the lower the population\n")
    db = Program()
    db.run()
