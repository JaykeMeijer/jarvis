"""
Optimization idea: Pre-soundex all words in tree, triggers
"""
from redis_funcs import say
from actions import Actions
import json
import random
from phonetics import awis, cwis


class SpeechTree:
    # Currently we threshold on number of matches. Perhaps add a fraction?
    score_threshold = 1

    def __init__(self, filename):
        with open(filename) as f:
            config = json.load(f)

        self.action_tree = config['tree']
        self.keyword = config['keyword']
        self.repeat = config['repeat']
        self.stop = config['stop']

        self.current = None

    @property
    def active(self):
        return self.current is not None

    def activate(self):
        if self.current is None:
            self.current = self.action_tree
        else:
            print("Already active!")

    def deactivate(self):
        self.current = None

    def set_active(self, action):
        self.current = action

    def process_text(self, text):
        if self.active:
            if awis(self.stop['triggers'], text):
                say(random.choice(self.stop['responses']))
                self.deactivate()
            else:
                scores = []
                for action in self.current:
                    score = cwis(action['trigger'], text)
                    #print(action['trigger'], score)
                    if score >= self.score_threshold:
                        scores.append((score, action))

                if len(scores) > 0:
                    best_action = sorted(
                        scores, key=lambda x: x[0], reverse=True)[0][1]
                    self.handle_action(best_action)
                else:
                    say("I can't help you with that")
        else:
            if awis(self.keyword['triggers'], text):
                say(random.choice(self.keyword['responses']))
                self.activate()

    def handle_action(self,action):
        for a in action['actions']:
            if hasattr(Actions, a['type']):
                getattr(Actions, a['type'])(self, a['value'])
            else:
                say(f"ERROR! Unknown action type {a['type']}")

        if "next" in action:
            self.set_active(action['next'])
        else:
            self.deactivate()

    def please_repeat(self):
        say(random.choice(self.repeat))
