# -*- coding: utf-8 -*-
from enum import Enum

from django.test import SimpleTestCase

from rest_framework.exceptions import ValidationError

from rest_enumfield import EnumField


class SomeEnum(Enum):
    test1 = 1
    test2 = 2


class TestEnumField(SimpleTestCase):
    def test_choices(self):

        field = EnumField(choices=SomeEnum)

        self.assertDictEqual(field.choices, {"test1": 1, "test2": 2})

        field = EnumField(choices=SomeEnum)

        self.assertDictEqual(field.choices, {"test1": 1, "test2": 2})

    def test_to_internal_value_works(self):

        field = EnumField(choices=SomeEnum)

        self.assertEqual(field.to_internal_value(2), SomeEnum.test2)
        self.assertEqual(field.to_internal_value("test2"), SomeEnum.test2)

        field = EnumField(choices=SomeEnum)

        self.assertEqual(field.to_internal_value(2), SomeEnum.test2)
        self.assertEqual(field.to_internal_value("test2"), SomeEnum.test2)

    def test_to_internal_value_validates(self):

        field = EnumField(choices=SomeEnum)

        with self.assertRaises(ValidationError):
            field.to_internal_value("test3")

        with self.assertRaises(ValidationError):
            field.to_internal_value(3)

        field = EnumField(choices=SomeEnum)

        with self.assertRaises(ValidationError):
            field.to_internal_value("test3")

        with self.assertRaises(ValidationError):
            field.to_internal_value(3)

    def test_to_representation_works(self):

        field = EnumField(choices=SomeEnum)

        self.assertEqual(field.to_representation(SomeEnum.test1), "test1")

    def test_to_representation_handles_none(self):

        field = EnumField(choices=SomeEnum)

        value = field.to_representation(None)

        self.assertIsNone(value)
