'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from spython.logger import bot
import os
import sys

def execute(self, image=None, command=None, app=None, writable=False, contain=False):
    '''execute: send a command to a container
    
       Parameters
       ==========

       image: full path to singularity image
       command: command to send to container
       app: if not None, execute a command in context of an app
       writable: This option makes the file system accessible as read/write
       contain: This option disables the automatic sharing of writable
                        filesystems on your host

    '''

    cmd = self._init_command('exec')
    self.check_install()

    # If the image is given as a list, it's probably the command
    if isinstance(image, list):
        command = image
        image = None

    if command is not None:
        
        # No image provided, default to use the client's loaded image
        if image is None:
            image = self._get_uri()

        # Does the user want to run an app?
        if app is not None:
            cmd = cmd + ['--app', app]

        sudo = False
        if writable is True:
            sudo = True

        if not isinstance(command, list):
            command = command.split(' ')

        cmd = cmd + [image] + command
        return self._run_command(cmd,sudo=sudo)

    bot.error('Please include a command (list) to execute.')
