import unittest
import numpy as np
from analysis import score, ahp, metrics, read, CODES
class TestAnalysis(unittest.TestCase):
    def test_constant(self):
        np.testing.assert_allclose(score(np.full((4,10),.6),np.ones(10)),.6)
    def test_scale_invariance(self):
        q=np.array([[float(r[c]) for c in CODES] for r in read('site_subindices.csv')])
        np.testing.assert_allclose(score(q,np.ones(10)),score(q,np.ones(10)*5))
    def test_ranking(self):
        q=np.array([[float(r[c]) for c in CODES] for r in read('site_subindices.csv')])
        w=[float(r['reported_weight']) for r in read('weights.csv')]
        self.assertEqual(np.argsort(-score(q,w)).tolist(),[2,3,0,1])
    def test_ahp(self):
        w,cr=ahp(np.ones((3,3)));np.testing.assert_allclose(w,[1/3]*3);self.assertAlmostEqual(cr,0)
    def test_bad_weights(self):
        with self.assertRaises(ValueError):score(np.full((1,10),.5),np.zeros(10))
    def test_bad_q(self):
        with self.assertRaises(ValueError):score(np.full((1,10),float('nan')),np.ones(10))
    def test_metrics(self):
        m=metrics(np.array([1.,2.,3.]),np.array([1.,2.,3.]));self.assertEqual(m['RMSE'],0);self.assertEqual(m['NSE'],1)
if __name__=='__main__':unittest.main()
