#/usr/bin/env python
# Copyright (c) 2013, Tyndyll
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met: 
# 
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer. 
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution. 
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies, 
# either expressed or implied, of the FreeBSD Project.

"""
.. module:: morse.code
   :platform: Unix, Windows
   :synopsis: Provides code "Telegraphs" to generate morse code

.. moduleauthor:: Tyndyll <morse@tyndyll.net>


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
    """Base Telegraph Class

    .. note::

       This class is used primarily as a parent class to be inherited from. Please see :class:`TelegraphWriter`
       or :class:`TelegraphPlayer`. It is created as a "new style" class.

    """

    __codes = None
    __alphabet = None

    def __init__(self, morse_alphabet="international"):
        """Initialisation. 

        Args:
            alphabet (str): Name of alphabet encodig to be used. See TODO

        """
        self.__alphabet = morse_alphabet

    def generate_tones(self, frequency=660, wpm=20, rate=44100):
        """Utility function to generate character generate_tones

        Args:
            frequency (int): Tone frequency. Default 660Hz is 'A' TODO
            wpm (int): Words per minute. Determines the length of a '.' and '-'. Higher wpm rates 
                        require shorter tones
            rate (int): Sample rate. 
        """

        # PARIS duration standard. See http://en.wikipedia.org/wiki/Morse_code
        length = (1200.0 / wpm) / 1000

        # Create a silent tone with the appropriate length
        self.__codes = { " ": self.__note(0,length, rate) }
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
        """Internal function to generate the data structure for the frequency, rate and length"""
        data = sin(linspace(0, length * frequency * 2 * pi, round(length * rate)))
        return data.astype(float64)

    def get_character(self, character, ignore_unknown=True):
        """Return the Morse Code string for a character

        Args:
            character (str): alphabetic character, in the range A-Z, a-z and 0-9
            ignore_unknown (bool): Return a blank character if the character is not found, 
                                    or raise an Exception
        Returns:
            encoded_character (str): '.-' encoding of character

        Raises: 
            TypeError: If a single character is not passed
            CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        if self.__codes is None:
            self.generate_tones()
        character = character.upper()
        char_int = ord(character)
        if (48 <= char_int and char_int <= 57) or (65 <= char_int and char_int <= 90):
            return self.__codes[character]
        else:
            if ignore_unknown:
                return self.__codes["BLANK"]
            else:
                raise CharacterNotFound(character)

    def _encode_message(self, message, output):
        """Encode a message into generated tones and output

        Args:
            message (str): String to be encoded
            output (func): function which will be used to output the generated tones

        .. note::

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
                output(self.get_character(letter))
                for i in xrange(2):
                    output(self.silence())        

    
    def silence(self):
        """Return the data structure for a tones length of silence"""
        return self.__codes[" "]


class TelegraphWriter(Telegraph):

    """Write Morse Code to an Audio File

    Encode text as Morse Code into an audio file
    """

    def __init__(self, filename, audio_format="ogg", audio_encoding="vorbis", alphabet="international"):
        """Constructor

        Args:
            filename (str): Filename to output to
            audio_format (str): Audio format
            audio_encoding (str): Encoding of audio_format
            alphabet (str): Morse Code alphabet to be used

        TelegraphWriter uses SndFile from the scikits.audiolab package to write out audio data, 
        and as such TelegraphWriter can output to whatever formats are available. See the 
        :func:`available_file_formats` and :func:`available_encodings to determine what audio
        outputs are available.

        The default format and encoding is ogg vorbis (http://www.vorbis.com). This produces 
        good quality compressed files, but is slower that (say) WAV 16pcm
        """
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

    def encode_character(self, character):
        """Write a character to the output file. 

        Args:
            character (str): Character to be written

        Raises: 
            TypeError: If a single character is not passed
            CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        self.__output_file.write_frames(self.get_character(character))

    def encode_message(self, message):
        """Write a message to the output file. 

        Args:
            message (str): Message to be written

        Raises:             
            CharacterNotFound: if ignore_unknown is set to False and a character is not found
        """
        super(TelegraphWriter, self).encode_message(message, self.encode_character)
        self.__output_file.sync()


class TelegraphPlayer(Telegraph):

    def __init__(self, alphabet="international"):
        """

        """
        super(TelegraphPlayer, self).__init__(alphabet)        

    def encode_character(self, character):
        """Play a character through the audio device

        Args:
            character (str): Character to be played

        Raises: 
            TypeError: If a single character is not passed
        """
        play(character)

    def encode_message(self, message):
        """Play a message through the audio device

        Args:
            message (str): Message to be played

        """
        super(TelegraphPlayer, self)._encode_message(message, self.encode_character)