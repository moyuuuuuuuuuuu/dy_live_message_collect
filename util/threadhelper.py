import threading


def createThread(func=None, name=None, args=()):
    t = threading.Thread(target=func, name=name, args=args)
    t.setDaemon(True)
    t.start()
