from django.db import models



class UserTypes(models.IntegerChoices):
    CUSTOMER = 0, 'customer'
    COMPANY = 1, 'company'


class ScoreTypes(models.IntegerChoices):
    BAD = 0, 'bad'
    OK = 1, 'ok'
    GOOD = 2, 'good'


class BoolStates(models.IntegerChoices):
    NO = 0, 'no'
    YES = 1, 'yes'


class ObjectTypes(models.IntegerChoices):
    USER = 0, 'user'
    COMPLAINT = 1, 'complaint'
