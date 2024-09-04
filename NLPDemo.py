from datetime import datetime
import spacy

class NLPDemo():

    def __init__(self):
        print(f"Please Wait...loading model...")
        begin_load = datetime.now()
        self.__nlp = spacy.load("en_core_web_sm")
        time_taken = datetime.now() - begin_load
        print(f"...Finished loading.<{time_taken}>")

    def getNamesByPartsOfSpeech(self, speech):
        names = []
        doc = self.__nlp(speech)
        for token in doc:
            print(f"{token.text:10s}, {token.lemma_:10s}, {token.pos_:10s}, {token.tag_:5s}, {token.dep_:10s}, {token.shape_:10s}, {token.is_alpha}, {token.is_stop}")
            if token.pos_ in ["PROPN"]:
                names.append(token.text)
        name = " ".join(names)
        return name
    
    def getNameByEntityType(self, speech):
        names = []
        doc = self.__nlp(speech)
        print("Entities found: ")
        for ent in doc.ents:
            print(ent.text, ent.start_char, ent.end_char, ent.label_)
            if ent.label_ == "PERSON":
                names.append(ent.text)
        name = " ".join(names)
        return name
    
    def getNounsByPartsOfSpeech(self, speech):
        '''Returns the nouns detected in speech. '''
        nouns = []
        doc = self.__nlp(speech)
        for token in doc:
            #print(f"{token.text:10s}, {token.lemma_:10s}, {token.pos_:10s}, {token.tag_:5s}, {token.dep_:10s}, {token.shape_:10s}, {token.is_alpha}, {token.is_stop}")
            if token.pos_ in ["NOUN", "PROPN"]:
                nouns.append(token.text)
        item = " ".join(nouns)
        return item
    
    def getNumbersByPartsOfSpeech(self, speech):
        '''Returns the numerical part of speech. '''
        nums = []
        doc = self.__nlp(speech)
        for token in doc:
            #print(f"{token.text:10s}, {token.lemma_:10s}, {token.pos_:10s}, {token.tag_:5s}, {token.dep_:10s}, {token.shape_:10s}, {token.is_alpha}, {token.is_stop}")
            if token.pos_ in ["NUM"]:
                nums.append(token.text)
        return nums


def main():
    nlpDemo = NLPDemo()

    sentence = 'Hello! Introducing the infamous John Michael Anthony Elias Smith-Jones. How are you today?'
    print(f">>> Process: {sentence}")
    name = nlpDemo.getNamesByPartsOfSpeech(sentence)
    print(f">>> Name by Speech found: {name}")

    sentence = 'Hello! Introducing the infamous John Michael Anthony Elias Smith-Jones. I love swimming, jumping, running and althletics?'
    print(f">>> Process: {sentence}")
    name = nlpDemo.getNameByEntityType(sentence)
    print(f">>> Name by Speech found: {name}")

    sentence = 'Hello! I would like to order chicken noodle soup once please! Thank you!'
    print(f">>> Process: {sentence}")
    num = nlpDemo.getNumbersByPartsOfSpeech(sentence)
    print(f">>> Item: Quantity: {num}")

if __name__ == "__main__":
    main()