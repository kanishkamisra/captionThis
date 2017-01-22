import requests
import pandas as pd
from clarifai import rest
from clarifai.rest import ClarifaiApp, Image as ClImage
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import time

def clarifaize(img):
    app = ClarifaiApp("mrKZLVJBD6mWwmzTg_84YsbDlZRj1yQPIlBlfQZd", "vuuKXEtODxS8RHNo-a0wfF4vMJr4pVojR-mEScL3")
    # get the general model
    model = app.models.get("general-v1.3")
    # predict with the model
#     prediction = model.predict_by_url(url=img)['outputs'][0]['data']['concepts']
#     prediction = model.predict_by_filename(img)['outputs'][0]['data']['concepts']
    test_image = ClImage(file_obj=open(img, 'rb'))
    prediction = model.predict([test_image])['outputs'][0]['data']['concepts']
    tags = pd.DataFrame({'Tag': [], 'Probability': []})
    for item in prediction:
        tags = tags.append(pd.DataFrame({'Tag': [item['name']], 'Probability': [item['value']]}))
#     return tags.reset_index(drop=True)
    tags = list(tags['Tag'])
    if('no person' in tags):
        tags.remove('no person')
    
    return tags

def tagPhrase(tags):
	# Returns the phrase with all the tags

	return " ".join(tags)

def urlize(tags):
	# Returns urls as list

	urls = []
	for tag in tags:
		urls.append("https://favqs.com/api/quotes/?filter=" + tag)

	return urls

headers = {'Authorization' : 'Token token="b09904a4d885299ee386f5cbbf795c56"'}

def get_quotes(urls):
    quotes = pd.DataFrame({'Quote': [], 'Author': []})
    for url in urls:
        req = requests.get(url, headers = headers).json()
        time.sleep(0.2)
        print "Processing: " + url
        for item in req['quotes']:
            if item['body'] != 'No quotes found':
                # quotes = quotes.append(pd.DataFrame({'Quote': [item['body']], 'Author': [item['author']]}))
                quotes = quotes.append(pd.DataFrame({'Quote': [item['body']]}))
    return quotes.reset_index(drop=True)

def similarity_matrix(dataframe):
    tfidf = TfidfVectorizer(analyzer = 'word', ngram_range = (1,3), min_df = 0, stop_words = 'english')
    tfidf_matrix = tfidf.fit_transform(dataframe)
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)
    return pd.DataFrame(cosine_similarities)

def best_similarities(dataframe):
    return dataframe[len(dataframe)-1].sort_values(ascending=False)[1:2].reset_index()

def candidate_indexes(dataframe):
	return dataframe['index']

def candidate_captions(dataframe, indexes):
	captions = []
	for index in indexes:
		captions.append(dataframe[index])
	return captions


def captionize(img):
    tags = clarifaize(img)
    # print "clarifized"
    tag_phrase = tagPhrase(tags)
    # print "phrased"
    urls = urlize(tags)
    # print "urllized"
    # quotes = pd.DataFrame({'Quote': get_quotes(urls)['Quote'], 'Author': get_quotes(urls)['Author']})
    quotes = pd.DataFrame({'Quote': get_quotes(urls)['Quote']})
    # phrases = quotes.append(pd.DataFrame({'Quote' : [tag_phrase], 'Author': ['No One']})).reset_index(drop=True)
    phrases = quotes.append(pd.DataFrame({'Quote' : [tag_phrase]})).reset_index(drop=True)
    matrix = similarity_matrix(phrases['Quote'])
    best = best_similarities(matrix)
    captions =candidate_captions(phrases['Quote'], candidate_indexes(best_similarities(matrix)))
    # print "Get ready...\n"
    return captions

	# return captions

def hashtagger(img):
	tags = clarifaize(img)
	alltags = []
	for tag in tags[:6]:
		alltags.append("#"+tag)
	return alltags

# print(captionize('lake2.jpg'))
