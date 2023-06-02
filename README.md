# CIPeval
A set of automatic evaluation metrics based on ChatMatch to evaluate our chatbots

### Running
To run algorithm 1 and 2, one should run "evaluation.py" with the parameter "-l" set to the location of the transscript at hand. For example:
```python3 evaluation.py -l ../logs/my_transcript.csv```

### Interpretation
Regular scores indicate how many utterances have "violated" ChatMatch rules, e.g. repetition has occured. The percentage provides information about how many "violations" had occured in relation to the total amount of utterances made by one bot. 
