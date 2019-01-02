import uuid, enum
from django.db import models

# Other Django Applications
from serviceaccounts.models import Member as ACCOUNT
from healthstandards.models import ExaminationStandard as EXAMINATIONSTANDARD


# We decided to use a model(table) instead of having choices for one attribute of the model in order to have more dynamic application
# not use yet
class FormGenderChoice(enum.Enum):   # A subclass of Enum 
    M = "Male"
    F = "Female"
    B = "Both"
    G = "General"


class Examination(models.Model):
    # 'user_created' Hint!! 'user_created' Must not be defined One_to_One because " “reverse” side of the relation will directly return a single object. "
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    gender = models.CharField(max_length=15,
        choices=[(tag, tag.value) for tag in FormGenderChoice]  # Choices is a list of Tuple
    )
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    user_created = models.ForeignKey(ACCOUNT, related_name='user_created_examinations', on_delete=models.PROTECT) 


class ExaminationField(models.Model):
    name = models.CharField(max_length=127)
    examination = models.ForeignKey(Examination, db_index=True, related_name='examination_field', on_delete=models.PROTECT)

# Middle Class between Examination-heathrecords and \\
# ExaminationStandard in health standards for Examination Models
class StandardExamfieldMapping(models.Model): 
    # 'examination_field' Hint!! Must not define many_to_many field relation!! because: they actually have many_to_one relation and defining middle class is just because we want these both classes be seperated logically
    examination_field = models.OneToOneField(ExaminationField, db_index=True, related_name='examinationfield_standard', on_delete=models.PROTECT)
    standard = models.ForeignKey(EXAMINATIONSTANDARD, related_name='standard_examination_mapping', on_delete=models.PROTECT)

class ExaminationRecord(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(ACCOUNT, related_name='user_examination_records', on_delete=models.PROTECT)
    examination = models.ForeignKey(Examination, related_name='examination_records', on_delete=models.PROTECT)


class ExaminationRecordField(models.Model):
    # 'description' Hint!! Adding description to the existing or nonexisting record field if it is required
    examination_record = models.ForeignKey(ExaminationRecord, related_name='examination_record_results', on_delete=models.PROTECT)
    examination_field = models.ForeignKey(ExaminationField, related_name='examination_field_results', on_delete=models.PROTECT)
    value = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=500, blank=True, null=True) 


from django.contrib.postgres.fields import FloatRangeField, ArrayField
from healthstandards.models import TestStandard as TESTSTANDARD


# We decided to use a model(table) instead of having choices for one attribute of the model in order to have more dynamic application
# from enum import Enum
# class TestFieldTypeChoice(Enum):   # A subclass of Enum
#     INT = "Integer"
#     STR = "String"
#     BOOL = "Boolean"
#     FLO = "Float"

class Test(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    name = models.CharField(max_length=127)
    gender = models.CharField(max_length=15,
        choices=[(tag, tag.value) for tag in FormGenderChoice]  # Choices is a list of Tuple
    )

    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    user_created = models.ForeignKey(ACCOUNT, related_name='user_created_tests', on_delete=models.PROTECT)


class TestFieldTypeChoice(models.Model):
    name = models.CharField(max_length=63)
    index = index = models.IntegerField(default=0, blank=True, null=True)


class TestField(models.Model):
    name = models.CharField(max_length=127)
    test = models.ForeignKey(Test, db_index=True, related_name='test_field', on_delete=models.PROTECT)
    # We decided not to use choices for attribute and instead having foreign key to a separate table in order to get more comfort
    # field_type = models.CharField(max_length=5,
    #     choices=[(tag, tag.value) for tag in TestFieldTypeChoice]  # Choices is a list of Tuple
    # )              
    field_type = models.ForeignKey(TestFieldTypeChoice, related_name='test_field_type', on_delete=models.PROTECT)

class TestFieldValidFloatRange(models.Model):
    rang_or_not = models.BooleanField()
    value = FloatRangeField()
    test_field = models.ForeignKey(TestField, related_name='test_field_valid_float_range', on_delete=models.PROTECT)

class TestFieldValidBoolean(models.Model):
    value = models.BooleanField()
    test_record_field = models.ForeignKey(TestField, related_name='test_field_valid_boolean', on_delete=models.PROTECT)

class TestFieldValidIntArray(models.Model):
    value = ArrayField(models.IntegerField())
    test_record_field = models.ForeignKey(TestField, related_name='test_field_valid_Integer_Array', on_delete=models.PROTECT)

class TestFieldValidStrArray(models.Model):
    value = ArrayField(models.CharField(max_length=255))
    test_record_field = models.ForeignKey(TestField, related_name='test_field_valid_String_Array', on_delete=models.PROTECT)

# Middle Class between Test-heathrecords and TestStandard in health standards for Test Models
class StanardTestfieldMapping(models.Model): 
    # 'test_field' Hint!! Must not define many_to_many field relation!! because: they actually have many_to_one relation and defining middle class is just because we want these both classes be seperated logically
    test_field = models.OneToOneField(TestField, db_index=True, related_name='test_field_standard', on_delete=models.PROTECT)
    standard = models.ForeignKey(TESTSTANDARD, related_name='standard_test_mapping', on_delete=models.PROTECT)

class TestRecord(models.Model):
    uuid = models.UUIDField(db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(ACCOUNT, related_name='user_test_records', on_delete=models.PROTECT)
    test = models.ForeignKey(Test, related_name='test_records', on_delete=models.PROTECT)


class TestRecordField(models.Model):
    test_record = models.ForeignKey(TestRecord, related_name='test_record_results', on_delete=models.PROTECT)
    test_field = models.ForeignKey(TestField, related_name='test_field_result', on_delete=models.PROTECT)
    description = models.CharField(max_length=511)

class TestRecordFieldFloatRangeValue(models.Model):
    rang_or_not = models.BooleanField()
    value = FloatRangeField()
    test_record_field = models.ForeignKey(TestRecordField, related_name='test_field_float_result', on_delete=models.PROTECT)

class TestRecordFieldIntegerArrayValue(models.Model):
    rang_or_not = models.BooleanField()
    value = ArrayField(models.IntegerField())
    test_record_field = models.ForeignKey(TestRecordField, related_name='test_field_integer_array_result', on_delete=models.PROTECT)

class TestRecordFieldBooleanValue(models.Model):
    value = models.BooleanField()
    test_record_field = models.ForeignKey(TestRecordField, related_name='test_field_boolean_result', on_delete=models.PROTECT)

class TestRecordFieldStringValue(models.Model):
    value = ArrayField(models.CharField(max_length=1023))
    test_record_field = models.ForeignKey(TestRecordField, related_name='test_field_string_array_result', on_delete=models.PROTECT)
