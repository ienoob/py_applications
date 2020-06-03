#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 51desk.com. All rights reserved.
#
# @author: ChenXiao <xavier.chen@51desk.com>
# Created on 2, Mar, 2016

from jobmgr import state
import uuid
import threading


class ThreadJobRunner(threading.Thread):
    def __init__(self, job, listener=None):
        super(ThreadJobRunner, self).__init__()
        self.job = job
        self._state = state.ReadyState(runner=self, listener=listener)
        self._started_time = 0
        self._paused_time = 0
        self._resumed_time = 0
        self._terminated_time = 0
        self._id = None
        self.job = job

    @property
    def ID(self):
        return self.job.ID

    def get_state(self):
        return self._state

    def set_state(self, st):
        self._state = st

    def get_state_code(self):
        return self._state.get_code()

    def get_sign(self):
        return self.job.get_sign()

    def run(self):
        self._state.start()
        self._state.finish()

    # def pause(self):
    #     self._state.pause()
    #
    # def resume(self):
    #     self._state.resume()

    def terminate(self):
        self._state.terminate()

    # def check_state(self):
    #     self.job.check_state()


class Job(object):
    def __init__(self):
        self._id = ""
        self.runner = None
        self.sign = ""

    @property
    def ID(self):
        if self._id is "":
            self._id = str(uuid.uuid4())

        return self._id

    def get_sign(self):
        return self.sign

    def set_runner(self, runner):
        self.runner = runner

    def start(self):
        pass

    # def pause(self):
    #     pass
    #
    # def resume(self):
    #     pass

    def terminate(self):
        pass

    def check_state(self):
        pass
