import sys
import csv
import nltk
from nltk.corpus import wordnet
import re
import codecs
import os
import copy

player_dict = {}
player_pos_neg = {}
# Empty list with counters for the 12 categories of Bales, a word and sentence counter and a positive and negative score
empty_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


def import_files(text_file_path):
    # Import CSV File if available
    if os.path.isfile(text_file_path):
        SpeechDataCSVFile = open(text_file_path)
        SpeechDataFile = csv.reader(SpeechDataCSVFile, delimiter=",")
        return SpeechDataFile
    else:
        print("No file available at the selected location...")
        exit()


# Import Bales CSV Files
bales_file_path = "bales-categories"
bales_dict_raw = {}
bales_dict = {}
files = os.listdir(bales_file_path)
for f in files:
    if os.path.isfile(bales_file_path + "/" + f):
        bales_dict_raw[f] = open(bales_file_path + "/" + f)
        bales_dict[f] = csv.reader(bales_dict_raw[f], delimiter=",")
    else:
        print("No file available at the selected location...")
        exit()


class SentiWordNetCorpusReader:
    def __init__(self, filename):
        """
        Argument:
        filename -- the name of the text file containing the
                    SentiWordNet database
        """
        self.filename = filename
        self.SentiWordDict = {}
        self.parse_src_file()

    # Parse the SentiWordNet file into usable format
    def parse_src_file(self):
        lines = codecs.open(self.filename, "r", "utf8").read().splitlines()
        lines = filter((lambda x: not re.search(r"^\s*#", x)), lines)
        # Split the lines into the different fields.
        for i, line in enumerate(lines):
            fields = re.split(r"\t+", line)
            fields = map(str.strip, fields)
            try:
                pos, id_number, pos_score, neg_score, synset_terms, gloss = fields
            except:
                sys.stderr.write("Line %s formatted incorrectly: %s\n" % (i, line))
            # Match the first letter and word id to a positive and negative score and put into dictionary
            if pos and id_number:
                id_number = int(id_number)
                self.SentiWordDict[(pos, id_number)] = (float(pos_score), float(neg_score))

    def senti_synset(self, vals):
        if tuple(vals) in self.SentiWordDict:
            pos_score, neg_score = self.SentiWordDict[tuple(vals)]
            pos, offset = vals
            synset = wordnet.synset_from_pos_and_offset(pos, int(offset))
            return SentiSynset(pos_score, neg_score, synset)
        else:
            pos, offset = vals
            synset = wordnet.synset_from_pos_and_offset(pos, int(offset))
            if (pos, offset) in self.SentiWordDict:
                pos_score, neg_score = self.SentiWordDict[(pos, offset)]
                return SentiSynset(pos_score, neg_score, synset)
            else:
                return None

    def senti_synsets(self, string, pos=None):
        sentis = []
        synset_list = wordnet.synsets(string, pos)
        for synset in synset_list:
            sentis.append(self.senti_synset(synset.name))
        sentis = filter(lambda x: x, sentis)
        return sentis

    # def all_senti_synsets(self):
    #     for key, fields in self.SentiWordDict.iteritems():
    #         pos, id_number = key
    #         pos_score, neg_score = fields
    #         synset = wordnet.synset_from_pos_and_id_number(pos, id_number)
    #         yield SentiSynset(pos_score, neg_score, synset)


class SentiSynset:
    def __init__(self, pos_score, neg_score, synset):
        self.pos_score = pos_score
        self.neg_score = neg_score
        self.obj_score = 1.0 - (self.pos_score + self.neg_score)
        self.synset = synset

    def __str__(self):
        """Prints just the Pos/Neg scores for now."""
        s = ""
        s += self.synset.name() + "\t"
        s += "PosScore: %s\t" % self.pos_score
        s += "NegScore: %s" % self.neg_score
        return s

    def __repr__(self):
        return "Senti" + repr(self.synset)


# Creates a list of all sentences and a list of all names
def speech_dict(speech_data):
    speech_list_dict = []
    speech_name_list = []
    for line in speech_data:
        speech_list_dict.append(line[0])
        speech_name_list.append(line[1])
    return speech_list_dict, speech_name_list


def bales_csv_reader(csv_dict):
    bales_words_dict = {}
    for key in csv_dict:
        temp_list = []
        for value in csv_dict[key]:
            for word in value:
                temp_list.append(word)
            bales_words_dict[key] = temp_list
    return bales_words_dict


# return true if a string ia a stopword (the, a , an, in, etc.)
def is_stopword(string):
    if string.lower() in nltk.corpus.stopwords.words('english'):
        return True
    else:
        return False


# return true if a string is punctuation
def is_punctuation(string):
    for char in string:
        # isAlpha checks whether alphabet letter, isdigit checks if number
        if char.isalpha() or char.isdigit():
            return False
    return True


