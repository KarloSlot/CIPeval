from collections import defaultdict
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from rich.console import Console
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import pandas as pd
import string


nltk.download('punkt', quiet=True)
console = Console()


class RelevanceBonus():
    '''Instantiate an object with the ability to retrieve
    relevancy bonus points for a dialogue list of sentence strings
    '''
    def __init__(
        self,
        min_max_df:list[int|float]=[2, 1.0],
        min_dist:int=2,
        max_dist:int | None=None,
        top_percentage:float=.5,
        exclude:list[str]=['yes', 'no', 'he', 'their', 'her', 'its', 'my', 'I', 'us'],
        least_frequent:bool=True,
        verbose=True,
    ) -> None:
        self.min_max_df = min_max_df
        self.min_dist = min_dist
        self.max_dist = max_dist
        self.top_percentage = top_percentage
        self.checklist = exclude
        self.ignore_tokens = string.punctuation
        self.least_frequent = least_frequent
        self.verbose = verbose

        self.tokenizer = self._lemma_tokenize
        self.wnl = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer(
            stop_words=stopwords.words('english'),
            min_df=min_max_df[0],
            max_df=min_max_df[1],
        )

    def _lemma_tokenize(self, sent:str) -> str:
        '''Return a given sentence string that has been tokenized and lemmatized'''
        return ' '.join([self.wnl.lemmatize(token.lower()) for token in word_tokenize(sent)
                         if token not in self.ignore_tokens])

    def _fit_vectorizer(self, sent_list:list[str]) -> None:
        '''Fit a given sentence list to the vectorizer'''
        self.vectorizer.fit(sent_list)

    def _retrieve_top_idf(self) -> list[str]:
        '''Return a list of top idf items using the fitted items from self.vectorizer.idf'''
        sorted_idf = sorted(
            [[i, self.vectorizer.idf_[idx]]
             for idx, i in enumerate(self.vectorizer.get_feature_names_out())],
            key=lambda x : x[-1],
            reverse=self.least_frequent,
        )

        sorted_idf = [[x, y] for x, y in sorted_idf if x.lower() not in self.checklist]
        if self.least_frequent:
            return [x for x, y in sorted_idf if y >= ((1 - self.top_percentage) * sorted_idf[0][-1])]
        else:
            return [x for x, y in sorted_idf if y <= ((1 + self.top_percentage) * sorted_idf[0][-1])]

    def _top_percentage(self, sent_list:list[str]) -> list[str]:
        '''Return a sorted list of top idf items from a given sentence list
        that is tokenized, lemmatized, and fitted to the vectorizer
        '''
        tokenized_list = [self._lemma_tokenize(sent) for sent in sent_list]
        self._fit_vectorizer(tokenized_list)
        return self._retrieve_top_idf()

    def _turn_token_check(self, token, turn, turn_token):
        if turn_token[token]:
            if self.max_dist:
                if (turn - turn_token[token] > self.min_dist
                    and turn - turn_token[token] < self.max_dist):
                    return True
            else:
                if turn - turn_token[token] > self.min_dist:
                    return True

        return False

    def _run_speaker(self, df:pd.DataFrame, speaker:str) -> list[bool]:
        '''Return the sum of bonus points
        for a given dialogue list of sentence strings
        '''
        top_percentage = self._top_percentage(df.utterance.to_list())
        if self.verbose:
            if self.least_frequent:
                freq_state = 'least frequent words'
            else:
                freq_state = 'most frequent words'
            if self.max_dist == None:
                max_dist_statement = f'{self.max_dist}'
            else:
                max_dist_statement = f'{self.max_dist} turn(s)'
            console.print(f'\nImportant words ({self.top_percentage:.2%} {freq_state} '
                          f'with a minimum frequency of {self.min_max_df[0]} turn(s) '
                          f'and a maximum frequency of {self.min_max_df[-1]} (1.0 is no maximum) '
                          f'with a minimum turn distance of {self.min_dist} turn(s) '
                          f'and a maximum turn distance of {max_dist_statement}): '
                          f'{top_percentage}\n')
        turn_token = defaultdict(lambda: False)
        bonus = []

        for turn, sent in df.iterrows():
            get_bonus = 0

            for token in self._lemma_tokenize(sent.utterance).split(' '):
                if (
                    self._turn_token_check(token, turn, turn_token)
                    and token in top_percentage
                    and speaker in sent.speaker
                ):
                    if get_bonus == 1:
                        bonus_statement = ''
                    else:
                        bonus_statement = '+1'
                    get_bonus = 1
                    if self.verbose:
                        console.print(
                            f'[bold green]{bonus_statement}',
                            f'[bold red]{token}',
                            f'\t{turn} - ("{sent.speaker}")',
                            sent.utterance.replace(
                                token,
                                f'[bold underline green]{token}[/bold underline green]'
                            ),
                            f'[bold red](Links back to)->[/bold red] {turn_token[token]} '
                            f'- ("{df.iloc[turn_token[token]].speaker}")',
                            df.iloc[turn_token[token]].utterance.replace(
                                token,
                                f'[bold underline green]{token}[/bold underline green]'
                            )
                        )

                turn_token[token] = turn

            bonus.append(get_bonus)

        return bonus

    def __call__(self, df_logs:pd.DataFrame, speaker:str,) -> None:
        '''Retrieve the relevance bonus for a given speaker
        and dataframe
        '''
        try:
            point_list = self._run_speaker(df_logs, speaker)
        except:
            point_list = [0,]
            console.print('\n[bold red]No items found with current settings')

        console.print(f'\nRelevance bonus points ("{speaker}"):',
                      sum(point_list),
                      '\n')


class main:
    def __init__(self) -> None:
        df = pd.read_csv('./test.csv')
        find_relevance_bonus = RelevanceBonus(verbose=True, least_frequent=True, top_percentage=0.2, max_dist=None, min_max_df=[2, 1.0])
        for speaker in ['SNO', 'JAM']:
            find_relevance_bonus(df, speaker)


if __name__ == '__main__':
    main()