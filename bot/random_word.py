#!/usr/bin/env python

""" This module contains a function that returns a random word. """

from config import WORDNIK_KEY
import requests
import logging


def get_random_word(**kwargs):
    """
    Get a random word with the specified frequency from the Wordnik API.

    Keyword args override the defaults and are passed directly to the Wordnik
    API. See http://developer.wordnik.com/docs.html#!/words/getRandomWord_get_4
    for a full list of parameters.
    """
    base_url = 'http://api.wordnik.com/v4/words.json/randomWord'
    defaults = {
        'minCorpusCount': 1000,  # Eliminates some of the really weird words
        'maxCorpusCount': -1,
        'minDictionaryCount': 1,
        'maxDictionaryCount': 1,
        'minLength': 1,
        'maxLength': -1,
        'excludePartOfSpeech': 'proper-noun,family-name,affix,given-name,proper-noun-plural,proper-noun-posessive,noun-posessive,suffix',
        'hasDictionaryDef': True,
        'api_key': WORDNIK_KEY
    }
    r = requests.get(base_url, params={**defaults, **kwargs})
    try:
        # Raise HTTP Error if a failure status code is returned
        r.raise_for_status()
        json = r.json()
        return json['word'].lower()
    except KeyError:
        # Wordnik API returns errors of the form {message: 'Something went wrong', type: 'error'}
        logging.error('Wordnik API error at URL: %s \nError: %s', r.url, json['message'])
    except Exception as e:
        logging.error(e)
