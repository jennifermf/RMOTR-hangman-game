from .exceptions import *
import random

# Complete with your own, just for fun :)
LIST_OF_WORDS = ['muzzle',
    'theology',
    'nontoxic',
    'toxic',
    'satire',
    'outlast',
    'witch',
    'nerves',
    'intense',
    'faint',
    'rigging',
    'swept',
    'sandy',
    'copyright',
    'slashed',
    'pittance',
    'electricity',
    'beater',
    'chalkboard',
    'woodsy',
    'outlaw',
    'sluggish',
    'arbitrate',
    'devoured',
    'dismissive',
    'epiphany',
    'illegible',
    'sewing',
    'vines',
    'batteries',
    'razors',
    'vegan',
    'annihilate',
    'ataxia',
    'college',
    'collage',
    'glucose',
    'chorus',
    'parsed',
    'cautioned',
    'supplier',
    'impounded',
    'primitive',
    'turtle',
    'spurts',
    'mobility',
    'allergy']


def _get_random_word(list_of_words):
    if not list_of_words:
        raise InvalidListOfWordsException()
    else:
        return random.choice(list_of_words)

def _mask_word(word):
    if word == '':
        raise InvalidWordException()
    else:
        return '*' * len(word)

def _uncover_word(answer_word, masked_word, character):
    character = character.lower()
    if answer_word == '' and masked_word == '':
        raise InvalidWordException()
    elif len(character) > 1:
        raise InvalidGuessedLetterException
    elif len(answer_word) != len(masked_word):
        raise InvalidWordException
    elif character.lower() in answer_word.lower():
        newmasked = ''
        for a,b in zip(answer_word, masked_word):
            if a.lower() == character.lower():
                newmasked += a.lower()
            else:
                newmasked += b.lower()
        masked_word = newmasked
    return masked_word

def guess_letter(game, letter):
    letter = letter.lower()
    if game['remaining_misses'] == 0:
        raise GameFinishedException()
    elif letter.lower() not in game['answer_word'].lower():
        if game['masked_word'].lower() == game['answer_word'].lower():
            raise GameFinishedException()
        game['remaining_misses'] -= 1
        game['previous_guesses'].append(letter)
        if game['remaining_misses'] == 0:
            raise GameLostException
    else:
        if game['masked_word'].lower() == game['answer_word'].lower():
            raise GameWonException()
        elif letter.lower() in game['previous_guesses']:
            raise InvalidGuessedLetterException()
        elif letter.lower() in game['answer_word'].lower():
            game['previous_guesses'].append(letter)
            game['masked_word'] = _uncover_word(game['answer_word'], game['masked_word'], letter)
            if game['masked_word'].lower() == game['answer_word'].lower():
                raise GameWonException()
        else:
            raise GameFinishedException()
    return game

def start_new_game(list_of_words=None, number_of_guesses=5):
    if list_of_words is None:
        list_of_words = LIST_OF_WORDS

    word_to_guess = _get_random_word(list_of_words)
    masked_word = _mask_word(word_to_guess)
    game = {
        'answer_word': word_to_guess,
        'masked_word': masked_word,
        'previous_guesses': [],
        'remaining_misses': number_of_guesses,
    }
    return game
