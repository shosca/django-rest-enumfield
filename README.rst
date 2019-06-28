Django REST EnumField
=====================

|Build Status| |PyPI version| |Coveralls Status| |Black|

**EnumField that uses python enums for Django REST Framework**

Installation
============

::

   pip install django-rest-enumfield


Usage
=====

Use it as if its a ``ChoiceField``:

.. code:: python

   import enum
   from rest_enumfield import EnumField

   class Color(enum.Enum):
      RED = "red"
      GREEN = "green"
      BLUE = "blue"

   class SomeSerializer(Serializer):

      color = EnumField(choices=Color)


Additionally you can override choice name and value generation by providing ``to_choice`` or ``to_repr`` arguments:

.. code:: python

   class SomeSerializer(Serializer):

      color = EnumField(choices=Color, to_choice=lambda x: (x.value, x.name), to_repr=lambda x: x.value)

This will cause the enum's value instead of the name to be represented.

Thats it.

.. |Build Status| image:: https://travis-ci.com/shosca/django-rest-enumfield.svg?branch=master
   :target: https://travis-ci.com/shosca/django-rest-enumfield
.. |PyPI version| image:: https://badge.fury.io/py/django-rest-enumfield.svg
   :target: https://badge.fury.io/py/django-rest-enumfield
.. |Coveralls Status| image:: https://coveralls.io/repos/github/shosca/django-rest-enumfield/badge.svg?branch=master
   :target: https://coveralls.io/github/shosca/django-rest-enumfield?branch=master
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
