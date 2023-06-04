# CIPeval
A set of automatic evaluation metrics based on ChatMatch to evaluate our chatbots

### Running
To run algorithms 1 and 2, one should run "evaluation.py" with the parameter "-l" set to the location of the transcript at hand. For example:
```python3 evaluation.py -l ../logs/my_transcript.csv```

### Interpretation
Regular scores indicate how many utterances have "violated" ChatMatch rules, e.g. repetition has occurred. The percentage provides information about how many "violations" had occurred in relation to the total amount of utterances made by one bot. The lower the scores, the better.

#### Relevancy
Relevancy works differently from the other scores because it was created as a bonus point system within ChatMatch. In practice, this means that Relevancy gives a bonus point to a turn if a word has been used in another turn that has occurred before. The higher the score, the more relevant bonus points a bot has been given. It should also be noted that this system uses Inverse Document Frequency (IDF) as a way to calculate the most important words, but this is very error-prone with the large quantity of repetition in our bots. Therefore, information is colored and highlighted with verbose information set to on by default, to make human analysis easier.
