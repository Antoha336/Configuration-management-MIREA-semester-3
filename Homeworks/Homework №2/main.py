import os
import sys
import subprocess

from shutil import rmtree
from zipfile import ZipFile 
from xml.etree import ElementTree

class DependencyDrawer:
    def __init__(self, 
                 config_file_path: str) -> None:
        
        self.config_paht = config_file_path
        self.ns = {'nuspec': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
        self.__load_config()

    def __load_config(self) -> tuple[str, str]:
        tree = ElementTree.parse(self.config_paht)
        root = tree.getroot()

        graphviz_path = root.find('GraphvizPath').text
        if not os.path.isfile(graphviz_path):
            graphviz_path = 'dot'
        self.graphviz_path = graphviz_path

        package_path = root.find('PackagePath').text
        if not os.path.isfile(package_path):
            raise Exception("Package file not found")
        self.package_path = package_path

    def __analyze(self) -> tuple[str, str, list[tuple[str, str]]]:
        with ZipFile(self.package_path, 'r') as zip_ref:
            zip_ref.extractall('extracted_package')
        
        nuspec_file = [f for f in os.listdir('extracted_package') if f.endswith('.nuspec')][0]
        tree = ElementTree.parse(os.path.join('extracted_package', nuspec_file))
        root = tree.getroot()

        package_id = root.find("nuspec:metadata/nuspec:id", self.ns).text
        package_version = root.find("nuspec:metadata/nuspec:version", self.ns).text
        dependencies = []
        for group in root.findall(".//nuspec:group", self.ns):
            for dependency in group.findall("nuspec:dependency", self.ns):
                dep_name = dependency.attrib['id']
                dep_version = dependency.attrib['version']
                dependencies.append((dep_name, dep_version))
        
        rmtree('extracted_package')

        return package_id, package_version, dependencies
    
    def __render(self, 
                 package_name: str, 
                 package_version: str, 
                 dependencies: list[tuple[str, str]]) -> None:
        
        dot_graph = 'digraph G {\n'
        dot_graph += f'    "{package_name}" [label="{package_name}\\n{package_version}"];\n'
        for dep_name, dep_version in set(dependencies):
            dot_graph += f'    "{dep_name}" [label="{dep_name}\\n{dep_version}"];\n'
            dot_graph += f'    "{package_name}" -> "{dep_name}";\n'
        dot_graph += '}\n'
        
        with open(f'dependencies.dot', 'w') as f:
            f.write(dot_graph)
        
        subprocess.run([self.graphviz_path, '-Tpng', 'dependencies.dot', '-o', f'dependencies.png'])

    def run(self) -> None:
        package_name, package_version, dependencies = self.__analyze()
        self.__render(package_name, package_version, dependencies)
        print("Drawed successfully!")


def main(config_file_path):
    drawer = DependencyDrawer(config_file_path)
    drawer.run()
    
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python main.py <config_file_path>')
        sys.exit(1)
    
    main(sys.argv[1])
