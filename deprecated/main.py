import spacy
from allennlp.predictors.predictor import Predictor
import utils
import re

SRL_MODEL_PATH = "srl.tar.gz"
COREF_MODEL_PATH = "coref.tar.gz"

nlp = spacy.load("en_core_web_sm")

#DOCUMENT = "Chris Mitchell left the house and went to the garden. He met Melissa Smith and proceeded to climb the wall. Next the man jumped into the rose bush and she watched him."
with open('a_little_princess.txt', 'r') as file:
    content = file.read()
print("file read")

doc1 = nlp(content)
sentences = [sent.text for sent in doc1.sents]
print(len(sentences))

# Process every 3 sentences as a batch
batches = []
batch_size = 3
for i in range(0, len(sentences), batch_size):
    # Combine the current batch of sentences into a single string
    batch = ' '.join(sentences[i:i + batch_size])
    batches.append(batch)

predictor_srl = Predictor.from_path(SRL_MODEL_PATH)
predictor_coref = Predictor.from_path(COREF_MODEL_PATH)

print("models loaded")

for index, DOCUMENT in enumerate(batches, start=1):
    #print(DOCUMENT)
    predictions_srl = predictor_srl.predict(sentence=DOCUMENT)
    predictions_coref = predictor_coref.predict(document=DOCUMENT)
    doc = nlp(DOCUMENT)
    #print("predictors done")

    protagonist_dict = utils.make_protagonist_dict(predictions_coref, doc)


    for idx, i in enumerate(predictions_coref["clusters"]):
        protagonist = 0
        for ent in doc.ents:
            if utils.contains_number(ent.start,i):
                protagonist = ent.text
                print("........")
                print(ent.text, ent.label_)
                print("........")
        
        if protagonist != 0:
            for j in i:
                for n in predictions_srl['verbs']:
                    try:
                        if 'ARG' in n['tags'][j[0]]:
                            if 'ARG0' in n['tags'][j[0]]:
                                print(protagonist, utils.lemmatize(n['verb'], nlp), utils.check_for_matches(protagonist_dict, n, "B-ARG1"))
                            elif 'ARG1' in n['tags'][j[0]]:
                                print(utils.check_for_matches(protagonist_dict, n, "B-ARG0"), utils.lemmatize(n['verb'],nlp), protagonist)
                    except IndexError:
                        #print("oopsiest")
                        continue
            #print("--------------------------------")