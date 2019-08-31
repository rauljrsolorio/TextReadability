# -*- coding: utf-8 -*-
"""
CECS 174 Homework 3
Due April 11 2017

TODO: This assignment allow us to analyze a piece of text to determine
the level of readability. We use three equations to give us the 
Dale-Chall Readability Score, Flesch Reading ease and Flesch-Kincaid grade level.

@author: Raul Solorio rauljr1910@yahoo.com # TODO: complete information
@author: Khorey Dang Khorey.Dang@student.csulb.edu # TODO: complete information
"""

# import statements
import text_file_reader

def count_syllables(word):
   # TODO: write the docstring
   """Counts and returns the number of syllables of a word.

      Uses a loop to test the position of each letter to determine
   whether it is a syllable or not.
      If it is a syllable, it adds to the counter.

      Args:
         word: a string to be used to count syllables
         
      Returns:
         The number of syllables of the word
         
   """
   # TODO: define function
   word = word.lower()
   vowels = "aeiouy"
   syllables = 0

   for i in range(len(word) - 1): 
      if i == 0: #Checks the first letter and determines if it is a vowel or not
         if word[i] in vowels:
            if word[i + 1] in vowels:
               syllables += 1
            else:
               syllables += 1
      if i < len(word) and i != 0: #Checks every letter that is not the first and last to deteermine if it is a vowel or not
         if word[i] in vowels:
            if word[i + 1] in vowels:
               syllables += 1
            elif word[i - 1] not in vowels:
               syllables += 1
      if i == len(word) - 2: #Checks the last letter and determines if it is a vowel or not
         if word[i + 1] in vowels: 
            if word[i + 1] != "e" and word[i] not in vowels: #If the last letter is not an e and if the current word is a consonant add syllables
               syllables += 1
            elif word[i:i + 2] == "le": 
               if word[i - 1] not in vowels: #Checks if the last three letters are in the format consonant+'le'
                  syllables += 1
               else:
                  pass
            else:
               pass

   if syllables == 0: #If the word has no syllables, it will add one.
      syllables += 1

   return syllables


def get_readability_scores(filename, header_length, easy_words):
   # TODO: write the docstring
   """Calculates the readability score of a file using the number of words, sentences, and syllabus in the file.

      Uses a loop to determine the number of words, sentences and difficult words.
      It then puts these values into a formula to get the Dale-Chall Readability Score, Flesch Reading ease, and Flesch-Kincaid greade level.

      Args:
         filename: The name of the file to be analyzed
         header_length: The amount of lines at the top of the file to be skipped
         easy_words: A file that contains a list of easy or familiar words
         
      Returns:
         Three scores that measures the readability of the text
         
   """   
   # TODO: define function
   difficult_words = 0
   words = 0
   punctuation = ".?:;!,"
   sentence_punctuation = ".?:;!"
   quotes = "\"”“"
   sentences = 0
   syllables = 0
   filename = [line.lower() for line in text_file_reader.get_lines(filename, header_length)] #Lowers every string in the file
   for line in filename: 
      for char in sentence_punctuation:
         if char in line:
            lines = line.split(char)#Split ever line by punctuation
            for i in range(len(lines)): 
               if lines[i] != "" and lines[i] != "”" and lines[i] != "“" and lines[i] != "\"": #Counts the number of sentence that is not an empty space or single punctuation
                  sentences += 1
      for word in line.split(): #Splits the word in each sentence
         if word[0].isalpha(): 
            if "-" not in word:
               if word.isalpha(): #If the word contains only letters
                  words += 1
                  syllables += count_syllables(word)
                  for char in punctuation:
                     word = word.replace(char, "") #Takes away the punctuation in a word
                  for char in quotes:
                     word = word.replace(char, "") #Takes away the quotes in a word
                  if word not in easy_words and word != "i": #Checks if word is in the list of easy words
                     difficult_words += 1
               elif "’" or "'" in word: #If the word contains an apostrophe
                  words += 1
                  syllables += count_syllables(word)
                  for char in punctuation:
                     word = word.replace(char, "")
                  for char in quotes:
                     word = word.replace(char, "")
                  if word not in easy_words and (word != "i'd" or word != "i'm" or word != "i'll" or word != "i've"): 
                     difficult_words += 1
               else: #If the word ends in a punctuation
                  for char in punctuation:
                     if word.endswith(char):
                        words += 1
                        syllables += count_syllables(word)
                        for char in punctuation:
                           word = word.replace(char, "")
                        for char in quotes:
                           word = word.replace(char, "")
                        if word not in easy_words:
                           difficult_words += 1
                     else:
                        pass
   if difficult_words / words > .05: #Checks if the percentage of difficult words is greater than 5 percent.
      dale_chall_score = 0.1579 * (difficult_words / words * 100) + 0.0496 * (words / sentences) + 3.6365 #Got formula from wikipidia
   else:
      dale_chall_score = 0.1579 * (difficult_words / words * 100) + 0.0496 * (words / sentences) #Got formula from wikipidia
   flesh_ease_score = 206.835 - (words / sentences) - 84.6 * (syllables / words) #Got formula from wikipidia
   flesh_grade_level = (0.39 * (words / sentences)) + (11.8 * (syllables / words)) - 15.59 #Got formula from wikipidia
   return (dale_chall_score, flesh_ease_score, flesh_grade_level)

def main():
   '''The instructions to be executed when this Python script is run.
   '''
   print("Hello Users, the purpose of this program is to analyze pieces of text")
   print("by counting the number of syllables and gets the score of readability." )
   print("")
   continue_loop = "0"
   filename = ""
   while continue_loop != "-1" : #Loops until user decides to exit
      try: 
          filename = input("Enter the name of the file to be analyzed: ")
          header_length = int(input("Enter the number of lines in the file that are in the heading: "))
          print("")
          easy_words = text_file_reader.get_lines("DaleChallEasyWordList.txt")
          Dale_chall_readability_score, Flesch_reading_ease, Flesch_kincaid_grade_level = get_readability_scores(filename, header_length, easy_words) 
          print ("The Value for Dale chall readability score is: ", Dale_chall_readability_score)
          print("The Flesch reading ease is: ", Flesch_reading_ease)
          print("The Flesch kincaid grade level is: ", Flesch_kincaid_grade_level)
          print("")
          continue_loop = input("To exit press -1, to continue press any other key: ")
      except: #Checks if the file name does not exist
         print("Error! Wrong file name!")
       
######################################
# Do not modify any of the code below    
######################################

if __name__ == "__main__":
    # execute only if run as a script
    main()

