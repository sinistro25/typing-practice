import random
from pygame import Rect
import words_selector
import numpy as np
from key_score import score
from config import *
from enum import Enum,auto

class Kind(Enum):
    UNIFORM     = auto()
    WEIGHTED    = auto()
    NUMBERS     = auto()
    REDUCED     = auto()
    

class TextGenerator():   
    
    def __init__(self,kind=Kind.UNIFORM,min_len=3,max_len=7,min_words=20,max_words=30):
        self.min_len = min_len
        self.max_len = max_len
        self.min_words = min_words
        self.max_words = max_words
        self.kind = kind
        
    def gen(self):
        if self.kind is Kind.WEIGHTED:
            choice = np.random.choice(list(ALPHABET),p=score())
            words = words_selector.words_by_letter(choice)
        elif self.kind is Kind.REDUCED:
            choice = "bcdjkqtvxz"
            words = words_selector.words_by_letter(choice)
        elif self.kind is Kind.NUMBERS:    
            words = words_selector.digit_generator()
        elif self.kind is Kind.UNIFORM:
            words = words_selector.words

        n = random.randint(self.min_words, self.max_words)
        line = []
        for i in range(n):
            line.append(random.choice(words))
        return line

if __name__ == "__main__":
    tg = TextGenerator()
    for i in range(10):
        print(tg.gen())


# draw some text into an area of a surface
# automatically wraps words
# returns any text that didn't get blitted
def draw(surface, text, colors, rect, font):
    rect = Rect(rect)
    y = rect.top
    lineSpacing = -2

    # get the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 0

        # determine if the row of text will be outside our area
        if y + fontHeight > rect.bottom:
            break
        x = rect.left
        # determine maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            image = font.render(text[i], False, colors[i])
            x = rect.left + font.size(text[:i])[0]
            i += 1
            surface.blit(image, (x, y))
        y += fontHeight + lineSpacing
        

        # remove the text we just blitted
        colors = colors[i:]
        text = text[i:]

    return text