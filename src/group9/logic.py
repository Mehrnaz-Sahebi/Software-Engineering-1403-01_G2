from group9.models import *
from hazm import Normalizer
from group9.database.query import *
from django.contrib.auth.models import User

CORRECT_SPACING = "فاصله‌گذاری"
REMOVE_DIACRITIES = "اعراب"
REMOVE_SPECIAL_CHARS = "نشانه‌های ویژه"
DECREASE_REPEATED_CHARS = "تکرار حروف"
PERSIAN_STYLE = "جایگزینی با حروف و نشانه‌های فارسی"
PERSIAN_NUMBER = "اعداد فارسی"
UNICODES_REPLACEMENT = "یونیکدها"
SEPERATE_MI = "جداسازی می و نمی"

notes = {
    CORRECT_SPACING: "حواست باشد کجاها فاصله می‌گذاری!",
    REMOVE_DIACRITIES: "متن فارسی اعراب ندارد.",
    REMOVE_SPECIAL_CHARS: "نیازی به استفاده از این نشانه‌ها نبود.",
    DECREASE_REPEATED_CHARS: "‌بعضی حروف بیش‌تر از دوبار پشت سر هم استفاده شده‌اند.",
    PERSIAN_STYLE: "خیلی از نشانه‌ها معادل فارسی دارند.",
    PERSIAN_NUMBER: "اعداد باید به فارسی باشند.",
    UNICODES_REPLACEMENT: "بهتر است به جای کاراکترهای خاص از کلمه‌ای معادل آن‌ها استفاده شود.",
    SEPERATE_MI: "بن فعل‌های مضارع باید از می و نمی با یک نیم‌فاصله جدا شود.",
}


def find_out_mistakes(
    normalizing_function: callable,
    text_before_change: str,
    text_after_change: str,
    text_id: int,
    username: str,
    mistake_type: str,
    db_connection,
):
    """
    This function checks whether applying a normalizing function has changed the text.
    If there is a modification in the text, the mistake is logged in the database for further analysis.

    The primary goal of this function is to monitor if the text undergoes a transformation that corresponds to a mistake.
    If a mistake occurs, it is captured and stored in the database.

    The normalizing function is applied to the provided text before the change, and the result is compared with the original.
    If the text has been modified, the mistake is saved in the database.

    Parameters:
    - normalizing_function: The normalization function that applies a specific transformation to the text.
    - text_before_change: The original version of the input text.
    - text_after_change: The text after applying the normalizing function. (Initially set to None)
    - text_id: A unique identifier for the text in the database.
    - username: The username of the user making the changes.
    - mistake_type: The type of mistake that was potentially corrected by the normalization.
    - db_connection: The connection object for accessing the database.

    Returns:
    - None: This function does not return any values but interacts directly with the database to log mistakes.
    """

    text_after_change = normalizing_function(text_before_change)
    if not text_before_change == text_after_change:
        does_current_mistake_exist = does_mistake_exist(
            db_connection, text_id, mistake_type, username
        )
        print(does_current_mistake_exist)
        if not does_current_mistake_exist:
            save_mistake(
                db_connection,
                text_id,
                mistake_type,
                "-",
                username,
                notes[mistake_type],
                text_after_change,
            )


