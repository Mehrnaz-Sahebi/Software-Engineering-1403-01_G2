import mysql.connector as mysql
from datetime import date
from registration.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from registration.database.query import *
import mysql.connector as mysql


# Function to save a text optimization record
def save_text(mydb, username, input_text, optimized_text):
    cursor = mydb.cursor()
    user_id = get_user_id_by_username(mydb, username)
    print(f"user={user_id}")
    if not user_id:
        print(f"User with username '{username}' does not exist.")
        return None

    query = """
    INSERT INTO group9_text_optimization (user_id, input_text, optimized_text, created_at)
    VALUES (%s, %s, %s, %s);
    """
    try:
        cursor.execute(query, (user_id, input_text, optimized_text, date.today()))
        mydb.commit()
        print("Text saved successfully.")
        return cursor.lastrowid  # Return the ID of the inserted record
    except mysql.Error as e:
        print(f"Failed to insert text: {e}")
        return None
    finally:
        cursor.close()

# Function to fetch a text by ID
def fetch_text_by_id(mydb, text_id):
    cursor = mydb.cursor(dictionary=True)  # Use dictionary=True for column names in the result
    query = "SELECT * FROM group9_text_optimization WHERE id = %s"
    try:
        cursor.execute(query, (text_id,))
        return cursor.fetchone()
    except mysql.Error as e:
        print(f"Failed to fetch text: {e}")
        return None
    finally:
        cursor.close()

def does_text_exist(mydb, input, username, date=date.today()):
    print(date)
    if get_text_id_by_input_and_date(mydb, input, username, date) == None:
        return False
    return True

def get_text_id_by_input_and_date(mydb, input_text, username, date=date.today()):
    """
    This function retrieves the ID of a text optimization entry based on the input text, the username of the user who submitted it,
    and the date when the text was created. This is useful for checking if the same text has already been optimized by the user 
    on a particular day.
    """
    cursor = mydb.cursor(dictionary=True)  # Use dictionary=True for more readable results
    query = """
    SELECT t.id
    FROM group9_text_optimization t
    INNER JOIN users u ON t.user_id = u.id
    WHERE t.input_text = %s AND u.username = %s AND t.created_at = %s
    """
    try:
        # Execute the query
        cursor.execute(query, (input_text, username, f"{date} 00:00:00"))
        results = cursor.fetchall()  # Fetch all rows to avoid unread results        
        if results:
            return results[0]["id"]  # Return the text ID
        else:
            return None  # No match found
    except mysql.Error as e:
        print(f"Failed to fetch text ID: {e}")
        return None
    finally:

        cursor.close()


# def get_text_id_by_input_and_date(mydb, input_text, username, date=date.today()):
#     """
#     Retrieve the ID of a text optimization entry based on input text, username, and date.
#     """
#     cursor = mydb.cursor(dictionary=True)  # Use dictionary=True for more readable results
#     query = """
#     SELECT t.id
#     FROM group9_text_optimization t
#     INNER JOIN users u ON t.user_id = u.id
#     WHERE t.input_text = %s 
#       AND u.username = %s 
#     """
#     try:
#         # Execute the query
#         cursor.execute(query, (input_text, username))
#         results = cursor.fetchall()  # Fetch all rows to avoid unread results  
#         print(results)
#         print("*****")      
#         if results:
#             return results[0]["id"]  # Return the text ID
#         else:
#             return None  # No match found
#     except mysql.Error as e:
#         print(f"Failed to fetch text ID: {e}")
#         return None
#     finally:
#         cursor.close()


