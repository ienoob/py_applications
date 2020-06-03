#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 51desk.com. All rights reserved.
#
# @author: ChenXiao <xavier.chen@51desk.com>
# Created on 2, Mar, 2016
#
from jobmgr.job import ThreadJobRunner
from jobmgr import listener
from jobmgr import state
import copy
import threading


def singleton(cls, *args, **kw):
    """ 单例模式装饰器
    """
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


class BaseJobMgr(object):
    """ 任务管理器的基类
    """
    workers = dict()

    def __init__(self, cache_server):
        """ 任务管理器构造函数

            :arg
                cache_server: redis 的连接器

        """
        self.cache_server = cache_server

    def commit_job(self, job, ln=None):
        pass

    def get_job(self, job_id):
        return self.workers[job_id]

    def lock(self):
        pass

    def release_lock(self):
        pass

    def get_job_status(self, jid="", sign=""):
        result = dict()

        def mk_res(j):
            return {
                'sign': j.get_sign(),
                'state': copy.copy(j.get_state().__dict__)
            }

        self.lock()
        if jid == "":
            for k, v in self.workers.items():
                if v.get_state_code() not in [state.Code.TERMINATED, state.Code.FINISHED] \
                        and (sign == "" or v.get_sign().startswith(sign)):
                    result[k] = mk_res(v)
        else:
            if jid in self.workers \
                    and self.workers[jid].get_state_code() not in [state.Code.TERMINATED, state.Code.FINISHED]:
                result = mk_res(self.workers[jid])

        self.release_lock()
        return result


class ThreadJobMgr(BaseJobMgr):
    """ 基于线程的任务管理器
    """
    def __init__(self, *args, **kwargs):
        super(ThreadJobMgr, self).__init__(*args, **kwargs)
        self.mutex = threading.Lock()

    def lock(self):
        self.mutex.acquire()

    def release_lock(self):
        self.mutex.release()

    def commit_job(self, job, ln=None):
        """ 提交一个任务

            :arg:
                job: 要提交执行的任务
        """
        # worker = threading.Thread(target=job.run)

        if isinstance(job, listener.Listener):
            ln = job

        runner = ThreadJobRunner(job, ln)
        job.set_runner(runner)

        self.lock()
        self.workers[job.ID] = runner
        self.release_lock()

        return job.ID, runner


# 每个进程中只有一个 _jobmgr
_jobmgr = 0


def init(cache_server=None, generator="thread"):
    global _jobmgr
    if _jobmgr == 0:
        if generator == "thread".lower():
            _jobmgr = ThreadJobMgr(cache_server)
    else:
        raise Exception("The job manager type is not supported!")


def instance():
    if _jobmgr != 0:
        return _jobmgr
    else:
        raise Exception("The job manager has not initialized yet!")

