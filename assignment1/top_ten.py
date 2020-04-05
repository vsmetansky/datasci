import sys
import json
import re
from operator import itemgetter
from collections import OrderedDict


def insert_tag(tag_nums, tag):
    if tag_nums.get(tag):
        tag_nums[tag] += 1
    else:
        tag_nums[tag] = 1


def update_tag_nums(tag_nums, tags):
    for t in tags:
        insert_tag(tag_nums, t.get('text'))


def has_tags(data):
    try:
        return bool(data['entities']['hashtags'])
    except (TypeError, KeyError):
        return False


def tag_nums(tweet_file):
    tag_nums = dict()
    for l in tweet_file:
        data = json.loads(l)
        if has_tags(data):
            tags = data['entities']['hashtags']
            update_tag_nums(tag_nums, tags)
    return tag_nums


def get_top(tag_nums, n):
    k = n if n < len(tag_nums) else len(tag_nums)
    return sorted(tag_nums.items(), key=itemgetter(1))[:-k-1:-1]


def main():
    tweet_file= open(sys.argv[1])

    nums = tag_nums(tweet_file)

    for t, n in get_top(nums, 10):
        print(u'{} {}'.format(t, n))

    tweet_file.close()


if __name__ == '__main__':
    main()
