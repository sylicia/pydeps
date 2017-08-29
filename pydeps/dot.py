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


import pydeps
from pprint import pprint


class Graph(object):
    def __init__(self, title, output):
        self.title = title
        self.output = output
        self.clusters = {}
        self.links = {}

    def add_project_cluster(self, project_id, components=()):
        """ Add a dot cluster definition for a project

        It creates the cluster structure with all applications and components by
        default but you can also specify a component in parameters.

        :param Project project: Project to look for
        :param list components: Filter on a list specified components
        """
        project = pydeps.PROJECTS[project_id]
        self.clusters[project_id] = Cluster(project, components)



    @property
    def struct(self):
        graph_def = {
            'title': self.title,
            'clusters': {}
        }
        for c_name, c_info in self.clusters.items():
            graph_def['clusters'] = c_info.struct

        return graph_def

    def write_dot_file(self, dot_path):
        pass


class Cluster(object):
    def __init__(self, obj, components=()):
        self.label = obj.name
        self.id = obj.id
        self.clusters = {}
        self.nodes = {}
        self.display = obj.dot['custom']
        self.source_ref = obj

        try:
            if len(components) == 0:
                for appli in obj.applis.values():
                    self.clusters[appli.id] = Cluster(appli)
                    for compo in appli.components.values():
                        self.add_node(compo)
            else:
                external_components = {}
                for compo in components:
                    if compo.appli.name not in external_components.items():
                        external_components[compo.appli.name] = []
                    external_components[compo.appli.name].append(compo)
                for compo_list in external_components.values():
                    for compo in compo_list:
                        self.add_node(compo)
        except:
            pass

    def add_project_cluster(self):
        pass

    def add_node(self, obj):
        self.nodes[obj.id] = Node(obj)

    @property
    def struct(self):
        return {
            'label': self.label
        }


class Node(object):
    def __init__(self, obj):
        self.source_ref = obj
        self.label = obj.name
        self.id = obj.id
        self.shape = ''
        self.style = 'filled'

    @property
    def struct(self):
        pass


def generate_detailed_graph(project_id, output):
    graph = Graph('Detailed dependencies for {}'.format(project_id), output)
    graph.add_project_cluster(project_id)
    pprint(graph.struct)
