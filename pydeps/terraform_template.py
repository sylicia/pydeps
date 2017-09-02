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


import logging
import pydeps
# from exceptions import DependencyError, ArgumentError
# import os
# from pprint import pprint

logger = logging.getLogger(__name__)


def terraform_userdata_flat(compo):
    """generate variables for text output

    :param Component compo: Component object
    :return str output: Output in flat format
    """
    output = '# Flat user-data usage\n'
    for parent_info in compo.parents_full:
        parent_key = '_'.join([parent_info[0].id.replace('.', '_'),
                               parent_info[1]])
        service_used = parent_info[1]
        if parent_info[1] not in pydeps.SERVICES:
            service_used = 'default'

        for service_keys in pydeps.SERVICES[service_used]:
            var_name = '_'.join([parent_key, service_keys])
            line = '%s=${%s}' % (var_name, var_name)
            output = '\n'.join([output, line])

    return '{}\n'.format(output)


def generate_userdata(compo_id, output_path, output_format):
    """Generate userdata template

    The format can be selected and it supports to write user-data information
    in a file or in stdout.

    :param str compo_id: Component identifier
    :param str output_path: Path of the output file
    :param str output_format: Format of the output file
    """
    compo = pydeps.get_component(compo_id)
    if output_format == 'flat':
        output_content = terraform_userdata_flat(compo)
    else:
        print('not yet implemented')
        output_content = ''

    if output_path == 'stdout':
        print(output_content)
    else:

        with open(output_path, 'w') as dot:
            dot.write(output_content)
            dot.close()




