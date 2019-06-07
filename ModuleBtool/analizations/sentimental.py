import re
import os
import csv
from collections import defaultdict


class Sentimental(object):
    def __init__(self, word_list=None, negation=None):
        if word_list is None and negation is None:
            base_dir = os.path.dirname(__file__)
            word_list = [os.path.join(base_dir, p) for p in ['./word_list/sentimental/afinn.csv',
                                                             './word_list/sentimental/russian.csv']]
            negation = os.path.join(base_dir, './word_list/sentimental/negations.csv')

        self.word_list = {}
        self.negations = set()

        for wl_filename in self.__to_arg_list(word_list):
            self.load_word_list(wl_filename)
        for negations_filename in self.__to_arg_list(negation):
            self.load_neagations(negations_filename)

        self.__negation_skip = {'a', 'an', 'so', 'too'}

    @staticmethod
    def __to_arg_list(obj):
        if obj is not None:
            if not isinstance(obj, list):
                obj = [obj]
        else:
            obj = []
        return obj

    def __is_prefixed_by_negation(self, token_idx, tokens):
        #   True if i != 0 and tokens[i - 1] in self.negations else False
        prev_idx = token_idx - 1
        if tokens[prev_idx] in self.__negation_skip:
            prev_idx -= 1

        is_prefixed = False
        if token_idx > 0 and prev_idx >= 0 and tokens[prev_idx] in self.negations:
            is_prefixed = True

        return is_prefixed

    def load_neagations(self, filename):
        with open(filename, 'r') as f:
            reader = csv.DictReader(f)
            negations = set([row['token'] for row in reader])
        self.negations |= negations

    def load_word_list(self, filename):
        with open(filename, 'r', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            word_list = {row['word']: float(row['score']) for row in reader}
        self.word_list.update(word_list)

    def analyze(self, sentence):
        sentence_clean = re.sub(r'[^\w ]', ' ', sentence.lower())
        tokens = sentence_clean.split()

        scores = defaultdict(float)
        words = defaultdict(list)
        comparative = 0

        for i, token in enumerate(tokens):
            is_prefixed_by_negation = self.__is_prefixed_by_negation(i, tokens)
            if token in self.word_list and not is_prefixed_by_negation:
                score = self.word_list[token]

                score_type = 'negative' if score < 0 else 'positive'
                scores[score_type] += score
                words[score_type].append(token)

        if len(tokens) > 0:
            comparative = (scores['positive'] + scores['negative']) / len(tokens)

        result = {
            'score': scores['positive'] + scores['negative'],
            'positive': scores['positive'],
            'negative': scores['negative'],
            'comparative': comparative,
        }

        return result


def main(list_massage):
    sent = Sentimental(word_list=['./word_list/sentimental/afinn.csv', './word_list/sentimental/russian.csv'],
                       negation='./word_list/negations.csv')

    response = {'good': 0, 'bad': 0, 'neutral': 0}
    for_mean = []
    for item in list_massage:
        result = sent.analyze(item.lower())
        for_mean.append(result['score'])
        if result['score'] > 0:
            response['good'] += 1
        elif result['score'] < 0:
            response['bad'] += 1
        else:
            response['neutral'] += 1
    response['mean'] = float(sum(for_mean)) / max(len(for_mean), 1)

    return response
