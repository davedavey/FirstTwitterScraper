# -*- coding: utf-8 -*-≈
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import tweepy
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import random
from Tkinter import Tk, Label, Button, Entry, StringVar, DISABLED, NORMAL, END, W, E
from Tkinter import BOTH, END, LEFT
import Tkinter as tk


class MyFirstGUI:
 
        def __init__(self, master):
                self.master = master
                self.master.title("Python Scraper")
                
                self.label1 = Label(self.master, text="Please enter a hashtag (#hashtag) to search twitter for.")
                self.label1.pack()
                
                #Box to input hashtag
                
                v = StringVar()
                e = Entry( self.master, textvariable = v)
                e.pack()
                #gets the value from the box.
                #We could do this on the button call and pass all values on
                #to the real program.
                
                
                self.label2 = Label(self.master, text = "How many results would you like per search? Recommended: 200-1000.")
                self.label2.pack()
                
                #Box to enter results per search
                
                results = StringVar()
                r = Entry( self.master, textvariable = results)
                r.pack()
                
                
                
                self.label3= Label(master, text = "How many times would you like Twitter scraped? Warning: do not exceed the data cap! Recommended 6 or less times")
                self.label3.pack()
                
                #box to enter number of times to scrape twitter
                times = StringVar()
                t = Entry( self.master, textvariable = times)
                t.pack()
                
                
                
                
                self.label4 = Label(self.master, text = "What would you like on your y-axis?")
                self.label4.pack()
                
                #drop down box with the 5 options
                List1 = tk.Listbox(exportselection=0)
                
                for item in ["created_at", "retweet_count", "favorite_count", "source", "user_id", "user_screen_name", "user_name", "user_created_at", "user_followers_count", "user_friends_count", "user_location"]:
                        List1.insert(END, item) 
                List1.pack()
                
                self.label5 = Label(self.master, text = "The x axis will be the number of sources")
                
                
                
                
                def runit(hashtag, other_variable, other_variable_times, yaxis):
                        #Credentials go here:
                        
                        #Credentials end here. Redacted due to the internet.
                        auth= tweepy.OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
                        api = tweepy.API(auth)
                        
                        l = StdOutListener()
                        auth = OAuthHandler(consumer_key, consumer_secret)
                        auth.set_access_token(access_token, access_token_secret)
                        stream = Stream(auth, l) 
                #results
                        results = []
                        x = 0
                        for x in range(0,other_variable_times):
                                geocode="39.999726,-83.015202,5mi"
                                for tweet in tweepy.Cursor(api.search, q = hashtag , return_type="recent").items(other_variable):
                                        results.append(tweet)
                 
                        #Begin making the data structure:
                 
                        id_list = [tweet.id for tweet in results]
                        data_set = pd.DataFrame(id_list, columns=["id"])
                 
                        # Processing Tweet Data
                 
                        data_set["text"] = [tweet.text for tweet in results]
                        data_set["created_at"] = [tweet.created_at for tweet in results]
                        data_set["retweet_count"] = [tweet.retweet_count for tweet in results]
                        data_set["favorite_count"] = [tweet.favorite_count for tweet in results]
                        data_set["source"] = [tweet.source for tweet in results]
                 
                        # Processing User Data
                        data_set["user_id"] = [tweet.author.id for tweet in results]
                        data_set["user_screen_name"] = [tweet.author.screen_name for tweet in results]
                        data_set["user_name"] = [tweet.author.name for tweet in results]
                        data_set["user_created_at"] = [tweet.author.created_at for tweet in results]
                        data_set["user_description"] = [tweet.author.description for tweet in results]
                        data_set["user_followers_count"] = [tweet.author.followers_count for tweet in results]
                        data_set["user_friends_count"] = [tweet.author.friends_count for tweet in results]
                        data_set["user_location"] = [tweet.author.location for tweet in results]
                        data_set["followers_count"] = [tweet.author.followers_count for tweet in results]
                 
                        #data_set = process_results(results)
                        #sources = data_set["retweet_count"].value_counts()[:5][::-1]
                        sources = data_set[yaxis].value_counts()[:20][::-1]
                   
                 
                        plt.barh(xrange(len(sources)), sources.values)
                        plt.yticks(np.arange(len(sources)) + 0.4, sources.index)
                        if x == 0:
                                plt.show(block=False)
                        else:
                                plt.draw()
                        print x
                        x = x + 1
                        plt.show()
    
                
                
                def search():
                
                    #This should take the inputs from the boxes and selections from the x and y axis and
                    #enter it into another program that will be pasted below. I don't want to share due to
                    #OAuth credentials etc..
                                #gets hashtag
                    hashtag = v.get()
                                #gets results per search
                    if r.get() != '':
                            other_variable = int(r.get())
                                #gets times to scrape twitter
                    if t.get() != '':
                            other_variable_times = int(t.get())
                                
                    yaxis = List1.get(List1.curselection()[0])
                    


                
                    
                    runit(hashtag, other_variable, other_variable_times, yaxis) 
                           
                
                search_button = Button(self.master, text = "Search", command = search)
                search_button.pack()
        
        
        
class StdOutListener(StreamListener):
 
    def on_data(self, data):
        print data
        return true
        
                
root = tk.Tk()
my_gui = MyFirstGUI(root)
root.mainloop()