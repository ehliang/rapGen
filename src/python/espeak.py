import collections
import re
import subprocess


class ESpeak:
    def __init__(self, amplitude=100, word_gap=10, capitals=1, line_length=1,
                 pitch=50, speed=175, voice='en', spell_punctuation=[],
                 split=''):
        """
        The base ESpeak class. You can set espeak's arguments from the
        named parameters or change them after creation using the properties
        """

        args = [('amplitude',         ['-a', amplitude, int]),
                ('word_gap',          ['-g', word_gap, int]),
                ('capitals',          ['-k', capitals, int]),
                ('line_length',       ['-l', line_length, int]),
                ('pitch',             ['-p', pitch, int]),
                ('speed',             ['-s', speed, int]),
                ('voice',             ['-v', voice, str]),
                ('spell_punctuation', ['--punct=', ''.join(spell_punctuation),
                                       str]),
                ('split',             ['--split=', split, str])]
        self.args = collections.OrderedDict(args)

    def say(self, text):
        """
        Make espeak read the text directly

        Parameters
        ----------
        text : str
            The text to be read

        Returns
        -------
        phoneme : str
            The phoneme, as read by speak

        """
        return self._execute(self._espeak_args(text))

    def save(self, text, filename):
        """
        Make espeak read the text silently, saving the speech to a file

        Parameters
        ----------
        text : str
            The text to be read
        filename : str
            The name of the target file

        Returns
        -------
        phoneme : str
            The phoneme, as read by speak

        """

        return self._execute(self._espeak_args(text, filename))

    def command(self, text, filename=''):
        """
        Generates a valid espeak command from the given state and parameters

        Parameters
        ----------
        text : str
            The text to be read
        filename : str, optional
            The name of the target file

        Returns
        -------
        command : str
            The complete command
        """

        return ' '.join(self._espeak_args(text, filename))

    @property
    def voices(self):
        """
        Generates a dict containing all available voices for espeak

        Returns
        -------
        voices : dict
           The generated voices dict
        """

        def other_languages_list(text):
            n_text = text.strip()
            print(text)
            if not text:
                return []
            else:
                return re.findall('\((\S+)\s(\d+)\)', n_text)
        entries = self._execute(['espeak', '--voices']).split("\n")[1:-1]
        voices_dict = {}
        for entry in entries:
            extracted = self._extract_entry(entry)
            voices_dict[extracted['voice_name']] = {
                'PTY': extracted['pty'],
                'Age and Gender': extracted['age_gender'],
                'Language': extracted['language'],
                'File': extracted['file'],
                'Other Languages': other_languages_list(
                    extracted['other_languages'])
                }
        return voices_dict

    def _extract_entry(self, entry):
        extract_re = re.compile(r"""
                                  ^\s+
                                     (?P<pty>\d+)
                                  \s+
                                     (?P<language>\S+)
                                  \s+
                                     (?P<age_gender>\S+)
                                  \s+
                                     (?P<voice_name>\S+)
                                  \s+
                                     (?P<file>\S+)
                                     (?P<other_languages>.+)""", re.X)
        return re.match(extract_re, entry).groupdict()

    def _espeak_args(self, text, filename=''):
        self._validate_args()
        if filename:
            save = ["{0}{1}".format(self.split[0], self.split[1]),
                    "-w{}".format(filename)]
        else:
            save = []
        args = ['espeak'] + \
               ["{0}{1}".format(v[0], v[1]) for v in self.args.values()] + \
               ['-x'] + save + [text]
        print(args)
        return args

    def _validate_args(self):
        for k, v in self.args.items():
            if type(v[1]) != v[2]:
                raise TypeError(
                    "Error: argument {0} does not match {1}".format(k, v[2]))

    def _execute(self, cmd):
        return subprocess.check_output(cmd,
                                       stderr=subprocess.PIPE).decode('UTF-8')

    """
    Below are some automatically generated getters/setters useful for setting
    espeak's parameters.
    """

    @property
    def amplitude(self):
        return self.args['amplitude']

    @amplitude.setter
    def amplitude(self, v):
        self.args['amplitude'][1] = v

    @property
    def word_gap(self):
        return self.args['word_gap']

    @word_gap.setter
    def word_gap(self, v):
        self.args['word_gap'][1] = v

    @property
    def capitals(self):
        return self.args['capitals']

    @capitals.setter
    def capitals(self, v):
        self.args['capitals'][1] = v

    @property
    def line_length(self):
        return self.args['line_length']

    @line_length.setter
    def line_length(self, v):
        self.args['line_lenght'][1] = v

    @property
    def pitch(self):
        return self.args['pitch']

    @pitch.setter
    def pitch(self, v):
        self.args['pitch'][1] = v

    @property
    def speed(self):
        return self.args['speed']

    @speed.setter
    def speed(self, v):
        self.args['speed'][1] = v

    @property
    def voice(self):
        return self.args['voice']

    @voice.setter
    def voice(self, v):
        self.args['voice'][1] = v

    @property
    def spell_punctuation(self):
        return self.args['spell_punctuation']

    @spell_punctuation.setter
    def spell_punctuation(self, v):
        self.args['spell_punctuation'][1] = v

    @property
    def split(self):
        return self.args['split']

    @split.setter
    def split(self, v):
        self.args['split'][1] = v