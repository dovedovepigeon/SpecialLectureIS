#!/usr/bin/env python3

import argparse
import logging
import os
import sys
from typing import List
import sacrebleu

logging.basicConfig(
    format="| %(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level="INFO",
    stream=sys.stdout,
)
logger = logging.getLogger("calculate_oracle_bleu")


def add_args(parser: argparse.ArgumentParser) -> argparse.ArgumentParser:
    # fmt: off
    parser.add_argument("--input", "-i", type=str, required=True,
                        help="path to input file")
    parser.add_argument("--reference", "-r", type=str, required=True,
                        help="path to reference file")
    parser.add_argument("--n-best", "-b", type=int, required=True,
                        help="n of n-best of input text")
    parser.add_argument("--oracle-at-n", "-n", type=int, nargs="+", required=True,
                        help="n of oracle@n")
    parser.add_argument("--output-prefix", "-o", type=str, required=True,
                        help="output prefix to oracles")
    parser.add_argument("--trg-lang", "-t", type=str, default="en",
                        help="target language")
    # fmt: on
    return parser


def calculate_oracle_bleu(
    input_path: str,
    reference_path: str,
    n_best: int,
    n_oracle: List[int],
    output_prefix: str,
    trg_lang: str = "en",
):
    assert max(n_oracle) <= n_best, "n_oracle must be less than or equal to n_best"

    s_bleu = sacrebleu.BLEU(
        smooth_method="add-k", smooth_value=1, effective_order=True, trg_lang=trg_lang
    )
    # s_bleu = sacrebleu.BLEU(smooth_method="exp", effective_order=True)
    bleu = sacrebleu.BLEU(smooth_method="none", trg_lang=trg_lang)

    with open(input_path, mode="r") as f_input:
        with open(reference_path, mode="r") as f_reference:
            input_lines = f_input.readlines()
            references_rstrip = [line.rstrip() for line in f_reference.readlines()]
            # fmt: off
            assert len(input_lines) % n_best == 0, "invalid n_best"
            assert len(input_lines) / n_best == len(references_rstrip), "len(input) must be equal to len(reference) * n_best"
            # fmt: on

    candidates_list = [
        input_lines[i : i + n_best] for i in range(0, len(input_lines), n_best)
    ]
    inputs_with_scores = []
    for candidates, reference_rstrip in zip(candidates_list, references_rstrip):
        candidates_with_score = []
        for candidate in candidates:
            score = s_bleu.sentence_score(candidate.rstrip(), [reference_rstrip])
            score = score.score
            candidates_with_score.append((candidate, score))
        inputs_with_scores.append(candidates_with_score)

    oracle_scores = []
    for n in n_oracle:
        best_sents = []
        with open(output_prefix + f".bleu.oracle_at_{n}.out", mode="w") as out:
            for input_with_score in inputs_with_scores:
                sorted_input = sorted(
                    input_with_score[:n], key=lambda x: x[1], reverse=True
                )
                best_sent = sorted_input[0][0]
                best_sents.append(best_sent.rstrip())
                out.write(best_sent)
        corpus_score = bleu.corpus_score(best_sents, [references_rstrip])
        oracle_scores.append(f"{corpus_score.score:.4g}")
        print(f"oracle@{n}: {corpus_score}")
    print(*[f"oracle@{n}" for n in n_oracle], sep="\t")
    print(*oracle_scores, sep="\t")


def main():
    parser = argparse.ArgumentParser(
        description="""
Calculate oracle@n from n-best hypotheses.
Example:
python calculate_oracle_bleu.py -i hyp.true.detok -r test.en -b 20 -n 1 5 10 20 -o exp

Note:
output files: exp.oracle_at_1.out, exp.oracle_at_5.out, exp.oracle_at_10.out, exp.oracle_at_20.out
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser = add_args(parser)
    args = parser.parse_args()
    logger.info(args)

    calculate_oracle_bleu(
        args.input,
        args.reference,
        args.n_best,
        args.oracle_at_n,
        args.output_prefix,
        args.trg_lang,
    )


if __name__ == "__main__":
    main()
