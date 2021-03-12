# Necesarry imports
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.stem.porter import *
import os
import string
import email
import nltk
nltk.download('stopwords', quiet=True)
nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)

# Data Processing 

#PATH = r"C:\\Users\\tedma\\Desktop\\cp465_project\\data"
PATH = r"static\\data"
lemmatizer = WordNetLemmatizer()
porter = PorterStemmer()
stop_words = set(stopwords.words('english'))
files =  [f for f in os.listdir(PATH) if os.path.isfile(os.path.join(PATH, f))]
tokens = [] #should be our final tokens list
word_dict = {}
# Tokenization
# Lower casing
# Stop words removal
# Stemming
# Lemmatization
for file in files:
    
    #get file contents
    file_content = open(PATH+"\\"+file, 'r',encoding="utf8").read()


    #get the contents of email
    email_content = str(email.message_from_string(file_content))
    #lower case content
    email_content = email_content.lower()
    #remove punctuation  
    email_content = email_content.translate(str.maketrans('', '', string.punctuation))
    #porter stemming
    email_content = porter.stem(email_content)
    
    
    #tokenize content
    word_tokens = word_tokenize(email_content)
    #lemmatize
    word_tokens = [lemmatizer.lemmatize(token) for token in word_tokens]
    #print(word_tokens)
    #remove stop words from our word_tokens list
    cleaned_tokens = [token for token in word_tokens if not token in stop_words]  
    
    for clean_token in cleaned_tokens:
        #append that set into tokens if not already in it
        if clean_token not in tokens:
            tokens.append(clean_token)
            
            
    cleaned_tokens = list(dict.fromkeys(cleaned_tokens))
    
    
    #building our inverted index
    for word in cleaned_tokens:
        if word in word_dict:
            temp = word_dict[word]
            temp = temp + ', ' + str(file)
            word_dict[word] =  temp
            
        else:
            word_dict[word] = str(file)


for word, index in word_dict.items():
    word_dict[word] = word_dict[word].split(", ") #before my inverted index didn't have linked list, it was a string
    #so we're now changing the string into the linked list

#we want our inverted index to be in alphabetical order
sorted_dict = sorted(word_dict.items())
inverted_index = {} 

for i in sorted_dict:
    inverted_index[i[0]] = i[1]

def search_and(inverted_index: dict, term1:str, term2:str) -> list:
    """Intersect"""
    results = []
    try:
        t1_postings = inverted_index[term1]
    except:
        t1_postings = []
    try:
        t2_postings = inverted_index[term2]
    except:
        t2_postings = []
    #just getting the intersecting postings for AND
    for docID in t1_postings:
        if docID in t2_postings:
            results.append(docID)    
    return results

def search_or(inverted_index: dict, term1:str, term2:str) -> list:
    """Union"""
    results = []
    try:
        t1_postings = inverted_index[term1]
    except:
        t1_postings = []
    try:
        t2_postings = inverted_index[term2]
    except:
        t2_postings = []

    #get everything if not already in results
    for docID in t1_postings:
        if docID not in results:
            results.append(docID)
    for docID in t2_postings:
        if docID not in results:
            results.append(docID)

    return results

def search_not(inverted_index: dict, term1:str, term2:str) -> list:
    results = []
    try:
        t1_postings = inverted_index[term1]
    except:
        t1_postings = []
    try:
        t2_postings = inverted_index[term2]
    except:
        t2_postings = []

    for docID in t1_postings:
        if docID not in t2_postings:
            results.append(docID)

    
    return results
    
def print_lines(results:list) -> None:
    if len(results) == 0:
        print("Search returned no results")
        final_text = {}
        final_text[0] = 'No resukts for this search'
        total = 0
        return {'No records found':'Sorry, we could not find any data in our records that match your search'}, total
    else:
        final_text = {}
        total = 0
        #base case empty 
        for i in results:#go through every document
            total+=1
            print()
            set_i = i.replace(".txt","")
         #print(f"**************Document: {set_i}*********************")
            line_count = 0
        
            #get the contents of document
            file_content =  open(PATH+"\\"+i, 'r',encoding="utf8").read()      
            msg = email.message_from_string(file_content)
            fin = ""
            for part in msg.walk():
                set_ = ""
                if line_count == 3:
                    break
                    
                if part.get_content_type() == 'text/plain':
                    for text in part.get_payload().splitlines():
                        text = text.replace("\n", "")
                    
                        if text == "":
                            set_ = " "
                        else:
                            set_ = set_ + text
                            line_count +=1
                            if line_count == 3:
                                break
                fin = set_
            final_text[set_i] = fin
        
        #print("----------------------------------------")
        #print(f"Number of results: {len(results)}")
        #print()  
        records = total
        return final_text, records
        

def process_query(query:list, inverted_index) -> None:
    res_and = {}
    res_or = {}
    res_not = {}
    res_no_op = {}
    num_records = 0
    if "and" in query_array:
        #print(f"Query is {query}: ")
        #print(search_and(inverted_index,query[0], query[2]))
        res_and,num_records = print_lines(search_and(inverted_index,query[0], query[2]))

    elif "or" in query_array:
        #print(f"Query is {query_array}: ")
        #print(search_or(inverted_index,query[0], query[2]))
        res_or,num_records = print_lines(search_or(inverted_index,query[0], query[2]))

    elif "not" in query_array:
        #print(f"Query is {query_array}: ")
        #print(search_not(inverted_index,query[0], query[2]))
        res_not,num_records = print_lines(search_not(inverted_index,query[0], query[2]))
    
    else: #no operators
        #print(f"Query is {query_array}: ")
        #print(search_and(inverted_index,query[0], query[1]))
        
        res_no_op,num_records = print_lines(search_and(inverted_index,query[0], query[1]))
    return res_and, res_or, res_not, res_no_op,num_records
#For testing
#query_array = input("Enter query: ").strip().split(" ")

query_array = ""
def runner(set_value):
    query_array = set_value.strip().split(" ")  
    res_and, res_or, res_not, res_no_op,num_records= process_query(query_array,inverted_index)

    return res_and, res_or, res_not, res_no_op,num_records
"""
for i in res_and:
    print("*********************************"+i+"*********************************")
    print(res_and.get(i))
    print()

for i in res_or:
    print("*********************************"+i+"*********************************")
    print(res_or.get(i))
    print()


for i in res_not:
    print("*********************************"+i+"*********************************")
    print(res_not.get(i))
    print()


print("******************************************************************")
print("Number of Search Results : {}".format(num_records))
print("******************************************************************")
print()

for i in res_no_op:
    print("*********************************"+i+"*********************************")
    print(res_no_op.get(i))
    print()


#print(res_no_op.keys())
#print(res_and.keys())
#print(res_or.keys())

"""