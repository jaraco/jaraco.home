import datetime
import json
import os
import re
import types

import autocommand
import jaraco.collections
from splinter import Browser


DROPPED_CALL = '2'


class IdentifierDict(jaraco.collections.KeyTransformingDict):
    @staticmethod
    def transform_key(key):
        return key.replace(' ', '_')


def read_contact_info():
    return types.SimpleNamespace(
        **IdentifierDict(json.loads(os.environ['CONTACT_INFO']))
    )


def clean_phone(number):
    return re.sub(r'[-. ]', '', number.removeprefix('+1'))


@autocommand.autocommand(__name__)
def report_spam_call(number, comment='', close=False):
    """
    Report the common spam calls.
    """
    contact = read_contact_info()
    browser = Browser('firefox')
    browser.visit('https://www.donotcall.gov/report.html')
    browser.find_by_value('Continue').click()
    browser.fill('PhoneTextBox', clean_phone(contact.phone))
    now = datetime.datetime.now()
    browser.fill('DateOfCallTextBox', now.strftime('%m/%d/%Y'))
    browser.select('TimeOfCallDropDownList', now.strftime('%H'))
    browser.select('ddlMinutes', now.strftime('%M'))
    browser.choose('PrerecMsg', 'PrerecordMessageYESRadioButton')
    browser.choose('TextMsg', 'PhoneCallRadioButton')
    browser.select(
        'ddlSubjectMatter',
        DROPPED_CALL,
    )
    browser.find_by_value('Continue').click()
    browser.fill('CallerPhoneNumberTextBox', clean_phone(number))
    browser.choose('HaveBusiness', 'HaveBusinessNoRadioButton')
    browser.choose('StopCalling', 'StopCallingNoRadioButton')
    browser.fill('FirstNameTextBox', contact.first_name.replace('.', ''))
    browser.fill('LastNameTextBox', contact.last_name)
    browser.fill('StreetAddressTextBox', contact.street_address)
    browser.fill('CityTextBox', contact.city)
    browser.select('StateDropDownList', contact.state)
    browser.fill('ZipCodeTextBox', contact.zip)
    browser.fill('CommentTextBox', comment)
    browser.find_by_value('SUBMIT').click()
    if close:
        browser.windows.current.close()
