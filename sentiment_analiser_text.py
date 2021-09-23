from nltk.sentiment.vader import SentimentIntensityAnalyzer

def analyse_text():
	sentence="i a am a bad bad bad boy"
	analyser=SentimentIntensityAnalyzer()
	
	ss=analyser.polarity_scores(sentence)
	result=ss["compound"]

	if result>=0.05:
		print('positive statement')
	elif result<=-.05:
		print('negative statement')
	else:
		print('neutral statement')

	print(ss)

analyse_text()