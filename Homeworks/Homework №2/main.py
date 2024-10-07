import os
import sys
import subprocess
import requests

from bs4 import BeautifulSoup
from shutil import rmtree
from zipfile import ZipFile 
from xml.etree import ElementTree

class DependencyDrawer:
    def __init__(self, config_file_path: str) -> None:
        self.ns = {'nuspec': 'http://schemas.microsoft.com/packaging/2013/05/nuspec.xsd'}
        self.graphviz_path = None
        self.package_url = None
        self.max_depth = None
        self.__load_config(config_file_path)

    def __load_config(self, config_file_path: str) -> tuple[str, str]:
        if not os.path.isfile(config_file_path):
            raise Exception('Configuration file not found')

        tree = ElementTree.parse(config_file_path)
        root = tree.getroot()

        graphviz_path = root.find('GraphvizPath').text
        if not os.path.isfile(graphviz_path):
            graphviz_path = 'dot'
        self.graphviz_path = graphviz_path

        package_url = root.find('PackagePath').text
        self.package_url = package_url

        max_depth = root.find('MaxDepth').text
        self.max_depth = int(max_depth)

    def __parse(self, package_url: str, depth: int = 1) -> dict[str: tuple[str, str]]:
        response = requests.get(package_url + '#dependencies-body-tab')
        print(package_url)
        if response.status_code != 200:
            raise Exception('HTML page parse error')
        
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')
        package_name = soup.find('span', {'class': 'title'}).text.strip()
        package_version = soup.find('span', {'class': 'version-title'}).text.strip()
        dependencies = dict()

        dependencies_div = soup.find('ul', {'id': 'dependency-groups'})
        if not dependencies_div:
            return package_name, package_version, dependencies
        
        dependencies_rows = dependencies_div.findAll('li', recursive=False)
        if dependencies_rows:
            for dependency_row in dependencies_rows:
                dependencies_group = dependency_row.find('h4').find('span').text.strip()
                dependencies_list = dependency_row.find('ul', recursive=False).findAll('li', recursive=False)
                for dependency in dependencies_list:
                    dependency_name = dependency.find('a')
                    if dependency_name:
                        dependency_link = dependency_name.get('href')
                        if dependency_link and depth + 1 <= self.max_depth:
                            dependency_dependencies = self.__parse('https://www.nuget.org' + dependency_link, depth + 1)[2]
                            dependencies.update(dependency_dependencies)
                        dependency_name = dependency_name.text.strip()
                        dependency_version = dependency.find('span').text.strip()
                        dependencies.setdefault(dependencies_group, set()).add((dependency_name, dependency_version))
                        

        return package_name, package_version, dependencies
    
    def __render(self, 
                 package_name: str, 
                 package_version: str, 
                 dependencies: dict[str: tuple[str, str]]) -> None:
        
        dot_graph = 'digraph G {\n'
        dot_graph += f'    "{package_name}" [label="{package_name}\\n{package_version}", shape=box, style=filled, fillcolor=lightblue];\n'
        for group, dependencies in dependencies.items():
            dot_graph += f'    "{group}" [shape=ellipse, style=filled, fillcolor=lightgray];\n'
            dot_graph += f'    "{package_name}" -> "{group}";\n'
            for dep_name, dep_version in dependencies:
                dot_graph += f'    "{dep_name}" [label="{dep_name}\\n{dep_version}", shape=box];\n'
                dot_graph += f'    "{group}" -> "{dep_name}";\n'
        dot_graph += '}\n'
        
        with open(f'dependencies.dot', 'w') as f:
            f.write(dot_graph)
        
        subprocess.run([self.graphviz_path, '-Tpng', 'dependencies.dot', '-o', f'dependencies.png'])

    def run(self) -> None:
        package_name, package_version, dependencies = self.__parse(self.package_url)
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
