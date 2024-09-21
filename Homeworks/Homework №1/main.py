import tarfile
import sys

from pathlib import Path
from tkinter import Tk, WORD, END, Entry, Button
from tkinter.scrolledtext import  ScrolledText

class ShellEmulator:
    def __init__(self, 
                 computer_name: str, 
                 file_system_archive: str, 
                 startup_script: str | None = None) -> None:
        
        self.root = Tk()
        self.working_directory = Path('/')
        self.computer_name = computer_name
        self.file_system_archive = file_system_archive
        self.file_system = {}
        self.files = {}

        self.__load_virtual_file_system(file_system_archive)
        self.__init_display()

    def __load_virtual_file_system(self,
                                   file_system_archive: str) -> None:
    
        if tarfile.is_tarfile(file_system_archive):
            with tarfile.open(file_system_archive, 'r') as tar:
                files = tar.getmembers()
                for member in files[1:]:
                    path = Path(member.path.replace(files[0].name + '/', '/'))
                    folder, file = path.parent, path.name
                    self.file_system.setdefault(folder, list()).append(file)
                    if member.isfile():
                        self.files[path] = member
        else:
            self.command_output.insert(END, 'Ошибка: Архив .tar не найден\n')
        
    def __init_display(self) -> None:
        self.root.title(f'{self.computer_name}: Командная строка')
        self.command_output = ScrolledText(self.root, wrap=WORD, height=20, width=60)
        self.command_output.pack(padx=10, pady=10)
        
        self.command_input = Entry(self.root, width=50)
        self.command_input.pack(padx=10, pady=5)
        
        self.submit_button = Button(self.root, text='Ввод', command=self.__handle_command)
        self.submit_button.pack(padx=10, pady=5)
        
        self.__display_prompt()

    def __display_line(self,
                       line: str) -> None:
        
        self.command_output.config(state='normal')
        self.command_output.insert(END, line)
        self.command_output.config(state='disabled')

    def __display_prompt(self) -> None:
        self.__display_line(f'{self.computer_name}@vsh:{self.working_directory.as_posix()}$ ')

    def __handle_command(self) -> None:
        command_line = self.command_input.get().strip()
        self.command_input.delete(0, END)
        self.__display_line(command_line + '\n')
        if command_line:
            command_split = command_line.split()
            command, args = command_split[0], command_split[1:]
            
            if command == 'ls':
                self.__ls(args)
            elif command == 'cd':
                self.__cd(args)
            elif command == 'exit':
                self.__exit()
            elif command == 'wc':
                self.__wc(args)
            elif command == 'uniq':
                self.__uniq(args)
            else:
                self.__display_line('command not found\n')
        
        self.__display_prompt()

    def __interpret_path(self,
                         directory_path: str) -> Path:
        
        if directory_path.startswith('/'):
            search_directory = Path(directory_path)
        elif directory_path == '..':
            search_directory = self.working_directory.parent
        elif directory_path == '.' or directory_path == './':
            search_directory = self.working_directory
        elif directory_path.startswith('..'):
            return self.__interpret_path((self.working_directory.parent / directory_path[2:]).as_posix())
        elif directory_path.startswith('./'):
            return self.__interpret_path((self.working_directory / directory_path[2:]).as_posix()) 
        else:
            search_directory = self.working_directory / directory_path

        return search_directory

    def __set_working_directory(self, 
                                new_working_directory: Path) -> None:
        
        if new_working_directory in self.file_system:
            self.working_directory = new_working_directory
        else:
            self.__display_line(f'{new_working_directory.as_posix()}: No such file or directory\n')

    def __get_directory_content(self, 
                                search_directory: Path) -> str:
        
        if search_directory in self.file_system:
            content = '    '.join(self.file_system[search_directory])
        else:
            content = f'cannot access "{search_directory.as_posix()}": No such file or directory'

        return content

    def __ls(self, 
             directories: list[str]) -> None:
        
        contents = list()
        for directory in directories:
            search_directory = self.__interpret_path(directory)
            contents.append(f'{directory}: {self.__get_directory_content(search_directory)}')
        if not contents:
            contents.append(f'{self.working_directory.as_posix()}: {self.__get_directory_content(self.working_directory)}')
    
        for content in contents:
            self.__display_line(content + '\n')
                    
    def __cd(self, 
             directories: list[str]) -> None:

        if len(directories) > 1:
            self.__display_line('too many arguments')
            return

        if len(directories) == 0:
            search_directory = Path('/')
        else:
            search_directory = self.__interpret_path(directories[0])

        self.__set_working_directory(search_directory)

    def __exit(self) -> None:
        self.root.quit()

    def __wc(self, 
             files_pathes: list[str]):
        
        contents = list()
        summary = [0, 0, 0]
        for file_path in files_pathes:
            path = self.__interpret_path(file_path)
            if path in self.files:
                with tarfile.open(self.file_system_archive, 'r') as tar:
                    file_obj = tar.extractfile(self.files[path]).read().decode()
                lines, words, byte = len(file_obj.split('\n')), len(file_obj.split()), self.files[path].size
                contents.append(f'{lines} {words} {byte} {path}')
                summary[0] += lines
                summary[1] += words
                summary[2] += byte
            else:
                contents.append(f'{path}: No such file or directory')
        
        for content in contents:
            self.__display_line(content + '\n')
        self.__display_line(' '.join(list(map(str, summary))) + ' total\n')
        
    def __uniq(self, 
               files_pathes: list[str]):
        pass

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Использование: python main.py <имя компьютера> <архив файловой системы> <стартовый скрипт>')
        sys.exit(1)

    computer_name, fs_archive, startup_script = sys.argv[1], sys.argv[2], sys.argv[3]
    shell = ShellEmulator(computer_name, fs_archive, startup_script)
    shell.run()