from threading import Lock
type Args = list[object] | tuple[object,...]
type Kwargs = dict[str,object]
class Box[T]:
    __inner:T
    def __init__(self,value:T) -> None:
        self.__inner = value
    @property
    def value(self):
        return self.__inner

    @value.setter
    def value(self, val):
        self.__inner = val
class ThreadSafe[T]:
    __inner:Box[T]
    def __init__(self, value:T):
        self.__inner = Box(value)
        self.__lock = Lock()

    def __enter__(self):
        self.__lock.acquire()
        return self.__inner

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.__lock.release()



