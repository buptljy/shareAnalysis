#coding=utf8
import asyncio
import time
import TushareTool
from pandas import DataFrame as df
from pandas import Series

class MultiThreadHelper(object):

    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.tst = TushareTool.TushareTool()

    @asyncio.coroutine
    def getLimitupStocks(self, args):
        date, code = args[0], args[1]
        print(code + " " + str(time.time()))
        # resultDF = yield from asyncio.ensure_future(self.tst.getHistoryDetails(date, code))
        resultDF = self.tst.getHistoryDetails(date, code)
        expectDF = df({"type": ["卖盘" for i in range(0, 10)]})["type"]
        print(code + " " + str(time.time()))
        if Series(resultDF).equals(expectDF):
            return code
        else:
            return None

    def runAsync(self, func, args):
        t1 = time.time()
        if func == "getLimitupStocks":
            tasks = [self.getLimitupStocks(arg) for arg in args]
        else:
            raise Exception("Wrong function name !")
        results = []
        # for task in tasks:
        #     result = yield from asyncio.wait_for(task, None)
        #     results.append(result)
        self.loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            result = yield from task
            results.append(result)
        t2 = time.time()
        print("Finish Async tasks, time cost: %s seconds" % str(t2 - t1))
        return results

    def stop(self):
        self.loop.stop()

    def close(self):
        self.loop.close()

