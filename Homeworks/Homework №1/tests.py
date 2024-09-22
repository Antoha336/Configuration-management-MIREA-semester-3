import unittest
from main import ShellEmulator
from pathlib import Path

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.shell = ShellEmulator('TestPC', 'Homeworks\Homework №1\system.tar', '123')

    def get_command_output(self, command: str) -> str:
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command(command)

        return self.shell.command_output.get(start_line_index, "end-2c")

    def test_ls_root(self):
        output = self.get_command_output('ls')
        self.assertIn('Documents', output)
        self.assertIn('Downloads', output)

    def test_ls_documents(self):
        output = self.get_command_output('ls Documents')
        self.assertIn('temp.txt', output)
        self.assertIn('пароли.txt', output)
        self.assertIn('Study', output)

    def test_ls_nonexistent_directory(self):
        output = self.get_command_output('ls non_existent_dir')
        self.assertIn('No such file or directory', output)

    def test_cd_documents(self):
        self.shell.execute_command('cd Documents')
        self.assertEqual(self.shell.working_directory.as_posix(), '/Documents')

    def test_cd_parent_directory(self):
        self.shell.working_directory = Path('/Documents/Study')
        self.shell.execute_command('cd ..')
        self.assertEqual(self.shell.working_directory.as_posix(), '/Documents')

    def test_cd_nonexistent_directory(self):
        output = self.get_command_output('cd non_existent_dir')
        self.assertIn('No such file or directory', output)
            
    def test_wc_file(self):
        output = self.get_command_output('wc Documents/temp.txt')
        self.assertIn('7 21 161 /Documents/temp.txt\n7 21 161 total', output)
    
    def test_wc_nonexistent_file(self):
        output = self.get_command_output('wc non_existent_file.txt')
        self.assertIn('No such file or directory', output)

    def test_wc_empty_file(self):
        output = self.get_command_output('wc /Documents/Study/1.txt')
        self.assertIn('1 0 0 /Documents/Study/1.txt\n1 0 0 total', output)

    def test_uniq_file(self):
        output = self.get_command_output('uniq Documents/temp.txt')
        self.assertIn('Debug|x64 = Debug|x64\nDebug|x86 = Debug|x86\nRelease|x64 = Release|x64\nDebug|x64 = Debug|x64', output)

    def test_uniq_nonexistent_file(self):
        output = self.get_command_output('uniq non_existent_file.txt')
        self.assertIn('No such file or directory', output)

    def test_uniq_file_no_duplicates(self):
        output = self.get_command_output('uniq Documents/пароли.txt')
        self.assertIn('root: root\nanonymous: anonymous\nantes: 112', output)

if __name__ == '__main__':
    unittest.main()
