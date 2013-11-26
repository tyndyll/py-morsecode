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

__author__ = 'tyndyll'

__international = {
    "0":    "-----",
    "1":    ".----",
    "2":    "..---",
    "3":    "...--",
    "4":    "....-",
    "5":    ".....",
    "6":    "-....",
    "7":    "--...",
    "8":    "---..",
    "9":    "----.",
    "A":    ".-",
    "B":    "-...",
    "C":    "-.-.",
    "D":    "-..",
    "E":    ".",
    "F":    "..-.",
    "G":    "--.",
    "H":    "....",
    "I":    "..",
    "J":    ".---",
    "K":    "-.-",
    "L":    ".-..",
    "M":    "--",
    "N":    "-.",
    "O":    "---",
    "P":    ".--.",
    "Q":    "--.-",
    "R":    ".-.",
    "S":    "...",
    "T":    "-",
    "U":    "..-",
    "V":    "...-",
    "W":    ".--",
    "X":    "-..-",
    "Y":    "-.--",
    "Z":    "--.."
}

__codes = {}

def get_alphabet(alphabet_name="international"):
    """Get a mapping of characters to their morse equivalent, by alphabet

    Args:
        alphabet_name: Name of the alphabet chart to return. Default is international

    Returns:
        A dict mapping characters to the corresponding morse code string equivalent (i.e. -.)
    """
    global __international
    return {
        "international": __international
    }[alphabet_name]