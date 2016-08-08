"""
Evaluate a set of test alignments against a gold set
Computes precision, recall, f1-score, aer
"""
from __future__ import division
import sys, re, json
from collections import defaultdict

class Alignment:
    def __init__(self, handle):
        self.all_align = set()
        self.sents_align = {}

        for l in handle:
          t = l.strip().split() 
          sent = int(t[0])
          align = (int(t[1]), int(t[2]))
          self.all_align.add((sent, align))

class Score:
    def __init__(self):
        self.gold = 0
        self.test = 0
        self.correct = 0

    def increment(self, gold_set, test_set):
        self.gold += len(gold_set)
        self.test += len(test_set)
        self.correct += len(gold_set & test_set)

    def aer(self):
        if self.test + self.gold == 0: return 0.0
        return 1.0 - float(2.0*self.correct)/(self.test+self.gold)

    def fscore(self): 
        pr = self.precision() + self.recall()
        if pr == 0: return 0.0
        return (2 * self.precision() * self.recall()) / pr

    def precision(self): 
        if self.test == 0: return 0.0
        return self.correct / self.test

    def recall(self): 
        if self.gold == 0: return 0.0
        return self.correct / self.gold    

    def output_score(self, name):
        print("Fname     : " + str(name) + "\n" +\
              "Total     : " + str(self.gold) + "\n" +\
              "Precision : " + str(self.precision()) + "\n" +\
              "Recall    : " + str(self.recall()) + "\n" +\
              "F1-Score  : " + str(self.fscore()) + "\n" +\
              "AER       : " + str(self.aer()))

def compute_score(align1, align2):
    score = Score()
    score.increment(align1.all_align, align2.all_align)
    return score

def main(gold_alignment, test_alignment):
    align1 = Alignment(gold_alignment)
    align2 = Alignment(test_alignment)
    score = compute_score(align1, align2)
    score.output_score("test")
      
if __name__ == "__main__": 
    if len(sys.argv) != 3:
        print("Usage: python eval_alignment.py [key_file] [output_file]")
        sys.exit(1)
    main(open(sys.argv[1]), open(sys.argv[2])) 
