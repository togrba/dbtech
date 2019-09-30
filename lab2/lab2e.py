#!/usr/bin/python
import pgdb

'''
Isolation levels in SQL
1. READ COMMITTED - default
    In select query it will take only commited values of table. 
    If any transaction is opened and incompleted on table in 
    others sessions then select query will wait till no transactions 
    are pending on same table.
2. READ UNCOMMITTED
    If any table is updated(insert or update or delete) under a transaction 
    and same transaction is not completed that is not committed or roll backed 
    then uncommitted values will displaly(Dirty Read) in select query 
    of "Read Uncommitted" isolation transaction sessions. 
    There won't be any delay in select query execution because this 
    transaction level does not wait for committed values on table.
3. REPEATABLE READ
    select query data of table that is used under transaction of 
    isolation level "Repeatable Read" can not be modified from any other 
    sessions till transcation is completed.
4. SERIALIZABLE
    Serializable Isolation is similar to Repeatable Read Isolation but 
    the difference is it prevents Phantom Read. This works based on range lock. 
    If table has index then it locks records based on index range used 
    in WHERE clause(like where ID between 1 and 3). If table doesn't have index 
    then it locks complete table.

source: http://www.besttechtools.com/articles/article/sql-server-isolation-levels-by-example
'''

class Demo_program:
    def __init__(self):
        #If you are using a local postgres server as user postgres with default database 'postgres'
        params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':''}

        self.connection1 = pgdb.Connection(**params)
        self.connection1.autocommit=False
        self.cursor1 = self.connection1.cursor()

        self.connection2 = pgdb.Connection(**params)
        self.connection2.autocommit=False
        self.cursor2 = self.connection2.cursor()

    def drop(self):
        # delete the table Sales if it does already exist
        try:
            query = "DROP TABLE Sales";
            self.cursor1.execute(query)
            self.connection1.commit()
            # by default in pgdb, all executed queries for connection 1 up to here form a transaction
            # we can also explicitly start tranaction by executing BEGIN TRANSACTION
        except:
            # Errors in python are caught using try ... except
            print("ROLLBACK: Sales table does not exists or other error.")
            self.connection1.rollback()
            pass

    def initialize(self):
        # Create table sales and add two initial tuples
        query = "CREATE TABLE Sales(name VARCHAR(30), price float)";
        self.cursor1.execute(query)
        query = """INSERT INTO Sales VALUES('Toothbrush', 100)""";
        self.cursor1.execute(query)
        query = """INSERT INTO Sales VALUES('Pen', 10)""";
        self.cursor1.execute(query)

        # this commits all executed queries forming a transaction up to this point
        self.connection1.commit()

    def scenario0(self):
        # Here we test some concurrency issues.
        print("----------------------------------------------------------------------------------------------------------")
        print("EXAMPLE transactions.py\n")

        tr1 = "BEGIN TRANSACTION"
        q_max = "select MAX(price) from Sales";
        q_min = "select MIN(price) from Sales";
        tr2 = "BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE"
        q_del = "delete from sales";
        q_ins = "insert into sales values('Chair', 2000)";

        print("U1: (start) " + tr1)
        self.cursor1.execute(tr1)
        print("U1: (max)   " + q_max)
        self.cursor1.execute(q_max)
        # result of fetchone is a tuple with 1 attribute, we access first component value with [0]
        user_max = self.cursor1.fetchone()[0]
        print("... max=" + str(user_max))

        print("U2: (start) " + tr2)
        self.cursor2.execute(tr1)
        print("U2: (del)   " + q_del)
        self.cursor2.execute(q_del)
        print("U2: (ins)   " + q_ins)
        self.cursor2.execute(q_ins)
        self.connection2.commit()

        print("U1: (min)   " + q_min)
        self.cursor1.execute(q_min)
        # result of fetchone is a tuple with 1 attribute, we access first component value with [0]
        user_min = self.cursor1.fetchone()[0]
        print("... min=" + str(user_min))
        print("... min > max as highlighted in lecture notes")
        self.connection1.commit()

    def scenario1(self):
        print("----------------------------------------------------------------------------------------------------------")
        print("DEMO: A phantom tuple that occurs in Nonrepeatable Read and then disappears when we switch to Serializable.\n")
        print("READ COMMITTED vs. SERIALIZABLE")

        tr1 = "BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;"
        tr2 = "BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;"
        q_sel = "SELECT * FROM Sales;"
        q_ins = "INSERT INTO Sales VALUES('Kool Chair', 3000);"
        com = "COMMIT;"

        print("U1: (start) " + tr1)
        self.cursor1.execute(tr1)
        print("U1: (get table) ", q_sel)
        self.cursor1.execute(q_sel)
        user1_table = self.cursor1.fetchall()
        print("... table = " + str(user1_table))

        print("U2: (start): ", tr2)
        self.cursor2.execute(tr2)
        print("U2: (insert): ", q_ins)
        self.cursor2.execute(q_ins)
        print("U2: (commit): ", com)
        self.cursor2.execute(com)

        print("U1: (get all): ", q_sel)
        self.cursor1.execute(q_sel)
        user2_table = self.cursor1.fetchall()
        print("... table = ", str(user2_table))

        print("U1: (commit): ", com)
        self.cursor1.execute(com)

    def scenario2(self):
        print("----------------------------------------------------------------------------------------------------------")
        print("DEMO: How non-repeatable reads can affect the outcome of a query in Read Commited vs Repeatable Read.\n")
        print("READ COMMITTED vs. REPEATABLE READ")

        tr1 = "BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;"
        tr2 = "BEGIN TRANSACTION ISOLATION LEVEL READ COMMITTED;"
        q_sel = "SELECT * FROM Sales;"
        q_upd = "UPDATE Sales SET price = 2500 WHERE price = 2000;"
        com = "COMMIT;"

        print("U1: (start) " + tr1)
        self.cursor1.execute(tr1)
        print("U1: (get table) ", q_sel)
        self.cursor1.execute(q_sel)
        user_table = self.cursor1.fetchall()
        print("... table = " + str(user_table))

        print("U2: (start): ", tr2)
        self.cursor2.execute(tr2)
        print("U2: (update): ", q_upd)
        self.cursor2.execute(q_upd)
        print("U2: (commit): ", com)
        self.cursor2.execute(com)
        print("U2: (get all): ", q_sel)
        self.cursor2.execute(q_sel)
        user_table = self.cursor2.fetchall()
        print("... table = ", str(user_table))

        print("U1: (get all): ", q_sel)
        self.cursor1.execute(q_sel)
        user_table = self.cursor1.fetchall()
        print("... table = ", str(user_table))

        print("U1: (commit): ", com)
        self.cursor1.execute(com)

    def scenario3(self):
        print("----------------------------------------------------------------------------------------------------------")
        print("DEMO: How a transaction with two insert statements of which the second fails can be rolled back without affecting another user’s queries.\n")

        tr1 = "BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;"
        tr2 = "BEGIN TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;"
        q_sel = "SELECT * FROM Sales;"
        q_ins1 = "INSERT INTO Sales VALUES('Basic Chair', 500);"
        q_ins2 = "INSERT INTO Sales VALUES('Luxe Chair', 6000);"
        q_ins3 = "INSERT INTO Sales VALUES(10000, 'Art Chair');"
        com = "COMMIT;"

        print("U1: (start) " + tr1)
        self.cursor1.execute(tr1)
        print("U1: (insert " + q_ins1)
        self.cursor1.execute(q_ins1)
        print("U1: (get table) ", q_sel)
        self.cursor1.execute(q_sel)
        user_table = self.cursor1.fetchall()
        print("... table = " + str(user_table))

        try:
            print("U2: (start): ", tr2)
            self.cursor2.execute(tr2)
            print("U2: (insert): "+ q_ins2)
            self.cursor2.execute(q_ins2)
            print("U2: (insert - fail): "+ q_ins3)
            self.cursor2.execute(q_ins3)
            print("U2: (commit): ", com)
            self.cursor2.execute(com)
        except:
            print("Insertion failed, rollback")
            self.connection2.execute(com)

        print("U1: (get all): ", q_sel)
        self.cursor1.execute(q_sel)
        user_table = self.cursor1.fetchall()
        print("... table = ", str(user_table))

        print("U1: (commit): ", com)
        self.cursor1.execute(com)

    def showall(self):
        self.cursor1.execute("SELECT * FROM Sales;");
        self.connection1.commit()
        print(self.cursor1.rowcount)
        for i in range(self.cursor1.rowcount):
            print(self.cursor1.fetchone())
        # results = self.cursor1.fetchall()
        # print "Sales relation contents:"
        # for r in results:
        # print r;

    def close(self):
        self.connection1.close()
        self.connection2.close()




