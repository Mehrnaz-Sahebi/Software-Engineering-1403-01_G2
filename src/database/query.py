import mysql.connector as mysql

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

def save_user(mydb, name, username, password, email, age):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن کاربر
    add_user_query = """
    INSERT INTO users (name, username, password, email, age)
    VALUES (%s, %s, %s, %s, %s);
    """
    
    try:
        # اجرای دستور و اضافه کردن کاربر
        my_cursor.execute(add_user_query, (name, username, password, email, age))
        mydb.commit() # تایید تغییرات
        print("User saved successfully.")
    except mysql.Error as err:
        print("Failed to insert user:", err)
    finally:
        my_cursor.close()



def save_post(mydb, description, email, state, category, image_address, image_name, image_tags, user_id):
    my_cursor = mydb.cursor()

    # دستور SQL برای اضافه کردن پست
    add_post_query = """
    INSERT INTO posts (description, email, state, category, image_address, image_name, image_tags, user_id)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """
    
    try:
        # اجرای دستور و اضافه کردن پست
        my_cursor.execute(add_post_query, (description, email, state, category, image_address, image_name, image_tags, user_id))
        mydb.commit() # تایید تغییرات
        print("Post saved successfully.")
        return my_cursor.lastrowid
    except mysql.Error as err:
        print("Failed to insert post:", err)
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
    


def get_posts_by_user_id(db_connection, user_id):
    cursor = db_connection.cursor(dictionary=True)  # استفاده از dictionary=True برای بازگرداندن نتایج به صورت دیکشنری
    query = "SELECT * FROM posts WHERE user_id = %s"
    cursor.execute(query, (user_id,))
    posts = cursor.fetchall()  # Fetchall برای دریافت تمام نتایج مطابق با کوئری استفاده می‌شود
    cursor.close()

    return posts


def get_posts_for_user(db_connection, username):
    cursor = db_connection.cursor(dictionary=True)

    # پیدا کردن id کاربر با استفاده از username
    find_user_query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(find_user_query, (username,))
    user_result = cursor.fetchone()

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    if user_result:
        user_id = user_result['id']

        # دریافت تمام پست‌های مربوط به این کاربر
        get_posts_query = "SELECT * FROM posts WHERE user_id = %s"
        cursor.execute(get_posts_query, (user_id,))
        posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list


def search_posts_tag_for_user(db_connection, username, query):
    cursor = db_connection.cursor(dictionary=True)

    # پیدا کردن id کاربر با استفاده از username
    find_user_query = "SELECT id FROM users WHERE username = %s"
    cursor.execute(find_user_query, (username,))
    user_result = cursor.fetchone()

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    if user_result:
        user_id = user_result['id']

        # اصلاح کوئری برای دریافت پست‌هایی که در ستون category حاوی کلمه query هستند
        # و مربوط به کاربر مشخص شده با user_id هستند
        get_posts_query = """
        SELECT * FROM posts
        WHERE user_id = %s AND category LIKE %s
        """
        like_pattern = "%" + query + "%"
        cursor.execute(get_posts_query, (user_id, like_pattern))
        posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list



def search_posts_tag_for_all(db_connection, query):
    cursor = db_connection.cursor(dictionary=True)

    posts_list = []  # ایجاد یک لیست خالی برای نگهداری دیکشنری‌های پست

    # اصلاح کوئری برای دریافت پست‌هایی که در ستون category حاوی کلمه query هستند
    get_posts_query = "SELECT * FROM posts WHERE category LIKE %s"
    like_pattern = "%" + query + "%"
    cursor.execute(get_posts_query, (like_pattern,))
    posts_list = cursor.fetchall()  # این حالا یک لیست از دیکشنری‌ها است

    cursor.close()
    return posts_list

from group9.models import User, Text, Mistake

# Method to create a new User
def create_user(email, full_name, password, phone_number=None):
    user = User.objects.create(
        email=email,
        full_name=full_name,
        password=password,
        phone_number=phone_number
    )
    return user

# Method to fetch a user by email
def fetch_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return user
    except User.DoesNotExist:
        return None

# Method to create a new Text for a User
def create_text(user_id, content):
    user = User.objects.get(id=user_id)
    text = Text.objects.create(user=user, content=content)
    return text

# Method to fetch a Text by ID
def fetch_text_by_id(text_id):
    try:
        text = Text.objects.get(id=text_id)
        return text
    except Text.DoesNotExist:
        return None

# Method to create a new Mistake for a Text
def create_mistake(text_id, mistake_type, statement):
    text = Text.objects.get(id=text_id)
    mistake = Mistake.objects.create(
        text=text,
        mistake_type=mistake_type,
        statement=statement
    )
    return mistake

# Method to fetch all Mistakes for a specific Text
def fetch_mistakes_by_text(text_id):
    mistakes = Mistake.objects.filter(text_id=text_id)
    return mistakes

# Method to delete a user by email
def delete_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        user.delete()
        return True
    except User.DoesNotExist:
        return False

# Method to delete a Text by ID
def delete_text_by_id(text_id):
    try:
        text = Text.objects.get(id=text_id)
        text.delete()
        return True
    except Text.DoesNotExist:
        return False

# Method to delete a Mistake by ID
def delete_mistake_by_id(mistake_id):
    try:
        mistake = Mistake.objects.get(id=mistake_id)
        mistake.delete()
        return True
    except Mistake.DoesNotExist:
        return False
