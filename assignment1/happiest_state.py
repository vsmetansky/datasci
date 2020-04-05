import sys
import json
import re
import operator

STATE_SCORES = {
    'WA': [0, 0],
    'WI': [0, 0],
    'WV': [0, 0],
    'FL': [0, 0],
    'WY': [0, 0],
    'NH': [0, 0],
    'NJ': [0, 0],
    'NM': [0, 0],
    'NA': [0, 0],
    'NC': [0, 0],
    'ND': [0, 0],
    'NE': [0, 0],
    'NY': [0, 0],
    'RI': [0, 0],
    'NV': [0, 0],
    'GU': [0, 0],
    'CO': [0, 0],
    'CA': [0, 0],
    'GA': [0, 0],
    'CT': [0, 0],
    'OK': [0, 0],
    'OH': [0, 0],
    'KS': [0, 0],
    'SC': [0, 0],
    'KY': [0, 0],
    'OR': [0, 0],
    'SD': [0, 0],
    'DE': [0, 0],
    'DC': [0, 0],
    'HI': [0, 0],
    'PR': [0, 0],
    'TX': [0, 0],
    'LA': [0, 0],
    'TN': [0, 0],
    'PA': [0, 0],
    'VA': [0, 0],
    'VI': [0, 0],
    'AK': [0, 0],
    'AL': [0, 0],
    'AS': [0, 0],
    'AR': [0, 0],
    'VT': [0, 0],
    'IL': [0, 0],
    'IN': [0, 0],
    'IA': [0, 0],
    'AZ': [0, 0],
    'ID': [0, 0],
    'ME': [0, 0],
    'MD': [0, 0],
    'MA': [0, 0],
    'UT': [0, 0],
    'MO': [0, 0],
    'MN': [0, 0],
    'MI': [0, 0],
    'MT': [0, 0],
    'MP': [0, 0],
    'MS': [0, 0]
}


def scores_to_dict(scores_file):
    scores = dict()
    for l in scores_file:
        word, score = l.split('\t')
        scores[word] = int(score)
    return scores


def word_score(word, scores):
    score = scores.get(word.lower())
    return score if score else 0


def tweet_score(line, scores):
    return sum(word_score(w, scores) for w in re.findall(r'\w+', line))


def tweet_state(tweet):
    place = tweet.get('place')
    if not place:
        return None
    if place['country_code'] != 'US':
        return None
    return place['full_name'].split().pop()


def update_state_score(tweet, state, scores):
    if state in STATE_SCORES:
        words = tweet.get('text')
        score = tweet_score(words, scores) if words else 0
        STATE_SCORES[state][0] += score
        STATE_SCORES[state][1] += 1


def happiest():
    max_key = max(STATE_SCORES.iteritems(), key=operator.itemgetter(1))[0]
    print(max_key)


def scores(tweet_file, scores):
    for l in tweet_file:
        data = json.loads(l)
        state = tweet_state(data)
        update_state_score(data, state, scores)
    for state, scores in STATE_SCORES.items():
        STATE_SCORES[state] = scores[0] / float(scores[1]) if scores[1] else 0


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    scores(tweet_file, scores_to_dict(sent_file))
    happiest()

    sent_file.close()
    tweet_file.close()


if __name__ == '__main__':
    main()
