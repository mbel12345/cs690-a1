# CS 690 Assignment 1 Report: Replicating a Controlled Evaluation

## Part 1. Verification evidence

Command:

```text
python -m harness.verify
```

Paste the five `OK` lines here. Keep `results/verification.json` in your repository.

OK: loaded 20 frozen tasks
OK: dataset sha256 5d84176547cb679f4145676d1f4dfd5061bf3b9600904911da8e5700e82eee3b
OK: generated Python executed in Docker sandbox
OK: candidate network probe was blocked
OK: model/configuration metadata written to results/verification.json

## Part 2. Tests and code questions

Paste the final summary line of `pytest -q` here.

....................                                                                                                                                                                    [100%]
20 passed in 1.06s

Answer each question in your own words, in about 75 to 150 words. Base every answer on the code in this repository, and name the files and functions you describe.

### Q1. The path of one attempt

These steps are initiated from run function in runner.py. Tasks.py loads the task set from the json file (load_tasks). Then the prompt is passed to provider_for in provider.py, which does the OpenAI call. Then a docker session is started (sandbox.py and docker_entry.py) where the output gets sent and ran (run_source). Grader.py checks if the code was successful (grade_candidate), and metrics.py and report.py (in write_summary) produce the json output.

Code needs to be run in Docker so that it is a sealed and consistent environment with no outside networking.


### Q2. What is sent and what comes back

"id" uniquely identifies the test. The "provider" and "model" are which exact LLM version answers you. "Temperature" is how much randomness is allowed. High "top-p" means many possible words can be chosen. "seed" is controls the random seed for the model. "effort" is how much of the reasoning is hidden.

"text" is the output. "provider" is openAI. "requested_model" and "returned_model" specify which models were used including version. "input_tokens" and "output_tokens" are the number of input tokens and output tokens. "stop_reason" is why the response ended.

With just the model name, you wouldn’t know its reasoning for stopping or which specific model was used.


### Q3. Same prompt, different answers

Even with high temperature, there can be multiple good solutions that the model cannot choose from. For example, I saw in my output that the code was exactly the same for one prompt, except that "item" was the loop var in one and "value" in the other. Both are common choices. This is intentional because if the model was too rigid and always chose the single best answer, it could really dig in to the wrong answers. It is good to see if the models non-first-pick choices are valid too, because if there are not, that would diminish faith in the model.

The harness records candidate_path (output python program), condition_id + dataset_id + dataset_sha256 + experiment_id + prompt_path (combined to determine where the input tokens come from), duration_ms + effort + error + output_tokens + passed (show results). The max_output_tokens and seed are important too for reproducibility.


### Q4. pass@k by hand

Show your work for pass@1 and pass@2 with n = 3 and c = 1, the values `pass_at_k` returned, and the shortcut `1 - (1 - c/n) ** k` for k = 2.

pass_k = 1.0 - comb(n - c, k) / comb(n, k)
pass_1 = 1.0 - comb(3 - 1, 1) / comb(3, 1)
pass_1 = 1.0 - 2 / 3
pass_1 = 0.333

pass_2 = 1.0 - comb(3 - 1, 2) / comb(3, 2)
pass_2 = 1.0 - 1 / 3
pass_2 = 0.667

Shortcut:
pass_2 = 1 - (1 - 1/3)**2
pass_2 = 5/9 = 0.556

The true pass_2 of 0.667 is correct and higher because the shortcut assumes no replacement, which is not true since each result will not be repeated more than once.


### Q5. Why whole problems are redrawn

Bootstrap_task_ci samples the results of pass@k multiple times. It then is able to compute confidence in how accurate the value of pass@k is. In detail, bootstrap_ci gets a random sample of pass@k values, then averages them. It then cuts off the lowest and highest (1-confidence) / 2 of these samples. It draws whole problems because all the attempts within one problem are not independent, so it would be misleading/biased if we grouped individual ones together.

The test for test_metrics that enforces this is test_task_bootstrap_resamples_tasks_not_candidate_rows. By running a very large number of times, it can detect if the model is ever fully confident (1 or its inverse 0) which is not possible unless two of the related samples are grouped together.


## Part 3. Replication

Part 3 has no written section. Its evidence is the committed `results/experiment/` and `prompts/` folders, and the dollars you spent, which go in the Part 4 table.

## Part 4. Results

Take every number from `results/experiment/summary_A.json` and `results/experiment/summary_B.json`, not from the console. Dollars spent come from the Usage page of your OpenAI account. If your account does not show them, write `not available`. If it shows only one total for the whole run, write the total in row A and `included in A` in row B.

| Condition | Requested model | Returned model version | Attempts per task | Total attempts | pass@1 | 95 percent CI for pass@1 | pass@2 | Input tokens | Output tokens | Dollars spent |
| --- | --- | --- | ---: | ---: | ---: | --- | ---: | ---: | ---: | --- |
| A | gpt-5.6-luna | gpt-5.6-luna | 3 | 60 | 0.9833 | 0.95, 1.0 | 1.0 | 7146 | 3791 | 0.07 |
| B | gpt-5.6-terra | gpt-5.6-terra | 3 | 60 | 1.0 |1.0, 1.0 | 1.0 | 7146 | 4272 | 0.07 |

### Memo, no more than 500 words, not counting the table

Address all five items:

1. State the observed ranking by pass@1 point estimate.
2. State whether the uncertainty evidence supports ranking the two conditions.
3. If it does not, include the exact sentence: `The evidence does not support a ranking.`
4. State one external-validity limitation specific to `CS690-Eval20`.
5. State one likely source of variance specific to this experiment, and explain why a rerun, or a classmate's run, gives somewhat different numbers.

Overlapping intervals are not a formal significance test, and you are not asked to run one.

## Part 5. Reading a published score, 300 to 400 words

Benchmark chosen (HumanEval, MBPP, LiveCodeBench, or SWE-bench):

Use the benchmark's primary paper or its official documentation for the task definition. Cite evidence for any contamination, saturation, or current-status claim, and date any current-status source.

### 1. What does it measure?

### 2. What does it not measure that a software project may depend on?

### 3. How can a reported score rise without the underlying model becoming better?

### 4. Could the model have seen the answers already?

End with at least one sentence explaining why the published score is not interchangeable with your `CS690-Eval20` result.

## References
