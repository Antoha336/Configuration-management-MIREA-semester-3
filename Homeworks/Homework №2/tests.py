import unittest
import os

from main import DependencyDrawer
from xml.etree import ElementTree as ET


class TestDependencyDrawer(unittest.TestCase):
    def create_test_config(self, package_url: str):
        configuration = ET.Element("Configuration")
    
        graphviz = ET.SubElement(configuration, "GraphvizPath")
        graphviz.text = 'dot'
        
        package = ET.SubElement(configuration, "PackagePath")
        package.text = package_url
        
        tree = ET.ElementTree(configuration)
        tree.write('test_config.xml', encoding="utf-8", xml_declaration=True)

    def test_1(self):
        self.create_test_config('https://www.nuget.org/packages/Newtonsoft.Json')
        drawer = DependencyDrawer('test_config.xml')
        drawer.run()

        with open(f'dependencies.dot') as file:
            dot_content = file.read()
        
        packages = {
            '.NETStandard 1.0', '.NETStandard 1.3', 
            'System.Runtime.Serialization.Formatters', 'System.Runtime.Serialization.Primitives',
            'Microsoft.CSharp', 'System.Xml.XmlDocument', 'System.ComponentModel.TypeConverter'
        }
        for package in packages:
            self.assertIn(package, dot_content)

    def test_2(self):
        self.create_test_config('https://www.nuget.org/packages/Microsoft.Extensions.DependencyInjection')
        drawer = DependencyDrawer('test_config.xml')
        drawer.run()

        with open(f'dependencies.dot') as file:
            dot_content = file.read()
        
        packages = {
            '.NETFramework 4.6.2', '.NETStandard 2.0', '.NETStandard 2.1', 'net6.0', 'net7.0', 'net8.0',
            'Microsoft.Bcl.AsyncInterfaces', 'Microsoft.Extensions.DependencyInjection.Abstractions',
            'System.Threading.Tasks.Extensions'
        }
        for package in packages:
            self.assertIn(package, dot_content)
    
    def tearDown(self):
        files_to_remove = ['test_config.xml', 'dependencies.dot', 'dependencies.png']
        for file in files_to_remove:
            if os.path.exists(file):
                os.remove(file)

if __name__ == '__main__':
    unittest.main()