if __name__ == "__main__":
    demo = Demo_program()
    demo.drop()
    demo.initialize()
    demo.showall()
    demo.scenario0()
    demo.scenario1()
    demo.scenario2()
    demo.scenario3()
    demo.showall()
    demo.close()




class Program_R:
    print("==========================================================================================")

    def __init__(self):
        #If you are using a local postgres server as user postgres with default database 'postgres'
        params = {'host':'localhost', 'user':'postgres', 'database':'postgres', 'password':''}

        self.connection1 = pgdb.Connection(**params)
        self.connection1.autocommit=False
        self.cursor1 = self.connection1.cursor()

        self.connection2 = pgdb.Connection(**params)
        self.connection2.autocommit=False
        self.cursor2 = self.connection2.cursor()

    def drop(self):
        # delete the table R if it does already exist
        try:
            query = "DROP TABLE R";
            self.cursor1.execute(query)
            self.connection1.commit()
            # by default in pgdb, all executed queries for connection 1 up to here form a transaction
            # we can also explicitly start tranaction by executing BEGIN TRANSACTION
        except:
            # Errors in python are caught using try ... except
            print("ROLLBACK: R table does not exists or other error.")
            self.connection1.rollback()
            pass

    def initialize(self):
        # Create table R and add two initial tuples
        query = "CREATE TABLE R(a INT, b INT)";
        self.cursor1.execute(query)
        query = """INSERT INTO R VALUES(0, 1)""";
        self.cursor1.execute(query)
        query = """INSERT INTO R VALUES(0, 2)""";
        self.cursor1.execute(query)
        query = """INSERT INTO R VALUES(1, 10)""";
        self.cursor1.execute(query)
        query = """INSERT INTO R VALUES(1, 20)""";
        self.cursor1.execute(query)

        # this commits all executed queries forming a transaction up to this point
        self.connection1.commit()

    def showall(self):
        self.cursor1.execute("SELECT * FROM R;");
        self.connection1.commit()
        print(self.cursor1.rowcount)
        for i in range(self.cursor1.rowcount):
            print(self.cursor1.fetchone())
        # results = cursor1.fetchall()
        # print "Sales relation contents:"
        # for r in results:
        # print r;

    def step1(self):
        q_sel = "SELECT * FROM R;"
        com = "COMMIT;"

        tr1 = "BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;"
        print("U1: (start) " + tr1)
        self.cursor1.execute(tr1)
        xval = "SELECT SUM(b) FROM R WHERE a=0;"  # a1
        self.cursor1.execute(xval)
        a1 = self.cursor1.fetchall()
        print("U1: (a1) ", a1)
        q_ins1 = "INSERT INTO R VALUES(1, a1);" #b1
        print("U1: (insert b1) ", q_ins1)
        self.cursor1.execute(q_ins1)
        print("U1: (commit): ", com)
        self.cursor1.execute(com)

        # print("U1: (get table) ", q_sel)
        # self.cursor1.execute(q_sel)
        # user_table = self.cursor1.fetchall()
        # print("... table = " + str(user_table))


    def step2(self):
        q_sel = "SELECT * FROM R;"
        com = "COMMIT;"

        tr2 = "BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;"
        print("U2: (start) " + tr2)
        self.cursor2.execute(tr2)
        xval2 = "SELECT SUM(b) FROM R WHERE a=0;" #a2
        self.cursor2.execute(xval2)
        print("U2: (a2) "), xval2
        q_ins2 = "INSERT INTO R VALUES(0, xval2);" #b2
        print("U2: (insert b2) ", q_ins2)
        self.cursor2.execute(q_ins2)
        print("U2: (commit): ", com)
        self.cursor2.execute(com)

        # print("U2: (get table) ", q_sel)
        # self.cursor2.execute(q_sel)
        # user_table = self.cursor2.fetchall()
        # print("... table = " + str(user_table))


if __name__ == "__main__":
    r = Program_R()
    r.drop()
    r.initialize()
    r.showall()
    r.step1()
    r.step2()
    r.showall()


