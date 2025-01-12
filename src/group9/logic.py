from group9.models import *
from hazm import Normalizer
from group9.database.query import *
from django.contrib.auth.models import User



def optimize_text(input: str,
                  user: User,
                  correct_spacing: bool,
                  remove_diacrities: bool,
                  remove_special_chars: bool,
                  decrease_repeated_chars: bool,
                  persian_style: bool,
                  persian_numbers: bool,
                  unicodes_replacement: bool,
                  seperate_mi: bool):
    

    does_text_exist = does_text_exist(input, user.username)
    normalizer = Normalizer()
    completely_normalized_output = normalizer.normalize(input)
    if not does_text_exist:
        save_text(db_connection, user.username, input, completely_normalized_output)

    text_id = get_text_id_by_input_and_date(input, user.username)

    text_before_change = input
    text_after_change = None

    partially_normalized_output = input

    # if correct_spacing:
    #     text_after_change = normalizer.correct_spacing(text_before_change)
    #     if not text_before_change == text_after_change:
