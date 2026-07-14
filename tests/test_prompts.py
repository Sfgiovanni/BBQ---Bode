from brbbq.prompts import render_prompt


def test_prompts_follow_experimental_language(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    pt = expanded[expanded["language"] == "pt"].iloc[0].to_dict()
    en = expanded[expanded["language"] == "en"].iloc[0].to_dict()
    prompt_pt = render_prompt(pt, "alpaca")
    prompt_en = render_prompt(en, "alpaca")
    assert "### Instrução:" in prompt_pt and "Contexto:" in prompt_pt and "Pergunta:" in prompt_pt
    assert "### Instruction:" in prompt_en and "Context:" in prompt_en and "Question:" in prompt_en
    assert "apenas com A, B ou C" in prompt_pt
    assert "with A, B, or C only" in prompt_en


def test_context_and_question_do_not_change_between_permutations(dataset_bundle):
    _, _, _, _, expanded = dataset_bundle
    group = next(iter(expanded.groupby("logical_id")))[1]
    prompts = [render_prompt(row, "simple") for row in group.to_dict("records")]
    for row, prompt in zip(group.to_dict("records"), prompts):
        assert row["context"] in prompt and row["question"] in prompt
