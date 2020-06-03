#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 51desk.com. All rights reserved.
#
# @author: ChenXiao <xavier.chen@51desk.com>
# Created on 2, Mar, 2016
#

import datetime


class Code(object):
    UNKNOWN = 0
    READY = 1
    RUNNING = 2
    PAUSED = 3
    FINISHED = 4
    TERMINATED = 5

    state_dict = {
        UNKNOWN: "UNKNOWN",
        READY: "READY",
        RUNNING: "RUNNING",
        PAUSED: "PAUSED",
        FINISHED: "FINISHED",
        TERMINATED: "TERMINATED"
    }


class BaseState(object):
    state_code = Code.UNKNOWN

    def __init__(self, runner=None, listener=None, last_state=None):
        if None == last_state:
            self.runner = runner
            self.listener = listener
            self.started_time = 0
            # self.paused_time = 0
            # self.resumed_time = 0
            self.terminated_time = 0
            self.finished_time = 0
            self.last_state_code = Code.UNKNOWN
        else:
            self.runner = last_state.runner
            self.listener = last_state.listener
            self.last_state_code = last_state.state_code

            self.started_time = last_state.started_time
            # self.resumed_time = last_state.resumed_time
            # self.paused_time = last_state.paused_time
            self.finished_time = last_state.finished_time
            self.terminated_time = last_state.terminated_time

            # 触发状态转换
            if self.listener:
                self.listener.on_state(self)

    def get_code(self):
        return self.state_code

    def start(self):
        pass

    # def pause(self):
    #     pass
    #
    # def resume(self):
    #     pass

    def terminate(self):
        pass

    def finish(self):
        pass

    @staticmethod
    def make_cannot_msg(my_state, target):
        return "I am in %s stated, can not be %s!" % (my_state, target)


def deco_msg(msg):

    def on_msg(fn):
        def real_deco(*args, **kwargs):
            fn(*args, **kwargs)
            if args[0].listener is not None:
                args[0].listener.on_msg(msg)
        return real_deco

    return on_msg


class ReadyState(BaseState):
    state_code = Code.READY

    def __init__(self, *args, **kwargs):
        super(ReadyState, self).__init__(*args, **kwargs)

    def start(self):
        self.started_time = datetime.datetime.now()
        self.runner.set_state(RunningState(last_state=self))
        self.runner.job.start()

    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'paused'))
    # def pause(self):
    #     pass
    #
    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'resumed'))
    # def resume(self):
    #     pass

    def finish(self):
        self.finished_time = datetime.datetime.now()
        self.runner.set_state(FinishedState(last_state=self))

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'terminated'))
    def terminate(self):
        pass


class RunningState(BaseState):
    state_code = Code.RUNNING

    def __init__(self, *args, **kwargs):
        super(RunningState, self).__init__(*args, **kwargs)

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'started'))
    def start(self):
        # self.runner.check_state()
        pass

    # def pause(self):
    #     self.runner.set_state(PauseState(self))
    #     self.runner.job.pause()
    #     self.paused_time = datetime.datetime.now()
    #     self.resumed_time = 0
    #
    #
    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'resumed'))
    # def resume(self):
    #     pass

    def finish(self):
        self.finished_time = datetime.datetime.now()
        self.runner.set_state(FinishedState(last_state=self))

    def terminate(self):
        self.terminated_time = datetime.datetime.now()
        self.runner.set_state(TerminatedState(last_state=self))
        self.runner.job.terminate()


# class PauseState(BaseState):
#     state_code = Code.PAUSED
#
#     def __init__(self, *args, **kwargs):
#         super(PauseState, self).__init__(*args, **kwargs)
#
#     def start(self):
#         self.resume()
#
#     @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'paused'))
#     def pause(self):
#         pass
#
#     def resume(self):
#         self.runner.set_state(RunningState(self))
#         self.runner.job.resume()
#         self.resumed_time= datetime.datetime.now()
#
#
#     def terminate(self):
#         self.runner.set_state(TerminatedState(self))
#         self.runner.job.terminate()
#
#         self.terminated_time = datetime.datetime.now()

class FinishedState(BaseState):
    state_code = Code.FINISHED

    def __init__(self, *args, **kwargs):
        super(FinishedState, self).__init__(*args, **kwargs)

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'started'))
    def start(self):
        pass

    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'paused'))
    # def pause(self):
    #     pass
    #
    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'resumed'))
    # def resume(self):
    #     pass

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'terminated'))
    def terminate(self):
        pass


class TerminatedState(BaseState):
    state_code = Code.TERMINATED

    def __init__(self, *args, **kwargs):
        super(TerminatedState, self).__init__(*args, **kwargs)

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'started'))
    def start(self):
        pass

    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'paused'))
    # def pause(self):
    #     pass
    #
    # @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'resumed'))
    # def resume(self):
    #     pass

    @deco_msg(msg=BaseState.make_cannot_msg(Code.state_dict[state_code], 'terminated'))
    def terminate(self):
        pass
