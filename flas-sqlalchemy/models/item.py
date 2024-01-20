import sqlite3


class ItemModel:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "SELECT * FROM items WHERE name=?"

        result = cursor.execute(sql_query, (name,))
        row = result.fetchone()

        connection.close()
        if row:
            return cls(*row)

    def insert(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "INSERT INTO items VALUES (?,?)"
        cursor.execute(sql_query, (self.name, self.price))

        connection.commit()
        connection.close()

    def update(self):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        sql_query = "UPDATE items SET price=? WHERE name=?"
        cursor.execute(sql_query, (self.price, self.name))
        connection.commit()
        connection.close()