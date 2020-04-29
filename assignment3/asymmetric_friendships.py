import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    mr.emit_intermediate(record[0], record[1])  

def reducer(key, vals):
    for v in vals:
        friends_of_friend = mr.intermediate.get(v)
        if not friends_of_friend or key not in friends_of_friend:
            mr.emit((v, key))
            mr.emit((key, v))

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
