import threading


def process_request(task:str):
    print(f"定时任务执行中。。。。。{task}")

timer = threading.Timer(2, process_request,args=["task"])

timer.start()