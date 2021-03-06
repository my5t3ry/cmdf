#!/usr/bin/python3 -u
import subprocess
from collections import Counter

import Levenshtein
import numpy
import pandas as pd
from flask import Flask, request

app = Flask(__name__)

words =[]
probs  =[]
word_freq_dict = None
Total = None

@app.route('/correct', methods=['POST'])
def get_tasks():
  global words
  global probs
  global word_freq_dict
  global Total

  for k in word_freq_dict.keys():
    probs[k] = word_freq_dict[k] / Total
  cmd = request.form['cmd']

  similarities = [(Levenshtein.distance(v, cmd)) for v in
                  word_freq_dict.keys()]
  df = pd.DataFrame.from_dict(probs, orient='index').reset_index()
  df = df.rename(columns={ 0: 'Prob'})
  df['Similarity'] = similarities
  df['cmd'] =  word_freq_dict.keys()
  output = df.sort_values(['Similarity'], ascending=True)

  return "{\"cmd\":\"" + list(output.head(1).to_dict('dict')["cmd"].values())[0]+"\"}"


def init():
  global words
  global probs
  global word_freq_dict
  global Total
  words_str = subprocess.check_output(
      "echo \"$(cat /home/my5t3ry/.zsh_history)\"", shell=True)

  for word in words_str.splitlines():
    try:
      cur = word.decode(encoding="utf-8").split(";")[1]
      words.append(cur)
      if "sshc" in cur:
        print(cur)
    except Exception as e:
      print("shit")

  V = numpy.array(words)
  unique, counts = numpy.unique(V, return_counts=True)
  dict(zip(unique, counts))

  print(f"The first ten words in the text are: \n{words[0:10]}")
  print(f"There are {len(unique)} unique words in the vocabulary")
  word_freq_dict = {}
  word_freq_dict = Counter(words)
  print(word_freq_dict.most_common()[0:10])
  probs = {}
  Total = sum(word_freq_dict.values())



if __name__ == '__main__':
  init()
  app.run(debug=True, port=7755)



