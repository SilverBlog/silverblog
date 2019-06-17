# whiptail.py - Use whiptail to display dialog boxes from shell scripts
# Copyright (c) 2013 by Marwan Alsabbagh and contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#
# * The names of the contributors may not be used to endorse or
#   promote products derived from this software without specific
#   prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# Reall Computer modified 20171210

import itertools
import os
import shlex
import sys
from collections import namedtuple
from subprocess import Popen, PIPE

Response = namedtuple('Response', 'returncode value')

def flatten(data):
    return list(itertools.chain.from_iterable(data))



class Whiptail(object):
    def __init__(self, title='', backtitle='', height=0, width=0,
                 auto_exit=True):
        self.title = title
        self.backtitle = backtitle
        self.height = height
        self.width = width
        self.auto_exit = auto_exit
        self.command = None
        if os.system("command -v whiptail > /dev/null 2>&1") << 8 == 0:
            self.command = 'whiptail'
        if self.command is None:
            print("Please check if newt is installed.")
            exit(1)

    def run(self, control, msg, extra=(), exit_on=(1, 255)):

        cmd = [
            self.command, '--title', self.title, '--backtitle', self.backtitle,
            '--' + control, msg, str(self.height), str(self.width)
        ]
        cmd += list(extra)
        p = Popen(cmd, stderr=PIPE)
        out, err = p.communicate()
        if self.auto_exit and p.returncode in exit_on:
            print('User cancelled operation.')
            sys.exit(p.returncode)
        return Response(p.returncode, err)

    def prompt(self, msg, default='', password=False):
        control = 'passwordbox' if password else 'inputbox'
        return self.run(control, msg, [default]).value.decode("utf-8")

    def confirm(self, msg, default='yes'):
        defaultno = '--defaultno' if default.lower() == 'no' else ''
        return self.run('yesno', msg, [defaultno], [255]).returncode == 0

    def alert(self, msg):
        self.run('msgbox', msg)

    def alert_muilt_line(self, msg):
        self.run('msgbox', msg, ['--scrolltext'])

    def view_file(self, path):
        self.run('textbox', path, ['--scrolltext'])

    def calc_height(self, msg):
        height_offset = 8 if msg else 7
        return [str(self.height - height_offset)]

    def menu(self, msg='', items=(), prefix=' - '):
        if isinstance(items[0], str):
            items = [(i, '') for i in items]
        else:
            items = [(k, prefix + v) for k, v in items]
        extra = self.calc_height(msg) + flatten(items)
        return self.run('menu', msg, extra).value.decode("utf-8")

    def showlist(self, control, msg, items, prefix):
        if isinstance(items[0], str):
            items = [(i, '', 'OFF') for i in items]
        else:
            items = [(k, prefix + v, s) for k, v, s in items]
        extra = self.calc_height(msg) + flatten(items)
        return shlex.split(self.run(control, msg, extra).value.decode("utf-8"))

    def radiolist(self, msg='', items=(), prefix=' - '):
        return self.showlist('radiolist', msg, items, prefix)

    def checklist(self, msg='', items=(), prefix=' - '):
        return self.showlist('checklist', msg, items, prefix)
