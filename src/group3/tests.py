# tests.py
import unittest
from django.test import TestCase, Client
from django.urls import reverse
from .models import TextOptimization
from .logic import process_input, fix_delimiters
from .parse import find_suggestions
from .serializer import SuggestionSerializer, TextSuggestionSerializer
from .database.query import save_suggestion, create_db_connection
from .database import secret
import mysql.connector

#Logic
class LogicTestCase(TestCase):

    def test_process_input(self):
        input_text = "این ( متن تست ) است"
        output_text = process_input(input_text)
        self.assertNotEqual(input_text, output_text)
        self.assertIn("", output_text)

    def test_fix_delimiters(self):
        input_text = "سلام)"
        result = fix_delimiters(input_text)
        self.assertEqual(result, "سلام")
        input_text = "(سلام خوبی))"
        result = fix_delimiters(input_text)
        self.assertEqual(result, "(سلام خوبی)")

    def test_process_input_removes_extra_spaces(self):
        input_text = "این   متن   تست   است"
        output_text = process_input(input_text)
        self.assertEqual(output_text, "این متن تست است")

    def test_process_input_handles_empty_string(self):
        input_text = ""
        output_text = process_input(input_text)
        self.assertEqual(output_text, "")

    def test_process_input_handles_no_parentheses(self):
        input_text = "این متن بدون پرانتز است"
        output_text = process_input(input_text)
        self.assertEqual(output_text, input_text)


    def test_fix_delimiters_balances_opening_parentheses(self):
        input_text = "(سلام"
        result = fix_delimiters(input_text)
        self.assertEqual(result, "(سلام)")

    def test_fix_delimiters_removes_extra_closing_parentheses(self):
        input_text = "سلام)))"
        result = fix_delimiters(input_text)
        self.assertEqual(result, "سلام")

    def test_fix_delimiters_handles_nested_parentheses(self):
        input_text = "((سلام) خوبی)"
        result = fix_delimiters(input_text)
        self.assertEqual(result, "((سلام) خوبی)")

    def test_fix_delimiters_handles_empty_string(self):
        input_text = ""
        result = fix_delimiters(input_text)
        self.assertEqual(result, "")

#Parse
class ParseTestCase(TestCase):
    def test_find_suggestions_no_change(self):
        input_text = "این یک تست است."
        output_text = "این یک تست است."
        suggestions = find_suggestions(input_text, output_text)
        self.assertEqual(len(suggestions), 0)

    def test_find_suggestions_with_change(self):
        input_text = "این    است"
        output_text = "این است"
        suggestions = find_suggestions(input_text, output_text)
        self.assertTrue(len(suggestions) > 0)
        first_suggestion = suggestions[0]
        self.assertIn("start", first_suggestion)
        self.assertIn("end", first_suggestion)
        self.assertIn("suggest", first_suggestion)
        
    def test_find_suggestions_with_replacement(self):
        input_text = "این یک مثال است."
        output_text = "این یک نمونه است."
        suggestions = find_suggestions(input_text, output_text)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]['suggest'], "نمونه")

    def test_find_suggestions_with_addition(self):
        input_text = "تست خوب"
        output_text = "تست عالی"
        suggestions = find_suggestions(input_text, output_text)
        self.assertEqual(len(suggestions), 1)
        self.assertEqual(suggestions[0]['suggest'], "عالی")

    def test_find_suggestions_with_removal(self):
        input_text = "این یک متن طولانی است."
        output_text = "این یک متن است."
        suggestions = find_suggestions(input_text, output_text)
        self.assertEqual(suggestions[0]['suggest'], " ")

    def test_find_suggestions_with_multiple_changes(self):
        input_text = "این متن    با   فاصله‌های اضافی   است."
        output_text = "این متن با فاصله‌های اضافی است."
        suggestions = find_suggestions(input_text, output_text)
        self.assertEqual(len(suggestions), 3)


