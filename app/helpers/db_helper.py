""" This module contains the DBHelper class to interact with the database. """
import mysql.connector


class DBHelper:
    """DBHelper class:
    Description:
        This class contains methods to interact with the database.
    Methods:
        insert_order_item(food_item, quantity, order_id)
        insert_order_tracking(order_id, status)
        get_total_order_price(order_id)
        get_next_order_id()
        get_order_status(order_id)
    """

    def __init__(
        self, host: str, user: str, password: str, database: str
    ) -> None:
        """Constructor for DBHelper class:
        Description:
            Creates a connection to the database
        Args:
            host (str): Hostname of the database server
            user (str): Username to access the database
            password (str): Password to access the database
            database (str): Name of the database
        """
        self.cnx = mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )

    def insert_order_item(
        self, food_item: str, quantity: int, order_id: int
    ) -> int:
        """Method: insert_order_item
        Description:
            Inserts an order item into the database
        Args:
            food_item (str): Name of the food item
            quantity (int): Quantity of the food item
            order_id (int): Order ID
        Returns:
            int: 1 if successful, -1 otherwise
        """
        try:
            cursor = self.cnx.cursor()
            cursor.callproc(
                "insert_order_item", (food_item, quantity, order_id)
            )
            self.cnx.commit()
            cursor.close()
            print("Order item inserted successfully!")

            return 1

        except mysql.connector.Error as err:
            print(f"Error inserting order item: {err}")
            self.cnx.rollback()
            return -1

        except Exception as e:
            print(f"An error occurred: {e}")
            self.cnx.rollback()

            return -1

    def insert_order_tracking(self, order_id: int, status: str) -> None:
        """Method: insert_order_tracking
        Description:
            Inserts an order tracking entry into the database
        Args:
            order_id (int): Order ID
            status (str): Status of the order
        """
        cursor = self.cnx.cursor()
        insert_query = (
            "INSERT INTO order_tracking (order_id, status) VALUES (%s, %s)"
        )
        cursor.execute(insert_query, (order_id, status))
        self.cnx.commit()
        cursor.close()

    def get_total_order_price(self, order_id: int) -> float:
        """Method: get_total_order_price
        Description:
            Fetches all the details of an order and calculates the total price
        Args:
            order_id (int): Order ID
        Returns:
            float: Total price of the order
        """
        cursor = self.cnx.cursor()
        query = f"SELECT get_total_order_price({order_id})"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        if result is None:
            return 0
        else:
            total_price = float(result)

        return total_price

    def get_next_order_id(self):
        """Method: get_next_order_id
        Description:
            Fetches the next order ID
        Returns:
            int: Next order ID
        """
        cursor = self.cnx.cursor()
        query = "SELECT MAX(order_id) FROM orders"
        cursor.execute(query)
        result = cursor.fetchone()[0]
        cursor.close()
        if result is None:
            return 1

        else:
            return result + 1

    def get_order_status(self, order_id: int) -> str:
        """Method: get_order_status
        Description:
            Fetches the status of an order
        Args:
            order_id (int): Order ID
        Returns:
            str: Status of the order
        """
        cursor = self.cnx.cursor()
        query = (
            f"SELECT status FROM order_tracking WHERE order_id = {order_id}"
        )
        cursor.execute(query)
        result = cursor.fetchone()
        cursor.close()
        if result:
            return result[0]
        else:
            return None

    def close(self):
        """Method: close
        Description:
            Closes the connection to the database
        """
        self.cnx.close()