# Translation from nltk to Wordnet (words tag) (code)
def wordnet_pos_code(tag):
    if tag.startswith('NN'):
        return wordnet.NOUN
    elif tag.startswith('VB'):
        return wordnet.VERB
    elif tag.startswith('JJ'):
        return wordnet.ADJ
    elif tag.startswith('RB'):
        return wordnet.ADV
    else:
        return ''


# Translation from nltk to Wordnet (words tag) (label)
def wordnet_pos_label(tag):
    if tag.startswith('NN'):
        return "Noun"
    elif tag.startswith('VB'):
        return "Verb"
    elif tag.startswith('JJ'):
        return "Adjective"
    elif tag.startswith('RB'):
        return "Adverb"
    else:
        return tag


# Input a sentence
# Output a sentence in which each words is enriched of -> lemma, wordnet_pos, wordnet_definitions
def wordnet_definitions(sentence):
    wnl = nltk.WordNetLemmatizer()
    for token in sentence:
        word = token['word']
        # Transform NLTK code to Wordnet (NN = Noun, etc)
        wn_pos = wordnet_pos_code(token['pos'])
        if is_punctuation(word):
            token['punct'] = True
        # Pass if it is a word as the, a , an, in, etc.
        elif is_stopword(word):
            pass
        # If there is a synset
        elif len(wordnet.synsets(word, wn_pos)) > 0:
            token['wn_lemma'] = wnl.lemmatize(word.lower())
            token['wn_pos'] = wordnet_pos_label(token['pos'])
            defs = [sense.definition() for sense in wordnet.synsets(word, wn_pos)]
            token['wn_def'] = "; \n".join(defs)
        else:
            pass
    return sentence


# Tokenization of the words in a sentence
def tag_sentence(sentence):
    words = nltk.word_tokenize(sentence)
    sentence = []
    tag_tuples = nltk.pos_tag(words)
    for (string, tag) in tag_tuples:
        token = {'word': string, 'pos': tag}
        sentence.append(token)
    return sentence


# Return the best definition (make a word clear, what does the word mean?)
def word_sense_disambiguate(word, wn_pos, sentence):
    senses = wordnet.synsets(word, wn_pos)
    if len(senses) > 0:
        cfd = nltk.ConditionalFreqDist(
            (sense, def_word) for sense in senses for def_word in sense.definition().split() if def_word in sentence)
        best_sense = senses[0]  # start with first sense
        for sense in senses:
            try:
                if cfd[sense].max() > cfd[best_sense].max():
                    best_sense = sense
            except:
                pass
        return best_sense
    else:
        return None


def positive_sentence(sentence, bales_word_dict):
    sentence_words = re.findall(r"[\w']+|[.,!?;]", sentence)
    for i in sentence_words:
        if i == "?":
            category = neutral_question(sentence_words, bales_word_dict)
            return category
    solidarity = bales_word_dict["bales_01.csv"]
    tension_release = bales_word_dict["bales_02.csv"]
    agreement = bales_word_dict["bales_03.csv"]
    solidarity_score = tension_release_score = agreement_score = 0
    for i in sentence_words:
        if i in solidarity or i.capitalize() in solidarity:
            solidarity_score += 1
        if i in tension_release or i.capitalize() in tension_release:
            tension_release_score += 1
        if i in agreement or i.capitalize() in agreement:
            agreement_score += 1
    if tension_release_score > solidarity_score and tension_release_score > agreement_score:
        category = 2
    elif agreement_score > solidarity_score and agreement_score > tension_release_score:
        category = 3
    else:
        category = 1
    return category


def negative_sentence(sentence, bales_word_dict):
    sentence_words = re.findall(r"[\w']+|[.,!?;]", sentence)
    for i in sentence_words:
        if i == "?":
            category = neutral_question(sentence_words, bales_word_dict)
            return category
    disagreement = bales_word_dict["bales_10.csv"]
    tension = bales_word_dict["bales_11.csv"]
    antagonism = bales_word_dict["bales_12.csv"]
    disagreement_score = tension_score = antagonism_score = 0
    for i in sentence_words:
        if i.lower() in disagreement or i.capitalize() in disagreement:
            disagreement_score += 1
        if i in tension or i.capitalize() in tension:
            tension_score += 1
        if i in antagonism or i.capitalize() in antagonism:
            antagonism_score += 1
    if tension_score > antagonism_score and tension_score > disagreement_score:
        category = 11
    elif disagreement_score > tension_score and disagreement_score > antagonism_score:
        category = 10
    else:
        category = 12
    return category


def neutral_sentence(sentence, bales_word_dict):
    sentence_words = re.findall(r"[\w']+|[.,!?;]", sentence)
    question_bool = True
    for i in sentence_words:
        if i == "?":
            category = neutral_question(sentence_words, bales_word_dict)
            question_bool = False
    if question_bool:
        category = neutral_answer(sentence_words, bales_word_dict)
    return category


