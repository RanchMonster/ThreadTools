from threading import Event, Thread, Lock,current_thread,main_thread
import os
from queue import Queue, Empty
from collections.abc import Callable
class ThreadPool:
    __threads:list[Thread]
    __task:Queue[tuple[Callable[...,object],Args,Kwargs]]
    __lock:Lock
    __shutdown:Event
    def __init__(self, count: int = os.cpu_count() or 4, daemon: bool = True) -> None:
        self.__threads: list[Thread] = []
        self.__shutdown = Event()
        self.__task = Queue()
        self.__lock = Lock()

        for x in range(count):
            t = Thread(target=self.__worker_loop, name=f"Pool Worker {x}", daemon=daemon)
            t.start()
            self.__threads.append(t)

    def __worker_loop(self):
        while True:
            if self.__shutdown.is_set() and self.__task.empty():
                return
            try:
                task, args, kwargs = self.__task.get(timeout=0.1)
                try:
                    task(*args, **kwargs)
                except Exception as e:
                    print(f"[Worker Error] {e}")
                self.__task.task_done()
            except Empty:
                continue

    def apply(self, target: Callable[..., object], *args, **kwargs) -> None:
        if self.__shutdown.is_set():
            raise RuntimeError("Cannot submit task to shutdown ThreadPool.")
        self.__task.put((target, args, kwargs))

    def shutdown(self, wait: bool = True) -> None:
        self.__accepting = False
        self.__shutdown.set()
        if wait:
            self.join()
        for t in self.__threads:
            t.join()
    def __len__(self):
        count = 0
        for x in self.__threads:
            if x.is_alive():
                count+=1
        return count
    def join(self):
        if current_thread() == main_thread():
            self.__worker_loop()
        else:
            return

