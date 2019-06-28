# -*- coding: utf-8 -*-
from rest_framework import fields
from contextlib import suppress


class EnumField(fields.ChoiceField):
    def __init__(
        self, enum_class=None, choices=None, to_choice=lambda x: (x.name, x.value), to_repr=lambda x: x.name, **kwargs
    ):
        self.enum_class = enum_class or choices
        self.to_repr = to_repr
        self.to_choice = to_choice
        kwargs["choices"] = [to_choice(e) for e in self.enum_class]
        kwargs.pop("max_length", None)
        super(EnumField, self).__init__(**kwargs)

    def to_internal_value(self, data):
        with suppress(KeyError, ValueError):
            return self.enum_class[data]
        with suppress(KeyError, ValueError):
            return self.enum_class(data)

        self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        if not value:
            return None

        return self.to_repr(value)
