"""
isort:skip_file
# flake8: noqa

Generated with:
manage dumpscript core > scripts/fixture_sample_data1.py
"""
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file has been automatically generated.
# Instead of changing it, create a file called import_helper.py
# and put there a class called ImportHelper(object) in it.
#
# This class will be specially casted so that instead of extending object,
# it will actually extend the class BasicImportHelper()
#
# That means you just have to overload the methods you want to
# change, leaving the other ones inteact.
#
# Something that you might want to do is use transactions, for example.
#
# Also, don't forget to add the necessary Django imports.
#
# This file was generated with the following command:
# /Users/nimiq/workspace/mybottles/manage.py dumpscript core
#
# to restore it, run
# manage.py runscript module_name.this_script_name
#
# example: if manage.py is at ./manage.py
# and the script is at ./some_folder/some_script.py
# you must make sure ./some_folder/__init__.py exists
# and run  ./manage.py runscript some_folder.some_script
import os, sys
from uuid import UUID
from django.db import transaction

class BasicImportHelper(object):

    def pre_import(self):
        pass

    @transaction.atomic
    def run_import(self, import_data):
        import_data()

    def post_import(self):
        pass

    def locate_similar(self, current_object, search_data):
        # You will probably want to call this method from save_or_locate()
        # Example:
        #   new_obj = self.locate_similar(the_obj, {"national_id": the_obj.national_id } )

        the_obj = current_object.__class__.objects.get(**search_data)
        return the_obj

    def locate_object(self, original_class, original_pk_name, the_class, pk_name, pk_value, obj_content):
        # You may change this function to do specific lookup for specific objects
        #
        # original_class class of the django orm's object that needs to be located
        # original_pk_name the primary key of original_class
        # the_class      parent class of original_class which contains obj_content
        # pk_name        the primary key of original_class
        # pk_value       value of the primary_key
        # obj_content    content of the object which was not exported.
        #
        # You should use obj_content to locate the object on the target db
        #
        # An example where original_class and the_class are different is
        # when original_class is Farmer and the_class is Person. The table
        # may refer to a Farmer but you will actually need to locate Person
        # in order to instantiate that Farmer
        #
        # Example:
        #   if the_class == SurveyResultFormat or the_class == SurveyType or the_class == SurveyState:
        #       pk_name="name"
        #       pk_value=obj_content[pk_name]
        #   if the_class == StaffGroup:
        #       pk_value=8

        search_data = { pk_name: pk_value }
        the_obj = the_class.objects.get(**search_data)
        #print(the_obj)
        return the_obj


    def save_or_locate(self, the_obj):
        # Change this if you want to locate the object in the database
        try:
            the_obj.save()
        except:
            print("---------------")
            print("Error saving the following object:")
            print(the_obj.__class__)
            print(" ")
            print(the_obj.__dict__)
            print(" ")
            print(the_obj)
            print(" ")
            print("---------------")

            raise
        return the_obj


importer = None
try:
    import import_helper
    # We need this so ImportHelper can extend BasicImportHelper, although import_helper.py
    # has no knowlodge of this class
    importer = type("DynamicImportHelper", (import_helper.ImportHelper, BasicImportHelper ) , {} )()
except ImportError as e:
    # From Python 3.3 we can check e.name - string match is for backward compatibility.
    if 'import_helper' in str(e):
        importer = BasicImportHelper()
    else:
        raise

import datetime
from decimal import Decimal
from django.contrib.contenttypes.models import ContentType

try:
    import dateutil.parser
except ImportError:
    print("Please install python-dateutil")
    sys.exit(os.EX_USAGE)

def run():
    importer.pre_import()
    importer.run_import(import_data)
    importer.post_import()

