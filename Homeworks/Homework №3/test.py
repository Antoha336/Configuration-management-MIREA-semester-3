import unittest

from main import YamlParser

class TestYamlParser(unittest.TestCase):

    def setUp(self):
        self.parser = YamlParser()

    def test_simple_yaml(self):
        input_data = '''
        name: "John"
        '''
        expected_output = '''struct {
  name = @"John",
}'''
        self.assertEqual(self.parser.parse(input_data), expected_output)

    def test_yaml_with_list(self):
        input_data = '''
        items:
          - "apple"
          - "banana"
        '''
        expected_output = '''struct {
  items = [ @"apple" @"banana" ],
}'''
        self.assertEqual(self.parser.parse(input_data), expected_output)

    def test_yaml_with_comments(self):
        input_data = '''# Commentary
        name: "John" # Commentary for name
        age: 30 # Commentary for age
        '''
        expected_output = '''*> Commentary
struct {
  name = @"John",  *> Commentary for name
  age = 30,  *> Commentary for age
}'''
        self.assertEqual(self.parser.parse(input_data), expected_output)

    def test_yaml_with_nesting_and_vars(self):
        input_data = '''stages:
          - build

        variables:
          MYVARIABLE: "Hello"
          LIST: [ 123, 321 ]
          COMPUTEDVARIABLE: "{{ MYVARIABLE + 1 }} World"

        buildjob:
          stage: build
          script:
            - echo {{ COMPUTEDVARIABLE }}
        '''
        output_data = '''
struct {
  stages = [ @"build" ],
  variables = struct {
    MYVARIABLE = @"Hello",
    LIST = [ 123 321 ],
    COMPUTEDVARIABLE = @"#(MYVARIABLE + 1) World",
  },
  buildjob = struct {
    stage = @"build",
    script = [ @"echo #(COMPUTEDVARIABLE)" ],
  },
}'''


if __name__ == "__main__":
    unittest.main()
