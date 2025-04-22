import re

def find_arguments(input_string):
    # Define the regex pattern for ARG1, ARG2, ARG3, and ARG4
    pattern = r'\[ARG[1-4]: (.*?)\]'
    
    # Find all matches in the input string
    matches = re.findall(pattern, input_string)
    
    return matches

def extract_between_brackets(input_string):
    # Define the regex pattern for text between brackets
    pattern = r'\[(.*?)\]'
    
    # Use re.findall to find all occurrences of the pattern
    results = re.findall(pattern, input_string)
    
    return results

def lemmatize(word, nlp):
    doc = nlp(word)
    return doc[0].lemma_

def contains_number(num, list_of_lists):
    return any(num in sublist for sublist in list_of_lists)

def make_protagonist_dict(predictions_coref, doc):
    protagonist_dict = {}

    for idx, i in enumerate(predictions_coref["clusters"]):
        for ent in doc.ents:
            if contains_number(ent.start,i):
                for sublist in i:
                    for number in sublist:
                    # Assign the specific string to the number in the dictionary
                        protagonist_dict[number] = ent.text
    return protagonist_dict

def get_arg1_value(string_list):
    for string in string_list:
        # Check if the string contains 'ARG1:'
        if "ARG1:" in string:
            # Split the string on 'ARG1:' and return the part after it
            return string.split("ARG1:", 1)[1].strip()  # Strip to remove leading/trailing whitespace
    return None  # Return None if no such string is found

def find_string_position(string_list, target_string):
    try:
        # Find the index of the target string in the list
        position = string_list.index(target_string)
        return position
    except ValueError:
        # Return -1 if the string is not found
        return -1

def check_for_matches(protagonist_dict, n, tag):
    position = find_string_position(n['tags'], tag)
    if position==-1:
        return '0'
    else:
        if position in protagonist_dict.keys():
            return protagonist_dict[position]
        else:
            return get_arg1_value(extract_between_brackets(n["description"]))