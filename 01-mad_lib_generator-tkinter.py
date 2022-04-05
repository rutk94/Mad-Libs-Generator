# -*- coding: utf-8 -*-
"""
Created on Sun Jan 23 11:42:57 2022

@author: patry
"""

from tkinter import *
from tkinter import messagebox
import tkinter.font as font
import os
import random as rd
import shutil


root = Tk()
root.title('MAD LIB GAME')


# Showing text options - function
def text_options():
    global my_font
    my_font = font.Font(slant='italic', size=11)
    
    path = os.path.join(os.getcwd(), 'texts')
    global text_titles
    text_titles = []
    
    for root, dirs, files in os.walk(path):
        for name in files:
            text_titles.append("'"+name.replace('.txt','').replace('_',' ')+"'")
    
    # make option radio-buttons
    global r
    r = StringVar()
    global r_buttons
    r_buttons=[]
    for option in text_titles:        
        r_button = Radiobutton(make_choice_frame, text=option, variable=r, 
                               value=option, font=my_font, activebackground='#ffcc99')
        r_button.grid(sticky=W)
        r_buttons.append(r_button)
    
    r_buttons[0].select()
    
      
# Start game - function
def start_game():
    # creating a new window
    global game_root
    game_root = Toplevel()
    game_root.title('MAD LIB GAME - type words')
    # creating a frame
    frame = LabelFrame(game_root, text='Type random words in brackets')
    frame.grid(row=0, column=0, columnspan=2, sticky=W+E, padx=5)
    
    # Generate types of needed words
    filename = r.get().replace(' ','_').replace("'",'').capitalize()+'.txt'
    filepath = os.path.join(os.getcwd(), 'texts', filename)
    with open(filepath, 'r') as file:
        text = file.read()   
        text_mod = text.replace('.','').replace('\n',' ').replace(',','').split(' ')
        
        global inputs
        inputs = []
        i = 0   
        for word in text_mod:
            if word.startswith('['):
                i += 1
                
                # Labels
                new_word_type = Label(frame, text=word[1:-1].capitalize().replace('_',' ')
                                      .replace('\'','').replace(']','')+':')
                new_word_type.grid(row=i, column=1, pady=5, sticky=W)
                
                new_word = Entry(frame, width=30)
                new_word.grid(row=i, column=2, pady=5, padx=5)
                
                inputs.append(new_word)     
    
                
    ### BUTTONS
    # clear button
    clear_button_game_root = Button(game_root, text='Clear all', bd=3, bg='#c2c2c2', 
                                    command=clear)
    clear_button_game_root.grid(row=2, column=1, sticky=E)
    
    # Generate button
    generate_button_game_root = Button(game_root, text='Generate', bd=3, bg='#c2c2c2', 
                                       command=generate)
    generate_button_game_root.grid(row=3, ipady=5, pady=(10,0), columnspan=2, sticky=W+E)

    # Exit button
    back_button_game_root = Button(game_root, text='Back', bg='#c2c2c2', 
                                   command=lambda: back('game_root'), bd=3)
    back_button_game_root.grid(row=4, columnspan=2, sticky=W+E)


# generate text
def generate():  
    # creating text window
    global text_root
    text_root = Toplevel()
    text_root.title('MAD LIBS GAME - generated text')
    
    # Open original text and delete words in []
    filename = r.get().replace(' ','_').replace("'",'').capitalize()+'.txt'
    filepath = os.path.join(os.getcwd(), 'texts', filename)
    with open(filepath, 'r') as file:
        text = file.read()   
        text_mod = text.replace('.','').replace('\n',' ').replace(',','').split(' ')
    
    # Get new words from entry boxes and make list of them
    new_words_list = []
    for input in inputs:       
        new_words_list.append(input.get())
    
    # put new words into text
    new_words_list_copy = new_words_list.copy()
    for i in new_words_list:        
        a = text.find('[')
        b = text.find(']')
        text = text[:a]+new_words_list_copy.pop(0).upper()+text[b+1:]
    
    # show a story with new words
    story_frame = LabelFrame(text_root, text=r.get().replace("'",''), 
                             font=font.Font(slant='italic',size=11))
    story_frame.grid(row=0, padx=5, pady=20, sticky=W+E)
    
    story = Label(story_frame, text=text, justify=LEFT)
    story.grid()
    
    # Exit button
    back_button_text_root = Button(text_root, text='Back', bg='#c2c2c2', 
                                   command=lambda: back('text_root'), bd=3)
    back_button_text_root.grid(row=1, sticky=W+E)


