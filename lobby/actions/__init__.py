#!/usr/bin/python
# -*- coding: utf-8 -*-

''' Lobby
    2011 - Gökmen Göksel <gokmeng:gmail.com> '''

# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.

import comar

class Action(object):

    def __init__(self, key):
        self.actionKey = key
        self.knownActions = []

    def run(self, action, *args):
        if hasattr(self, "_" + action):
            if args:
                return getattr(self, "_" + action)(args)
            else:
                return getattr(self, "_" + action)()
        else:
            return "No such %s method defined for %s Action !" % (action, self.actionKey)

class ActionServices(Action):

    def __init__(self):
        Action.__init__(self, "SERVER")
        self.link = comar.Link()

    def _listServices(self):
        return list(self.link.System.Service)

    def _isRunning(self, args):
        if service in self._listServices:
            if unicode(link.System.Service[args[0]].info()[2]) == "on":
                return "TRUE"
        return "FALSE"

class ActionPackages(Action):

    def __init__(self):
        Action.__init__(self, "PACKAGE")

