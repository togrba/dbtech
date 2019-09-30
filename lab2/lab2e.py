#!/usr/bin/python
import pgdb

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

    def scenario1(self):
        # Here we test some concurrency issues.

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


    ''' Case 1: a phantom tuple that occurs in Repeatable Read and then disappears when we switch to Serializable.'''
    #def scenario1():


if __name__ == "__main__":
    demo = Demo_program()
    demo.drop()
    demo.initialize()
    demo.showall()
    demo.scenario1()
    demo.showall()
    demo.close()




# ==========================================================================================

class Program_R:

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


if __name__ == "__main__":
    r = Program_R()
    r.drop()
    r.initialize()

