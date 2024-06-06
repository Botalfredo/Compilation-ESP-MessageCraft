import re
import logging

# Logging configuration initialization
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

class LexerException(Exception):
    """Exception raised when lexer encounters an unexpected character."""
    pass

class Lexem:
    def __init__(self, tag, value, position):
        self.type = tag
        self.value = value
        self.position = position

    def __repr__(self):
        return f"{self.type}({self.value})@{self.position}"


class Lexer:
    TOKEN_REGEXES = [
        (r'\bunit\s+[A-Za-z0-9_]+\b', 'UNIT'),
        (r'\bmessage\s*:\s*', 'MESSAGE_START'),
        (r'=', 'ASSIGN'),
        (r'\b(broadcast|sender|listener)\b', 'ROLE'),
        (r'\bName\s*=\s*', 'NAME'),
        (r'\bVariable\s*:\s*', 'VARIABLE'),
        (r'\bComment\s*=\s*(.*)', 'COMMENT'),
        (r'\b(char\[\d+\]|char|int|float|double|bool|int8_t|uint8_t|int32_t|uint32_t)\b', 'TYPE'),
        (r'[A-Za-z0-9_]+', 'IDENTIFIER'),
        (r'\[\d+\]', 'ARRAY_SIZE'),
        (r'[ \t]+', 'WHITESPACE'),
        (r'.', 'MISMATCH')
    ]

    def __init__(self):
        """Initialisation du composant d'analyse lexicale."""
        self.lexems = []
        self.current_line_number = 0
        self.current_position = 0

    def lex(self, input):
        """Génère des lexèmes pour chaque ligne d'entrée."""
        for line_nb, line in enumerate(input):
            self.current_line_number = line_nb + 1
            self.current_position = 0
            line = line.strip()
            if not line:
                continue
            try:
                self.match_line(line)
            except LexerException as err:
                logger.error(f"Lexing error on line {self.current_line_number}: {err}")
                raise
        return self.lexems

    def match_line(self, line):
        """Faire correspondre une ligne à tous les motifs d'expressions rationnelles."""
        while self.current_position < len(line):
            match = False
            for pattern, tag in self.TOKEN_REGEXES:
                if match := self.match_lexem(line, pattern, tag):
                    break
            if not match:
                error_message = f"ERROR at: ({self.current_line_number},{self.current_position}):\n" + line + "\n" + " " * self.current_position + "^" * (len(line) - self.current_position)
                logger.error(error_message)
                raise LexerException(error_message)

    def match_lexem(self, line, pattern, tag):
        """Faire correspondre la ligne avec un motif et une balise regex spécifiques."""
        regex = re.compile(pattern)
        match = regex.match(line, self.current_position)
        if match:
            data = match.group(0)
            if tag and tag != 'WHITESPACE':
                end_position = self.current_position + len(data)
                lexem = Lexem(tag, data, (self.current_line_number, self.current_position))
                self.lexems.append(lexem)
                #logger.debug(f"Matched {lexem}")
            self.current_position = match.end()
            return True
        return False
