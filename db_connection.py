import mariadb

try:
    conn = mariadb.connect(
        user="user",
        password="password",
        host="localhost",
        port=3306,
        database="testing"
    )
    print("Successfully connected to MariaDB")
    
    # Create a cursor
    cur = conn.cursor()
    
    # Execute a query
    cur.execute("SELECT * FROM your_table")
    
    # Fetch and print results
    for row in cur:
        print(row)
    
    # Close the connection
    conn.close()

except mariadb.Error as e:
    print(f"Error connecting to MariaDB: {e}")