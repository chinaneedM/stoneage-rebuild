"""Adversarial R58 static-return spelling tests using invented operand rows."""
import unittest
from tools.stoneage_tw10_savedata_r58_syntax_contract import derive, expect_row

def r(kind, register=None, constant=None):
    return {'kind':kind, 'register':register, 'constant':constant}

class R58SyntaxTests(unittest.TestCase):
    def test_exact_invented_register_operands(self):
        rows={17:{'mnemonic':'mov','operands':[r('register','eax'),r('register','ebx')]}}
        self.assertIsNotNone(expect_row(rows,17,'mov',[
            ('register','eax',None),('register','ebx',None)]))

    def test_source_register_swap_rejected(self):
        rows={17:{'mnemonic':'mov','operands':[r('register','eax'),r('register','ecx')]}}
        with self.assertRaises(ValueError):
            expect_row(rows,17,'mov',[('register','eax',None),('register','ebx',None)])

    def test_all_ones_to_zero_rejected(self):
        rows={21:{'mnemonic':'or','operands':[r('register','ebx'),r('immediate',constant=0)]}}
        with self.assertRaises(ValueError):
            expect_row(rows,21,'or',[('register','ebx',None),('immediate',None,0xffffffff)])

    def test_missing_instruction_rejected(self):
        with self.assertRaises(ValueError):expect_row({},17,'ret',[])

    def test_wrong_mnemonic_rejected(self):
        with self.assertRaises(ValueError):expect_row({17:{'mnemonic':'jmp','operands':[]}},17,'ret',[])

    def test_nonmatching_original_report_rejected(self):
        with self.assertRaises(ValueError):derive(b'{}')


if __name__=='__main__':
    unittest.main()
