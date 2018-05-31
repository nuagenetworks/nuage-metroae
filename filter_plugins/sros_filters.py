#!/usr/bin/python

# Copyright 2017 Nokia
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.


import re


def rm_insignificant_lines(in_cfg):
    """
    Remove insignificant lines from input config file.
    These lines are starting with '#' or 'echo'
    :param in_cfg: cfg as a multiline string
    :return: cleanified array of config lines
    """
    cfg_arr = in_cfg.splitlines()
    # make a dup array for in-place deletion
    for line in list(cfg_arr):
        if not is_cfg_statement(line):
            cfg_arr.remove(line)
    return cfg_arr


def is_cfg_statement(line):
    # if line is empty, or first elements are not spaces
    # consider this line for deletion
    line = line.lstrip()
    if line.strip() == '' or line.startswith('#') or line.startswith('echo'):
        return False
    else:
        return True


def rootify(clean_cfg):
    cfg_string = ['configure']
    rootified_cfg = []
    # init previous indent level as 0 for /configure line
    ind_level = [-1]

    for i, line in enumerate(clean_cfg):
        if line.strip().startswith('exit all'):
            cfg_string = []
            ind_level = [-1]
            continue
        if line.strip() == 'exit':
            cfg_string.pop()
            ind_level.pop()
            continue

        # calc current indent
        prev_ind_level = ind_level[-1]
        cur_ind_level = len(line) - len(line.lstrip())
        # append a command if it is on a next level of indent
        if cur_ind_level > prev_ind_level:
            cfg_string.append(line.strip())
            ind_level.append(cur_ind_level)
        # if a command on the same level of indent
        # we delete the prev. command and append the new one to the base string
        elif cur_ind_level == prev_ind_level:
            cfg_string.pop()
            # removing (if any) `customer xxx create` or `create` at the end
            # of the line since it was previously printed out
            cfg_string[-1] = re.sub('\scustomer\s\d+\screate$|\screate$',
                                    '', cfg_string[-1])
            cfg_string.append(line.strip())

        # if we have a next line go check it's indent value
        if i < len(clean_cfg) - 1:
            next_ind_level = len(
                clean_cfg[i + 1]) - len(clean_cfg[i + 1].lstrip())
            # if a next ind level is deeper (>) then we can continue
            # accumulation of the commands
            if next_ind_level > cur_ind_level:
                continue
            # if the next level is the same or lower, we must save a line
            else:
                rootified_cfg.append(' '.join(cfg_string))
        else:
            # otherwise we have a last line here, so print it
            rootified_cfg.append(' '.join(cfg_string))

    return rootified_cfg


def sros_rootify(input_cfg_file):
    ''' Given a string representation of the output of
    '''

    clean_cfg = rm_insignificant_lines(input_cfg_file)
    return rootify(clean_cfg)


class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'sros_rootify': sros_rootify
        }
