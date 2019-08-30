# -*- coding: utf-8 -*-
from rest_framework import fields


class EnumField(fields.ChoiceField):
    def __init__(self, choices=None, to_choice=lambda x: (x.name, x.value), to_repr=lambda x: x.name, **kwargs):
        self.enum_class = choices
        self.to_repr = to_repr
        self.to_choice = to_choice
        kwargs["choices"] = [to_choice(e) for e in self.enum_class]
        kwargs.pop("max_length", None)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        try:
            return self.enum_class[data]
        except (KeyError, ValueError):
            pass

        try:
            return self.enum_class(data)
        except (KeyError, ValueError):
            pass

        self.fail("invalid_choice", input=data)

    def to_representation(self, value):
        if not value:
            return None

        return self.to_repr(value)