#Serilizer
class SerializerTestCase(TestCase):
    def test_suggestion_serializer_valid(self):
        data = {"start": 3, "end": 6, "suggest": " "}
        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["start"], 3)
        self.assertEqual(serializer.validated_data["end"], 6)
        self.assertEqual(serializer.validated_data["suggest"], " ")

    def test_suggestion_serializer_invalid_type(self):
        data = {"start": "abc", "end": 6, "suggest": "test"}
        serializer = SuggestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("start", serializer.errors)

    def test_text_suggestion_serializer_valid(self):
        data = {"text": "این یک متن تست است."}
        serializer = TextSuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["text"], "این یک متن تست است.")

    def test_text_suggestion_serializer_no_text(self):
        data = {}
        serializer = TextSuggestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("text", serializer.errors)

    def test_suggestion_serializer_valid_complete(self):
        data = {"start": 0, "end": 10, "suggest": "test suggestion"}
        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["start"], 0)
        self.assertEqual(serializer.validated_data["end"], 10)
        self.assertEqual(serializer.validated_data["suggest"], "test suggestion")

    def test_suggestion_serializer_missing_suggest(self):
        data = {"start": 1, "end": 5}
        serializer = SuggestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("suggest", serializer.errors)

    def test_suggestion_serializer_invalid_range(self):
        data = {"start": 10, "end": 5, "suggest": "test"}
        serializer = SuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["start"], 10)
        self.assertEqual(serializer.validated_data["end"], 5)


    def test_text_suggestion_serializer_extra_spaces(self):
        data = {"text": "   این یک متن تست است.   "}
        serializer = TextSuggestionSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data["text"], "   این یک متن تست است.   ")


    def test_text_suggestion_serializer_exceeds_max_length(self):
        data = {"text": "a" * 300}
        serializer = TextSuggestionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("text", serializer.errors)

#Model
class ModelTestCase(TestCase):
    def test_text_optimization_creation(self):
        obj = TextOptimization.objects.create(
            input_text="ورودی تست",
            optimized_text="خروجی تست"
        )
        self.assertIsNotNone(obj.id)
        self.assertEqual(obj.input_text, "ورودی تست")
        self.assertEqual(obj.optimized_text, "خروجی تست")

    def test_text_optimization_update(self):
        obj = TextOptimization.objects.create(
            input_text="متن اولیه",
            optimized_text="متن بهینه شده"
        )
        obj.optimized_text = "متن جدید بهینه شده"
        obj.save()

        updated_obj = TextOptimization.objects.get(id=obj.id)
        self.assertEqual(updated_obj.optimized_text, "متن جدید بهینه شده")

    def test_text_optimization_deletion(self):
        obj = TextOptimization.objects.create(
            input_text="متن تستی",
            optimized_text="متن تستی بهینه"
        )
        obj_id = obj.id

        obj.delete()

        with self.assertRaises(TextOptimization.DoesNotExist):
            TextOptimization.objects.get(id=obj_id)
#Database
class DatabaseTestCase(TestCase):
    def setUp(self):
        self.connection = create_db_connection(
            secret.DB_HOST,
            secret.DB_PORT,
            secret.DB_USER,
            secret.DB_PASSWORD,
            secret.DB_NAME
        )

    def tearDown(self):
        if self.connection.is_connected():
            self.connection.close()

    def test_save_suggestion(self):
        try:
            save_suggestion(self.connection, 1, 2, " ")
        except mysql.connector.Error as e:
            self.fail(f"save_suggestion raised an exception: {e}")
        except Exception as e:
            self.fail(f"Unexpected exception: {e}")
        def test_fetch_suggestions(self):
            try:
                suggestions = fetch_suggestions(self.connection)
                self.assertIsInstance(suggestions, list)
            except mysql.connector.Error as e:
                self.fail(f"fetch_suggestions raised an exception: {e}")
            except Exception as e:
                self.fail(f"Unexpected exception: {e}")

    def test_connection_is_open(self):
        self.assertTrue(self.connection.is_connected())
