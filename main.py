from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.clock import Clock
#from android.permissions import request_permissions, Permission

import sys, os

from deep_translator import GoogleTranslator, PonsTranslator, LingueeTranslator, MyMemoryTranslator

Window.clearcolor = (1, 1, 1, 1)

import requests
import json

from plyer import stt

__version__ = "0.1.10"

# Detect Source Language
# http://mt.roboticpolyglot.com/detect?input='This is English'

# Get Source Languages
# http://mt.roboticpolyglot.com/languages?source=all

# Get Target Language (based on source)
# http://mt.roboticpolyglot.com/languages?source=en

# Translate
# http://mt.roboticpolyglot.com/translate?source=en&target=fr&input='I am a robot that speaks many languages'


LANGUAGE_CODES_LANGS = \
{
    'af': 'afrikaans',
    'sq': 'albanian',
    'am': 'amharic',
    'ar': 'arabic',
    'hy': 'armenian',
    'az': 'azerbaijani',
    'eu': 'basque',
    'be': 'belarusian',
    'bn': 'bengali',
    'bs': 'bosnian',
    'bg': 'bulgarian',
    'ca': 'catalan',
    'ceb': 'cebuano',
    'ny': 'chichewa',
    'zh-cn': 'chinese (simplified)',
    'zh-tw': 'chinese (traditional)',
    'co': 'corsican',
    'hr': 'croatian',
    'cs': 'czech',
    'da': 'danish',
    'nl': 'dutch',
    'en': 'english',
    'eo': 'esperanto',
    'et': 'estonian',
    'tl': 'filipino',
    'fi': 'finnish',
    'fr': 'french',
    'fy': 'frisian',
    'gl': 'galician',
    'ka': 'georgian',
    'de': 'german',
    'el': 'greek',
    'gu': 'gujarati',
    'ht': 'haitian creole',
    'ha': 'hausa',
    'haw': 'hawaiian',
    'iw': 'hebrew',
    'hi': 'hindi',
    'hmn': 'hmong',
    'hu': 'hungarian',
    'is': 'icelandic',
    'ig': 'igbo',
    'id': 'indonesian',
    'ga': 'irish',
    'it': 'italian',
    'ja': 'japanese',
    'jw': 'javanese',
    'kn': 'kannada',
    'kk': 'kazakh',
    'km': 'khmer',
    'ko': 'korean',
    'ku': 'kurdish (kurmanji)',
    'ky': 'kyrgyz',
    'lo': 'lao',
    'la': 'latin',
    'lv': 'latvian',
    'lt': 'lithuanian',
    'lb': 'luxembourgish',
    'mk': 'macedonian',
    'mg': 'malagasy',
    'ms': 'malay',
    'ml': 'malayalam',
    'mt': 'maltese',
    'mi': 'maori',
    'mr': 'marathi',
    'mn': 'mongolian',
    'my': 'myanmar (burmese)',
    'ne': 'nepali',
    'no': 'norwegian',
    'ps': 'pashto',
    'fa': 'persian',
    'pl': 'polish',
    'pt': 'portuguese',
    'pa': 'punjabi',
    'ro': 'romanian',
    'ru': 'russian',
    'sm': 'samoan',
    'gd': 'scots gaelic',
    'sr': 'serbian',
    'st': 'sesotho',
    'sn': 'shona',
    'sd': 'sindhi',
    'si': 'sinhala',
    'sk': 'slovak',
    'sl': 'slovenian',
    'so': 'somali',
    'es': 'spanish',
    'su': 'sundanese',
    'sw': 'swahili',
    'sv': 'swedish',
    'tg': 'tajik',
    'ta': 'tamil',
    'te': 'telugu',
    'th': 'thai',
    'tr': 'turkish',
    'uk': 'ukrainian',
    'ur': 'urdu',
    'uz': 'uzbek',
    'vi': 'vietnamese',
    'cy': 'welsh',
    'xh': 'xhosa',
    'yi': 'yiddish',
    'yo': 'yoruba',
    'zu': 'zulu',
    'fil': 'Filipino',
    'he': 'Hebrew'
}

LANGUAGE_LANGS_CODES = {v: k for k, v in LANGUAGE_CODES_LANGS.items()}


