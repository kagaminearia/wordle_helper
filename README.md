# Wordle Magic
A helper for the game [wordle](https://www.nytimes.com/games/wordle/index.html)! Just take a screenshot of the game, it will help you figure out possible words in just seconds. 

# Instructions on Installation and Usage

__Installation__

Create a new directory and push this repo to that directory. Install the required packages. Give permission to the shell script file. 

**This package is tested on Ubuntu 20.04. It should work on Ubuntu 18.04 as well.**

```
git clone git@github.com:kagaminearia/wordle_helper.git
cd wordle_helper
sudo apt install python3-pip
pip3 install -r requirements.txt
chmod +x wordle_magic.sh
```

__Usage__

1. Take a screenshot of the wordle game you are struggling with. Name your picture as `wordle.png` or anything and save it in the `~/wordle_helper` directory.
2. Open your terminal and navigate to the `~/wordle_helper` directory. Simply type `./wordle_magic` if you named it `wordle.png`, or type `./wordle_magic $NAME_OF_YOUR_IMAGE$` if you named it differently. The magic will happen in just seconds!

__Explanation__

`characters.pickle`: stores the binary mask of every English character.

`c_store.pickle`: stores a dictionary of English characters mapping to its binary mask.

`img_data`: a directory contains images for training, used by `data_collector.py`.


### Reference

Dictionary of words: [Google 10000 words no swear](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english-no-swears.txt) and [All English words](https://github.com/dwyl/english-words/blob/master/words.txt).
