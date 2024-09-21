import tarfile
import sys
from tkinter import Tk, WORD, END, Entry, Button
from tkinter.scrolledtext import  ScrolledText

class ShellEmulator:
    def __init__(self, 
                 computer_name: str, 
                 file_system_archive: str, 
                 startup_script: str | None = None):
        
        self.root = Tk()
        self.current_directory = "/"
        self.computer_name = computer_name
        self.file_system = {}

        self.__load_virtual_file_system(file_system_archive)
        self.__init_display()

    def __load_virtual_file_system(self,
                                   file_system_archive: str):
    
        if tarfile.is_tarfile(file_system_archive):
            with tarfile.open(file_system_archive, "r") as tar:
                for member in tar.getmembers():
                    self.file_system[member.name] = member
        else:
            self.command_output.insert(END, "Ошибка: Архив .tar не найден\n")
        
    def __init_display(self):
        self.root.title(f"{self.computer_name}: Командная строка")
        self.command_output = ScrolledText(self.root, wrap=WORD, height=20, width=60)
        self.command_output.pack(padx=10, pady=10)
        
        self.command_input = Entry(self.root, width=50)
        self.command_input.pack(padx=10, pady=5)
        
        self.submit_button = Button(self.root, text="Ввод")
        self.submit_button.pack(padx=10, pady=5)
        
        self.__display_prompt()

    def __display_prompt(self):
        self.command_output.config(state='normal')
        self.command_output.insert(END, f"{self.computer_name}@virtual_shell:{self.current_directory}$ ")
        self.command_output.config(state='disabled')

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Использование: python main.py <имя компьютера> <архив файловой системы> <стартовый скрипт>")
        sys.exit(1)

    computer_name, fs_archive, startup_script = sys.argv[1], sys.argv[2], sys.argv[3]
    shell = ShellEmulator(computer_name, fs_archive, startup_script)
    shell.run()