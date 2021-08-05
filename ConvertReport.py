import xmltodict
import collections
import time
import uuid


def convert_xml(xml_path):
    xml_content = open(xml_path, "r")
    xml_text = xml_content.read()
    old_format = xmltodict.parse(xml_text)
    test_suites = collections.OrderedDict()
    test_suites['testsuites'] = collections.OrderedDict()
    test_suites['testsuites']['testsuite'] = old_format['testsuite']
    test_suites['testsuites']['testsuite']['@failures'] = test_suites['testsuites']['testsuite']['@errors']
    test_suites['testsuites']['testsuite']['@id'] = str(uuid.uuid1())
    test_suites['testsuites']['testsuite']['@name'] = "Build " + str(time.time())
    test_suites['testsuites']['testsuite']['@log'] = "created: " + str(time.time())
    del test_suites['testsuites']['testsuite']['@errors']
    del test_suites['testsuites']['testsuite']['@hostname']
    for testcase in test_suites['testsuites']['testsuite']['testcase']:
        del testcase['@classname']
        if 'error' in testcase:
            del testcase['error']['@type']
            testcase['failure'] = testcase['error']
            del testcase['error']
    output = xmltodict.unparse(test_suites)
    with open(xml_path, 'w') as file_to_write:
        file_to_write.write(output)
