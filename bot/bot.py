#!/usr/bin/env python

"""
This module runs the toast every word twitter bot.

Every time it runs, it retrieves a random word from the Wordnik API, 'toasts' it
into an image of a piece of toast, and tweets that image from @toasteveryword
(https://twitter.com/toasteveryword)
"""

import logging
import config
from random_word import get_random_word
from toaster import Toaster
from twython import Twython


class Bot:
    def __init__(self, error_log='../error.log', word_log='../words.txt'):
        self.toaster = Toaster()
        self.word_log = word_log
        self.twitter_api = Twython(
            config.TWITTER['key'],
            config.TWITTER['secret'],
            config.TWITTER['token'],
            config.TWITTER['token_secret']
        )

        logging.basicConfig(
            filename=error_log,
            format='%(asctime)s %(message)s',
            datefmt='%m/%d/%Y %I:%M:%S %p'
        )

    def run(self):
        self.get_word()
        toast = self.toaster.make_toast(self.word)
        self.tweet_image(toast)

    def get_word(self):
        self.word = get_random_word()
        with open(self.word_log, 'a') as log_file:
            print(self.word, file=log_file)

    def tweet_image(self, image):
        try:
            response = self.twitter_api.upload_media(media=image)
            self.twitter_api.update_status(media_ids=[response['media_id']])
        except KeyError:
            with open('assets/' + self.word, 'wb') as image_file:
                image_file.write(image)
            raise Exception('Unable to upload image.')


if __name__ == '__main__':
    bot = Bot()
    try:
        bot.run()
    except Exception as e:
        logging.error(e)
        exit(1)
