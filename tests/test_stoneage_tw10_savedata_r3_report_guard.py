import unittest
from tools.stoneage_tw10_savedata_r3_report_guard import validate,TITLE,SCOPE,RESOLUTION
from tools.stoneage_tw10_savedata_instruction_probe import RUNTIME_SHA256,SAVEDATA_SHA256

WORDS=(0x40065,0x400e5,0x40116,0x402a1)


def fixture(candidates=False,api=False):
    lines=[
        TITLE,SCOPE,
        f"IDENTITY|runtime_sha256={RUNTIME_SHA256}|savedata_sha256={SAVEDATA_SHA256}",
        "PATH|string_rva=0x63634|target_va=0x463634|section=.data",
    ]
    for n,rva in enumerate(WORDS,1):
        lines.append(f"WORD|n={n}|rva=0x{rva:x}|linear_overlap=1|linear_whole=0|linear_start_at_word=0|alternate_ref_candidates={int(candidates and n==1)}")
        if candidates and n==1:
            lines.append("CANDIDATE|word=1|n=1|start_rva=0x40064|end_rva=0x40069|mnemonic=push|word_operand_offset=1|linear_start_match=0|linear_incoming_direct_edges=0|forward_64_file_api_count="+("1" if api else "0"))
            if api:
                lines.append("FORWARD_API|word=1|candidate=1|dll=KERNEL32.dll|name=CreateFileA|count=1")
    lines += [
        "COUNT|word_sites=4|alignment_candidates="+str(int(candidates)),
        "BOUNDARY|Four matching address words and alternate decodings are static facts; actual instruction alignment, indirect callsites, savedata IO reachability, early client framing/checksum and runtime persistence remain OPEN.",
        RESOLUTION,
    ]
    return "\n".join(lines)+"\n"


class R3ReportGuardTests(unittest.TestCase):
    def test_exact_four_site_zero_candidate_report(self):
        r=validate(fixture())
        self.assertEqual(r["word_sites"],4)
        self.assertEqual(r["candidates"],0)
        self.assertFalse(r["actual_instruction_reachability_admitted"])

    def test_candidate_and_matching_api(self):
        r=validate(fixture(True,True))
        self.assertEqual(r["candidates"],1)
        self.assertEqual(r["forward_file_api_mentions"],1)

    def test_wrong_original_identity(self):
        with self.assertRaisesRegex(ValueError,"hash pins"):
            validate(fixture().replace(RUNTIME_SHA256,"0"*64))

    def test_missing_fourth_word(self):
        doc=fixture().splitlines()
        with self.assertRaisesRegex(ValueError, "word/candidate count"):
            validate("\n".join(line for line in doc if "|n=4|" not in line))

    def test_unknown_raw_report_line_rejected(self):
        with self.assertRaisesRegex(ValueError,"unexpected report row"):
            validate(fixture().replace("COUNT|","RAW_BYTES|dump=deadbeef\nCOUNT|"))

    def test_bad_instruction_window_rejected(self):
        with self.assertRaisesRegex(ValueError,"window"):
            validate(fixture(True).replace("end_rva=0x40069","end_rva=0x40068"))

    def test_wrong_api_count_rejected(self):
        with self.assertRaisesRegex(ValueError, "API count"):
            validate(fixture(True,True).replace("name=CreateFileA|count=1","name=CreateFileA|count=2"))

    def test_bad_candidate_count_rejected(self):
        with self.assertRaisesRegex(ValueError, "candidate"):
            validate(fixture(True).replace("alignment_candidates=1","alignment_candidates=9"))

    def test_unrecognized_arbitrary_text_rejected(self):
        with self.assertRaisesRegex(ValueError,"invalid.*report"):
            validate(fixture().replace("linear_whole=0","linear_whole=some raw secret"))

    def test_no_missing_resolution_allowed(self):
        with self.assertRaisesRegex(ValueError,"resolution"):
            validate(fixture().replace(RESOLUTION,"RESOLUTION|RUNTIME_NATIVE_IO_ACCEPTED"))


    def test_boundary_cannot_be_weakened_by_preserving_only_prefix(self):
        changed=fixture().replace(
            "actual instruction alignment, indirect callsites, savedata IO reachability,",
            "original native file IO is ACCEPTED,")
        with self.assertRaisesRegex(ValueError,"exact explicit non-runtime"):
            validate(changed)

    def test_file_api_must_be_from_pinned_emitter_allowlist(self):
        with self.assertRaisesRegex(ValueError,"recognized file API"):
            validate(fixture(True,True).replace("name=CreateFileA","name=UnknownFileApi"))

    def test_duplicate_file_api_summary_rejected_even_if_counts_balance(self):
        lines=fixture(True,True).splitlines()
        line=next(x for x in lines if x.startswith("FORWARD_API|"))
        lines.insert(lines.index(line)+1,line)
        changed="\n".join(lines).replace(
            "forward_64_file_api_count=1","forward_64_file_api_count=2")+"\n"
        with self.assertRaisesRegex(ValueError,"duplicate API summary"):
            validate(changed)

    def test_candidate_cannot_precede_word_header(self):
        lines=fixture(True).splitlines()
        candidate=next(x for x in lines if x.startswith("CANDIDATE|"))
        lines.remove(candidate)
        lines.insert(4,candidate)
        with self.assertRaisesRegex(ValueError,"candidate before"):
            validate("\n".join(lines)+"\n")

    def test_forward_api_cannot_precede_candidate(self):
        lines=fixture(True,True).splitlines()
        api=next(x for x in lines if x.startswith("FORWARD_API|"))
        lines.remove(api)
        candidate_idx=next(i for i,x in enumerate(lines) if x.startswith("CANDIDATE|"))
        lines.insert(candidate_idx,api)
        with self.assertRaisesRegex(ValueError,"API out of candidate"):
            validate("\n".join(lines)+"\n")

    def test_overlap_must_fit_four_byte_window(self):
        with self.assertRaisesRegex(ValueError,"linear overlap bounds"):
            validate(fixture().replace("linear_overlap=1","linear_overlap=5"))

    def test_candidate_count_per_site_cannot_exceed_x86_start_window(self):
        with self.assertRaisesRegex(ValueError,"unbounded report integer"):
            validate(fixture().replace(
                "alternate_ref_candidates=0","alternate_ref_candidates=16",1))

    def test_zero_api_mentions_rejected(self):
        with self.assertRaisesRegex(ValueError,"zero API mention count"):
            validate(fixture(True,True).replace("name=CreateFileA|count=1",
                                                  "name=CreateFileA|count=0").replace(
                "forward_64_file_api_count=1","forward_64_file_api_count=0"))

if __name__=="__main__":
    unittest.main()