def import_data():
    # Initial Imports

    # Processing model: core.models.Location

    from core.models import Location

    core_location_1 = Location()
    core_location_1.uuid = UUID('7c2770bd-233a-4cbd-97aa-98acfa145ac1')
    core_location_1.name = 'Soave'
    core_location_1 = importer.save_or_locate(core_location_1)

    core_location_2 = Location()
    core_location_2.uuid = UUID('28a95549-1d7f-4cb8-9bd3-f0821e44a9c6')
    core_location_2.name = 'Valpolicella'
    core_location_2 = importer.save_or_locate(core_location_2)

    core_location_3 = Location()
    core_location_3.uuid = UUID('49e307ed-976c-46bd-9af2-08d885fd84c7')
    core_location_3.name = 'Alice Bel Colle'
    core_location_3 = importer.save_or_locate(core_location_3)

    core_location_4 = Location()
    core_location_4.uuid = UUID('701a0678-7db2-4c04-9801-e033d49b3221')
    core_location_4.name = 'Langhe'
    core_location_4 = importer.save_or_locate(core_location_4)

    # Processing model: core.models.Store

    from core.models import Store

    core_store_1 = Store()
    core_store_1.uuid = UUID('41822acd-7609-405d-8bd0-6ba1219418d7')
    core_store_1.name = 'Carrefour Verdello'
    core_store_1 = importer.save_or_locate(core_store_1)

    core_store_2 = Store()
    core_store_2.uuid = UUID('4ed34efd-786f-4d8e-85e4-dc10a9eb32ef')
    core_store_2.name = 'Iper Brembate'
    core_store_2 = importer.save_or_locate(core_store_2)

    core_store_3 = Store()
    core_store_3.uuid = UUID('3915861e-9032-476f-9f25-42f554ff4051')
    core_store_3.name = 'Carrefour Bergamo via Broseta'
    core_store_3 = importer.save_or_locate(core_store_3)

    # Processing model: core.models.Producer

    from core.models import Producer

    core_producer_1 = Producer()
    core_producer_1.uuid = UUID('60321e2a-2d04-484f-8008-d874a590c4b6')
    core_producer_1.name = 'Le Poiane'
    core_producer_1.winery_location = core_location_1
    core_producer_1 = importer.save_or_locate(core_producer_1)

    core_producer_2 = Producer()
    core_producer_2.uuid = UUID('aea39309-4ee4-4870-a464-aae9f4cf4ea9')
    core_producer_2.name = "Tenimenti Ca' Bianca"
    core_producer_2.winery_location = core_location_3
    core_producer_2 = importer.save_or_locate(core_producer_2)

    # Processing model: core.models.Bottle

    from core.models import Bottle

    core_bottle_1 = Bottle()
    core_bottle_1.uuid = UUID('0216c987-77c7-4554-b562-f64206fdb332')
    core_bottle_1.creation_ts = dateutil.parser.parse("2019-04-07T19:49:28.709537+00:00")
    core_bottle_1.update_ts = dateutil.parser.parse("2019-04-07T19:49:28.709612+00:00")
    core_bottle_1.name = 'Valpolicella Ripasso DOC Classico Superiore'
    core_bottle_1.producer = core_producer_1
    core_bottle_1.vineyard_location = core_location_2
    core_bottle_1.year = 2015
    core_bottle_1.alcohol = Decimal('13.0')
    core_bottle_1 = importer.save_or_locate(core_bottle_1)

    core_bottle_2 = Bottle()
    core_bottle_2.uuid = UUID('9ec758ae-f380-428c-b380-109476b13b6d')
    core_bottle_2.creation_ts = dateutil.parser.parse("2019-04-07T19:49:28.711111+00:00")
    core_bottle_2.update_ts = dateutil.parser.parse("2019-04-07T19:49:28.711149+00:00")
    core_bottle_2.name = 'Barolo DOCG'
    core_bottle_2.producer = core_producer_2
    core_bottle_2.vineyard_location = core_location_4
    core_bottle_2.year = 2013
    core_bottle_2.alcohol = Decimal('16.0')
    core_bottle_2 = importer.save_or_locate(core_bottle_2)

    # Processing model: core.models.Purchase

    from core.models import Purchase

    core_purchase_1 = Purchase()
    core_purchase_1.uuid = UUID('e451f503-846c-4686-9d24-578cfa938489')
    core_purchase_1.bottle = core_bottle_2
    core_purchase_1.quantity = 2
    core_purchase_1.price_paid = Decimal('18.00')
    core_purchase_1.price_original = Decimal('25.00')
    core_purchase_1.date = dateutil.parser.parse("2019-04-01")
    core_purchase_1.store = core_store_3
    core_purchase_1 = importer.save_or_locate(core_purchase_1)

    core_purchase_2 = Purchase()
    core_purchase_2.uuid = UUID('7cebbf9e-eb13-4631-a9b4-0d55d62ce200')
    core_purchase_2.bottle = core_bottle_2
    core_purchase_2.quantity = None
    core_purchase_2.price_paid = None
    core_purchase_2.price_original = None
    core_purchase_2.date = dateutil.parser.parse("2019-04-07")
    core_purchase_2.store = core_store_1
    core_purchase_2 = importer.save_or_locate(core_purchase_2)

    core_purchase_3 = Purchase()
    core_purchase_3.uuid = UUID('46f1dab0-08a2-4db3-b46e-ba64bf708f0e')
    core_purchase_3.bottle = core_bottle_1
    core_purchase_3.quantity = 2
    core_purchase_3.price_paid = Decimal('12.50')
    core_purchase_3.price_original = Decimal('15.80')
    core_purchase_3.date = None
    core_purchase_3.store = core_store_2
    core_purchase_3 = importer.save_or_locate(core_purchase_3)

    # Processing model: core.models.Photo

    from core.models import Photo

    core_photo_1 = Photo()
    core_photo_1.bottle = core_bottle_1
    core_photo_1.file = 'photos/valpolicella-classico-superiore-ripasso-novaia_2.jpg'
    core_photo_1 = importer.save_or_locate(core_photo_1)

    core_photo_2 = Photo()
    core_photo_2.bottle = core_bottle_2
    core_photo_2.file = 'photos/barolo-demarie.jpg'
    core_photo_2 = importer.save_or_locate(core_photo_2)

    core_photo_3 = Photo()
    core_photo_3.bottle = core_bottle_2
    core_photo_3.file = 'photos/Barolo-noannata.jpg'
    core_photo_3 = importer.save_or_locate(core_photo_3)

