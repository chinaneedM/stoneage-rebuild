import unittest
from tools.stoneage_inium_trial_menu_probe import P,KEY

class IniumTrialMenuProbeTests(unittest.TestCase):
    def test_parser_trial_link(self):
        p=P();p.feed('<a href="trial.htm">체험판하기</a>')
        self.assertEqual(p.links[0][2],"trial.htm")
        self.assertTrue(KEY.search(p.links[0][3]))
if __name__=="__main__":unittest.main()
