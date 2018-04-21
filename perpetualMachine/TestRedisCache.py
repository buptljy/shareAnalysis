import unittest
import RedisCache
import pandas as pd

class TestRedisCache(unittest.TestCase):


    def test_getStockListDetails(self):
        code_list = ["601009", "601015"]
        cache = RedisCache.RedisCache()
        result = cache.getStockListDetails(code_list, "2018-04-13")
        expect_list = [
            ["2018-04-13", "8.49", "8.33", "8.55", "8.31", "307346.0", "601009"],
            ['2018-04-13', "7.32", "7.62", "7.85", "7.31", "168834.0", "601015"]
        ]
        expect_df = pd.DataFrame.from_records(expect_list, columns=['date', 'open', 'close', 'high', 'low', 'volume', 'code'])
        self.assertTrue(expect_df.equals(result))

if __name__ == "__main__":
    unittest.main()