def optimize_text(
    input: str,
    user: User,
    correct_spacing: bool,
    remove_diacrities: bool,
    remove_special_chars: bool,
    decrease_repeated_chars: bool,
    persian_style: bool,
    persian_number: bool,
    unicodes_replacement: bool,
    seperate_mi: bool,
    db_connection,
) -> str:
    """
    This function applies a series of text normalizations based on the user's preferences and saves the mistakes.

    The process involves running various normalization functions such as correcting spacing, removing diacritics,
    handling repeated characters, converting numbers, and more. Each normalization is applied individually based on user selections.

    The function also tracks and logs any mistakes made during the normalization process. A mistake is logged in the database
    if a normalization is applied and the text changes as a result.

    Additionally, if the same text has been processed previously by the same user on the same day, the system will prevent
    redundant normalization actions by checking for text existence before performing operations.

    After each normalization step, the modified text is saved in the database, and the final optimized output is returned.

    Parameters:
    - input: The original text provided by the user that needs to be normalized.
    - user: The current authenticated user whose preferences and history are used in the process.
    - correct_spacing: A boolean flag indicating whether spacing corrections should be applied.
    - remove_diacrities: A boolean flag indicating whether diacritics should be removed.
    - remove_special_chars: A boolean flag indicating whether special characters should be removed.
    - decrease_repeated_chars: A boolean flag indicating whether repeated characters should be reduced.
    - persian_style: A boolean flag indicating whether Persian-style formatting should be applied.
    - persian_number: A boolean flag indicating whether Persian numbers should replace Arabic numerals.
    - unicodes_replacement: A boolean flag indicating whether Unicode characters should be replaced with corresponding text.
    - seperate_mi: A boolean flag indicating whether "می" and "نمی" should be separated with a half-space.
    - db_connection: The connection object used to interact with the database.

    Returns:
    - partially_normalized_output: The fully normalized version of the input text after applying all selected normalizations.
    """

    # checks if the current input text has been processed before (the exact same text in the same day by the same user)
    does_input_exist = does_text_exist(db_connection, input, user.username)
    print(does_input_exist)

    normalizer = Normalizer()
    # completely normalizes the input text and if it doesn't already exists, saves the text in the database
    completely_normalized_output = normalizer.normalize(input)
    if not does_input_exist:
        save_text(db_connection, user.username, input, completely_normalized_output)

    text_id = get_text_id_by_input_and_date(db_connection, input, user.username)

    # declaring two variables for saving the mistakes in each step
    text_before_change = input
    text_after_change = None

    # declaring a variable to store the text, on which the requested fixes will be applied
    partially_normalized_output = input

    if correct_spacing:
        find_out_mistakes(
            normalizer.correct_spacing,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            CORRECT_SPACING,
            db_connection,
        )
        partially_normalized_output = normalizer.correct_spacing(
            partially_normalized_output
        )

    if remove_diacrities:
        find_out_mistakes(
            normalizer.remove_diacritics,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            REMOVE_DIACRITIES,
            db_connection,
        )
        partially_normalized_output = normalizer.remove_diacritics(
            partially_normalized_output
        )

    if remove_special_chars:
        find_out_mistakes(
            normalizer.remove_specials_chars,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            REMOVE_SPECIAL_CHARS,
            db_connection,
        )
        partially_normalized_output = normalizer.remove_specials_chars(
            partially_normalized_output
        )

    if decrease_repeated_chars:
        find_out_mistakes(
            normalizer.decrease_repeated_chars,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            DECREASE_REPEATED_CHARS,
            db_connection,
        )
        partially_normalized_output = normalizer.decrease_repeated_chars(
            partially_normalized_output
        )

    if persian_style:
        find_out_mistakes(
            normalizer.persian_style,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            PERSIAN_STYLE,
            db_connection,
        )
        partially_normalized_output = normalizer.persian_style(
            partially_normalized_output
        )

    if persian_number:
        find_out_mistakes(
            normalizer.persian_number,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            PERSIAN_NUMBER,
            db_connection,
        )
        partially_normalized_output = normalizer.persian_number(
            partially_normalized_output
        )

    if unicodes_replacement:
        find_out_mistakes(
            normalizer.unicodes_replacement,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            UNICODES_REPLACEMENT,
            db_connection,
        )
        partially_normalized_output = normalizer.unicodes_replacement(
            partially_normalized_output
        )

    if seperate_mi:
        find_out_mistakes(
            normalizer.seperate_mi,
            text_before_change,
            text_after_change,
            text_id,
            user.username,
            SEPERATE_MI,
            db_connection,
        )
        partially_normalized_output = normalizer.seperate_mi(
            partially_normalized_output
        )

    return partially_normalized_output


def fetch_user_history(user, db_connection):
    """
    This function retrieves the user's history of previously made mistakes from the database.

    It uses the user's username to fetch their unique user ID from the database.
    Once the user ID is retrieved, the function queries the database for the user's history of mistakes and corrections.

    This history is then returned to be displayed on the user’s history page, showing all previous mistakes and their corresponding corrections.

    Parameters:
    - user: The current authenticated user whose history is to be fetched.
    - db_connection: The database connection object used for interacting with the database.

    Returns:
    - A list of the user's history, which includes all the mistakes and the corresponding corrections.
    """
    print(user)
    userID = get_user_id_by_username(db_connection, user)
    print(userID)
    return get_user_history(db_connection, userID)
