from Node import Node
from Tree import Tree
from TreeParser import TreeParser

import os
import json
import subprocess
import xml.etree.ElementTree as XMLParser

JAVA_COMPILE = "jar"
TRAVIS_LOG_FILE = "raw-output.txt"
DEPENDENCY_CONNECTOR = ":"

MAVEN_PACKAGE_MANAGER = "mvn"
MAVEN_POM_FILE_NAME = "pom.xml"
MAVEN_NAMESPACE = "{http://maven.apache.org/POM/4.0.0}"
MAVEN_LOG_PREFIX = "[INFO] "
MAVEN_ENDLING_LINE = "[INFO] ------------------------------------------------------------------------"

GRADLE_PACKAGE_MANAGER = "gradle"
GRADLE_BUILD_FILE_NAME = "build.gradle"
GRADLE_CONFIG_MODE = "compile"
GRADLE_LOG_PREFIX = ""
GRADLE_CONNECTOR = " - "
GRADLE_STARTING_LINE = "Dependencies for source set 'main' (deprecated, use 'implementation ' instead)."
GRADLE_ENDLING_LINE = "\n"

class TreeBuilder:
    def __init__(self, data, rootName, starting_line, ending_line, package_manager):
        self.data = data
        self.rootName = rootName
        self.starting_line = starting_line
        self.ending_line = ending_line
        self.root = Node(self.rootName)
        self.tree = Tree(self.root, package_manager)

    def computeLevel(self, rawNode):
        level = 1
        for c in rawNode:
            if(c == '|'):
                level = level + 1
            elif(c == '+' or c == '\\'):
                break
        return level

    def build(self):
        nodeList = TreeParser(self.data, self.rootName, self.starting_line, self.ending_line).parse()
        parent = self.root

        for rawNode in nodeList:
            level = self.computeLevel(rawNode)
            child = Node(rawNode)
            while(parent.getLevel() >= level):
                parent = parent.getParent()
            parent.addChild(child)
            parent = child

        return self.tree




class Project(object):
    def __init__(self, group_id, artifact_id, version, package_manager, config_mode, packaging):
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version
        self.package_manager = package_manager
        self.config_mode = config_mode
        self.parent = None
        self.packaging = packaging

        self._id = None

    @property
    def id(self):
        if self._id is None:
            self._id = (self.group_id, self.artifact_id)
        return self._id

    def get_root_name(self):
        if self.package_manager == MAVEN_PACKAGE_MANAGER:
            return MAVEN_LOG_PREFIX + self.group_id + DEPENDENCY_CONNECTOR + \
                    self.artifact_id + DEPENDENCY_CONNECTOR + \
                    JAVA_COMPILE + DEPENDENCY_CONNECTOR + self.version
        if self.package_manager == GRADLE_PACKAGE_MANAGER:
            return GRADLE_LOG_PREFIX+self.group_id + DEPENDENCY_CONNECTOR + \
                    DEPENDENCY_CONNECTOR + self.version
    
    def get_starting_line(self):
        if self.package_manager == MAVEN_PACKAGE_MANAGER:
            return MAVEN_LOG_PREFIX + self.group_id + DEPENDENCY_CONNECTOR + \
                    self.artifact_id + DEPENDENCY_CONNECTOR + \
                    self.packaging + DEPENDENCY_CONNECTOR + self.version
        if self.package_manager == GRADLE_PACKAGE_MANAGER:
            return GRADLE_LOG_PREFIX + self.config_mode + GRADLE_CONNECTOR + \
            GRADLE_STARTING_LINE
    
    def get_endling_line(self):
        if self.package_manager == MAVEN_PACKAGE_MANAGER:
            return MAVEN_ENDLING_LINE
        if self.package_manager == GRADLE_PACKAGE_MANAGER:
            return GRADLE_ENDLING_LINE

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

def main(current_path):
    project = initialize_project(current_path[0])
    if project is None:
        print("cannot find project")
        return
    root_name = project.get_root_name()
    ending_line = project.get_endling_line()
    starting_line = project.get_starting_line()
    package_manager = project.package_manager
    print(root_name)
    print(ending_line)
    print(starting_line)
    print(package_manager)
    generate_package_manager_log(project)
    data_file_path = os.path.join(current_path[0],TRAVIS_LOG_FILE)
    if os.path.isfile(data_file_path):
        print('datafile exists')
        data_file = TRAVIS_LOG_FILE
        tree = TreeBuilder(data_file, root_name, starting_line, ending_line, package_manager).build()
        tree_data = tree.buildWithChildrenToDict(False)

        with open('dependency-tree.json', 'w') as outfile:
            json.dump(tree_data, outfile)


def initialize_project(current_path):
    # find pom file in current folder
    init_project=None

    pom_file_path = os.path.join(current_path,MAVEN_POM_FILE_NAME)
    gradle_file_path = os.path.join(current_path,GRADLE_BUILD_FILE_NAME)

    if os.path.isfile(pom_file_path):
        init_project = get_project_from_pom(pom_file_path)
    elif os.path.isfile(gradle_file_path):
        init_project = get_project_from_gradle(gradle_file_path)
    return init_project


def get_project_from_pom(pom_path):
    pom = XMLParser.parse(pom_path)
    root = pom.getroot()
    group_id = ''
    artifact_id = ''
    version = ''
    package_manager = MAVEN_PACKAGE_MANAGER
    config_mode = None
    packaging = JAVA_COMPILE
    for item in root.getchildren():
        if item.tag == MAVEN_NAMESPACE + 'groupId':
            group_id = item.text
        if item.tag == MAVEN_NAMESPACE + 'artifactId':
            artifact_id = item.text
        if item.tag == MAVEN_NAMESPACE + 'version':
            version = item.text
        if item.tag == MAVEN_NAMESPACE + 'packaging':
            packaging = item.text

    if group_id is None:
        raise Exception('Missing groupId')
    if artifact_id is None:
        raise Exception('Missing artifactId')
    if version is None:
        raise Exception('Missing artifactId')

    project = Project(group_id, artifact_id, version, package_manager, config_mode, packaging)

    return project

def get_project_from_gradle(gradle_path):
    # pom = XMLParser.parse(gradle_path)
    # root = pom.getroot()
    group_id = "com.test.name"
    artifact_id = None
    version = "0.1.0.snapshot"
    package_manager = GRADLE_PACKAGE_MANAGER
    config_mode = GRADLE_CONFIG_MODE
    packaging = JAVA_COMPILE

    project = Project(group_id, artifact_id, version, package_manager, config_mode, packaging)

    return project

def generate_package_manager_log(project):
    print('-----------------generate_package_manager_log--------------------')
    if project.package_manager == MAVEN_PACKAGE_MANAGER:
        result = subprocess.run(['mvn','-B','dependency:tree'], stdout=subprocess.PIPE).stdout.decode('utf-8')
        with open(TRAVIS_LOG_FILE, 'w') as outfile:
            outfile.write(result)
        return True
    if project.package_manager == GRADLE_PACKAGE_MANAGER:
        result = subprocess.run(['gradle','dependencies', '--configuration', project.config_mode], stdout=subprocess.PIPE).stdout.decode('utf-8')
        with open(TRAVIS_LOG_FILE, 'w') as outfile:
            outfile.write(result)
        return True
    return False

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])

