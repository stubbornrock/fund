import sys
if __name__ == '__main__':
    total = 4978
    PROCESS_NUM = 500
    count = (total/PROCESS_NUM)+1
    for i in range(count):
        process_name = "process_%d" %i
        process_codes_start=i*PROCESS_NUM
        process_codes_end=i*PROCESS_NUM+PROCESS_NUM
        start = 0
        end = 0
        if process_codes_start <= total:
            start = process_codes_start
            if process_codes_end <= total:
                end = process_codes_end
            else:
                end = total
        print "%s->%s" %(start,end)
