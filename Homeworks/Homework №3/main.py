import sys
import yaml
import re

class SyntaxError(Exception):
    pass

class YamlParser:
    def __convert_value(self, value: str | int | list | dict, tabs: int = 0) -> str | int | list | dict:
        if isinstance(value, str) or isinstance(value, bool):
            return f'@"{value}"'
        elif isinstance(value, int) or isinstance(value, float):
            return str(value)
        elif isinstance(value, list):
            return self.__convert_list(value)
        elif isinstance(value, dict):
            return self.__convert_dict(value, tabs)
        else:
            raise SyntaxError("Неизвестный тип данных")

    def __check_name(self, name: str) -> bool:
        return bool(re.fullmatch(r'^[a-zA-Z][a-zA-Z0-9]*$', name))

    def __convert_list(self, data: list):
        conveted_values = map(self.__convert_value, data)
        elements = " ".join(conveted_values)

        return f'[ {elements} ]'

    def __convert_dict(self, data: dict, tabs: int = 0):
        tabulation = ' ' * 2 * tabs
        struct = 'struct {\n'
        for key, value in data.items():
            if not self.__check_name(key):
                raise SyntaxError(f"Некорректное имя: {key}")
            struct += tabulation + f"  {key} = {self.__convert_value(value, tabs + 1)},\n"
        struct += tabulation + "}"

        return struct
    
    def __parse_comments(self, raw_input: str) -> dict[str, list[str]]:
        lines = raw_input.split('\n')
        comments = dict()
        for line in lines:
            coms = re.findall(r'\s*#.*', line, re.MULTILINE)
            if not coms:
                continue

            tag = re.match(r'^\s*(\w+)', line)
            if not tag:
                if len(comments) <= 1:
                    tag = '_start'
                else:
                    tag = '_end'
            else:
                tag = tag.group(1)

            comments.setdefault(tag, list()).append(coms[0].replace('#', '*>', 1))
        
        return comments
    
    def __insert_comments(self, converted_data: str, comments: dict[str, list[str]]) -> str:
        lines = converted_data.split('\n')
        new_lines = list()
        if '_start' in comments:
            for comment in comments['_start']:
                new_lines.append(comment)

        for line in lines:
            tag = re.match(r'^\s*(\w+)', line)
            if tag:
                tag = tag.group(1)
                if tag in comments:
                    for comment in comments[tag]:
                        line = f'{line} {comment}'
            new_lines.append(line)

        if '_end' in comments:
            for comment in comments['_end']:
                new_lines.append(comment)

        return '\n'.join(new_lines)

    def parse(self, raw_input: str) -> dict:
        try:
            yaml_data = yaml.safe_load(raw_input)
            comments = self.__parse_comments(raw_input)
            converted_data = self.__convert_dict(yaml_data)
            result = self.__insert_comments(converted_data, comments)

            return result
        except yaml.YAMLError as e:
            print(f"Ошибка в YAML: {e}")
        except SyntaxError as e:
            print(f"Синтаксическая ошибка: {e}")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")

def main():
    input_data = sys.stdin.read()
    parser = YamlParser()
    result = parser.parse(input_data)
    print(result)


if __name__ == "__main__":
    main()
