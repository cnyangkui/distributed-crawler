# -*- encoding: utf-8 -*-
import os
from multiprocessing import Process
import time
import psutil
import signal

from geospider.control.spider_controller import init, run, delete, wait, scaner
from geospider.utils.mongodb_helper import connect_mongodb, ProcessDao, TaskDao


class ProcessController(object):
    def __init__(self, localhost):
        mongodb = connect_mongodb()
        self.processdao = ProcessDao(mongodb)
        self.taskdao = TaskDao(mongodb)
        self.localhost = localhost

    '''
        开始一个进程，开始任务
    '''

    def start_task(self, taskid, is_restart):
        processnum = self.taskdao.find_by_id(taskid)['processnum']
        # print(processnum)
        for i in range(0, processnum):
            init(taskid, is_restart)
            p = Process(name=taskid, target=run, args=(taskid,))
            p.start()
            print(p.pid)
            self.processdao.insert_process(self.localhost, p.pid, taskid, 'running')
            # self.process_list.append(p)

    '''
        唤醒一个暂停的任务，将暂停状态的任务重新启动
    '''

    def resume_task(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid:
                try:
                    ps = psutil.Process(p['pid'])
                    ps.resume()
                except:
                    continue
        self.processdao.update_status_by_localhost_and_taskid(self.localhost, taskid, 'running')

    '''
        唤醒一个阻塞的进程，将暂停状态的任务重新启动
    '''

    def resume_process(self, pid):
        try:
            print("唤醒进程%s" % (pid))
            ps = psutil.Process(pid)
            ps.resume()
            self.processdao.update_status_by_localhost_and_pid(self.localhost, pid, 'running')
        except:
            pass

    '''
        杀死一个进程，终止任务
    '''

    def terminate_task(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid and p['status'] != 'stopping':
                try:
                    print("杀死进程%s" % (p['pid']))
                    # p.terminate()
                    os.kill(p['pid'], signal.SIGKILL)
                except:
                    continue
        delete(taskid, True)
        self.processdao.delete_by_localhost_and_taskid(self.localhost, taskid)

    def terminate_process(self, pid):
        try:
            print("杀死进程%s" % (pid))
            # p.terminate()
            os.kill(pid, signal.SIGKILL)
            process_list = self.processdao.find_by_localhost_and_pid(self.localhost, pid)
            self.processdao.delete_by_localhost_and_pid(self.localhost, pid)
            if len(process_list) > 0:
                taskid = process_list[0]['taskid']
            self.taskdao.update_processnum(taskid)
        except:
            pass

    '''
        暂停进程，暂停任务
    '''

    def suspend_task(self, taskid):
        process_list = self.processdao.find_by_localhost_and_taskid(self.localhost, taskid)
        for p in process_list:
            if p['taskid'] == taskid and p['status'] != 'stopping':
                try:
                    ps = psutil.Process(p['pid'])
                    ps.suspend()
                except:
                    continue
        self.processdao.update_status_by_localhost_and_taskid(self.localhost, taskid, 'pausing')

    def suspend_process(self, pid):
        try:
            print("挂起进程%s" % (pid))
            ps = psutil.Process(pid)
            ps.suspend()
            self.processdao.update_status_by_localhost_and_pid(self.localhost, pid, 'pausing')
        except:
            pass

    '''
        休眠
    '''

    def sleep(self, taskid, t):
        process_list = self.processdao.find_all()
        for p in process_list:
            print(p['taskid'])
            if p['taskid'] == taskid:
                time.sleep(t)
                break

    '''
        查看所有的进程名
    '''

    def processes(self):
        process_list = self.processdao.find_all()
        for p in process_list:
            print(str(p['pid']) + " " + p['taskid'])

    '''
        开启一个进程，等待任务启动
    '''

    def wait_task(self, taskid, is_restart):
        processnum = self.taskdao.find_by_id(taskid)['processnum']
        for i in range(0, processnum):
            init(taskid, is_restart)
            p = Process(name=taskid, target=wait, args=(taskid,))
            p.start()
            print(p.pid)
            self.processdao.insert_process(self.localhost, p.pid, taskid, 'waitting')

    '''
        扫描所有进程，将到时间的进程杀死
    '''

    def scan_task(self):
        self.processdao.delete_by_localhost_and_status(self.localhost, 'scanner')
        p = Process(name='spider_scaner', target=scaner)
        p.start()
        self.processdao.insert_process(self.localhost, p.pid, '', 'scanner')


