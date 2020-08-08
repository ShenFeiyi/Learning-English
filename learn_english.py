#!/usr/bin/env python3
# -*- coding:utf-8 -*-

def read(d, word):
    import pyttsx3 as tts
    engine = tts.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if voice.name == 'Mei-Jia':
            cn_voice = voice
        if voice.name == 'Samantha':
            en_voice = voice

    engine.setProperty('rate', 175)
    engine.setProperty('voice',en_voice.id)
    engine.say(word)
    engine.setProperty('voice',cn_voice.id)
    for index in d[word]:
        engine.say(d[word][index])
    engine.runAndWait()
    engine.stop()
    del tts

def find_chinese_word(d, cn_word):
    word_dict = {}
    for w in d:
        for index in d[w]:
            meaning = d[w][index]
            if meaning == cn_word:
                word_dict[w] = d[w]
    return word_dict

def find_english_word(d, en_word):
    word_dict = {}
    if en_word in d:
        for index in d[en_word]:
            meaning = d[en_word][index]
            wd = find_chinese_word(d, meaning)
            for word in wd:
                if not word == en_word:
                    word_dict.update({word:wd[word]})
    else:
        raise KeyError('Word not in the dictionary.')
    return word_dict

def find_word(**kwarg):
    if 'dictionary' in kwarg:
        d = kwarg['dictionary']
        
        if 'word' in kwarg:
            word = kwarg['word']
            
            if 'lang' in kwarg:
                lang = kwarg['lang']
                if word[0].islower() or word[0].isupper():
                    if not lang is 'en':
                        lang = 'en'
                else:
                    if not lang is 'cn':
                        lang = 'cn'
            else:
                if word[0].islower() or word[0].isupper():
                    lang = 'en'
                else:
                    lang = 'cn'

            if lang is 'en':
                word_dict = find_english_word(d, word)
            elif lang is 'cn':
                word_dict = find_chinese_word(d, word)
            
        else:
            raise ValueError('Word not found.')
    else:
        raise ValueError('Dictionary not found.')
    
    return word_dict

def read_dict(filename,**kwarg):
    if 'dictionary' in kwarg:
        dictionary = kwarg['dictionary']
    else:
        dictionary = {}

    with open(filename,'r',encoding='UTF-8-sig') as file:
        lines = file.readlines()
    for line in lines:
        chars = line.split(' ')
        word = chars[0]
        for n_word in range(1,len(chars)):
            if chars[n_word][0].islower() or chars[n_word][0].isupper():
                word = word + ' ' + chars[n_word]
            else:
                break
        meanings = chars[n_word:len(chars)-1]
        last_meaning = chars[len(chars)-1][:-1]
        
        if word in dictionary:
            have_n_meanings = len(dictionary[word])
            pre_meanings = []
            for i in range(have_n_meanings):
                pre_meanings.append(dictionary[word][i])
            for meaning in meanings:
                if not meaning in pre_meanings:
                    pre_meanings.append(meaning)
                    dictionary[word][have_n_meanings] = meaning
                    have_n_meanings += 1
            if not last_meaning in pre_meanings:
                dictionary[word][have_n_meanings] = last_meaning
        else:
            dictionary[word] = {}
            have_n_meanings = 0
            pre_meanings = []
            for meaning in meanings:
                if not meaning in pre_meanings:
                    pre_meanings.append(meaning)
                    dictionary[word][have_n_meanings] = meaning
                    have_n_meanings += 1
            if not last_meaning in pre_meanings:
                dictionary[word][len(dictionary[word])] = last_meaning

    rm = []
    for word in dictionary:
        for index in dictionary[word]:
            if dictionary[word][index] == '':
                rm.append([word,index])
    for item in rm:
        dictionary[item[0]].pop(item[1])

    return dictionary

GRE = read_dict('GRE3000.txt')
word_list = read_dict('TOEFL.txt',dictionary=GRE)

import random
words = random.sample(word_list.keys(),10)
for word in words:
    word_dict = find_word(dictionary=word_list, word=word)
    print(f'{word} {word_list[word]}')
    read(word_list, word)
    for w in word_dict:
        print(f'{w} {word_dict[w]}')
        read(word_dict, w)
    print('')
