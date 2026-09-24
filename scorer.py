"""
Unit 2's scorer: decides pass/fail for each run in run_eval.py.

`judge(question, expects, answer, results) -> bool` is the contract
run_eval.py looks for. A run passes only if every phrase in `expects` (split
on commas) turns up, after normalizing away capitalization and formatting
noise, in BOTH:

  - retrieval: the text of the chunks actually retrieved for the question
  - generation: the final answer the model produced

Checking only the chunks would measure retrieval alone — did the right
material even come back — and would count a run as a pass even if the model
then botched the wording, dropped a fact, or refused despite good chunks
being available. Checking only the answer would measure generation alone,
and would let a lucky guess or a hallucinated-but-correct-sounding answer
pass even when retrieval brought back nothing useful. Requiring both catches
failures at either stage: a retrieval miss (chunks lack the phrase) and a
generation miss (chunks are fine, but the answer — including a gate refusal,
which never contains the expected phrases — doesn't say it).

Normalizing matters because the same fact shows up worded differently across
a chunk, a model's answer, and whatever you typed into `expects` — "9pm" vs.
"9 PM", "two-hourly" vs. "two hourly". None of that is the thing being
tested; the fact being present is. `_normalize` lowercases, turns hyphens
into spaces, and collapses repeated whitespace so those variants compare
equal, without trying to treat differently-*valued* numbers or times as the
same thing — "9pm" and "9:30pm" still won't match, on purpose.
"""

import re


def _normalize(text: str) -> str:
    text = text.lower().replace("-", " ")
    return re.sub(r"\s+", " ", text).strip()


def judge(question: str, expects: str, answer: str, results: list) -> bool | None:
    """Pass if every phrase in `expects` appears in both the chunks and the answer."""
    expects = expects.strip()
    if not expects:
        return None

    phrases = [_normalize(p) for p in expects.split(",") if p.strip()]

    chunk_text = _normalize(" ".join(r.text for r in results))
    answer_text = _normalize(answer)

    retrieval_ok = all(phrase in chunk_text for phrase in phrases)
    generation_ok = all(phrase in answer_text for phrase in phrases)

    return retrieval_ok and generation_ok
