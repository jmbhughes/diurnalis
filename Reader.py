import argparse, re
from dateutil.parser import parse as dateparser
from collections import Counter

class JournalEntry:
    ''' A container for a journal entry '''
    def __init__(self, title, date_string, contents):
        self.title = title
        self.date = dateparser(date_string) # a datetime object
        self.contents = contents
    
    def __len__(self):
        '''The length is the word count'''
        return len(self.contents.split()) - 1 # subtract one for the extra space

    def __str__(self):
        ''' convert to a string '''
        entry = "{}\n{}\n".format(self.title, self.date)
        entry += "-"*80
        entry += "\n"
        entry += self.contents
        return entry
    
class Reader():
    ''' A utility to read the LaTex journal '''
    
    def __init__(self, path):
        ''' creates and runs a reader object from the file path to the journal '''
        self.path = path
        self._read()
        
    def _read(self):
        ''' read in the journal and break the entries into pieces '''
        with open(self.path) as f: data = f.read()
        self.starts = [m.end() for m in re.finditer("begin{logentry}", data)] #lines for log entry beginnings
        self.ends = [m.start() for m in re.finditer("end{logentry}", data)] # lines for log entry endings
        self.string = data # entire journal as a string
        self.entries = [] # list of processed entries
        for start, end in zip(self.starts, self.ends):
            entry_string = self.string[start:end] # get the entry between those times
            date, title = [entry_string[m.start():m.end()] for m in re.finditer("\{([^\}]+)\}", entry_string)][:2]
            date, title = date[1:-1], title[1:-1] # remove the { }
            contents = "\n".join(entry_string.split("\n")[1:])
            entry = JournalEntry(title, date, contents)
            self.entries.append(entry)

    def get_journal_entries(self):
        ''' return the list of journal entry objects '''
        return self.entries

    def get_most_recent_entry(self, n=1):
        ''' Get the n-most recent journal entry '''
        return sorted(self.entries, key=lambda entry: entry.date, reverse=True)[:n]
    
class Explorer():
    ''' A utility to find interesting patterns in the parsed journal '''
    def __init__(self, journal_entries):
        ''' given a list of journal_entries, explore the data '''
        self.journal_entries = journal_entries
        
    def most_common_words(self, n):
        ''' determine the n-most commonly used words in the journal '''
        self.words = re.findall(r'\w+', " ".join([entry.contents for entry in self.journal_entries]).lower())
        self.word_freqs = Counter(self.words)
        return self.word_freqs.most_common(n)
    
if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--journal",
                        default="/home/marcus/grive/journal/journal.tex",
                        help="path to journal to process")
    args = vars(parser.parse_args())

    # Make reader
    reader = Reader(args['journal'])
    entries = reader.get_journal_entries()

    # Entry lengths
    #lengths = [len(entry) for entry in entries]
    #print(lengths)

    # Most common words
    #explorer = Explorer(entries)
    #print(explorer.most_common_words(150))
    
    
