#!/usr/bin/python
import pgdb
import matplotlib
import matplotlib.pyplot as plt
params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':''}

connection1 = pgdb.Connection(**params)
connection1.autocommit=False
cursor1 = connection1.cursor()

# Q2A

# Year - population
# def query():
#     # Here we test some concurrency issues.
#     xy = "SELECT year, population FROM popdata";
#     print("U1: (start) "+ xy)
#     cursor1.execute(xy)
#     data = cursor1.fetchall()
#     connection1.commit()
#     xs= []
#     ys= []
#     for r in data:
#         # you access ith component of row r with r[i], indexing starts with 0
#         # check for null values represented as "None" in python before conversion and drop
#         # row whenever NULL occurs
#         print("Considering tuple", r)
#         if (r[0]!=None and r[0]!=None):
#             xs.append(float(r[0]))
#             ys.append(float(r[1]))
#         else:
#             print("Dropped tuple ", r)
#     print("xs:", xs)
#     print("ys:", ys)
#     return [xs, ys]

# Number of cities - year
# def query():
#     # Here we test some concurrency issues.
#     xy = "SELECT year, COUNT(city) FROM popdata GROUP BY year";
#     print("U1: (start) "+ xy)
#     cursor1.execute(xy)
#     data = cursor1.fetchall()
#     connection1.commit()
#     xs= []
#     ys= []
#     for r in data:
#         # you access ith component of row r with r[i], indexing starts with 0
#         # check for null values represented as "None" in python before conversion and drop
#         # row whenever NULL occurs
#         print("Considering tuple", r)
#         if (r[0]!=None and r[0]!=None):
#             xs.append(float(r[0]))
#             ys.append(float(r[1]))
#         else:
#             print("Dropped tuple ", r)
#     print("xs:", xs)
#     print("ys:", ys)
#     return [xs, ys]
#
# def close():
#     connection1.close()

# Mean population - decade
# Standard deviation - decade
def query():
    # Here we test some concurrency issues.
    xy = "SELECT FLOOR(year/10)*10, AVG(population), STDDEV_POP(population) FROM popdata GROUP BY year ORDER BY year";
    print("U1: (start) "+ xy)
    cursor1.execute(xy)
    data = cursor1.fetchall()
    connection1.commit()
    xs= []
    ys= []
    error_std= []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0]!=None and r[0]!=None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
            error_std.append(float(r[2]))
        else:
            print("Dropped tuple ", r)
    print("xs:", xs)
    print("ys:", ys)
    print("error_std:", error_std)
    return [xs, ys, error_std]

def close():
    connection1.close()


# when calling python lab2.py the following functions will be executed:
[xs, ys, error_std] = query()
plt.scatter(xs, ys)
plt.xlabel("year")
plt.errorbar(xs, ys, yerr=error_std, fmt="", color="lightblue") ####
plt.show()  # display figure if you run this code locally
plt.savefig("figure.png") # save figure as image in local directory
close()