class MainLayout(BoxLayout):

    auto_inserted = False
    # dictate_btn = ObjectProperty()
    head_spinner = ObjectProperty(None)
    payload = ObjectProperty(None)
    from_spinner = ObjectProperty(None)
    dictate_btn = ObjectProperty(None)
    to_spinner = ObjectProperty(None)
    result_label = ObjectProperty(None)

    # def __init__(self, **kwargs):
    #      self.payload.bind(on_key_down)


    @staticmethod
    def get_supported_languages(translator='Robotic Polyglot', source='all', auto_included=False, *args):

        if translator == 'Google Translate' or translator == 'My Memory' \
                or translator == 'Pons' or translator == 'Linguee' : #or translator == 'Robotic Polyglot':
            # supported_languages = GoogleTranslator.supported_languages
            supported_languages = LANGUAGE_LANGS_CODES
            if auto_included and not MainLayout.auto_inserted:
                # supported_languages.insert(0, 'auto')
                MainLayout.auto_inserted = True

        # elif translator == 'Pons':
        #     supported_languages = PonsTranslator.supported_languages
        #
        # elif translator == 'Linguee':
        #     supported_languages = LingueeTranslator.supported_languages

        elif translator == 'Robotic Polyglot':
            # res = RoboticPolyglot(source=source, target=target).translate(input=text)
            # http://mt.roboticpolyglot.com/languages?source=all

            if source != 'all':
                #source = source.lower()
                source = LANGUAGE_LANGS_CODES[source.lower()]
                # source = next(key for key, value in LANGUAGE_CODES_LANGS.items() if value.lower() == source)

            url = "http://mt.roboticpolyglot.com/languages"
            params = {}
            params['source'] = source
            # res = requests.get(url=url, params=params).text
            res = requests.get(url=url, params=params).text
            robotic_languages = json.loads(res)

            supported_languages = []
            for dic in robotic_languages:
                name = dic['Name']
                supported_languages.append(name)

            # supported_languages
        else:
            return ""
            # raise Exception("You need to choose a translator")

        return supported_languages

    # @staticmethod
    # def dictate(language, *args):
    #     import speech_recognition as sr
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
    #         # wait for a second to let the recognizer
    #         # adjust the energy threshold based on
    #         # the surrounding noise level
    #         r.adjust_for_ambient_noise(source, duration=0.2)
    #
    #         # listens for the user's input
    #         audio = r.listen(source)
    #
    #         # Using google to recognize audio
    #         text = r.recognize_google(audio)
    #         # text = text.lower()
    #         # print("Did you say " + text)
    #
    #         return text

    # @staticmethod
    # def dictate(language, *args):
    def dictate(self, language, *args):

        self.result_label.text += "Inside dictate\n"

        try:
            if stt.listening:

                self.result_label.text += "Inside try (if listening):\n"

                self.dictate_btn.background_color = [0, 0, 0, 1]
                self.stop_listening()
                stt.stop()
                self.result_label.text += "Stop Listening"
                # start_button = self.dictate_btn
                # start_button.text = 'Speak'
                # self.payload.text = '\n'.join(stt.partial_results)
                self.payload.text = '\n'.join(stt.results[0])
                # self.payload.text = stt.results[0]
                # speech2text = stt.results[0]
                # return speech2text
                # return "shit"
                return

            # start_button = self.ids.dictate_btn
            # start_button.text = 'Stop'

            # self.payload.text
            # self.ids.results.text =
            # self.ids.partial.text = ''

            self.result_label.text += "\n\tBefore start Listening"
            self.dictate_btn.background_color = [255, 0, 0, 1]
            stt.start()
            self.result_label.text += "\n\tAfter Stop Listening"

        except Exception as ex:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            self.result_label.text = str(exc_type) + ", " + str(fname) + ", " + str(exc_tb.tb_lineno)
            # Clock.schedule_interval(self.check_state, 1 / 5)

    def translate(self):
        source = self.from_spinner.text.lower()
        target = self.to_spinner.text.lower()
        text = self.payload.text

        if text.strip() == '':
            self.result_label.text = 'provide a text to translate'
        else:
            try:
                if self.head_spinner.text == 'Google Translate':
                    res = GoogleTranslator(source=source, target=target).translate(text=text)
                    # if target == 'arabic':
                    #     res = get_display(arabic_reshaper.reshape(res))

                elif self.head_spinner.text == 'My Memory':
                    res = MyMemoryTranslator(source=source, target=target).translate(text=text)
                    # if target == 'arabic':
                    #     res = get_display(arabic_reshaper.reshape(res))

                elif self.head_spinner.text == 'Pons':
                    res = PonsTranslator(source=source, target=target).translate(word=text)
                    # if target == 'arabic':
                    #     res = get_display(arabic_reshaper.reshape(res))

                elif self.head_spinner.text == 'Linguee':
                    res = LingueeTranslator(source=source, target=target).translate(word=text)

                elif self.head_spinner.text == 'Robotic Polyglot':
                    # res = RoboticPolyglot(source=source, target=target).translate(input=text)
                    # http://mt.roboticpolyglot.com/translate?source=en&target=fr&input='I am a robot that speaks many languages'

                    src_lang = LANGUAGE_LANGS_CODES[source]
                    if target == 'chinese':
                        tgt_lang = 'zh'
                    else:
                        tgt_lang = LANGUAGE_LANGS_CODES[target]
                    url = "http://mt.roboticpolyglot.com/translate"
                    params = {}
                    params['source'] = src_lang
                    params['target'] = tgt_lang
                    params['input'] = text
                    res = requests.get(url=url, params=params).text

                else:
                    self.result_label.text = "you need to choose a translator"
                    return

                # return "No translation is provided" if not res else res
                if not res:
                    res = "No translation is provided"

                self.result_label.text = res
            except Exception as e:
                print(e.args)
                self.result_label.text = e.args


    def _on_key_down(self, window, keycode, text, modifiers):
        self.result_label.text += f"{keycode}"


class WrappedTextInput(TextInput):

    rootpar = ObjectProperty(None)

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        if keycode[1] == 'enter':
            self.rootpar.translate()
        else:
            super().keyboard_on_key_down(window, keycode, text, modifiers)


class TranslatorApp(App):

    # request_permissions([Permission.RECORD_AUDIO])

    def build(self):
        # Window.bind(on_keyboard=self.validate_input)
        return MainLayout()


if __name__ == '__main__':
    TranslatorApp().run()