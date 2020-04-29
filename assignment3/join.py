import MapReduce
import sys

"""
Word Count Example in the Simple Python MapReduce Framework
"""

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(record):
    mr.emit_intermediate(record[1], record)  

def reducer(key, vals):
    order = vals.pop(next(i for i in range(len(vals)) if vals[i][0] == 'order'))
    [mr.emit(order + v) for v in vals]

if __name__ == '__main__':
  inputdata = open(sys.argv[1])
  mr.execute(inputdata, mapper, reducer)