# Show options - function
def show_options():

    def add_new_story():
        def add_to_memory():
            # getting title from title entry
            title = "'"+add_new_story_title_box.get().capitalize()+"'" 
            text = add_new_story_text_box.get("1.0", END)
           
            # checking if this title already exist     
            if text_titles.count(title) > 0:
                q = messagebox.askyesno('MAD LIBS GAME - new text adding',
                                        'This title already exist! Would you like to overwrite?')
                # if u want to overwrite
                if q:
                    filename = title.replace(' ','_').replace("'",'').capitalize()+'.txt'
                    filepath = os.path.join(os.getcwd(), 'texts', filename)
                    with open(filepath, 'w') as file:
                        file.write(text)
                    
                    # Adding a new text to text_title
                    text_titles.append(title)
                    
                    # Show info about success
                    messagebox.showinfo('MAD LIBS GAME - new text adding',
                                        'Text overwrited succesfully!')
                    
                    # Actualize the choice frame
                    r_button = Radiobutton(make_choice_frame, text=title, variable=r, 
                                           value=title, font=my_font, activebackground='#ffcc99')
                    r_button.grid(sticky=W)
                    r_buttons.append(r_button)
                else:
                    return
            elif title == '':
                messagebox.showinfo('MAD LIBS GAME - new text adding',
                                    'Your text must have title!') 
            else:
                filename = title.replace(' ','_').replace("'",'').capitalize()+'.txt'
                filepath = os.path.join(os.getcwd(), 'texts', filename)
                with open(filepath, 'a') as file:
                    file.write(text)
                
                # Adding a new text to text_title
                text_titles.append(title)
                
                # Show info about success
                messagebox.showinfo('MAD LIBS GAME - new text adding',
                                    'Text added succesfully!')
               
                # Actualize the choice frame
                r_button = Radiobutton(make_choice_frame, text=title, variable=r, 
                                       value=title, font=my_font, activebackground='#ffcc99')
                r_button.grid(sticky=W)
                r_buttons.append(r_button)               
               

        adding_root = Toplevel()
        adding_root.title('MAD LIB GAME - add a new story')
        
        y = Scrollbar(adding_root, bg='#c2c2c2', troughcolor='black')
        y.grid(row=1, column=2, sticky=S+N+E)
        
        ### LABELS
        # title
        add_new_story_title = Label(adding_root, text='Title:')
        add_new_story_title.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        # text
        add_new_story_text = Label(adding_root, text='Text:')
        add_new_story_text.grid(row=1, column=0, padx=5, pady=5, sticky=W+N)
        
        # empty_label = Label(adding_root)
        # empty_label.grid(row=2)
       
        ### BOXES
        # title enter box
        add_new_story_title_box = Entry(adding_root, width=53)
        add_new_story_title_box.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        # text
        add_new_story_text_box = Text(adding_root, width=40, height=10, 
                                      yscrollcommand=y.set)
        add_new_story_text_box.grid(row=1, column=1, padx=(5,0), pady=5, sticky=W)
        
        ### BUTTONS
        add_button = Button(adding_root, text='Add', bd=3, bg='#c2c2c2',
                              command=add_to_memory)
        add_button.grid(columnspan=3, sticky=W+E, padx=10)
        close_button = Button(adding_root, text='Close', bd=3, bg='#c2c2c2',
                              command=adding_root.destroy)
        close_button.grid(columnspan=3, sticky=W+E, padx=10)

    def delete_story():
        title = r.get().replace("'","").replace(' ','_')+'.txt'
        
        # Ask to make sure about deleting
        q = messagebox.askyesno('MAD LIBS GAME - deleting text',
                                'Deleting {}. Are you sure?'
                                .format(r.get()))
        if q:
            src_path = os.path.join(os.getcwd(), 'texts', title)
            dst_path = os.path.join(os.getcwd(), 'trash')
            
            # if destination path exists check if there is
            # a file named the same as deleting file
            if os.path.exists(dst_path):
                same_filenames_list = []
                for roots, dirs, files in os.walk(dst_path):
                    for filename in files:
                        if filename.startswith(title.replace('.txt','')):
                            same_filenames_list.append(filename)
                amount = len(same_filenames_list)
                base, ext = os.path.splitext(title)
               
                # Change the name of deleting file and copying to trash
                if amount > 0:
                    dst_path = os.path.join(os.getcwd(), 'trash', base+'({})'.format(amount)+ext)
                    shutil.copy(src_path, dst_path)
                
                    # Removing a file from texts
                    os.remove(src_path)
                else:
                   shutil.move(src_path, dst_path) 
                
            else:
                os.mkdir(dst_path)
                shutil.move(src_path, dst_path)
        else:
            return
        
        # Show info about successfull deleting
        messagebox.showinfo('MAD LIBS GAME - deleting text',
                            '{} deleted successfully!'.format(r.get()))
        
        # Actualize the choice frame
        text_titles.remove(r.get())
        text_titles.sort()
        
        for widgets in make_choice_frame.winfo_children():
            widgets.destroy()
        
        for option in text_titles:        
            r_button = Radiobutton(make_choice_frame, text=option, variable=r, 
                                   value=option, font=my_font, activebackground='#ffcc99')
            r_button.grid(sticky=W)
            r_buttons.append(r_button)
                
    def restore_story_window():
        
        trash_path = os.path.join(os.getcwd(), 'trash')
        for roots, dirs, files in os.walk(trash_path):
            if len(files) == 0:
                messagebox.showerror('Error!','There are no stories to restore from trash.')
                
            else:        
                def restore_story(story_to_restore):            
                    # Ask to make sure about restoring
                    q = messagebox.askyesno('MAD LIBS GAME - restoring text',
                                            'Restoring {}. Are you sure?'
                                            .format(story_to_restore))
                    
                    if q:
                        # copying .txt to text folder
                        story_txt = str(story_to_restore).replace("'",'').replace(' ','_')+'.txt'
                        src_path = os.path.join(os.getcwd(), 'trash', story_txt)
                        dst_path = os.path.join(os.getcwd(), 'texts')
                        shutil.move(src_path, dst_path)
                        
                        # actualize restore_frame
                        del_stories.remove(story_to_restore)
                        
                        for widgets in restore_frame.winfo_children():
                            widgets.destroy()
                        
                        del_story_buttons=[]
                        for del_story in del_stories:
                            del_story_button = Radiobutton(restore_frame, 
                                                           text=del_story, 
                                                           variable=d,
                                                           value=del_story, 
                                                           font=my_font, 
                                                           activebackground='#ffcc99')
                            del_story_button.grid(sticky=W)
                            del_story_buttons.append(del_story_button)
                        
                        if len(del_story_buttons) > 0:
                            del_story_buttons[0].select()
                        
                        # Actualize the choice frame
                        text_titles.append(story_to_restore)
                        text_titles.sort()
                        
                        for widgets in make_choice_frame.winfo_children():
                            widgets.destroy()
                        
                        for option in text_titles:        
                            r_button = Radiobutton(make_choice_frame, text=option, variable=r, 
                                                   value=option, font=my_font, activebackground='#ffcc99')
                            r_button.grid(sticky=W)
                            r_buttons.append(r_button)
                            
                        # message box about success
                        messagebox.showinfo('MAD LIBS GAME - restoring text',
                                            '{} restored successfully!'
                                            .format(story_to_restore))
                        
                        # close window
                        restore_root.destroy()
                        
                    else:
                        return                      
            
                # create a new window
                restore_root = Toplevel()
                restore_root.title('MAD LIBS GAME - restore a story')        
                
                # create a frame
                restore_frame = LabelFrame(restore_root, text='Choose a story to restore from trash')
                restore_frame.grid(padx=5, sticky=W+E)
                
                # get stories from trash
                src_path = os.path.join(os.getcwd(), 'trash')
                
                del_stories = []
                d = StringVar()
                for roots, dirs, files in os.walk(src_path):
                    for filename in files:
                        del_stories.append("'"+filename.replace('_',' ').replace('.txt','')
                                           .capitalize()+"'")
                
                # showing stories from trash
                del_story_buttons=[]
                for del_story in del_stories:
                    del_story_button = Radiobutton(restore_frame, 
                                                   text=del_story, 
                                                   variable=d,
                                                   value=del_story, 
                                                   font=my_font, 
                                                   activebackground='#ffcc99')
                    del_story_button.grid(sticky=W)
                    del_story_buttons.append(del_story_button)
                    
                
                del_story_buttons[0].select()
                
                
                ### BUTTONS
                restore_button = Button(restore_root, text='Restore a story', bd=3, bg='#c2c2c2',
                                        command=lambda: restore_story(d.get()))
                restore_button.grid(column=0, sticky=W+E)
                
                close_button = Button(restore_root, text='Close', bd=3, bg='#c2c2c2',
                                        command=restore_root.destroy)
                close_button.grid(column=0, sticky=W+E)
            
        
    
    def edit_story():
        def text_to_edit():
            # Open original text
            filename = r.get().replace(' ','_').replace("'",'').capitalize()+'.txt'
            filepath = os.path.join(os.getcwd(), 'texts', filename)
            with open(filepath, 'r') as file:
                text = file.read()   
                text_mod = text.replace('.','').replace('\n',' ').replace(',','').split(' ')
            
            return text
        
        def save():
            # question
            q = messagebox.askyesno('MAD LIBS GAME - editing text',
                                    'Are you sure you want to edit {}?'
                                    .format(r.get()))
            if q:
                edited_title = "'"+edit_title_box.get()+"'"
                edited_text = edit_text_box.get('1.0', 'end-1c')
                
                edited_title_txt = edited_title.replace("'",'').replace(' ','_')+'.txt'
                edited_filepath = os.path.join(os.getcwd(), 'texts', edited_title_txt)
                org_title_txt = r.get().replace("'",'').replace(' ','_')+'.txt'
                org_filepath = os.path.join(os.getcwd(),'texts', org_title_txt)
                dst_path = os.path.join(os.getcwd(), 'archive_texts')
                
                # if os.path.exists(edited_filepath):
                if os.path.exists(dst_path):
                    same_filenames_list = []
                    for roots, dirs, files in os.walk(dst_path):
                        for filename in files:
                            if filename.startswith(org_title_txt.replace('.txt','')):
                                same_filenames_list.append(filename)
                    amount = len(same_filenames_list)
                    base, ext = os.path.splitext(org_title_txt)
                   
                    # Change the name of file and copying to archive
                    if amount > 0:
                        dst_path = os.path.join(os.getcwd(), 'archive_texts',
                                                base+'({})'.format(amount)+ext)
                        shutil.copy(org_filepath, dst_path)
                    
                        # Removing a file from texts
                        os.remove(org_filepath)
                    else:
                       shutil.move(org_filepath, dst_path)
                else:
                    os.mkdir(dst_path)
                    shutil.move(org_filepath, dst_path)
                    
                with open(edited_filepath, 'w') as file:
                    file.write(edited_text)
                # else:
                #     with open(edited_filepath, 'w') as file:
                #         file.write(edited_text)
            
            # closing window
            edit_root.destroy()
            
            # Actualize the choice frame
            text_titles.remove(r.get())
            text_titles.append(edited_title)
            text_titles.sort()
            
            for widgets in make_choice_frame.winfo_children():
                widgets.destroy()
            
            for option in text_titles:        
                r_button = Radiobutton(make_choice_frame, text=option, variable=r, 
                                       value=option, font=my_font, activebackground='#ffcc99')
                r_button.grid(sticky=W)
                r_buttons.append(r_button)
                
            # message box about success
            messagebox.showinfo('MAD LIBS GAME - editing text',
                                '{} edited successfully!'
                                .format(r.get()))
                    
                    
        
        #creating a root
        edit_root = Toplevel()
        edit_root.title('MAD LIBS GAME - text edition')
        
        
        
        
        ### LABELS
        # title
        edit_title = Label(edit_root, text='Title:')
        edit_title.grid(row=0, column=0, padx=5, pady=5, sticky=W)
        # text
        edit_text = Label(edit_root, text='Text:')
        edit_text.grid(row=1, column=0, padx=5, pady=5, sticky=W+N)
        
        # scrollbar
        y = Scrollbar(edit_root, bg='#c2c2c2', troughcolor='black')
        y.grid(row=1, column=2, sticky=S+N+E)
        
        ### BOXES
        # title enter box
        edit_title_box = Entry(edit_root)
        edit_title_box.grid(row=0, column=1, padx=5, pady=5, sticky=W)
        edit_title_box.insert(0, r.get().replace("'",""))
        # text
        edit_text_box = Text(edit_root,
                             height=10, 
                             yscrollcommand=y.set,
                             wrap=WORD)
        edit_text_box.grid(row=1, column=1, padx=(5,0), pady=5, sticky=W)
        edit_text_box.insert(END, text_to_edit())
        
        ### BUTTONS
        edit_button = Button(edit_root, text='Edit', bd=3, bg='#c2c2c2',
                              command=save)
        edit_button.grid(columnspan=3, sticky=W+E, padx=10)
        close_button = Button(edit_root, text='Close', bd=3, bg='#c2c2c2',
                              command=edit_root.destroy)
        close_button.grid(columnspan=3, sticky=W+E, padx=10)
        
        

    def random_story(value):
        random_story_title = text_titles[rd.randint(0, len(text_titles)-1)]
        if random_story_title != value:
            r.set(random_story_title)
            random_choice = Label(options_frame, text='Random choice: '+r.get(),
                                  anchor='w', justify=LEFT)
            random_choice.grid(row=4, column=1, sticky=W+E, padx=5)
        else:
            random_story(random_story_title)     

    def close_options():
        options_frame.destroy()
        close_button.destroy()
        # option button activation     
        options_button = Button(root, text='Options', bg='#c2c2c2', state=NORMAL,
                                command=show_options, bd=3)
        options_button.grid(row=3, column=0, sticky=W+E)
        

    # options button deacivation
    options_button = Button(root, text='Options', bg='#c2c2c2', state=DISABLED, 
                        bd=3)
    options_button.grid(row=3, column=0, sticky=W+E)
    
    # options frame
    options_frame = LabelFrame(root, text='Options')
    options_frame.grid(columnspan=2, padx=5, pady=20, sticky=W+E)
    
    ### Buttons        
    add_new_button = Button(options_frame, text='Add a new story', bd=3, bg='#c2c2c2', 
                            command=add_new_story)
    add_new_button.grid(column=0, sticky=W+E, pady=2)
    
    edit_button = Button(options_frame, text='Edit a story', bd=3, bg='#c2c2c2',
                          command=edit_story)
    edit_button.grid(column=0, sticky=W+E, pady=2)
    
    delete_button = Button(options_frame, text='Delete a story', bd=3, bg='#c2c2c2',
                           command=delete_story)
    delete_button.grid(column=0, sticky=W+E, pady=2)    
     
    restore_button = Button(options_frame, text='Restore a story', bd=3, bg='#c2c2c2',
                            command=restore_story_window)
    restore_button.grid(column=0, sticky=W+E, pady=2)    
    
    random_button = Button(options_frame, text='Random select', bd=3, bg='#c2c2c2',
                           command=lambda: random_story(r.get()))
    random_button.grid(column=0, sticky=W+E, pady=2)
    
    close_button = Button(root, text='Close options', bd=3, bg='#c2c2c2',
                          command=close_options)
    close_button.grid(column=0, columnspan=2, sticky=W+E, padx=10)



