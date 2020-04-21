#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  post_generator.py
#
#  Copyright 2020 Thiago da Silva Teixeira <teixeira.zeus@gmail.com>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#
import sys
import pickle
import random
import numpy as np
import statistics

def remove_asp(word):
    new = ""
    for w in word:
        if w not in ['"', '*', '.', '?']:
            new += w
    return new.lower()

def train():
    coments = []
    with open("train-balanced-sarcasm.csv", 'r') as file:
        line = file.readline()
        while line:
            line = file.readline().split(',')[1]
            coments.append(line)

    chain = {'BEGIN':{}}
    for coment in coments:
        words = coment.split()
        words = [remove_asp(w) for w in words]

        if len(words) == 0: continue

        if words[0] not in chain['BEGIN'].keys():
            chain['BEGIN'][words[0]] = 0

        chain['BEGIN'][words[0]] += 1

        for i in range(1,len(words)):
            if words[i-1] not in chain.keys(): chain[words[i-1]] = {}
            if words[i] not in chain[words[i-1]].keys(): chain[words[i-1]][words[i]] = 0
            chain[words[i-1]][words[i]] += 1
    return chain

def w_and_h(word):
    options = list(chain[word].keys())
    heights = [chain[word][op] for op in options]
    s = sum(heights)
    for i in range(len(heights)):
        heights[i] = heights[i]/s

    return options, heights

#chain = train()
#pickle.dump(chain, open('chain', 'wb'))
chain = pickle.load(open('chain', 'rb'))

o,h = w_and_h('BEGIN')
post = [np.random.choice(o, p=h)]

# the medium lenght of the posts is 32 words
for i in range(32):
    try:
        o,h = w_and_h(post[-1])
        post.append(np.random.choice(o, p=h))
    except:
        break

print( ' '.join(post).capitalize() )
