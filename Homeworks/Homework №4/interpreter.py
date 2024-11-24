import sys
import xml.etree.ElementTree as ET

from xml.dom import minidom

def create_mask(start: int, end: int) -> int:
    return ((1 << (end - start + 1)) - 1) << start


class Interpreter:
    def __init__(self):
        self.memory = [0] * 1024
        self.registers = [0] * 32
        self.commands = {
            5: 'LOAD_CONST',
            1: 'READ_MEM',
            9: 'WRITE_MEM',
            0: 'ADD',
        }
        
    
    def __get_command(self, opcode: int) -> str:
        command = self.commands.get(opcode)
        if not command:
            raise Exception(f'Unkwown opcode: {opcode}')

        return command


    def __get_operand(self, command_bytes: bytearray, start: int, end: int) -> int:
        return (int.from_bytes(command_bytes) & create_mask(start, end)) >> start


    def load_const(self, command_bytes: bytearray) -> None:
        b = self.__get_operand(command_bytes, 4, 32)
        c = self.__get_operand(command_bytes, 33, 37)
        
        self.registers[c] = b


    def read_memory(self, command_bytes: bytearray) -> None:
        b = self.__get_operand(command_bytes, 4, 8)
        c = self.__get_operand(command_bytes, 9, 13)

        self.registers[b] = self.memory[self.registers[c]]


    def write_memory(self, command_bytes: bytearray) -> None:
        b = self.__get_operand(command_bytes, 4, 8)
        c = self.__get_operand(command_bytes, 9, 13)
        d = self.__get_operand(command_bytes, 14, 28)

        self.memory[self.registers[b] + d] = self.registers[c]


    def add(self, command_bytes: bytearray) -> None:
        b = self.__get_operand(command_bytes, 4, 22)
        c = self.__get_operand(command_bytes, 23, 27)

        self.memory[b] = self.memory[b] + self.registers[c]


    def __process_command(self, command_bytes: bytearray):
        opcode = command_bytes[-1] & 0xF
        command = self.__get_command(opcode)
        match(command):
            case 'LOAD_CONST':
                self.load_const(command_bytes)
            case 'READ_MEM':
                self.read_memory(command_bytes)
            case 'WRITE_MEM':
                self.write_memory(command_bytes)
            case 'ADD':
                self.add(command_bytes)
            case '_':
                raise Exception(f'Unknown command: {command}')


    def interpret(self, binary_file: str, memory_range: tuple[int, int], result_file: str):
        bytecode = open(binary_file, 'rb')
        
        byte = bytecode.read(1)
        while byte:
            command_length = int.from_bytes(byte)
            command_bytes = bytearray(bytecode.read(command_length))
            command_bytes.reverse()
            self.__process_command(command_bytes)
            
            byte = bytecode.read(1)
        
        bytecode.close()
        root = ET.Element('memory')
        for addr in range(*memory_range):
            ET.SubElement(root, 'cell', address=str(addr), value=str(self.memory[addr]))

        rough_string = ET.tostring(root, encoding='utf-8')
        parsed = minidom.parseString(rough_string)
        pretty_xml = parsed.toprettyxml(indent="    ")
        
        with open(result_file, "w") as file:
            file.write(pretty_xml)


if __name__ == '__main__':
    if len(sys.argv) < 4:
        print('Usage: python interpreter.py <input_file> <interval_start> <interval_end> <result_file>')
        sys.exit(1)

    interpreter = Interpreter()
    input_file, interval, result_file = sys.argv[1], (int(sys.argv[2]), int(sys.argv[3])), sys.argv[4]
    interpreter.interpret(input_file, interval, result_file)   
