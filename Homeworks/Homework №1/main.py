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
        self.working_directory = '/'
        self.computer_name = computer_name
        self.file_system = {}

        self.__load_virtual_file_system(file_system_archive)
        self.__init_display()

    def __load_virtual_file_system(self,
                                   file_system_archive: str) -> None:
    
        if tarfile.is_tarfile(file_system_archive):
            with tarfile.open(file_system_archive, 'r') as tar:
                files = tar.getmembers()
                for member in files[1:]:
                    path = Path(member.path.replace(files[0].name + '/', '/'))
                    folder, file = path.parent.as_posix(), path.name
                    self.file_system.setdefault(folder, list()).append(file)
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
        self.__display_line(f'{self.computer_name}@vsh:{self.working_directory}$ ')

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
            else:
                self.__display_line('command not found\n')
        
        self.__display_prompt()

    def __ls(self, 
             directories: list[str]) -> None:
        
        def get_content(search_directory) -> str:
            if directory in self.file_system:
                content = '    '.join(self.file_system[search_directory])
            else:
                content = f'cannot access "{search_directory}": No such file or directory'

            return content
        
        if directories:
            for directory in directories:
                if directory.startswith('/'):
                    search_directory = directory
                elif directory == '.' or directory == './':
                    search_directory = self.working_directory
                elif directory.startswith('./') and self.working_directory + directory[2:] in self.file_system:
                    search_directory = self.working_directory + directory[2:]
                else:
                    search_directory = self.working_directory + directory
            
                content = get_content(search_directory)
                self.__display_line(f'{directory}:\n')
                self.__display_line(content + '\n')
        else:
            content = '    '.join(self.file_system[self.working_directory])
            self.__display_line(content + '\n')
                    
    def __cd(self, 
             directories: list[str]) -> None:
        
        def set_working_directory(new_working_directory):
            if new_working_directory in self.file_system:
                self.working_directory = new_working_directory
            else:
                self.__display_line(f'{new_working_directory}: No such file or directory\n')

        if len(directories) == 0:
            search_directory = '/'
        elif len(directories) > 1:
            self.__display_line('too many arguments')
        else:
            directory = directories[0]
            if directory.startswith('/'):
                search_directory = directory
            elif directory == '..':
                search_directory = Path(self.working_directory).parent.as_posix()
            elif directory == '.' or directory == './':
                search_directory = self.working_directory
            elif directory.startswith('./') and self.working_directory + directory[2:] in self.file_system:
                search_directory = self.working_directory + directory[2:]
            else:
                search_directory = self.working_directory + directory

            set_working_directory(search_directory)

    def __exit(self):
        self.root.quit()

    def run(self):
        self.root.mainloop()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Использование: python main.py <имя компьютера> <архив файловой системы> <стартовый скрипт>')
        sys.exit(1)

    computer_name, fs_archive, startup_script = sys.argv[1], sys.argv[2], sys.argv[3]
    shell = ShellEmulator(computer_name, fs_archive, startup_script)
    shell.run()