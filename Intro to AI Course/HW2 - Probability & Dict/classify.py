import os
import math

#These first two functions require os operations and so are completed for you
#Completed for you
def load_training_data(vocab, directory):
    """ Create the list of dictionaries """
    top_level = os.listdir(directory)
    dataset = []
    for d in top_level:
        if d[-1] == '/':
            label = d[:-1]
            subdir = d
        else:
            label = d
            subdir = d+"/"
        files = os.listdir(directory+subdir)
        for f in files:
            bow = create_bow(vocab, directory+subdir+f)
            dataset.append({'label': label, 'bow': bow})
    return dataset

#Completed for you
def create_vocabulary(directory, cutoff):
    """ Create a vocabulary from the training directory
        return a sorted vocabulary list
    """

    top_level = os.listdir(directory)
    vocab = {}
    for d in top_level:
        subdir = d if d[-1] == '/' else d+'/'
        files = os.listdir(directory+subdir)
        for f in files:
            with open(directory+subdir+f,'r', encoding='utf-8') as doc:
                for word in doc:
                    word = word.strip()
                    if not word in vocab and len(word) > 0:
                        vocab[word] = 1
                    elif len(word) > 0:
                        vocab[word] += 1
    return sorted([word for word in vocab if vocab[word] >= cutoff])

#The rest of the functions need modifications ------------------------------
#Needs modifications
def create_bow(vocab, filepath):
    """ Create a single dictionary for the data
        Note: label may be None
    """
    bow = {}
    with open(filepath, 'r', encoding='utf-8') as doc:
        for word in doc:    # Goes through the words in the doc
            word = word.strip()
            if word in vocab: #Checks if the word is in the vocab & adds count
                if not word in bow and len(word) > 0:
                       bow[word] = 1
                elif len(word) > 0:
                       bow[word] += 1
            else:   #If not in the vocab, a special "None" is counted instead.
                if not None in bow and len(word) > 0:
                       bow[None] = 1
                elif len(word) > 0:
                       bow[None] += 1
    return bow
        
#Needs modifications
def prior(training_data, label_list):
    """ return the prior probability of the label in the training set
        => frequency of DOCUMENTS
    """

    smooth = 1 # smoothing factor
    freq = []   #list of frequencies
    for label in label_list:    # All lables to check
        label_frequency = 0 # counts number of times label is found
        for data in training_data:  # All lables given
                if data.get("label") == label:
                    label_frequency += 1    # incriment frequency of label
        freq.append(label_frequency)    # add frequency number to frequency list
    logprob = {}
    for i in range(len(label_list)):
        logprob[label_list[i]] = math.log((freq[i]+smooth)/(len(training_data)+2))
        # calculate the log(frequency) using Laplace smoothing

    return logprob

#Needs modifications
def p_word_given_label(vocab, training_data, label):
    """ return the class conditional probability of label over all words, with smoothing """

    smooth = 1 # smoothing factor
    total_vocab = len(vocab)
    n_label = 0
    label_info = {}
    non_label_info = {}
    #print(training_data)
    for data in training_data:
            for word in data.get("bow"):   #goes over all the words used in doc
                if word is not None:
                    word = word.strip()
                num_value = data.get("bow")[word]
               # print(num_value)
                if data.get("label") == label: #If the document contains the label
                   # print("label: ", label, " equals ", data.get("label"))
                    if word in vocab:   #word is in vocab
                        if not word in label_info and len(word) >0:
                            label_info[word] = num_value
                            n_label += num_value
                           # total_vocab += num_value
                        elif len(word) >0:
                            label_info[word] += num_value
                            n_label += num_value
                    else: # word is not in vocab
                        if not None in label_info:
                            label_info[None] = num_value
                            n_label += num_value
                           # total_vocab += num_value
                        else: # word already found
                            label_info[None] += num_value
                            n_label += num_value
                else: # document does not contain the label
                    if word in vocab:   #word is in vocab
                            if not word in non_label_info and len(word) >0:
                                non_label_info[word] = num_value
                               # total_vocab += num_value
                             

                           
                    else: # word is not in vocab
                            if not None in non_label_info:
                                non_label_info[None] = num_value
                               # total_vocab += num_value
                            else: # word already found
                                non_label_info[None] += num_value
                                
    word_prob = {}     

    for word in vocab:
        word = word.strip()
        if word in label_info:  #If word is contained in docs of label
            n_w = label_info[word]
        else:
            n_w = 0
        num = n_w+smooth*1
        denom = n_label + smooth*(total_vocab + 1)
        word_prob[word] = math.log(num/denom)
    word = None #Now checking none
    if word in label_info:
        n_w = label_info[word]
    else:
        n_w = 0
    num = n_w+smooth*1
    denom = n_label + smooth*(total_vocab + 1)
    word_prob[word] = math.log(num/denom)
    
    #print("total label words: ", n_label)
    #print("total words: ", total_vocab)
    #print(word_prob)

    return word_prob


##################################################################################
#Needs modifications
def train(training_directory, cutoff):
    """ return a dictionary formatted as follows:
            {
             'vocabulary': <the training set vocabulary>,
             'log prior': <the output of prior()>,
             'log p(w|y=2016)': <the output of p_word_given_label() for 2016>,
             'log p(w|y=2020)': <the output of p_word_given_label() for 2020>
            }
    """
    retval = {}
    label_list = os.listdir(training_directory)
    vocabulary = create_vocabulary(training_directory, cutoff)
    training_data = load_training_data(vocabulary, training_directory)
    log_prior = prior(training_data, label_list)
    log_p_2016 = p_word_given_label(vocabulary, training_data, "2016")
    log_p_2020 = p_word_given_label(vocabulary, training_data, "2020")
    
    retval['vocabulary'.strip()] = vocabulary
    retval['log prior'.strip()] = log_prior
    retval['log p(w|y=2016)'.strip()] = log_p_2016
    retval['log p(w|y=2020)'.strip()] = log_p_2020
    

    return retval

#Needs modifications
def classify(model, filepath):
    """ return a dictionary formatted as follows:
            {
             'predicted y': <'2016' or '2020'>,
             'log p(y=2016|x)': <log probability of 2016 label for the document>,
             'log p(y=2020|x)': <log probability of 2020 label for the document>
            }
    """
    vocabulary_of_filepath = model['vocabulary']
    bow_of_filepath = create_bow(vocabulary_of_filepath, filepath)
    retval = {}
    prior_2020 = model['log prior']['2020']
    prior_2016 = model['log prior']['2016']
    prior_word_label_2016 = model['log p(w|y=2016)']
    prior_word_label_2020 = model['log p(w|y=2020)']
    total_2016 = 0
    total_2020 = 0
    for word in bow_of_filepath:
        if word is not None:
            word = word.strip()
        total_2016 += prior_word_label_2016[word]*bow_of_filepath[word]
        total_2020 += prior_word_label_2020[word]*bow_of_filepath[word]

    total_2016 += prior_2016
    total_2020 += prior_2020
    
    if total_2020 > total_2016: #Probability 2020 > 2016
        retval['predicted y'] = '2020'
    else: # predict 2016
        retval['predicted y'] = '2016'
    retval['log p(y=2016|x)'] = total_2016
    retval['log p(y=2020|x)'] = total_2020
#   prior_2016 = model['log prior']['2016']
#   print(model['log p(w|y=2020)'.strip()])
    
    return retval