def neutral_question(sentence_words, bales_word_dict):
    orientation = bales_word_dict["bales_07.csv"]
    opinion = bales_word_dict["bales_08.csv"]
    suggestion = bales_word_dict["bales_09.csv"]
    orientation_score = opinion_score = suggestion_score = 0
    for i in sentence_words:
        if i in orientation or i.capitalize() in orientation:
            orientation_score += 1
        if i in opinion or i.capitalize() in opinion:
            opinion_score += 1
        if i in suggestion or i.capitalize() in suggestion:
            suggestion_score += 1
    if orientation_score > opinion_score and orientation_score > suggestion_score:
        category = 7
    elif opinion_score > orientation_score and opinion_score > suggestion_score:
        category = 8
    else:
        category = 9
    return category


def neutral_answer(sentence_words, bales_word_dict):
    orientation = bales_word_dict["bales_06.csv"]
    opinion = bales_word_dict["bales_05.csv"]
    suggestion = bales_word_dict["bales_04.csv"]
    orientation_score = opinion_score = suggestion_score = 0
    for i in sentence_words:
        if i in orientation or i.capitalize() in orientation:
            orientation_score += 1
        if i in opinion or i.capitalize() in opinion:
            opinion_score += 1
        if i in suggestion or i.capitalize() in suggestion:
            suggestion_score += 1
    if orientation_score > opinion_score and orientation_score > suggestion_score:
        category = 6
    elif opinion_score > orientation_score and opinion_score > suggestion_score:
        category = 5
    else:
        category = 4
    return category


def bales_ipa(text_file_path):
    speech_data_file = import_files(text_file_path)
    bales_word_dict = bales_csv_reader(bales_dict)
    # Convert CSV File to Dictionary of sentences
    sentences, speech_names = speech_dict(speech_data_file)
    for i in speech_names:
        if i not in player_dict:
            player_dict[i] = empty_list
    sentiment = SentiWordNetCorpusReader("SentiWordNetList.txt")
    for index in range(len(sentences)):
        # If the sentence is an Error, don't use it
        if sentences[index] == "Error" or sentences[index] == "Error.":
            continue
        # Count the words and add to player total
        split_sentence = sentences[index].split(' ')
        player_list_value = copy.deepcopy(player_dict.get(speech_names[index]))
        player_list_value[12] = player_list_value[12] + len(split_sentence)
        player_list_value[13] = player_list_value[13] + 1
        player_dict[speech_names[index]] = player_list_value
        # Tokenize the words in the sentence
        a = wordnet_definitions(tag_sentence(sentences[index]))
        obj_score = 0  # objective score
        pos_score = 0  # positive score
        neg_score = 0  # negative score
        pos_score_tre = 0
        neg_score_tre = 0
        threshold = 0.75
        count = 0
        count_tre = 0

        # Convert the sentences to SentiWord scores
        for word in a:
            if 'punct' not in word:
                sense = word_sense_disambiguate(word['word'], wordnet_pos_code(word['pos']), sentences[index])
                sense_pos_offset = None
                if sense is not None:
                    sense_pos_offset = (sense.pos(), sense.offset())
                if sense_pos_offset is not None:
                    sent = sentiment.senti_synset(sense_pos_offset)  # LINE 50 REFERENCE
                    # Extraction of the scores
                    if sent is not None and sent.obj_score != 1:
                        obj_score = obj_score + float(sent.obj_score)  # ???????????????????????????????? NOT IN FILE
                        pos_score = pos_score + float(sent.pos_score)
                        neg_score = neg_score + float(sent.neg_score)
                        count = count + 1
                        if sent.obj_score < threshold:
                            pos_score_tre = pos_score_tre + float(sent.pos_score)
                            neg_score_tre = neg_score_tre + float(sent.neg_score)
                            count_tre = count_tre + 1

        # Evaluation by different methods

        avg_pos_score = 0
        avg_neg_score = 0
        avg_pos_score_tre = 0
        avg_neg_score_tre = 0

        # 2

        if count != 0:
            avg_pos_score = pos_score / count
            avg_neg_score = neg_score / count

        # 3

        if count_tre != 0:
            avg_pos_score_tre = pos_score_tre / count_tre
            avg_neg_score_tre = neg_score_tre / count_tre

        # If positive
        if pos_score > neg_score:
            category = positive_sentence(sentences[index], bales_word_dict)
            player_list_value_x = copy.deepcopy(player_dict.get(speech_names[index]))
            player_list_value_x[14] = player_list_value_x[14] + 1
            player_dict[speech_names[index]] = player_list_value_x
        # If negative
        elif neg_score > pos_score:
            category = negative_sentence(sentences[index], bales_word_dict)
            player_list_value_xx = copy.deepcopy(player_dict.get(speech_names[index]))
            player_list_value_xx[15] = player_list_value_xx[15] + 1
            player_dict[speech_names[index]] = player_list_value_xx
        else:
            category = neutral_sentence(sentences[index], bales_word_dict)

        player_list_value_bales = copy.deepcopy(player_dict.get(speech_names[index]))
        player_list_value_bales[category-1] = player_list_value[category-1] + 1
        player_dict[speech_names[index]] = player_list_value_bales

    print("PLAYER SCORES: ", player_dict)
    return player_dict
