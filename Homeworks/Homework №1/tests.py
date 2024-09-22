import unittest
from main import ShellEmulator
from pathlib import Path

class TestShellEmulator(unittest.TestCase):
    def setUp(self):
        self.shell = ShellEmulator('TestPC', 'Homeworks\Homework №1\system.tar', '123')

    def test_ls_root(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('ls')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('Documents', output)
        self.assertIn('Downloads', output)

    def test_ls_documents(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('ls Documents')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('temp.txt', output)
        self.assertIn('пароли.txt', output)
        self.assertIn('Study', output)

    def test_ls_nonexistent_directory(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('ls non_existent_dir')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('No such file or directory', output)

    def test_cd_documents(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('cd Documents')
        self.assertEqual(self.shell.working_directory.as_posix(), '/Documents')

    def test_cd_parent_directory(self):
        self.shell.working_directory = Path('/Documents/Study')
        self.shell.execute_command('cd ..')
        self.assertEqual(self.shell.working_directory.as_posix(), '/Documents')

    def test_cd_nonexistent_directory(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('cd non_existent_dir')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('No such file or directory', output)
            
    def test_wc_file(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('wc Documents/Study/1.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('1.txt', output)
    
    def test_wc_nonexistent_file(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('wc non_existent_file.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('No such file or directory', output)

    def test_wc_empty_file(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('wc Documents/empty.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('0 0 0', output)

    def test_uniq_file(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('uniq Documents/temp.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('Debug|x64 = Debug|x64\nDebug|x86 = Debug|x86\nRelease|x64 = Release|x64\nDebug|x64 = Debug|x64', output)

    def test_uniq_nonexistent_file(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('uniq non_existent_file.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('No such file or directory', output)

    def test_uniq_file_no_duplicates(self):
        start_line_index = self.shell.command_output.index("insert linestart")
        self.shell.execute_command('uniq Documents/пароли.txt')
        output = self.shell.command_output.get(start_line_index, "end-2c")
        self.assertIn('root: root\nanonymous: anonymous\nantes: 112', output)

if __name__ == '__main__':
    unittest.main()
