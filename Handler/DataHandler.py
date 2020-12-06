import psycopg2


class DataHandler:

    def __init__(self):
        self.connection = self.connect()

    def connect(self):
        try:
            connection = psycopg2.connect(user="postgres",
                                          password="postgres",
                                          host="127.0.0.1",
                                          port="5432",
                                          database="WCM")

            cursor = connection.cursor()
            print(connection.get_dsn_parameters(), "\n")
            cursor.execute("SELECT version();")
            record = cursor.fetchone()
            print("You are connected to - ", record, "\n")
            return connection
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)

    def insert(self, company):
        sql = "INSERT INTO \"Company\" VALUES('" \
               + company.id + "', '" + company.name + "', '" + company.branche + "', '" + company.street + "', '" \
               + company.plz + "', '" + company.city + "', '" + company.phone_number + "', '" + company.website + "', '"\
               + company.mail + "');"
        self.execute_sql(sql)
        print("Inserted: " + company.id)

    def delete(self, id):
        sql = "Delete from \"Company\" where id = '" + id + "';"
        self.execute_sql(sql)

    def delete_all(self):
        sql = "Delete from \"Company\";"
        self.execute_sql(sql)

    def execute_sql(self, sql):
        try:
            cur = self.connection.cursor()
            cur.execute(sql)
            self.connection.commit()
            cur.close()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close_connection(self):
        if self.connection is not None:
            self.connection.close()
            print("PostgreSQL connection is closed")