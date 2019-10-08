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
        self.actions = [self.population_query, self.trend_query, self.exit]
        # menu text for each of the actions above
        self.menu = ["Population Query", "Trend Examples", "Exit"]
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

    def exit(self):
        self.cur.close()
        self.conn.close()
        print("Buh-bye")
        exit()

    def population_query(self):
        city = input("City name: ")
        country = input("Country code: ")
        q1 = "SELECT year, population FROM PopData WHERE city LIKE '%s' AND country LIKE '%s'" % (city, country)
        q2 = """SELECT regr_slope(population,year), regr_intercept(population,year), regr_r2(population,year), COUNT(population)
        FROM PopData WHERE city LIKE '%s' AND country LIKE '%s'""" % (city, country)
        self.cur.execute(q1)
        [year, population] = self.print_answer()
        self.cur.execute(q2)
        self.append_answer(year,population)

    def print_answer(self):
        print("-----------------------------------")
        year_data = []
        pop_data = []
        result = []
        for r in self.cur.fetchall():
            if r[0] != None:
                year_data.append(float(r[0]))
                pop_data.append(float(r[1]))
                result.append(r)
            else:
                print("Dropped tuple ", r)
        #print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        return year_data,pop_data

    def append_answer(self, yr, pop):
        a = []
        b = []
        result = []
        for r in self.cur.fetchall():
            if r[0] != None:
                a.append(float(r[0]))
                b.append(float(r[1]))
                result.append(r)
            else:
                print("Dropped tuple ", r)
        print("r2:",result[0][2],"-","nsamples:",result[0][3])
        #print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        #print("a:",''.join(str(e) for e in a),"b:",''.join(str(e) for e in b), "years:",str(yr))
        for year in range(2020,2031):
            yr.append(year)
            pop.append(a*np.array(year) + b)
        print("Year : Population")
        for i in range(0,len(yr)):
            print(int(yr[i]),":",int(pop[i]))
        print("-----------------------------------")
        pred = a*np.array(yr) + b
        plt.scatter(yr, pop)
        plt.xlabel("year")
        plt.ylabel("population")
        plt.grid(True)
        plt.plot(yr,pred)
        plt.show()

    def trend_query(self):
        q1 = """SELECT linearprediction.name, linearprediction.country from LinearPrediction, PopData WHERE 
        linearprediction.country = popdata.country AND linearprediction.name = popdata.city AND linearprediction.r2 > 0.9
        AND linearprediction.nsamples > 4 AND linearprediction.a < 0 GROUP BY name, linearprediction.country LIMIT 4;"""
        self.cur.execute(q1)
        [city, country] = self.trend_examples()
        for i in range(4):
            curr_city = city[i]
            curr_country = country[i]
            q2 = "SELECT year, population FROM PopData WHERE city LIKE '%s' AND country LIKE '%s'" % (curr_city, curr_country)
            q3 = """SELECT regr_slope(population,year), regr_intercept(population,year), regr_r2(population,year), COUNT(population)
                    FROM PopData WHERE city LIKE '%s' AND country LIKE '%s'""" % (curr_city, curr_country)
            self.cur.execute(q2)
            [year, population] = self.print_answer()
            self.cur.execute(q3)
            self.print_examples(year,population,curr_city)
        plt.grid(True)
        plt.legend()
        plt.show()

    def trend_examples(self):
        print("-----------------------------------")
        city = []
        country = []
        result = []
        for r in self.cur.fetchall():
            if r[0] != None:
                print(r)
                city.append(str(r[0]))
                country.append(str(r[1]))
                result.append(r)
            else:
                print("Dropped tuple ", r)
        #print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        return city, country

    def print_examples(self, yr, pop,ci):
        a = []
        b = []
        result = []
        for r in self.cur.fetchall():
            if r[0] != None:
                a.append(float(r[0]))
                b.append(float(r[1]))
                result.append(r)
            else:
                print("Dropped tuple ", r)
        print("r2:",result[0][2],"-","nsamples:",result[0][3])
        #print("\n".join([", ".join([str(a) for a in x]) for x in result]))
        #print("a:",''.join(str(e) for e in a),"b:",''.join(str(e) for e in b), "years:",str(yr))
        for year in range(2020,2031):
            yr.append(year)
            pop.append(a*np.array(year) + b)
        print("Year : Population for",ci)
        for i in range(0,len(yr)):
            print(int(yr[i]),":",int(pop[i]))
        print("-----------------------------------")
        pred = a*np.array(yr) + b
        plt.scatter(yr, pop)
        plt.xlabel("year")
        plt.ylabel("population")
        plt.plot(yr,pred,label=ci)

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
