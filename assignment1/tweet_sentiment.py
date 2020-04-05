import sys
import json
import re


def scores_to_dict(scores_file):
    scores = dict()
    for l in scores_file:
        word, score = l.split('\t')
        scores[word] = int(score)
    return scores


def word_score(word, scores):
    score = scores.get(word.lower())
    return score if score else 0


def line_score(line, scores):
    return sum(word_score(w, scores) for w in re.findall(r'\w+', line))


def is_tweet(data):
    return bool(data.get('text'))


def scores(tweets_file, scores):
    for l in tweets_file:
        data = json.loads(l)
        if is_tweet(data):
            print(line_score(data.get('text'), scores))


def lines(fp):
    print str(len(fp.readlines()))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores(tweet_file, scores_to_dict(sent_file))

    sent_file.close()
    tweet_file.close()


if __name__ == '__main__':
    main()
