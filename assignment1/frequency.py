import sys
import json
import re


def insert_word(freqs, word):
    if is_present(freqs, word):
        freqs[word] += 1
    else:
        freqs[word] = 1


def update_word_nums(freqs, words):
    for w in words:
        w_norm = w.lower()
        insert_word(freqs, w_norm)


def is_present(freqs, word):
    return bool(freqs.get(word))


def is_tweet(data):
    return bool(data.get('text'))


def frequencies(tweet_file):
    word_nums = dict()
    total_word_count = 0
    for l in tweet_file:
        data = json.loads(l)
        if is_tweet(data):
            words = re.findall(r'\w+', data['text'])
            update_word_nums(word_nums, words)
            total_word_count += len(words)
    return {k: word_nums[k] / float(total_word_count) for k in word_nums}


def main():
    tweet_file = open(sys.argv[1])

    for t, f in frequencies(tweet_file).items():
        print('{} {}'.format(t, f))

    tweet_file.close()


if __name__ == '__main__':
    main()
