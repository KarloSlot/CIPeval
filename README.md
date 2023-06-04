# CIPeval
A set of automatic evaluation metrics based on ChatMatch to evaluate our chatbots

### Running
To run algorithms 1 and 2, one should run "evaluation.py" with the parameter "-l" set to the location of the transcript at hand. For example:
```python3 evaluation.py -l ../logs/my_transcript.csv```

### Interpretation
Regular scores indicate how many utterances have "violated" ChatMatch rules, e.g. repetition has occurred. The percentage provides information about how many "violations" had occurred in relation to the total amount of utterances made by one bot. The lower the scores, the better.