# Exit game - function
def exit_game():
    root.destroy()

def clear():
    for input in inputs:
        input.delete(0, END)
    
# Back to previous window
def back(window):
    if window == 'text_root':
        text_root.destroy()
    elif window == 'game_root':
        game_root.destroy()
    

### LABELS
# Introduction Label
intro_title = Label(root, text='--- Welcome to the MAD LIBS GAME! ---', 
                    font=('Arial', 20))
intro_title.grid(row=0, column=0, columnspan=2, sticky=W+E)

# Choosing Labels
# make_choice_title = Label(root, text='Choose a story from below:')
# make_choice_title.grid(row=1, column=0, pady=(20,5), sticky=W)

global make_choice_frame
make_choice_frame = LabelFrame(root, text='Choose a story from below:')
make_choice_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=20, sticky=W+E)


### BUTTONS
# Start button
start_button = Button(root, text='Start', bd=3, bg='#c2c2c2', 
                      command=lambda: start_game())
start_button.grid(row=2, ipady=5, pady=(10,0), columnspan=2, sticky=W+E)

# Options button
options_button = Button(root, text='Options', bg='#c2c2c2', command=show_options, 
                        bd=3)
options_button.grid(row=3, column=0, sticky=W+E)

# Exit button
exit_button = Button(root, text='Exit', bg='#c2c2c2', command=exit_game, bd=3)
exit_button.grid(row=3, column=1, sticky=W+E)



# Showing text options to choose       
text_options()


root.mainloop()
