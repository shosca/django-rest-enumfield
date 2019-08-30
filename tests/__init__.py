# -*- coding: utf-8 -*-
import django
from django.conf import settings
from django.test import utils


settings.configure()

django.setup()
utils.setup_test_environment()
