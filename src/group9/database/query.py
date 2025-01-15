import mysql.connector as mysql
from datetime import date
from registration.database.secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from registration.database.query import *
import mysql.connector as mysql
from mysql.connector import connect, Error


def save_text(mydb, username, input_text, optimized_text):
    """
    Saves the input and optimized text to the database, linking it to the user by username.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): Database connection object.
    - username (str): Username of the user.
    - input_text (str): Original input text.
    - optimized_text (str): Optimized text after processing.

    Returns:
    - int: ID of the newly inserted record, or None if an error occurs.
    """
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
        return cursor.lastrowid
    except mysql.Error as e:
        print(f"Failed to insert text: {e}")
        return None
    finally:
        cursor.close()


def fetch_text_by_id(mydb, text_id):
    """
    Fetches a text record from the database by its ID.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): Database connection object.
    - text_id (int): ID of the text record to fetch.

    Returns:
    - dict: The text record as a dictionary with column names as keys, or None if an error occurs.
    """
    cursor = mydb.cursor(dictionary=True)
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
    """
    Checks if a given text has been optimized by the user on a particular date.

    This function checks if the provided input text exists in the database for the specified user
    and date, using the `get_text_id_by_input_and_date` function.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - input (str): The input text to check.
    - username (str): The username of the user who submitted the text.
    - date (str, optional): The date to check. Defaults to the current date.

    Returns:
    - bool: True if the text exists, False if not.

    Example:
    - does_text_exist(mydb, 'sample text', 'john_doe')
    """
    if get_text_id_by_input_and_date(mydb, input, username, date) == None:
        return False
    return True


def get_text_id_by_input_and_date(mydb, input_text, username, date=date.today()):
    """
    Retrieves the ID of a text optimization entry based on the input text, username, and creation date.

    This helps check if a user has already optimized the same text on the specified date.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - input_text (str): The input text to search for.
    - username (str): The username of the user who submitted the text.
    - date (str, optional): The date to check. Defaults to the current date.

    Returns:
    - int: The ID of the text record if found, or None if no match is found.
    """
    cursor = mydb.cursor(dictionary=True)
    query = """
    SELECT t.id
    FROM group9_text_optimization t
    INNER JOIN users u ON t.user_id = u.id
    WHERE t.input_text = %s AND u.username = %s AND t.created_at = %s
    """
    try:
        cursor.execute(query, (input_text, username, f"{date} 00:00:00"))
        results = cursor.fetchall()
        if results:
            return results[0]["id"]
        else:
            return None
    except mysql.Error as e:
        print(f"Failed to fetch text ID: {e}")
        return None
    finally:

        cursor.close()


def save_mistake(
    mydb,
    text_id,
    mistake_type,
    wrong_part,
    mistake_made_by_username,
    note,
    correct_form,
):
    """
    Saves a user's mistake in the database related to a specific text optimization.

    This function records details about a mistake made by the user during the optimization process,
    such as the type of mistake, the incorrect part, and the correct form, along with a note.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - text_id (int): The ID of the text optimization entry where the mistake was made.
    - mistake_type (str): The type of the mistake (e.g., "spacing", "diacritic").
    - wrong_part (str): The part of the text where the mistake was identified.
    - mistake_made_by_username (str): The username of the person who made the mistake.
    - note (str): An optional note describing the mistake.
    - correct_form (str): The correct version of the mistaken part.

    Returns:
    - int: The ID of the inserted mistake entry if successful, None if an error occurs.
    """
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
        cursor.execute(
            query,
            (
                text_id,
                mistake_type,
                wrong_part,
                user_id,
                note,
                date.today(),
                correct_form,
            ),
        )
        mydb.commit()
        print("Mistake saved successfully.")
        return cursor.lastrowid
    except mysql.Error as e:
        print(f"Failed to insert mistake: {e}")
        return None
    finally:
        cursor.close()


def fetch_mistakes_by_text(mydb, text_id):
    """
    Fetches all mistakes associated with a specific text optimization entry.

    This function retrieves all recorded mistakes linked to a particular text optimization entry
    using the text ID. It returns a list of mistakes made for that text, including details such as
    the mistake type, incorrect part, and correction.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - text_id (int): The ID of the text optimization entry for which mistakes are being fetched.

    Returns:
    - list: A list of dictionaries, each containing details of a mistake if successful.
    - None: If the operation fails or no mistakes are found.
    """
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
    """
    Checks if a mistake of a particular type has been logged for a specific text, user, and date.

    This function helps determine whether a particular type of mistake has already been recorded
    for a specific user on a specific text for a given date.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - text_id (int): The ID of the text optimization entry.
    - mistake_type (str): The type of mistake being checked.
    - username (str): The username of the user who made the mistake.
    - date (str): The date when the mistake was made (default is today's date).

    Returns:
    - bool: True if the mistake exists, False if not.
    """
    if (
        get_mistake_by_text_type_date_user(mydb, text_id, mistake_type, username, date)
        == None
    ):
        return False
    return True


