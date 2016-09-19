#!/usr/bin/env python
import subprocess
import os
import tempfile

def exec_shell_result(cmd):
    p = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return_code = p.wait()
    result = None
    if return_code == 0:
        result = p.stdout.readline().strip()
    else:
        LOG.error("host exec subbprocess < %s >error!" %cmd)
    return result


def check(data=True):
    cmd='''grep -nr "FAIL" /var/log/crawler/*.* | awk -F':' '{print $4}' | awk -F'=>' '{print $1}' >tmp.txt'''
    result=exec_shell_result(cmd)
    lines = []
    with open('./tmp.txt') as tmp:
        lines = ["http:%s" %url.strip() for url in tmp.readlines()]
    if data:
        return lines
    else:
        return len(lines)


if __name__ == '__main__':
    print check(data=False)
