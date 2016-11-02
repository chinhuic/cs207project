
import unittest
import SimulatedTimeSeries
from random import normalvariate, random
from itertools import count


class TestSimulatedTimeSeries(unittest.TestCase):
    ## test eval
    
    def make_data(m, stop=None):
        for _ in count():
            if stop and _ > stop:
                break
            yield 1.0e09 + normalvariate(0, m*random() )
    
    def test_produce(self):
        g = make_data(5, 10)
        ts = SimulatedTimeSeries(g)
        m = ts.produce(4)
        list(m)
        self.assertTrue(all(isinstance(n, int) for n in m))
        
    
    


if __name__ == '__main__':
    unittest.main()
