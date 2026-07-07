import logging
import logging.handlers
import queue
import threading
import time

def setup_async_logging():
    log_queue = queue.Queue(-1)  
    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler("app.log", encoding="utf-8")

    formatter = logging.Formatter('%(asctime)s [%(levelname)s] (%(threadName)s) %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    listener = logging.handlers.QueueListener(log_queue, console_handler, file_handler)
    listener.start()  

    queue_handler = logging.handlers.QueueHandler(log_queue)


    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(queue_handler)

    return listener


if __name__ == "__main__":

    log_listener = setup_async_logging()
    
    logger = logging.getLogger("main_app")

    def worker_task(task_name):
        for i in range(3):
            logger.info(f"Task {task_name} đang xử lý bước {i}")
            time.sleep(0.1)

    print("finished, terminate listener...")
    log_listener.stop()