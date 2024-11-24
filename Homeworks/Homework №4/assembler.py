import sys
import xml.etree.ElementTree as ET

from xml.dom import minidom


class Assembler:
    def __init__(self) -> None:
        self.commands = {
            'LOAD_CONST': 5,
            'READ_MEM': 1,
            'WRITE_MEM': 9,
            'ADD': 0,
        }


    def __get_command(self, command: str) -> int:
        return self.commands[command]


    @staticmethod
    def load_const(a: int, b: int, c: int) -> bytearray:
        if not (0 <= a < 2**4):
            raise ValueError("Значение A должно быть в диапазоне от 0 до 15 (4 бит).")
        elif not (0 <= b < 2**29):
            raise ValueError("Значение B должно быть в диапазоне от 0 до 536_870_912 (29 бит).")
        elif not (0 <= c < 2**5):
            raise ValueError("Значение C должно быть в диапазоне от 0 до 31 (5 бит).")
        
        command_bits = (c << 33) | (b << 4) | a
        command_bits = command_bits & 0xFFFFFFFFFF

        byte1 = (command_bits >> 32) & 0xFF
        byte2 = (command_bits >> 24) & 0xFF
        byte3 = (command_bits >> 16) & 0xFF
        byte4 = (command_bits >> 8) & 0xFF
        byte5 = command_bits & 0xFF

        byte_array = bytearray([5, byte5, byte4, byte3, byte2, byte1])

        return byte_array


    @staticmethod
    def read_memory(a: int, b: int, c: int) -> bytearray:
        if not (0 <= a < 2**4):
            raise ValueError("Значение A должно быть в диапазоне от 0 до 15 (4 бит).")
        elif not (0 <= b < 2**5):
            raise ValueError("Значение B должно быть в диапазоне от 0 до 31 (5 бит).")
        elif not (0 <= c < 2**5):
            raise ValueError("Значение C должно быть в диапазоне от 0 до 31 (5 бит).")
        
        command_bits = (c << 9) | (b << 4) | a
        command_bits = command_bits & 0xFFFF

        byte1 = (command_bits >> 8) & 0xFF
        byte2 = command_bits & 0xFF

        byte_array = bytearray([2, byte2, byte1])

        return byte_array


    @staticmethod
    def write_memory(a: int, b: int, c: int, d: int) -> bytearray:
        if not (0 <= a < 2**4):
            raise ValueError("Значение A должно быть в диапазоне от 0 до 15 (4 бит).")
        elif not (0 <= b < 2**5):
            raise ValueError("Значение B должно быть в диапазоне от 0 до 31 (5 бит).")
        elif not (0 <= c < 2**5):
            raise ValueError("Значение C должно быть в диапазоне от 0 до 31 (5 бит).")
        elif not (0 <= d < 2**15):
            raise ValueError("Значение D должно быть в диапазоне от 0 до 32_768 (15 бит).")
        
        command_bits = (d << 14) | (c << 9) | (b << 4) | a
        command_bits = command_bits & 0xFFFFFFFF

        byte1 = (command_bits >> 24) & 0xFF
        byte2 = (command_bits >> 16) & 0xFF
        byte3 = (command_bits >> 8) & 0xFF
        byte4 = command_bits & 0xFF

        byte_array = bytearray([4, byte4, byte3, byte2, byte1])

        return byte_array


    @staticmethod
    def add(a: int, b: int, c: int) -> bytearray:
        if not (0 <= a < 2**4):
            raise ValueError("Значение A должно быть в диапазоне от 0 до 15 (4 бит).")
        elif not (0 <= b < 2**19):
            raise ValueError("Значение B должно быть в диапазоне от 0 до 524_288 (19 бит).")
        elif not (0 <= c < 2**5):
            raise ValueError("Значение C должно быть в диапазоне от 0 до 31 (5 бит).")
        
        command_bits = (c << 23) | (b << 4) | a
        command_bits = command_bits & 0xFFFFFFFF

        byte1 = (command_bits >> 24) & 0xFF
        byte2 = (command_bits >> 16) & 0xFF
        byte3 = (command_bits >> 8) & 0xFF
        byte4 = command_bits & 0xFF

        byte_array = bytearray([4, byte4, byte3, byte2, byte1])

        return byte_array
    

    def __parse_instruction(self, line: str) -> tuple[str, tuple[int, ...], bytearray]:
        parts = line.split()
        command = parts.pop(0)
        parts = list(map(int, parts))
        match(command):
            case 'LOAD_CONST':
                a, b, c = self.__get_command(command), parts[0], parts[1]
                args = a, b, c
                result = self.load_const(a, b, c)
            case 'READ_MEM':
                a, b, c = self.__get_command(command), parts[0], parts[1]
                args = a, b, c
                result = self.read_memory(a, b, c)
            case 'WRITE_MEM':
                a, b, c, d = self.__get_command(command), parts[0], parts[1], parts[2]
                args = a, b, c, d
                result = self.write_memory(a, b, c, d)
            case 'ADD':
                a, b, c = self.__get_command(command), parts[0], parts[1]
                args = a, b, c
                result = self.add(a, b, c)
            case '_':
                raise Exception(f'Unknown command: {command}')
        
        return (command, args, result)


    def __log_instructions(self, log_file: str, instructions: list[tuple[str, tuple[int, ...], bytearray]]) -> None:
        root = ET.Element("log")
        for i, instruction in enumerate(instructions):
            ET.SubElement(root, "instruction", id=str(i), tag=instruction[0]).text = f'{" ".join(f"{chr(65 + i)}={val}" for i, val in enumerate(instruction[1]))} {instruction[2].hex(",")}'

        rough_string = ET.tostring(root, encoding='utf-8')
        parsed = minidom.parseString(rough_string)
        pretty_xml = parsed.toprettyxml(indent="    ")

        with open(log_file, "w") as file:
            file.write(pretty_xml)


    def assemble(self, input_file: str, output_file: str, log_file: str):
        instructions: list[tuple[str, bytearray]] = list()
        
        with open(input_file, 'r') as file:
            for line in file:
                parts = line.split()
                if not parts:
                    continue

                instructions.append(self.__parse_instruction(line))
        
        with open(output_file, 'wb') as file:
            for instruction in instructions:
                file.write(instruction[2])
        
        self.__log_instructions(
            log_file=log_file,
            instructions=instructions,
        )
        

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python assembler.py <input_file> <output_file> <logs_file>')
        sys.exit(1)
    
    input_file, output_file, logs_file = sys.argv[1:4]
    assembler = Assembler()
    assembler.assemble(input_file, output_file, logs_file)

