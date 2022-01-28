from lsa_summarizer import LsaSummarizer
import nltk
from nltk.tokenize import sent_tokenize




def result(source_file):
        from nltk.corpus import stopwords
        source_file = "original_text.txt"

        with open(source_file, "r", encoding='utf-8') as file:
            text = file.readlines()
            
        text = ' '.join(text)
        number_of_sentences = len(sent_tokenize(text))



        summarizer = LsaSummarizer()
        print("length is ", len(text))
        stopwords = stopwords.words('english')
        summarizer.stop_words = stopwords
        summary =summarizer(text, number_of_sentences*0.3+1)
        number_of_summary = len(sent_tokenize(text))
        print("length of the summary", number_of_summary)
        print("====== Original text =====")
        print(text)
        print("====== End of original text =====")



        print("\n========= Summary =========")
        summary = " ".join(summary)
        return text, summary
        print(" ".join(summary))
        print("========= End of summary =========")


