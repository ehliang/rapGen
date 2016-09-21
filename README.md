# Hey Kanye
In recent time, data science has become relevant in every single field. We wanted to see how we can use it to create music.

HeyKanye takes bulk lyrical data from artists of any genre and applies statistical modelling to produce structurally accurate and meaningful music lyrics. It then syncs it to beats and uses text-to-speech to drop a sick new track. 


## Features:
•	Detect the parts of a track with repetitive patterns to determine beat, chorus location, etc
•	Sync lyrics to beats
•	Learns proper chorus-verse structure for a structurally accurate songs
•	Implement multiple rhyme schemes within songs
•	Analyzes common word-to-word relationships to simulate meaning
•	Analyzes common lyrical grammar to create musically relevant songs


## How did we build it?
We used music lyrics APIs to pull in bulk lyrics data to the database. We then further established database tables to map word relationships and line relationships. For example, our database stored data on common word pairs, common words in preceding lines of a word, common sentence structures, etc.

We used python to build Markov chains that likelihood of certain words following other words, similar to Swiftkey’s predictive text. By feeding our Azure SQL database the lyrics of the artists with which we want to base our rap on, our Markov chains become unique to that set of lyrics.

We defined the grammar used for the songs using parse trees (an ordered collection of Nouns, Verbs and Adjectives) built on top of the nltk library and connected our algorithm to Microsoft Azure's Web Language Model API. We also used common parse trees that were found in our dataset. We generated rap lines by conforming our Markov chains to valid parse trees.

From there, we seeded Azure’s algorithm with our generated sentences to add more vocabulary from the internet in the same style. Azure’s API was also used for validation and ensured only the sentences that made the most sense were used in our rap.

As for syncing the lyrics to the music, we used librosa to extract onset (key pitch and beat changes) features from the track. Using this data, we used an edge detecting algorithm and found the time differences between each onset in order to identify the timestamps chorus and the verses. Using that data, we use linux’s espeak to write the text-to-speech of our lyrics into .wav files with their timestamps as their filename. The speed of the speech was determined by the length of the verse relative to the timestamp it was allocated to. Once completed, we grafted every generated text-to-speech .wav onto the base beat to generate a new overlaid wav file which we converted to mp3.

## Algorithms Summary
•	Markov chains for lyrics generation
•	Parse trees for line structure definition
•	Azure API for further lyrical validation
•	Edge detection for detecting beats in music
•	Recursive patterning for detecting beats in music


## Technology stack
•	SQL Server database on MS Azure to host database of words, word relations, and grammar relations
•	Python to implement above mentionned lyric and music processing algorithms
•	Used MS Azure Cognitive Services API to help with lyrics generation
•	Node.js as backend web server
•	JQuery/Javascript for front-end scripting


## Challenges we ran into
1.	Database issues and using MS Azure
2.	How to implement HMM model to produce structurally correct data. We chose to construct the model based off word by word rather than line by line so we can have a truly random song implementation using grammar rules and parse trees.
3.	Insanely dirty lyrics generated by our program
4.	Connecting backend-to-frontend


## What’s next
•	Dynamic generation of different styles of songs based on user input
•	Create different databases to store lyrics of different groups (i.e. different genres, different eras etc) that can be used to produce different styled songs
•	Create a more full scale web application that permits sharing of music
•	Use any new text-to-speech libraries if they are made for different voices