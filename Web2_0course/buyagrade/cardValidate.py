""" Functions for validating credit card numbers. """

import re

def IsValidChecksum(number):
    """ Checks if the card number passes a luhn mod-10 checksum. """

    numlist = [int(x) for x in reversed(str(number)) if x.isdigit()]
    # digits that count once
    count = sum(x for i, x in enumerate(numlist) if i % 2 == 0)
    # digits that count double (add digits of double value)
    count += sum(sum(divmod(2 * x, 10)) for i, x in enumerate(numlist) if i % 2 != 0)
    return (count % 10 == 0)


def IsValidCharacters(number):
    """
        Checks if the number only contains digits and '-'.
        If the digits are grouped, checks if they are grouped correctly.
    """

    if re.compile('^[-0-9]*$').match(number):
        return True
    else:
        return re.compile('^([0-9]{4}[-])*([0-9]{4})$').match(number) != None

def IsValidPattern(number, type):
    """ Checks to make sure that the card number match the CC pattern. """
    CC_PATTERNS = {
    'mastercard':'^5[12345]([0-9]{14})$',
    'visa'      :'^4([0-9]{15})$',
    }

    return re.compile(CC_PATTERNS[type]).match(number) != None

def IsValid(number, type):
    if IsValidCharacters(number):
        clean = number.replace('-', '')
        if IsValidPattern(clean, type):
            return IsValidChecksum(clean)

    return False