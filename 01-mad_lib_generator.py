# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:03:28 2021

@author: patry
"""
import os
import random
import shutil

def intro():
    # game introduction and rules
    print('---Welcome to the MAD LIBS GAME!---')    
    print('Rules:')
    print('1) Choose a number of story;')
    print('2) Type some words below and click \'enter\' after each;')
    print('3) And most important: HAVE FUN!')  
    
    while True:
        try:
            answer = input('Do You want to start? (y/n): ')
            if answer == 'y':
                game_choose()
                break
            elif answer == 'n':
                input('Good Bye!')
                break
            else:
                1/0
        except ZeroDivisionError:
            print('Error! Wrong button, try again.')
            continue
        
def game_choose():
    # chosing a text
    path = os.path.join(os.getcwd(), 'texts')   
    texts = []
    for root, dirs, files in os.walk(path):
        for name in files:
            texts.append(name.replace('.txt','').replace('_',' ').upper())
            
    print('\nStories:')
    for story in texts:
        print('{}. {};'.format(texts.index(story)+1, story))
    print('\n0. Options')
        
    while True:
        try:
            answer = int(input('Choose a number of story (1-{}) or show other options (0): '
                           .format(len(texts))))
            if answer <= len(texts) and answer > 0:
                print('You choosed a story number {}.'.format(answer))
                print('Lets start typing!')
                game(answer-1, texts, path)
                break
            elif answer == 0:
                game_options(texts, path)
                break
            else:
                1/0
        except ValueError:
            print('Error! You need to type an integer! Try again.')
            continue
        except ZeroDivisionError:
            print('Error! Wrong button, try again.')
            continue
        
def game_options(texts, path):
    # showing game options
    options = ['Add a new story', #1
               'Delete a story',  #2
               'Restore a story', #3
               'Random select',   #4
               'Start again',     #5
               'Quit the game',   #6
               'Go back']         #7
    print('\nOptions:')
    for option in options:
        print('{}. {};'.format(options.index(option)+1, option))
        
    def game_options_choose(answer, options):
        if answer == options.index('Add a new story')+1: # adding a new text           
            print('Remember! Empty space in text need to be written in [], eg. "Very [ADJECTIVE] day."')
            new_text_title = str(input('Write the tile of a new text: '))
            new_text = str(input('Add a new text below:\n'))
            filepath = os.path.join(path, new_text_title.replace(' ','_')+'.txt')
            with open(filepath, 'w') as file:
                file.write(new_text)
            print('New text added succesfully!')
            game_choose()
        elif answer == options.index('Delete a story')+1: #deleting a text
            if len(texts) > 0:
                while True:
                    try:
                        answer = int(input('Choose a number of story to delete (1-{}): '
                                           .format(len(texts))))
                        if answer <= len(texts) and answer > 0:
                            delete_text(answer-1, texts, path)
                            print('Text no. {} deleted successfully.'.format(answer))
                            game_choose()
                            break
                        else:
                            1/0
                    except ValueError:
                        print('Error! You need to type an integer! Try again.')
                        continue
                    except ZeroDivisionError:
                        print('Error! Wrong button, try again.')
                        continue
            else:
                print('There are no stories to delete.')
                game_options(texts, path)
        elif answer == options.index('Restore a story')+1: # restoring a text from trash
            trash_texts = []
            trash_path = os.path.join(os.getcwd(), 'trash')
            for root, dirs, files in os.walk(trash_path):
                for name in files:
                    trash_texts.append(name.replace('.txt','').replace('_',' ').upper())
            if len(trash_texts) > 0:
                print('\nStories to restore:')
                for trash_story in trash_texts:
                    print('{}. {};'.format(trash_texts.index(trash_story)+1, trash_story))
                while True:
                    try:
                        answer = int(input('Choose a number of story to restore (1-{}): '
                                           .format(len(trash_texts))))
                        if answer <= len(trash_texts) and answer > 0:
                            restore_text(answer-1, trash_texts, trash_path)
                            print('Story no. {} restored successfully.'.format(answer))
                            game_choose()
                            break
                        else:
                            1/0
                    except ValueError:
                        print('Error! You need to type an integer! Try again.')
                        continue
                    except ZeroDivisionError:
                        print('Error! Wrong button, try again.')
                        continue
            else:
                print('There are no stories to restore.')
                game_options(texts, path)
        elif answer == options.index('Random select')+1: # random select
            rand_number = random.randint(0,len(texts)-1)
            print('Let\'s start a game no. {}!'.format(rand_number+1))
            game(rand_number, texts, path)
        elif answer == options.index('Start again')+1: # start again
            print('\n','#'*50,'\n')
            intro()
        elif answer == options.index('Quit the game')+1: # Quit the game
            input('Good bye!')
        elif answer == options.index('Go back')+1: # Go back
            game_choose()
    
    while True:
        try:
            answer = int(input('Choose a number of option (1-{}): '
                             .format(len(options))))
            if answer <= len(options) and answer > 0:
                print('You choosed an option number {}.'.format(answer))
                game_options_choose(answer, options)
                break
            else:
                1/0
        except ValueError:
            print('Error! You need to type an integer! Try again.')
            continue
        except ZeroDivisionError:
            print('Error! Wrong button, try again.')
            continue

def restore_text(number, texts, path):
    # restoring a text - moving to text dir
    src_path = os.path.join(path, texts[number].replace(' ','_').capitalize()+'.txt')
    dst_path = os.path.join(os.getcwd(), 'texts')
    shutil.move(src_path, dst_path)

def delete_text(number, texts, path):
    # deleteing a text - moving to trash
    src_path = os.path.join(path, texts[number].replace(' ','_').capitalize()+'.txt')
    dst_path = os.path.join(os.getcwd(), 'trash')
    if os.path.isdir(dst_path):
        shutil.move(src_path, dst_path)
    else:
        os.mkdir(dst_path)
        shutil.move(src_path, dst_path)                      

def game(number, texts, path):
    # showing a text
    choice = texts[number]   
    filename = choice.replace(' ','_').capitalize()+'.txt'
    filepath = os.path.join(path, filename)   
    
    with open(filepath, 'r') as file:
        text = file.read()
    
        text_mod = text.replace('.','').replace('\n',' ').replace(',','').split(' ')
        tuples_list = []
        i = 0
        
        for word in text_mod:
            if word.startswith('['):
                i += 1
                new_word = input('Word no. {} ({}): '
                                 .format(i, word[1:-1].lower().replace('_',' ')
                                         .replace('\'','').replace(']','')))
                tuples_list.append((word, new_word)) 
       
        tuples_list2 = tuples_list.copy()
        for i in tuples_list:        
            a = text.find('[')
            b = text.find(']')
            text = text[:a]+tuples_list2.pop(0)[1].upper()+text[b+1:]

    print('-'*30)
    print(choice.upper())
    print(text)
    again()

def again():
    while True:
        try:
            answer = input('One more time? (y/n): ')
            if answer == 'y':
                print('')
                print('#'*40)
                print('')
                intro()
                break
            elif answer == 'n':
                input('Good Bye!')
                break
            else:
                1/0
        except ZeroDivisionError:
            print('Error! Wrong button, try again.')
            continue

intro()              