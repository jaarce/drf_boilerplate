#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf_boilerplate.settings")
    os.environ.setdefault("SECRET_KEY", "e^rful55ieh9po!0cr_vp8wp$_*@hxb^rjxe!b4ns@l03pij60")
    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
