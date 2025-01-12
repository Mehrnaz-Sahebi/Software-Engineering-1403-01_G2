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
    SEPERATE_MI: "بن فعل‌های مضارع باید از می و نمی با یک نیم‌فاصله جدا شود."
}


def find_out_mistakes(normalizing_function,
                      text_before_change: str,
                      text_after_change: str, 
                      text_id: int,
                      username: str,
                      mistake_type: str):
    
    text_after_change = normalizing_function(text_before_change)
    if not text_before_change == text_after_change:
        does_current_mistake_exist = does_mistake_exist(db_connection, text_id, mistake_type, username)
        if not does_current_mistake_exist:
            save_mistake(db_connection, text_id, mistake_type, None, username, notes[mistake_type], text_after_change)



def optimize_text(input: str,
                  user: User,
                  correct_spacing: bool,
                  remove_diacrities: bool,
                  remove_special_chars: bool,
                  decrease_repeated_chars: bool,
                  persian_style: bool,
                  persian_number: bool,
                  unicodes_replacement: bool,
                  seperate_mi: bool) -> str:
    
    # checks if the current input text has been processed before (the exact same text in the same day by the same user)
    does_input_exist = does_text_exist(db_connection, input, user.username)

    normalizer = Normalizer()

    # completely normalizes the input text and if it doesn't already exists, saves the text in the database
    completely_normalized_output = normalizer.normalize(input)
    if not does_text_exist:
        save_text(db_connection, user.username, input, completely_normalized_output)
    
    text_id = get_text_id_by_input_and_date(input, user.username)

    # declaring two variables for saving the mistakes in each step
    text_before_change = input
    text_after_change = None

    # declaring a variable to store the text, on which the requested fixes will be applied
    partially_normalized_output = input

    if correct_spacing:
        find_out_mistakes(Normalizer.correct_spacing, text_before_change, text_after_change, text_id, user.username, CORRECT_SPACING)
        partially_normalized_output = normalizer.correct_spacing(partially_normalized_output)

    if remove_diacrities:
        find_out_mistakes(Normalizer.remove_diacritics, text_before_change, text_after_change, text_id, user.username, REMOVE_DIACRITIES)
        partially_normalized_output = normalizer.remove_diacritics(partially_normalized_output)

    if remove_special_chars:
        find_out_mistakes(Normalizer.remove_specials_chars, text_before_change, text_after_change, text_id, user.username, REMOVE_SPECIAL_CHARS)
        partially_normalized_output = normalizer.remove_specials_chars(partially_normalized_output)

    if decrease_repeated_chars:
        find_out_mistakes(Normalizer.decrease_repeated_chars, text_before_change, text_after_change, text_id, user.username, DECREASE_REPEATED_CHARS)
        partially_normalized_output = normalizer.decrease_repeated_chars(partially_normalized_output)

    if persian_style:
        find_out_mistakes(Normalizer.persian_style, text_before_change, text_after_change, text_id, user.username, PERSIAN_STYLE)
        partially_normalized_output = normalizer.persian_style(partially_normalized_output)

    if persian_number:
        find_out_mistakes(Normalizer.persian_number, text_before_change, text_after_change, text_id, user.username, PERSIAN_NUMBER)
        partially_normalized_output = normalizer.persian_number(partially_normalized_output)

    if unicodes_replacement:
        find_out_mistakes(Normalizer.unicodes_replacement, text_before_change, text_after_change, text_id, user.username, UNICODES_REPLACEMENT)
        partially_normalized_output = normalizer.unicodes_replacement(partially_normalized_output)

    if seperate_mi:
        find_out_mistakes(Normalizer.seperate_mi, text_before_change, text_after_change, text_id, user.username, SEPERATE_MI)
        partially_normalized_output = normalizer.seperate_mi(partially_normalized_output)

    return partially_normalized_output