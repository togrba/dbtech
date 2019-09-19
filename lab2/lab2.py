#!/usr/bin/python
import pgdb
import matplotlib
import matplotlib.pyplot as plt
params = {'host':'localhost', 'user':'Bang', 'database':'Bang', 'password':''}

# Q2A


connection1 = pgdb.Connection(**params)
connection1.autocommit=False
cursor1 = connection1.cursor()


# def drop():
#     # delete the table XYData if it does already exist
#     try:
#         query = "DROP TABLE XYData";
#         cursor1.execute(query)
#         connection1.commit()
#         # by default in pgdb, all executed queries for connection 1 up to here form a transaction
#         # we can also explicitly start tranaction by executing BEGIN TRANSACTION
#     except:
#         # Errors in python are caught using try ... except
#         print("ROLLBACK: XYData table does not exists or other error.")
#         connection1.rollback()
#         pass

# def init():
#     # Create table sales and add two initial tuples
#     query = "CREATE TABLE XYData(x decimal, y decimal)";
#     cursor1.execute(query)
#     query = """INSERT INTO XYData VALUES(12.1, 1.00)""";
#     cursor1.execute(query)
#     query = """INSERT INTO XYData VALUES(16.3, 12.1)""";
#     cursor1.execute(query)
#     query = """INSERT INTO XYData VALUES(6.3, 22.1)""";
#     cursor1.execute(query)
#     query = """INSERT INTO XYData VALUES(12.3, 32.1)""";
#     cursor1.execute(query)
#     query = """INSERT INTO XYData VALUES(NULL, 25.1)""";
#     cursor1.execute(query)
#
#     # this commits all executed queries forming a transaction up to this point
#     connection1.commit()

def query():
    # Here we test some concurrency issues.
    xy = "select year, population from popdata";
    print("U1: (start) "+ xy)
    cursor1.execute(xy)
    data = cursor1.fetchall()
    connection1.commit()
    xs= []
    ys= []
    for r in data:
        # you access ith component of row r with r[i], indexing starts with 0
        # check for null values represented as "None" in python before conversion and drop
        # row whenever NULL occurs
        print("Considering tuple", r)
        if (r[0]!=None and r[0]!=None):
            xs.append(float(r[0]))
            ys.append(float(r[1]))
        else:
            print("Dropped tuple ", r)
    print("xs:", xs)
    print("ys:", ys)
    return [xs, ys]


def close():
    connection1.close()


# when calling python filename.py the following functions will be executed:
# drop()
# init()
[xs, ys] = query()
plt.scatter(xs, ys)
plt.show()  # display figure if you run this code locally
plt.savefig("figure.png") # save figure as image in local directory
close()
