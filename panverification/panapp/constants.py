#!/usr/bin/env python
"""
All Constants here
"""


NAME_INVALID = 1
DOB_INVALID = 2
PAN_INVALID = 3
IMG_INVALID = 4
IMG_FORGED = 5

INVALID_CHOICES = (
	(NAME_INVALID, "Name Invalid"),
	(DOB_INVALID, "DOB Invalid"),
	(PAN_INVALID, "PAN Invalid"),
	(IMG_INVALID, "IMG Invalid"),
	(IMG_FORGED, "IMG Forged"),
)

NAME = 1
DOB = 2
PAN = 3
IMG = 4

FEEDBACK_CHOICES = (
	(NAME, "Name Feedback"),
	(DOB, "DOB Feedback"),
	(PAN, "PAN Feedback"),
	(IMG, "IMG Feedback")
)