def get_mistake_by_text_type_date_user(
    mydb, text_id, mistake_type, username, date=date.today()
):
    """
    Fetches a mistake record for a specific text, mistake type, user, and date.

    This function is used to check if a particular mistake has already been logged for a
    specific text, mistake type, user, and date. It helps prevent duplicate mistake records
    from being saved for the same mistake.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - text_id (int): The ID of the text optimization entry.
    - mistake_type (str): The type of mistake being checked.
    - username (str): The username of the user who made the mistake.
    - date (str): The date when the mistake was made (default is today's date).

    Returns:
    - dict: A dictionary containing the mistake details if found.
    - None: If no matching mistake is found or an error occurs.
    """
    cursor = mydb.cursor(dictionary=True)
    query = """
    SELECT m.*
    FROM group9_mistake m
    INNER JOIN users u ON m.user_id = u.id
    WHERE m.text_id = %s AND m.mistake_type = %s AND m.created_at = %s AND u.username = %s
    """
    try:
        cursor.execute(query, (text_id, mistake_type, date, username))
        result = cursor.fetchone()
        return result
    except mysql.Error as e:
        print(f"Failed to fetch mistake: {e}")
        return None
    finally:
        cursor.close()


def delete_text_by_id(mydb, text_id):
    """
    Deletes a text optimization entry by its ID from the 'group9_text_optimization' table.

    This function removes a specific text optimization entry from the database using its ID.
    If the text entry does not exist, it returns False, otherwise it commits the deletion and returns True.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - text_id (int): The ID of the text optimization entry to be deleted.

    Returns:
    - bool: True if the text entry was deleted successfully, False if it was not found or deletion failed.
    """
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


def delete_mistake_by_id(mydb, mistake_id):
    """
    Deletes a mistake entry by its ID from the 'group9_mistake' table.

    This function removes a specific mistake entry from the database using its ID.
    If the mistake entry does not exist, it returns False, otherwise it commits the deletion and returns True.

    Parameters:
    - mydb (mysql.connector.connection.MySQLConnection): The database connection object.
    - mistake_id (int): The ID of the mistake entry to be deleted.

    Returns:
    - bool: True if the mistake entry was deleted successfully, False if it was not found or deletion failed.

    Example:
    - delete_mistake_by_id(mydb, 1)
    """
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


def get_user_history(db_connection, userID):
    """
    Fetches the history of mistakes made by a user, including details of the optimized text and mistakes.

    This function retrieves all the mistakes a user has made based on their user ID. It fetches the input text,
    mistake type, notes, the correct form, and the date of each mistake from the database.

    Parameters:
    - db_connection (mysql.connector.connection.MySQLConnection): The database connection object.
    - userID (int): The ID of the user whose history is to be fetched.

    Returns:
    - list of dicts: A list of dictionaries, where each dictionary contains:
        - 'type' (str): The type of mistake made.
        - 'details' (str): Additional notes on the mistake.
        - 'correct_form' (str): The corrected version of the mistake.
        - 'Date' (str): The date the mistake was made.
        - 'input_text' (str): The input text where the mistake occurred.
    """
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

    return [
        {
            "type": row[1],
            "details": row[2],
            "correct_form": row[3],
            "Date": row[4],
            "input_text": row[0],
        }
        for row in results
    ]


def get_user_id_by_username(db_connection, username):
    """
    Fetches the user ID associated with a given username from the database.

    This function retrieves the ID of the user based on the provided username.

    Parameters:
    - db_connection (mysql.connector.connection.MySQLConnection): The database connection object.
    - username (str): The username of the user whose ID is to be fetched.

    Returns:
    - int or None: The user ID if the username exists, or None if the username is not found.
    """

    query = "SELECT id FROM users WHERE username = %s"
    try:
        cursor = db_connection.cursor()
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            return None
    except Error as e:
        print(f"Database query error: {e}")
        return None
