import re


def is_camel_case(s):
    return len(re.findall('[A-Z][a-z]', s)) > 1


def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    for m in matches:
        yield m.group(0)
