from string import *
def load_words(file_name):
    print("Loading word list from file...")
    in_file = open(file_name, 'r')
    word_list = []
    for line in in_file:
        word_list.extend([word.lower() for word in line.split(' ')])
    print("  ", len(word_list), "words loaded.")
    return word_list


def is_word(word_list, word):
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list


def get_story_string(file_name):
    f = open(file_name, "r")
    story0 = str(f.read())
    f.close()
    return story0


words_list = load_words('words.txt')



class Message(object):
    def __init__(self, text):
        self.text_message = text
        list1 = []
        for i in text.split():
            if is_word(words_list, i):
                list1.append(i)
        self.valid_words = list1

    def get_message_text(self):
        return self.text_message

    def get_valid_words(self):
        ret_val = self.valid_words[:]
        return ret_val

    def build_shift_dict(self, shift):
        dict1 = {}
        letters = ascii_lowercase
        LETTERS = ascii_uppercase
        for i in range(26):
            dict1[letters[i]] = letters[(i + shift) % 26]
        for j in range(26):
            dict1[LETTERS[j]] = LETTERS[(j + shift) % 26]
        return dict1

    def apply_shift(self, shift):
        cipher_text = ''
        for i in self.text_message:
            dictionary = self.build_shift_dict(shift)
            try:
                cipher_text += dictionary[i]
            except KeyError:
                cipher_text += i
        return cipher_text


class PlaintextMessage(Message):
    def __init__(self, text, shift):
        Message.__init__(self, text)
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        return self.shift

    def get_encryption_dict(self):
        ret_val = self.build_shift_dict(self.shift).copy()
        return ret_val

    def get_message_text_encrypted(self):
        return self.message_text_encrypted

    def change_shift(self, shift):
        self.shift = shift
        self.encryption_dict = self.build_shift_dict(self.shift).copy()
        self.message_text_encrypted = self.apply_shift(shift)


class CipherTextMessage(Message):
    def __init__(self, text):
        Message.__init__(self, text)

    def decrypt_message(self):
        list2 = []
        for i in range(0, 26):
            a = Message(self.apply_shift(26 - i))
            list2.append(len(a.get_valid_words()))
        our_shift = list2.index(max(list2)) 
        return self.apply_shift(26 - our_shift)
message = get_story_string('story.txt')
massage = CipherTextMessage(message)
dec = massage.decrypt_message()
f = open('RESULTS.txt', 'w')
f.write(dec)
f.close()