# Function to save a mistake
def save_mistake(mydb, text_id, mistake_type, wrong_part, mistake_made_by_username, note, correct_form):
    cursor = mydb.cursor()
    user_id = get_user_id_by_username(mydb, mistake_made_by_username)
    if not user_id:
        print(f"User with username '{mistake_made_by_username}' does not exist.")
        return None

    query = """
    INSERT INTO group9_mistake (text_id, mistake_type, wrong_part, user_id, note, created_at, correct_form)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    try:
        cursor.execute(query, (text_id, mistake_type, wrong_part, user_id, note, date.today(), correct_form))
        mydb.commit()
        print("Mistake saved successfully.")
        return cursor.lastrowid
    except mysql.Error as e:
        print(f"Failed to insert mistake: {e}")
        return None
    finally:
        cursor.close()

# Function to fetch mistakes by text ID
def fetch_mistakes_by_text(mydb, text_id):
    cursor = mydb.cursor(dictionary=True)
    query = "SELECT * FROM group9_mistake WHERE text_id = %s"
    try:
        cursor.execute(query, (text_id,))
        return cursor.fetchall()
    except mysql.Error as e:
        print(f"Failed to fetch mistakes: {e}")
        return None
    finally:
        cursor.close()

def does_mistake_exist(mydb, text_id, mistake_type, username, date=date.today()):
    if get_mistake_by_text_type_date_user(mydb, text_id, mistake_type, username, date) == None:
        return False
    return True

def get_mistake_by_text_type_date_user(mydb, text_id, mistake_type, username, date=date.today()):
    """
    This function fetches a mistake record based on the provided parameters: text ID, mistake type, username of the user, 
    and date. It helps track whether a particular type of mistake has already been logged for a specific text and user.
    """
    cursor = mydb.cursor(dictionary=True)  # Use dictionary=True for better readability of results
    query = """
    SELECT m.*
    FROM group9_mistake m
    INNER JOIN users u ON m.user_id = u.id
    WHERE m.text_id = %s AND m.mistake_type = %s AND m.created_at = %s AND u.username = %s
    """
    try:
        cursor.execute(query, (text_id, mistake_type, date, username))
        result = cursor.fetchone()
        # print(result)
        return result  # Return the mistake record if it exists
    except mysql.Error as e:
        print(f"Failed to fetch mistake: {e}")
        return None
    finally:
        cursor.close()



# Function to delete a text by ID
def delete_text_by_id(mydb, text_id):
    cursor = mydb.cursor()
    query = "DELETE FROM group9_text_optimization WHERE id = %s"
    try:
        cursor.execute(query, (text_id,))
        mydb.commit()
        if cursor.rowcount > 0:
            print(f"Text with ID {text_id} deleted successfully.")
            return True
        else:
            print(f"Text with ID {text_id} does not exist.")
            return False
    except mysql.Error as e:
        print(f"Failed to delete text: {e}")
        return False
    finally:
        cursor.close()

# Function to delete a mistake by ID
def delete_mistake_by_id(mydb, mistake_id):
    cursor = mydb.cursor()
    query = "DELETE FROM group9_mistake WHERE id = %s"
    try:
        cursor.execute(query, (mistake_id,))
        mydb.commit()
        if cursor.rowcount > 0:
            print(f"Mistake with ID {mistake_id} deleted successfully.")
            return True
        else:
            print(f"Mistake with ID {mistake_id} does not exist.")
            return False
    except mysql.Error as e:
        print(f"Failed to delete mistake: {e}")
        return False
    finally:
        cursor.close()



# def get_user_history(db_connection, userID):
#     query = """
#     SELECT mistake_type, note, correct_form,created_at
#     FROM group9_mistake
#     WHERE user_id = %s
#     ORDER BY created_at DESC
#     """
#     cursor = db_connection.cursor()
#     cursor.execute(query, (userID,))
#     results = cursor.fetchall()
#     # print(results)
#     cursor.close()
#     return [{'type': row[0], 'details': row[1], 'correct_form': row[2],'Date:' : row[3]} for row in results]

def get_user_history(db_connection, userID):
    query = """
    SELECT 
        t.input_text,
        m.mistake_type, 
        m.note, 
        m.correct_form, 
        m.created_at
    FROM group9_mistake AS m
    JOIN group9_text_optimization AS t ON m.text_id = t.id
    WHERE m.user_id = %s
    ORDER BY m.created_at DESC
    """
    cursor = db_connection.cursor()
    cursor.execute(query, (userID,))
    results = cursor.fetchall()
    cursor.close()

    return [{
        'type': row[1],
        'details': row[2],
        'correct_form': row[3],
        'Date': row[4],
        'input_text': row[0]
    } for row in results]




from mysql.connector import connect, Error
def get_user_id_by_username(db_connection, username):
    
    query = "SELECT id FROM users WHERE username = %s"
    try:
        cursor = db_connection.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return result[0]  # Return the user ID
        else:
            return None  # Username not found
    except Error as e:
        print(f"Database query error: {e}")
        return None


