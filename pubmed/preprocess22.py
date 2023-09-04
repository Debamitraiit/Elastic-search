"""  Importing libraries  """
import sys
import os
import json


"""  ES database name  """
INDEX_NAME = 'pubmed_24'
INDEX_TYPE = 'pubmed_24n'


"""  Creating ES indexing and data index  """
FILENAME = os.path.basename(sys.argv[1]).split('.')[0].strip()
idx = {"index": {"_index": INDEX_NAME, "_type": INDEX_TYPE}}

counter = 0
for rec in sys.stdin:
    counter += 1
    idx["index"]['_id'] = FILENAME + '_' + str(counter).zfill(8)
    print(json.dumps(idx))
    print(rec.strip())

