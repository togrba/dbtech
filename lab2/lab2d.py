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
            except IndexError:
                print("Bad choice")
                continue

    def population_query(self):
        print("\nExplore population by:")
        if self.print_explore_menu() == 1:
            self.latitude_program()
        else:
            self.elevation_program()

    '''Elevation functions'''

    def elevation_program(self):
        minelv = 0
        while True:
            try:
                if minelv == 0 or minelv < -30 or minelv > 4330:
                    minelv = int(input("\nChoose the minimum elevation for a city to explore: "))
                    if -30 <= minelv <= 4330:
                        maxelv = int(input("Choose the maximum elevation for a city to explore: "))
                        if -30 <= maxelv <= 4330:
                            query = "SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <=%s ORDER BY elevation" % (minelv, maxelv)
                            self.cur.execute(query)
                            self.print_elevation_options()
                            [pop_data1, elv_data1, chosen_city1] = self.choose_city1_elevation()
                            print("\nNow find a second city with")
                            self.elevation_program_next(pop_data1, elv_data1, chosen_city1)
                    print("Invalid choice. Choose an elevation between -30 and 4330")
                else:
                    maxelv = int(input("Choose the maximum elevation for a city to explore: "))
                    if -30 <= maxelv <= 4330:
                        query = "SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <=%s ORDER BY elevation" % (minelv, maxelv)
                        self.cur.execute(query)
                        self.print_elevation_options()
                        [pop_data1, elv_data1, chosen_city1] = self.choose_city1_elevation()
                        print("\nNow find a second city with")
                        self.elevation_program_next(pop_data1, elv_data1, chosen_city1)
                    print("Invalid choice. Choose an elevation between -30 and 4330")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number...")

    def elevation_program_next(self, pop_data1, elv_data1, chosen_city1):
        minelv = 0
        while True:
            try:
                if minelv == 0 or minelv < -30 or minelv > 4330:
                    minelv = int(input("Minimum elevation: "))
                    if -30 <= minelv <= 4330:
                        maxelv = int(input("Maximum elevation: "))
                        if -30 <= maxelv <= 4330:
                            query = "SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <=%s ORDER BY elevation" % (minelv, maxelv)
                            self.cur.execute(query)
                            self.print_elevation_options()
                            [pop_data2, elv_data2, chosen_city2] = self.choose_city2_elevation(chosen_city1)
                            print("\nPlotting data...\n")
                            self.print_elv_plot(pop_data1, elv_data1, pop_data2, elv_data2, chosen_city1, chosen_city2)
                            self.run()
                    print("Invalid choice. Choose an elevation between -30 and 4330")
                else:
                    maxelv = int(input("Maximum elevation: "))
                    if -30 <= maxelv <= 4330:
                        query = "SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <=%s ORDER BY elevation" % (minelv, maxelv)
                        self.cur.execute(query)
                        self.print_elevation_options()
                        [pop_data2, elv_data2, chosen_city2] = self.choose_city2_elevation(chosen_city1)
                        print("\nPlotting data...\n")
                        self.print_elv_plot(pop_data1, elv_data1, pop_data2, elv_data2, chosen_city1, chosen_city2)
                        self.run()
                    print("Invalid choice. Choose an elevation between -30 and 4330")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number...")

    def print_elevation_options(self):
        city_data = []
        country_data = []
        elevation_data = []
        result = []
        data = self.cur.fetchall()
        if len(data) != 0:
            for r in data:
                city_data.append(r[0])
                country_data.append(r[1])
                elevation_data.append(float(r[2]))
                result.append(r)
            print("-----------------------------------")
            print("\n".join([", ".join([str(a) for a in x]) for x in result]))
            print("-----------------------------------")
        else:
            print("Oups, no cities within the given latitude")
            self.elevation_program()

    def choose_city1_elevation(self):
        pop_data1 = []
        elv_data1 = []
        print("\nNow pick one of these cities to compare to another")
        while True:
            try:
                if len(pop_data1) == 0:
                    chosen_city1 = input("Type the name of the city: ")
                    if len(chosen_city1) != 0:
                        chosen_country1 = input("Type the country code for %s: " % chosen_city1)
                        if len(chosen_country1) != 0:
                            query = "SELECT name, country, population, elevation FROM city WHERE name LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
                            self.cur.execute(query)
                            data = self.cur.fetchall()
                            for r in data:
                                if (r[0]!=None and r[0]!=None):
                                    pop_data1.append(float(r[2]))
                                    elv_data1.append(float(r[3]))
                                    print("\nYou chose %s, %s at elevation %s" % (chosen_city1, chosen_country1, str(elv_data1).strip("[]")))
                                    return [pop_data1, elv_data1, chosen_city1]
                                else:
                                    print("Dropped tuple ", r)
                    print("Hmm. Unknown city.")
                else:
                    [pop_data2, elv_data2] = self.choose_city2_elevation(chosen_city1)
            except (NameError, ValueError, TypeError, SyntaxError):
                print("Hmm. Unknown city.")

    def choose_city2_elevation(self, chosen_city1):
        pop_data2 = []
        elv_data2 = []
        print("\nNow pick one of these cities to compare to %s" % (chosen_city1))
        while True:
            try:
                if len(pop_data2) == 0:
                    chosen_city2 = input("\nType the name of the city: ")
                    if len(chosen_city2) != 0:
                        chosen_country2 = input("Type the country code for %s: " % chosen_city2)
                        if len(chosen_country2) != 0:
                            query = "SELECT name, country, population, elevation FROM city WHERE name LIKE '%s' AND country LIKE '%s'" % (chosen_city2, chosen_country2)
                            self.cur.execute(query)
                            data = self.cur.fetchall()
                            for r in data:
                                if (r[0]!=None and r[0]!=None):
                                    pop_data2.append(float(r[2]))
                                    elv_data2.append(float(r[3]))
                                    print("\nYou chose %s, %s at elevation %s" % (chosen_city2, chosen_country2, str(elv_data2).strip("[]")))
                                    return [pop_data2, elv_data2, chosen_city2]
                                else:
                                    print("Dropped tuple ", r)
                    print("Hmm. Unknown city.")
                # else:
                #     print("OJ something went wrong. FIX ERROr")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("Hmm. Unknown city.")

    def print_elv_plot(self, pop_data1, elv_data1, pop_data2, elv_data2, chosen_city1, chosen_city2):
        plt.scatter(elv_data1, pop_data1, label=chosen_city1)
        plt.scatter(elv_data2, pop_data2, label=chosen_city2)
        plt.ylabel("POPULATION")
        plt.xlabel("ELEVATION")
        plt.legend(loc='best')
        plt.title("HYPOTHESIS: The higher the elevation, the lower the population")
        plt.show()

    '''Latitude functions'''

    def latitude_program(self):
        minlat = 0
        while True:
            try:
                if minlat == 0 or minlat < -90 or minlat > 90:
                    minlat = int(input("\nChoose the minimum latitude for a city to explore: "))
                    if -90 <= minlat <= 90:
                        maxlat = int(input("Choose the maximum latitude for a city to explore: "))
                        if -90 <= maxlat <= 90:
                            query = "SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <=%s ORDER BY latitude" % (minlat, maxlat)
                            self.cur.execute(query)
                            self.print_latitude_options()
                            [pop_data1, lat_data1, chosen_city1] = self.choose_city1_latitude()
                            print("\nNow find a second city with")
                            self.latitude_program_next(pop_data1, lat_data1, chosen_city1)
                    print("Invalid choice. Choose a latitude between -90 and 90")
                else:
                    maxlat = int(input("Choose the maximum latitude for a city to explore: "))
                    if -90 <= maxlat <= 90:
                        query = "SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <=%s ORDER BY latitude" % (minlat, maxlat)
                        self.cur.execute(query)
                        self.print_latitude_options()
                        [pop_data1, lat_data1, chosen_city1] = self.choose_city1_latitude()
                        print("\nNow find a second city with")
                        self.latitude_program_next(pop_data1, lat_data1, chosen_city1)
                    print("Invalid choice. Choose a latitude between -90 and 90")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number...")

    def latitude_program_next(self, pop_data1, lat_data1, chosen_city1):
        minlat = 0
        while True:
            try:
                if minlat == 0 or minlat < -90 or minlat > 90:
                    minlat = int(input("Minimum latitude: "))
                    if -90 <= minlat <= 90:
                        maxlat = int(input("Maximum latitude: "))
                        if -90 <= maxlat <= 90:
                            query = "SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minlat, maxlat)
                            self.cur.execute(query)
                            self.print_latitude_options()
                            [pop_data2, lat_data2, chosen_city2] = self.choose_city2_latitude(chosen_city1)
                            print("\nPlotting data...\n")
                            self.print_lat_plot(pop_data1, lat_data1, pop_data2, lat_data2, chosen_city1, chosen_city2)
                            self.run()
                    print("Invalid choice. Choose a latitude between -90 and 90")
                else:
                    maxlat = int(input("Maximum latitude: "))
                    if -90 <= maxlat <= 90:
                        query = "SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minlat, maxelv)
                        self.cur.execute(query)
                        self.print_latitude_options()
                        [pop_data2, lat_data2, chosen_city2] = self.choose_city2_latitude(chosen_city1)
                        print("\nPlotting data...\n")
                        self.print_lat_plot(pop_data1, lat_data1, pop_data2, lat_data2, chosen_city1, chosen_city2)
                        self.run()
                    print("Invalid choice. Choose a latitude between -90 and 90")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number...")

    def print_latitude_options(self):
        city_data = []
        country_data = []
        latitude_data = []
        result = []
        data = self.cur.fetchall()
        if len(data) != 0:
            for r in data:
                city_data.append(r[0])
                country_data.append(r[1])
                latitude_data.append(float(r[2]))
                result.append(r)
            print("-----------------------------------")
            print("\n".join([", ".join([str(a) for a in x]) for x in result]))
            print("-----------------------------------")
        else:
            print("Oups, no cities within the given latitude")
            self.latitude_program()

    def choose_city1_latitude(self):
        pop_data1 = []
        lat_data1 = []
        print("\nNow pick one of these cities to compare to another")
        while True:
            try:
                if len(pop_data1) == 0:
                    chosen_city1 = input("Type the name of the city: ")
                    if len(chosen_city1) != 0:
                        chosen_country1 = input("Type the country code for %s: " % chosen_city1)
                        if len(chosen_country1) != 0:
                            query = "SELECT name, country, population, latitude FROM city WHERE name LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
                            self.cur.execute(query)
                            data = self.cur.fetchall()
                            for r in data:
                                if (r[0]!=None and r[0]!=None):
                                    pop_data1.append(float(r[2]))
                                    lat_data1.append(float(r[3]))
                                    print("\nYou chose %s, %s at latitude %s" % (chosen_city1, chosen_country1, str(lat_data1).strip("[]")))
                                    return [pop_data1, lat_data1, chosen_city1]
                                else:
                                    print("Dropped tuple ", r)
                    print("Hmm. Unknown city.")
                else:
                    [pop_data2, lat_data2] = self.choose_city2_latitude(chosen_city1)
            except (NameError, ValueError, TypeError, SyntaxError):
                print("Hmm. Unknown city.")

    def choose_city2_latitude(self, chosen_city1):
        pop_data2 = []
        lat_data2 = []
        print("\nNow pick one of these cities to compare to %s" % (chosen_city1))
        while True:
            try:
                if len(pop_data2) == 0:
                    chosen_city2 = input("\nType the name of the city: ")
                    if len(chosen_city2) != 0:
                        chosen_country2 = input("Type the country code for %s: " % chosen_city2)
                        if len(chosen_country2) != 0:
                            query = "SELECT name, country, population, latitude FROM city WHERE name LIKE '%s' AND country LIKE '%s'" % (chosen_city2, chosen_country2)
                            self.cur.execute(query)
                            data = self.cur.fetchall()
                            for r in data:
                                if (r[0]!=None and r[0]!=None):
                                    pop_data2.append(float(r[2]))
                                    lat_data2.append(float(r[3]))
                                    print("\nYou chose %s, %s at latitude %s" % (chosen_city2, chosen_country2, str(lat_data2).strip("[]")))
                                    return [pop_data2, lat_data2, chosen_city2]
                                else:
                                    print("Dropped tuple ", r)
                    print("Hmm. Unknown city.")
                # else:
                #     print("OJ something went wrong. FIX ERROr")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("Hmm. Unknown city.")

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
