#!/usr/bin/python
import pgdb
from sys import argv

class Program:
    def __init__(self): #PG-connection setup
        # local server:
        params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':''}
        # kth server:
        # params = {'host':'nestor2.csc.kth.se', 'user': 'yourkthusername', 'database':'', 'password':'yournestorpassword'}
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
                print("That was not a number...")

    def population_query(self):
        print("\nExplore population by:")
        try:
            factors = int(input("1. Latitude\n2. Elevation\nChoose: "))
            if factors == 1:
                self.latitude_program()
            if factors == 2:
                self.elevation_program()
        except ValueError:
            print("Please choose between the given options, 1 or 2")
            return

    def elevation_program(self):
        minelv = input("\nChoose a city with minimum elevation: ")
        maxelv = input("Choose a city with maximum elevation: ")
        query ="SELECT name, country, elevation FROM city WHERE elevation >=%s AND elevation <= %s ORDER BY elevation" % (minelv, maxelv)


    def latitude_program(self):
        minlat = input("\nChoose a city with minimum latitude: ")
        maxlat = input("Choose a city with maximum latitude: ")
        query ="SELECT name, country, latitude FROM city WHERE latitude >=%s AND latitude <= %s ORDER BY latitude" % (minlat, maxlat)
        #print("Will execute: ", query)
        self.cur.execute(query)
        self.print_latitude_options()
        [pop_data1, lat_data1] = self.choose_city1_latitude()
        [pop_data2, lat_data2] = self.choose_city2_latitude(chosen_city1)


    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    def print_latitude_options(self):
        print("-----------------------------------")
        city_data = []
        country_data = []
        population_data = []
        latitude_data = []
        elevation_data = []
        result = []
        for r in self.cur.fetchall():
            if (r[0] != None and r[0] != None):
                city_data.append(r[0])
                country_data.append(r[1])
                #population_data.append(float(r[2]))
                latitude_data.append(float(r[2]))
                #elevation_data.append(float(r[2]))
                result.append(r)
            else:
                print("ERR", r)
        print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        print("-----------------------------------")

    def choose_city1_latitude(self):
        pop_data1 = []
        lat_data1 = []
        chosen_city1 = input("\nNOW CHOOSE ONE CITY TO COMPARE TO ANOTHER\nWhat's the name of the city: ")
        chosen_country1 = input("Enter country code for %s: " % chosen_city1)
        if len(pop_data1) == 0:
            query = "SELECT city, country, year, population, latitude FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data1.append(float(r[3]))
                    lat_data1.append(float(r[4]))
                    return [pop_data1, lat_data1, chosen_city1]
                else:
                    print("Dropped tuple ", r)
        else:
            print("popdata populated")

    def choose_city2_latitude(self, chosen_city1):
        pop_data2 = []
        lat_data2 = []
        chosen_city2 = input("NOW CHOOSE THE SECOND CITY TO COMPARE TO %s \nWhat's the name of the city: " % chosen_city1)
        chosen_country2 = input("Enter country code for %s: " % chosen_city2)
        if len(pop_data2) == 0:
            query = "SELECT city, country, year, population, latitude FROM popdata WHERE city LIKE '%s' AND country LIKE '%s'" % (chosen_city1, chosen_country1)
            self.cur.execute(query)
            data = self.cur.fetchall()
            for r in data:
                if (r[0]!=None and r[0]!=None):
                    pop_data2.append(float(r[3]))
                    lat_data2.append(float(r[4]))
                    return [pop_data2, lat_data2]
                else:
                    print("Dropped tuple ", r)


    def print_plot(self):
        plt.scatter(pop_data1, lat_data1)
        plt.xlabel("?")
        plt.show()  # display figure if you run this code locally
        #plt.savefig("figure.png") # save figure as image in local directory
        #return where?

    def run(self):
        while True:
            try:
                self.actions[self.print_menu()-1]()
            except IndexError:
                print("Bad choice")
                continue

if __name__ == "__main__":
    print("========================================================================\nWE PRESENT TO YOU OUR HYPOTHESES FOR CITIES AROUND THE 🌍:\n\nThe higher the elevation, the lower the population\nThe higher the latitude (both +/- values), the lower the population\n")
    db = Program()
    db.run()
