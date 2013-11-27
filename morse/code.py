#/usr/bin/env python
# This software is licensed as described in the file LICENSE.txt, which
# you should have received as part of this distribution.

"""
.. module:: morse.code
   :platform: Unix, Windows
   :synopsis: Provides code "Telegraphs" to generate morse code

.. moduleauthor:: Tyndyll <morse@tyndyll.net>

>>> import morse.code
>>> p = morse.code.TelegraphPrinter()
>>> p.encode("SMS SMS")
'...--...   ...--...'
>>> w = morse.code.TelegraphWriter("test.ogg")
>>> w.encode("SMS SMS")
Exports the Morse for "SMS SMS" to test.ogg
>>> p = morse.code.TelegraphPlayer()
>>> p.encode("SMS SMS")
Plays the Morse for "SMS SMS" to test.ogg
"""

import alphabet

from numpy import linspace, sin, pi, float64, concatenate
from scikits.audiolab import play, available_file_formats, available_encodings


class CharacterNotFound(Exception):
    """Exception returned if an encoding is not available for a character"""

    def __init__(self, char):
        self.__chr = char

    def __str__(self):
        return self.__chr


class InvalidFormatEncoding(Exception):
    """Exception returned if an encoding is not available for an audio format"""

    def __init__(self, audio_format=None, audio_encoding=None):
        self.__format = audio_format
        self.__encoding = audio_encoding

    def __str__(self):
        return "Invalid Format (%s) or Encoding (%s)" % (self.__format, self.__encoding)


