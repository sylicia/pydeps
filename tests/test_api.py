#! /usr/bin/env python
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
import pytest


def test_load_projects_invalid_path():
    """Test loading projects from invalid path"""
    with pytest.raises(StopIteration):
        pydeps.load_projects('invalid_path')


def test_load_projects_empty_directory():
    """Test loading projects from invalid path"""
    with pytest.raises(pydeps.ArgumentError):
        pydeps.load_projects('tests/empty')


def test_load_projects():
    """Test loading projects"""
    pydeps.load_projects('tests/valid_projects')

    expected = [
        'PROJECT_1',
        'PROJECT_2',
        'PROJECT_3'
    ]
    assert sorted(pydeps.PROJECTS.keys()) == expected

    expected = [
        'PROJECT_1.WEBSITE.BACKEND',
        'PROJECT_1.WEBSITE.DATABASE',
        'PROJECT_1.WEBSITE.FRONTEND',
        'PROJECT_2.WEBSITE_v1.BACKEND',
        'PROJECT_2.WEBSITE_v1.DATABASE',
        'PROJECT_2.WEBSITE_v1.FRONTEND',
        'PROJECT_2.WEBSITE_v2.BACKEND',
        'PROJECT_2.WEBSITE_v2.ELASTICSEARCH',
        'PROJECT_2.WEBSITE_v2.FRONTEND',
        'PROJECT_3.API.DATABASE',
        'PROJECT_3.API.FRONTEND',
        'PROJECT_3.API.MEMCACHE'
    ]
    assert sorted(pydeps.COMPONENTS.keys()) == expected


def test_project_applications_list():
    expected = ['WEBSITE_v1', 'WEBSITE_v2']
    assert sorted(pydeps.PROJECTS['PROJECT_2'].applis.keys()) == expected


def test_get_project_application():
    assert pydeps.PROJECTS['PROJECT_3'].get_application('API').name == 'API'


def test_application_components_list():
    expected = ['BACKEND', 'DATABASE', 'FRONTEND']
    application = pydeps.PROJECTS['PROJECT_1'].applis['WEBSITE']
    assert sorted(application.components.keys()) == expected


def test_get_application_component():
    application = pydeps.PROJECTS['PROJECT_3'].applis['API']
    assert application.get_component('DATABASE').id == 'PROJECT_3.API.DATABASE'


def test_project_id():
    assert pydeps.PROJECTS['PROJECT_1'].id == 'PROJECT_1'


def test_project_name():
    assert pydeps.PROJECTS['PROJECT_1'].name == 'PROJECT_1'


def test_project_team():
    assert pydeps.PROJECTS['PROJECT_1'].team == ''
    assert pydeps.PROJECTS['PROJECT_2'].team == 'devs'


def test_project_domain():
    assert pydeps.PROJECTS['PROJECT_1'].domain == ''
    assert pydeps.PROJECTS['PROJECT_2'].domain == 'project2.test'


def test_project_user():
    assert pydeps.PROJECTS['PROJECT_1'].user['owner'] == 'www-data'
    assert pydeps.PROJECTS['PROJECT_1'].user['group'] == 'www-data'
    assert pydeps.PROJECTS['PROJECT_3'].user['owner'] == 'me'
    assert pydeps.PROJECTS['PROJECT_3'].user['group'] == 'adm'


def test_application_id():
    application = pydeps.PROJECTS['PROJECT_1'].applis['WEBSITE']
    assert application.id == 'PROJECT_1.WEBSITE'


def test_application_name():
    application = pydeps.PROJECTS['PROJECT_1'].applis['WEBSITE']
    assert application.name == 'WEBSITE'


def test_graph_project_customization():
    assert not len(pydeps.PROJECTS['PROJECT_1'].dot['custom'].keys())
    project = pydeps.PROJECTS['PROJECT_2']
    assert project.dot['custom']['fillcolor'] == 'lightsteelblue1'
    assert project.dot['custom']['color'] == 'royalblue4'


def test_graph_application_customization():
    application = pydeps.PROJECTS['PROJECT_1'].applis['WEBSITE']
    assert not len(application.dot['custom'].keys())

    application = pydeps.PROJECTS['PROJECT_2'].applis['WEBSITE_v1']
    assert application.dot['custom']['fillcolor'] == 'lightsteelblue1'
    assert application.dot['custom']['color'] == 'royalblue4'

    application = pydeps.PROJECTS['PROJECT_2'].applis['WEBSITE_v2']
    assert application.dot['custom']['fillcolor'] == 'lemonchiffon'
    assert application.dot['custom']['color'] == 'darkgoldenrod'


def test_component_id():
    application = pydeps.PROJECTS['PROJECT_3'].applis['API']
    assert application.components['FRONTEND'].id == 'PROJECT_3.API.FRONTEND'


def test_component_name():
    application = pydeps.PROJECTS['PROJECT_3'].applis['API']
    assert application.components['FRONTEND'].name == 'FRONTEND'


def test_component_parents():
    assert not len(pydeps.COMPONENTS['PROJECT_2.WEBSITE_v1.DATABASE'].parents)
    expected = [
        'PROJECT_2.WEBSITE_v1.DATABASE',
        'PROJECT_2.WEBSITE_v2.ELASTICSEARCH',
        'PROJECT_3.API.FRONTEND'
    ]
    compo = 'PROJECT_2.WEBSITE_v2.BACKEND'
    result = [parent.id for parent in pydeps.COMPONENTS[compo].parents]
    assert sorted(result) == expected


def test_component_childs():
    assert not len(pydeps.COMPONENTS['PROJECT_2.WEBSITE_v2.BACKEND'].childs)
    expected = [
        'PROJECT_2.WEBSITE_v1.BACKEND',
        'PROJECT_2.WEBSITE_v1.FRONTEND',
        'PROJECT_2.WEBSITE_v2.BACKEND'
    ]
    compo = 'PROJECT_2.WEBSITE_v1.DATABASE'
    result = [parent.id for parent in pydeps.COMPONENTS[compo].childs]
    assert sorted(result) == expected
