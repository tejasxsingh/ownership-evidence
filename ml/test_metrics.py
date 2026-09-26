"""Check evaluation arithmetic, including undefined precision."""
import unittest
from train import metrics
class MetricsTest(unittest.TestCase):
 def test_mixed_errors(self):
  r=metrics([1,1,0,0],[1,0,1,0])
  self.assertEqual([r[k] for k in ['true_positives','false_positives','false_negatives','true_negatives']],[1,1,1,1])
  self.assertEqual([r[k] for k in ['precision','recall','f1']],[.5,.5,.5])
 def test_no_selected(self):
  r=metrics([1,0],[0,0]);self.assertIsNone(r['precision']);self.assertEqual(r['recall'],0);self.assertEqual(r['f1'],0)
 def test_perfect(self):
  r=metrics([1,0,1],[1,0,1]);self.assertEqual(r['recall'],1);self.assertEqual(r['f1'],1)
if __name__=='__main__':unittest.main()
