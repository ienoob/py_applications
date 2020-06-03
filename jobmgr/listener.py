#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 51desk.com. All rights reserved.
#
# @author: ChenXiao <xavier.chen@51desk.com>
# Created on 2, Mar, 2016
#


class Listener(object):
    def __init__(self):
        pass

    def on_state(self, st):
        pass

    def on_msg(self, msg):
        pass

    def on_exception(self, e):
        pass
