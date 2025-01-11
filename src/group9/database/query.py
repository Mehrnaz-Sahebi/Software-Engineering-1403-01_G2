import mysql.connector as mysql
from group9.models import CustomUser, TextOptimizer, Mistake

# تعریف تابع برای ایجاد اتصال به دیتابیس
def create_db_connection(DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME):
    try:
        mydb = mysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Connection to MySQL DB successful")
    except mysql.connector.Error as e:
        print(f"The error '{e}' occurred")
    return mydb



def create_table(mydb, create_table_query):
    cursor = mydb.cursor()
    try:
        cursor.execute(create_table_query)
        mydb.commit()
        print("Table created successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()



def drop_table(mydb, table_name):
    cursor = mydb.cursor()
    try:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        mydb.commit()
        print(f"Table {table_name} dropped successfully")
    except Exception as e:
        print(f"The error '{e}' occurred")
    finally:
        cursor.close()



def fetch_row_by_PRIMARY_KEY(mydb, table_name, id):
    cursor = mydb.cursor()
    try:
        query = f"SELECT * FROM {table_name} WHERE id = %s"
        cursor.execute(query, (id,))
        
        result = cursor.fetchone()
        
        if result:
            return result
        else:
            print("No row found for the given ID.")
            return None
    except Exception as e:
        print(f"The error '{e}' occurred")
        return None
    finally:
        cursor.close()



import mysql.connector as mysql

def save_user(mydb, username, password, email, first_name, last_name, phone_number):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن کاربر
    add_user_query = """
    INSERT INTO users (username, password, email, first_name, last_name, phone_number)
    VALUES (%s, %s, %s, %s, %s, %s);
    """
    
    try:
        # اجرای دستور و اضافه کردن کاربر
        my_cursor.execute(add_user_query, (username, password, email, first_name, last_name, phone_number))
        mydb.commit() # تایید تغییرات
        print("User saved successfully.")
    except mysql.Error as err:
        print("Failed to insert user:", err)
    finally:
        my_cursor.close()


def get_user_id_by_username(db_connection, username):
    cursor = db_connection.cursor()
    query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()  # Fetchone برای دریافت نتیجه اول کوئری استفاده می‌شود
    cursor.close()

    if result:
        return result[0]  # بازگرداندن id کاربر
    else:
        return None  # اگر کاربری با این username وجود نداشته باشد
    
# Method to create a new TextOptimizer for a User
def create_text(username, input_text, optimized_text):
    try:
        user = CustomUser.objects.get(username=username)
        text = TextOptimizer.objects.create(
            user=user,
            input_text=input_text,
            optimized_text=optimized_text
        )
        return text
    except CustomUser.DoesNotExist:
        return None

# Method to fetch a TextOptimizer by ID
def fetch_text_by_id(text_id):
    try:
        text = TextOptimizer.objects.get(id=text_id)
        return text
    except TextOptimizer.DoesNotExist:
        return None

# Method to create a new Mistake for a TextOptimizer
def create_mistake(text_id, mistake_type, wrong_part, mistake_made_by_username, note):
    try:
        text = TextOptimizer.objects.get(id=text_id)
        mistake_made_by = CustomUser.objects.get(username=mistake_made_by_username)
        mistake = Mistake.objects.create(
            text=text,
            mistake_type=mistake_type,
            wrong_part=wrong_part,
            mistake_made_by=mistake_made_by,
            note=note
        )
        return mistake
    except (TextOptimizer.DoesNotExist, CustomUser.DoesNotExist):
        return None


# Method to fetch all Mistakes for a specific TextOptimizer
def fetch_mistakes_by_text(text_id):
    mistakes = Mistake.objects.filter(text_id=text_id)
    return mistakes

# Method to delete a user by username
def delete_user_by_username(username):
    try:
        user = CustomUser.objects.get(username=username)
        user.delete()
        return True
    except CustomUser.DoesNotExist:
        return False

# Method to delete a TextOptimizer by ID
def delete_text_by_id(text_id):
    try:
        text = TextOptimizer.objects.get(id=text_id)
        text.delete()
        return True
    except TextOptimizer.DoesNotExist:
        return False

# Method to delete a Mistake by ID
def delete_mistake_by_id(mistake_id):
    try:
        mistake = Mistake.objects.get(id=mistake_id)
        mistake.delete()
        return True
    except Mistake.DoesNotExist:
        return False
