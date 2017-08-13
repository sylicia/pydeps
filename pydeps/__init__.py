#
#    Application dependencies management (pydeps)
#
#    Copyright (C) 2017 Cyrielle Camanes (sylicia) <cyrielle.camanes@gmail.com>
#
#    This file is part of pydeps
#
#    This program is free software; you can redistribute it and/or
#    modify it under the terms of the GNU General Public License
#    as published by the Free Software Foundation; either version 2
#    of the License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program; if not, see <http://www.gnu.org/licenses/>.

from exceptions import DependenceError, ArgumentError
import logging

# files functions
import os
from pprint import pprint

try:
    from yaml import load, CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import load, Loader, Dumper


PROJECTS = {}
COMPONENTS = {}
DEPENDENCIES = {}

logger = logging.getLogger(__name__)


#
#   Classes
#
class Project(object):
    """Initialize a project

    :param str name: The name of the project
    :param dict info: Information that describes the project
    """
    def __init__(self, name, info={}):
        """Init method"""
        self.id = name
        self.name = name
        self.applis = {}
        self.domain = info.get('domain', '')
        self.team = info.get('team', '')
        self.dot = {
            'custom': info.get('graph_customization',{}),
            'invis_links': {}
        }

        if 'graph_hidden_links' in info:
            for parent, childs in info['graph_hidden_links'].iteritems():
                for child in childs:
                    self.dot['invis_links'][parent] = child

        if 'user' in info:
            self.user = info['user']
        else:
            self.user = {
                'owner': 'www-data',
                'group': 'www-data'
            }

    def __repr__(self):
        return self.id

    def add_application(self, appli_name, appli_info):
        """Add a new application in the project

        :param str appli_name: Application name
        :param dict appli_info: Application data
        """
        application = Application(appli_name, appli_info, self)
        self.applis[appli_name] = application

    def get_application(self, appli_target):
        """Look for a specific application

        :param str appli_target: Application name to look for
        :return: The application data as :class:`Application`
        """
        for appli_name, appli in self.applis.iteritems():
            if appli_name == appli_target:
                return appli


class Application(object):
    """Initialize an application

    :param str name: The name of the project
    :param dict info: Information that describes the application
    :param Project project: Reference tlo the parent project
    """
    def __init__(self, name, info, project):
        """Init method"""
        self.id = "{}_{}".format(project.name, name)
        self.name = name
        self.project = project
        self.components = {}
        self.dot = {
            'custom': {}
        }

        if 'graph_customization' in info:
            self.dot['custom'] = info['graph_customization']
        else:
            self.dot['custom'] = project.dot['custom']

        for component_name, component_info in info.iteritems():
            if isinstance(component_info, dict) and \
              component_name not in ['user',
                                     'graph_customization',
                                     'graph_hidden_links']:
                self.add_component(component_name, component_info)

    def __repr__(self):
        return self.id

    def add_component(self, component_name, component_info):
        """Add a component in the application

        :param str component_name: The name of the component
        :param dict component_info: Some information to create the component
        """
        component = Component(component_name,
                              component_info,
                              self)

        self.components[component_name] = component

    def get_component(self, component_target):
        """Look for a specific component

        :param str component_target: Component name to look for

        :return: The component object
        :rtype: Component
        """
        for component_name, component in self.components.iteritems():
            if component_name == component_target:
                return component


class Component(object):
    """Initialize a component

    :param str name: The name of the component
    :param dict info: Information that describes the component
    :param Application appli: Reference to the parent application
    """

    def __init__(self, name, info, appli):
        """Init method"""
        self.id = "{}_{}_{}".format(appli.project.name, appli.name, name)
        self.name = name
        self.appli = appli
        self._parent_components = []
        self.dot = {
            'custom': appli.dot['custom']
        }

        self.register_global()
        self.register_dependencies(info)

    def register_global(self):
        """Register component to a global dict.
        """
        COMPONENTS[self.id] = self

    def register_dependencies(self, info):
        """Register dependencies in local for parents and in global DEPENDENCES
        for childs
        """
        global DEPENDENCIES
        if 'dependencies' not in info:
            return

        for dep in info['dependencies']:
            # add parent dependencies
            try:
                self._parent_components.append((dep['marque'],
                                                dep['application'],
                                                dep['component'],
                                                dep['soft']))
            except KeyError as e:
                raise DependenceError(("Missing key {} to define dependencies "
                                       "for component {}").format(e, self.id)
                                      )

            # add child dependences
            parent_id = "{}_{}_{}".format(dep['marque'],
                                          dep['application'],
                                          dep['component'])

            if parent_id not in DEPENDENCIES:
                DEPENDENCIES[parent_id] = []

            DEPENDENCIES[parent_id].append(self)

    def __repr__(self):
        return self.id

    @property
    def parents(self):
        """Get parent components

        :return: List of components it depends on
        :rtype: list
        """
        comp_list = []
        for comp in self._parent_components:
            comp_id = "{}_{}_{}".format(comp[0], comp[1], comp[2])
            comp_list.append(COMPONENTS[comp_id])
        return comp_list

    @property
    def childs(self):
        """Get child components

        :return: List of components depending on it
        :rtype: list
        """
        return DEPENDENCIES.get(self.id, [])


#
#   Functions
#

def generate_path(path_list):
    """Generate a path for the current os

    :param list path_list: path of directories (and optionally file at the end)

    :return: path generated with the os separator
    :rtype: str
    """
    return os.sep.join(path_list)


def load_yaml_file(yaml_file):
    """Load YAML file in a python structure

    :param str yaml_file: path of the YAML file

    :return: python structure of YAML file
    :rtype: list
    """
    with file(yaml_file, 'r') as stream:
        yaml_load = load(stream, Loader=Loader)
    stream.close()

    return yaml_load


def load_projects(projects_path):
    """Load all project YAML files

    It modifies global dict PROJECTS

    :param str projects_path: YAML files directory
    """

    global PROJECTS

    # set projects location path
    project_names = os.listdir(projects_path)

    if len(project_names) == 0:
        raise ArgumentError("No project directory found")

    # setup projects
    for project_name in project_names:
        project_path = generate_path([projects_path, project_name])
        appli_files = os.listdir(project_path)
        try:
            file_id = appli_files.index('defaults.yml')
            default_file = appli_files.pop(file_id)

            default_path = generate_path([project_path, default_file])
            project_struct = load_yaml_file(default_path)
            PROJECTS[project_name] = Project(project_name, project_struct)
        except ValueError:
            PROJECTS[project_name] = Project(project_name)

        # setup applications
        for appli_file in appli_files:
            appli_path = generate_path([project_path, appli_file])
            appli_info = load_yaml_file(appli_path)
            appli_name = appli_file.replace('.yml', '')
            PROJECTS[project_name].add_application(appli_name, appli_info)
