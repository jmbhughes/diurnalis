import argparse, re
from dateutil.parser import parse as dateparser
from collections import Counter

class JournalEntry:
    ''' A container for a journal entry '''
    def __init__(self, title, date_string, contents):
        self.title = title
        self.date = dateparser(date_string)
        self.contents = contents
        
class Reader():
    ''' A utility to read the LaTex journal '''
    def __init__(self, path):
        self.path = path
        self._read()
        
    def _read(self):
        with open(self.path) as f: data = f.read()
        self.starts = [m.end() for m in re.finditer("begin{logentry}", data)]
        self.ends = [m.start() for m in re.finditer("end{logentry}", data)]
        self.string = data
        self.entries = []
        for start, end in zip(self.starts, self.ends):
            entry_string = self.string[start:end]
            date, title = [entry_string[m.start():m.end()] for m in re.finditer("\{([^\}]+)\}", entry_string)][:2]
            date, title = date[1:-1], title[1:-1] # remove the { }
            contents = "\n".join(entry_string.split("\n")[1:])
            entry = JournalEntry(title, date, contents)
            self.entries.append(entry)

    def get_journal_entries(self):
        return self.entries
    
class Explorer():
    ''' A utility to find interesting patterns in the parsed journal '''
    def __init__(self, journal_entries):
        self.journal_entries = journal_entries
        
    def most_common_words(self, n):
        self.words = re.findall(r'\w+', " ".join([entry.contents for entry in self.journal_entries]).lower())
        self.word_freqs = Counter(self.words)
        return self.word_freqs.most_common(n)
    
if __name__ == "__main__":
    # Get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--journal",
                        default="/Users/mhughes/google_drive/journal/journal.tex",
                        help="path to journal to process")
    args = vars(parser.parse_args())

    # Make reader
    reader = Reader(args['journal'])
    entries = reader.get_journal_entries()
    explorer = Explorer(entries)
    print(explorer.most_common_words(150))
    
    
