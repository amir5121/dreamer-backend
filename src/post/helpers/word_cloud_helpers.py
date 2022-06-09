import itertools
import os
import re
from datetime import timedelta

from django.db.models import TextField
from django.db.models.functions import Concat, Coalesce
from django.utils import timezone
from wordcloud import WordCloud, STOPWORDS
import arabic_reshaper
from bidi.algorithm import get_display

from post.models import Dream


def _get_frequency_dict_for_text(sentence):
    tmp_dict = dict()
    for text in sentence.split(" "):
        tmp_dict[text] = tmp_dict.get(text, 0) + 1
    full_terms_dict = dict()
    for key in tmp_dict:
        full_terms_dict.update({key: tmp_dict[key]})
    return full_terms_dict


def clean_text(sentence):
    sentence = sentence.upper().replace("\n", "").replace(".", "")
    for i in [
        "der",
        "die",
        "das",
        "ich",
        "the",
        "of",
        "and",
        "to",
        "a",
        "in",
        "is",
        "that",
        "was",
        "it",
        "for",
        "on",
        "with",
        "be",
        "by",
        "as",
        "at",
        "are",
        "had",
        "not",
        "this",
        "have",
        "from",
        "but",
        "or",
        "an",
        "were",
        "there",
        "been",
        "has",
        "all",
        "would",
        "can",
        "if",
        "its",
    ]:
        sentence = sentence.replace(f" {i.upper()} ", "")
    return sentence


def get_word_cloud_image(dreams, duration, user_id) -> str:
    text = ""
    for dream in dreams:
        elements = dream.elements.values_list("elements", flat=True)
        elements = " ".join(list(itertools.chain.from_iterable(elements)))
        text += " ".join([dream.title, dream.text, elements, elements])
    text = arabic_reshaper.reshape(clean_text(text))
    text = get_display(text)
    word_cloud = WordCloud(
        width=600,
        height=350,
        max_words=144,
        background_color="rgb(33,33,33)",
        margin=16,
        font_path="media/assets/Cairo/Cairo-SemiBold.ttf",
    ).generate_from_frequencies(_get_frequency_dict_for_text(text))
    file_location = f"media/word-clouds/{user_id}/"
    os.makedirs(file_location, exist_ok=True)
    file_location += f"{duration}.jpg"
    word_cloud.to_file(file_location)
    return file_location
