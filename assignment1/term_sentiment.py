import sys
import re
import json


class Score:
    scale = 5

    def __init__(self, score):
        self.neg = self.pos = 0
        self.update(score)

    def update(self, score):
        if score > 0:
            self.pos += score
        else:
            self.neg -= score

    @property
    def value(self):
        d = self.pos - self.neg
        s = self.pos + self.neg
        return Score.scale * d / s if s else 0


def scores_to_dict(scores_file):
    scores = dict()
    for l in scores_file:
        word, score = l.split('\t')
        scores[word] = int(score)
    return scores


def score_present(word, scores):
    return bool(scores.get(word.lower()))


def unknowns_insert(unknowns, word, tweet_score):
    if unknowns.get(word):
        unknowns.get(word).update(tweet_score)
    else:
        unknowns[word] = Score(tweet_score)


def unknowns_update(unknowns, words, tweet_score, scores):
    for w in words:
        if not score_present(w, scores):
            unknowns_insert(unknowns, w.lower(), tweet_score)


def unknown_scores(tweet_file, scores):
    unknowns = dict()
    for l in tweet_file:
        data = json.loads(l)
        if is_tweet(data):
            words = re.findall(r'\w+', data['text'])
            score = tweet_score(words, scores)
            unknowns_update(unknowns, words, score, scores)
    return unknowns


def word_score(word, scores):
    score = scores.get(word.lower())
    return score if score else 0


def tweet_score(words, scores):
    return sum(word_score(w, scores) for w in words)


def is_tweet(data):
    return bool(data.get('text'))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores = scores_to_dict(sent_file)

    for word, score in unknown_scores(tweet_file, scores).items():
        print('{} {}'.format(word, score.value))

    sent_file.close()
    tweet_file.close()


if __name__ == '__main__':
    main()