class Telegraph(object):
    """
    .. warning::

       This class is used primarily as a parent class to be inherited from. Please see :class:`TelegraphWriter`
       ,:class:`TelegraphPlayer` OR :class:`TelegraphPrinter`. It is created as a "new style" class.

    :param morse_alphabet: (str) Name of alphabet encoding to be used.
    """

    __codes = None
    __alphabet = None
    __alphabet_codes = None

    def __init__(self, morse_alphabet="international"):
        self.__alphabet = morse_alphabet
        self.__alphabet_codes = alphabet.get_alphabet(self.__alphabet)

    def _clean_message(self, message):
        """Internal function to clean a message

        Upper cases message, TODO remove extra whitespace
        :param message: (str) Message to be cleaned
        :return message: (str) Cleaned message
        :rtype: (str) String
        """
        message = message.upper()
        return message

    def generate_code(self, character, ignore_unknown=True):
        """Return the Morse encoding of a character, according to the configured alphabet

        :param character: (str) Character to be encoded
        :return: '.-' encoding of character
        :rtype: String
        :raise TypeError: If a single character is not passed
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        character = self._clean_message(character)
        if character in self.__alphabet_codes:
            return self.__alphabet_codes[character]
        else:
            if ignore_unknown:
                return " "
            else:
                raise CharacterNotFound

    def generate_tones(self, frequency=660, wpm=20, rate=44100):
        """Generate character tones

        The '.' and '-' Morse characters are represented by a NumPy array data structure. The structure, and the tone
        are affected by the frequency of the 'note' (the default, 660Hz is the musical note 'A'), the Words Per Minute
        (the number of words per minute defines how long each tone will be) and the sample rate (the frequency at which
        the tone is passed to the sound card).

        When an instance of a subclass of the `class:Telegraph` is created the tones can be regenerated. For example, to
        change the note to a middle C (frequency 262Hz), with a slower WPM rate

        >>> p = morse.code.TelegraphPlayer()
        >>> p.generate_tones(frequency=262, wpm=10)

        :param frequency: (int) Tone frequency. Default 660Hz is 'A'
        :param wpm: (int) Words per minute. Determines the length of a '.' and '-'.
        :param rate: (int) Sample rate.
        """
        wpm = int(wpm)
        frequency = int(frequency)
        # PARIS duration standard. See http://en.wikipedia.org/wiki/Morse_code
        length = (1200.0 / wpm) / 1000

        # Create a silent tone with the appropriate length
        self.__codes = { " ": self.__note(0, length, rate) }
        # Create a blank tone to set the data structure
        self.__codes["BLANK"] = self.__note(0, 0, rate)
        for letter, coding in alphabet.get_alphabet(self.__alphabet).items():
            morse_pattern = self.__codes["BLANK"]
            for element in coding:
                tone = None
                if element == ".":
                    tone = self.__note(frequency,length, rate)
                elif element == "-":
                    tone = self.__note(frequency,length * 3, rate)
                morse_pattern = concatenate([morse_pattern, tone, self.__codes[" "]])
            self.__codes[letter] = morse_pattern

    def __note(self, frequency, length, rate):
        """Internal function to generate the data structure for the frequency, rate and length

        :param frequency: (int) Tone frequency. Default 660Hz is 'A'
        :param wpm: (int) Words per minute. Determines the length of a '.' and '-'.
        :param rate: (int) Sample rate.
        :return: NumPy data structure
        """
        data = sin(linspace(0, length * frequency * 2 * pi, round(length * rate)))
        return data.astype(float64)

    def get_tone(self, character, ignore_unknown=True):
        """Return the Morse Code NumPy Array for a character

        :param character: (str) alphabetic character, in the range A-Z, a-z and 0-9
        :param ignore_unknown: (bool) Return a blank character if the character is not found, or raise an
            CharacterNotFound exception
        :raise TypeError: If a single character is not passed
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """

        if self.__codes is None:
            self.generate_tones()
        character = character.upper()
        char_int = ord(character)
        if (48 <= char_int <= 57) or (65 <= char_int <= 90):
            return self.__codes[character]
        else:
            if ignore_unknown:
                return self.__codes["BLANK"]
            else:
                raise CharacterNotFound(character)

    def _encode_message(self, message, output):
        """Encode a message into generated tones and output

        :param message: (str) String to be encoded
        :return: (func) function which will be used to output the generated tones
        :rtype: Function

        .. warning::

        This method is primarily for use by the child classes TelegraphPlayer and TelegraphWriter, 
        but any function can be passed in if it can handle the data structures containing the 
        tones. 

        See :func:`generate_tones` for the data structures

        """
        if self.__codes is None:
            self.generate_tones()
        for letter in message:
            if letter == " ":
                for i in xrange(5):
                    output(self.silence())
            else:
                output(self.get_tone(letter))
                for i in xrange(2):
                    output(self.silence())        

    def silence(self):
        """Return the data structure for a tones length of silence.

        This can be used to populate the gaps between characters (2 '.' tones) or the gap between words (5 '.' tones)

        :return: a single '.' tones worth of silence.
        :rtype: NumPy array
        """
        return self.__codes[" "]


class TelegraphWriter(Telegraph):
    """Write Morse Code to an Audio File. TelegraphWriter uses SndFile from the scikits.audiolab package to write out
    audio data,  and as such TelegraphWriter can output to whatever formats are available. See the
    :func:`available_file_formats` and :func:`available_encodings` to determine what audio outputs are available.

    :param filename: (str) Filename to output to
    :param audio_format: (str) Audio format
    :param audio_encoding: (str) Encoding of audio_format
    :param alphabet: (str) Morse Code alphabet to be used
    :raise InvalidFormatEncoding:

    The default format and encoding is ogg vorbis (http://www.vorbis.com). This produces good quality compressed
    files, but is slower that (say) WAV 16pcm
    """

    def __init__(self, filename, audio_format="ogg", audio_encoding="vorbis", alphabet="international"):
        super(TelegraphWriter, self).__init__(alphabet)
        self.__filename = filename        
        self.__audio_format = audio_format
        self.__audio_encoding = audio_encoding

        self.__output_formats = available_file_formats()

        from scikits.audiolab import Format, Sndfile          
        if self.__audio_format not in available_file_formats() or self.__audio_encoding not in available_encodings(self.__audio_format):
            raise InvalidFormatEncoding(self.__audio_format, self.__audio_encoding)
        output_format = Format(self.__audio_format, self.__audio_encoding)
        self.__output_file = Sndfile(self.__filename, 'w', output_format, 1, 44100)

    def __write_character(self, character):
        """Write a character to the output file. 

        :param character: (str) Character to be written
        :raise TypeError: If a single character is not passed
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        self.__output_file.write_frames(character)

    def encode(self, message):
        """Write a message to the output file. 

        :param message: (str) Message to be written
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        super(TelegraphWriter, self)._encode_message(self._clean_message(message), self.__write_character)
        self.__output_file.sync()


class TelegraphPlayer(Telegraph):
    """Play the Morse Code through the audio device

    :param alphabet: (str) Morse Code alphabet to be used
    """

    def __init__(self, morse_alphabet="international"):
        super(TelegraphPlayer, self).__init__(morse_alphabet)

    def __play_character(self, character):
        """Play a character through the audio device

        :param character: (str) Character to be played
        :raise TypeError: If a single character is not passed
        """
        play(character)

    def encode(self, message):
        """Play a message to the output device.

        :param message: (str) Message to be played
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        super(TelegraphPlayer, self)._encode_message(self._clean_message(message), self.__play_character)


class TelegraphPrinter(Telegraph):
    """Convert ASCII text to Morse encoding
    :param alphabet: (str) Morse Code alphabet to be used
    """

    def __init__(self, morse_alphabet="international"):
        super(TelegraphPrinter, self).__init__(morse_alphabet)

    def encode(self, message):
        """Return the provided ASCII string as an encoded Morse string

        :param message: (str) Message to be played
        :raise CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        msg = ""
        for i in self._clean_message(message):
            if i == " ":
                msg += "   "
            else:
                msg += self.generate_code(i)
        return msg