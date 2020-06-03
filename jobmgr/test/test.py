#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 51desk.com. All rights reserved.
#
# @author: ChenXiao <xavier.chen@51desk.com>
# Created on 2, Mar, 2016
#

from jobmgr import job, state, jobmgr, listener

import time
# from gevent import monkey
# monkey.patch_all()


class TestJob(job.Job, listener.Listener):

    def __init__(self, sign):
        super(TestJob, self).__init__()
        self.sign = sign

    # job
    def start(self):
        times = 0

        while True:
            job_state = self.runner.get_state_code()
            if job_state == state.Code.TERMINATED or job_state == state.Code.FINISHED or times == 15:
                break

            time.sleep(1)
            times += 1
            print("[%s] I am running %d times" % (self.ID, times))

        print("")

    # def pause(self):
    #     pass
    #
    # def resume(self):
    #     pass

    def terminate(self):
        print("[%s] I am dead!" % self.ID)
        pass

    # listener
    def on_state(self, st):
        print("[%s] state changed from %s to %s" \
              % (self.ID, state.Code.state_dict[st.last_state_code], state.Code.state_dict[st.state_code]))

    def on_msg(self, msg):
        print("[%s] MSG: %s" % (self.ID, msg))

    def on_exception(self, e):
        print("[%s] Exception: %s" % (self.ID, e.msg))


if __name__ == "__main__":
    jobmgr.init()
    jm = jobmgr.instance()

    # 创建任务标识，可以作为 user id 等
    tj = TestJob("user1")
    tj2 = TestJob("user2")
    tj3 = TestJob("user3")



    # 提交任务并执行任务
    jid1, runner1 = jm.commit_job(tj)
    runner1.start()
    #
    print(jid1, "hello")
    #
    # jid2, runner2 = jm.commit_job(tj2)
    # runner2.start()
    #
    # print(jid2)
    #
    # jid3, runner3 = jm.commit_job(tj3)
    # runner3.start()
    #
    # print(jid3)
    #
    # time.sleep(5)
    #
    # # 获取所有任务信息
    # res = jm.get_job_status()
    # print(res)
    #
    # # 结束任务
    # jm.get_job(jid1).terminate()
    #
    # # 获取标识为 user2 的任务信息
    # res = jm.get_job_status(sign="user2")
    # print(res)
    #
    # # 获取标 id 为 jid3 的任务信息
    # res = jm.get_job_status(jid3)
    # print(res)
    #
    # time.sleep(5)
    # jm.get_job(jid2).terminate()
    #
    # time.sleep(10)
    # jm.get_job(jid3).terminate()

