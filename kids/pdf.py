#! /usr/bin/python
# -*- coding: utf-8 -*-

#from tracking.models import *
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image
from reportlab.platypus import BaseDocTemplate
from reportlab.platypus import Frame
from reportlab.platypus import PageTemplate
from reportlab.platypus import PageBreak
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.platypus import Spacer
from reportlab.lib.pagesizes import A4
from reportlab.lib.enums import TA_JUSTIFY
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import cm
from reportlab.lib import utils
import reportlab.rl_config
reportlab.rl_config.warnOnMissingFontGlyphs = 0
ruta = '/home/Django/palabrayespiritu/servidor/'
ruta_fonts = ruta + 'static/fonts/'
pdfmetrics.registerFont(TTFont('PatrickHand',
    ruta_fonts + 'PatrickHand-Regular.ttf'))
pdfmetrics.registerFont(TTFont('PermanentMarker',
    ruta_fonts + 'PermanentMarker.ttf'))
pdfmetrics.registerFont(TTFont('Julee',
    ruta_fonts + 'Julee-Regular.ttf'))
pdfmetrics.registerFont(TTFont('GloriaHallelujah',
    ruta_fonts + 'GloriaHallelujah.ttf'))
pdfmetrics.registerFont(TTFont('DroidSansMono',
    ruta_fonts + 'DroidSansMono.ttf'))
pdfmetrics.registerFontFamily('PatrickHandFamily',
    normal='PatrickHand',
    bold='PermanentMarker',
    italic='Julee',
    boldItalic='GloriaHallelujah')
import os
import time
import datetime
import threading
import random
import sys


class Guia(BaseDocTemplate):

    def __init__(self, instance):
        # Configuración
        filename = ruta + 'media/kids/guias/%d.pdf' % instance.id
        self.estilos = {
            'texto': ParagraphStyle(name='texto',
                alignment=TA_JUSTIFY,
                fontName='PatrickHand',
                fontSize=12,
                leading=17,
                firstLineIndent=20,
                ),
            'pregunta': ParagraphStyle(name='pregunta',
                alignment=TA_JUSTIFY,
                fontName='PatrickHand',
                fontSize=12,
                leading=20,
                firstLineIndent=30,
                ),
            'puntos': ParagraphStyle(name='puntos',
                alignment=TA_JUSTIFY,
                fontName='PatrickHand',
                fontSize=12,
                leading=25,
                ),
            'cabecera': ParagraphStyle(name='cabecera',
                alignment=TA_RIGHT,
                fontName='GloriaHallelujah',
                fontSize=9,
                leading=14,
                textColor='#444444',
                ),
            'titulo': ParagraphStyle(name='titulo',
                alignment=TA_CENTER,
                fontName='PermanentMarker',
                fontSize=20,
                leading=20,
                textColor='#00338e',
                ),
            'subtitulo': ParagraphStyle(name='subtitulo',
                alignment=TA_JUSTIFY,
                fontName='Julee',
                fontSize=14,
                leading=20,
                textColor='#00338e',
            ),
            'versiculo': ParagraphStyle(name='versiculo',
                alignment=TA_RIGHT,
                fontName='PatrickHand',
                fontSize=12,
                leading=14,
                firstLineIndent=100,
            ),
            'pupiletras': ParagraphStyle(name='pupiletras',
                alignment=TA_CENTER,
                fontName='DroidSansMono',
                fontSize=12,
                leading=15,
            ),
        }
        self.story = []
        self.header = 'Iglesia "La Palabra y El Espíritu"'
        BaseDocTemplate.__init__(self, filename)
        self.mostrar = 0
        self.allowSplitting = 1
        self.showBoundary = self.mostrar
        self.MARGEN = 0.5 * cm
        a4 = A4
        margen = self.MARGEN
        frameDatos = Frame(self.MARGEN * 2, self.MARGEN,
            A4[0] - 4 * self.MARGEN, A4[1] - 4 * self.MARGEN,
            id='datos', showBoundary=self.mostrar)
        height = frameDatos.height
        template = PageTemplate('pagina_normal', [frameDatos],
            self.formato)
        self.addPageTemplates(template)
        self.insertar(instance.nombre, 'titulo')
        self.insertar(u'Versículos de Estudio', 'subtitulo')
        estilo = 'texto'
        for linea in instance.versiculo.splitlines():
            self.insertar(linea, estilo)
            if estilo == 'texto':
                estilo = 'versiculo'
            else:
                estilo = 'texto'
        self.insertar(u'Bosquejo', 'subtitulo')
        estilo = 'texto'
        for linea in instance.bosquejo.splitlines():
            self.insertar(linea, estilo)
        self.insertar('Temas', 'subtitulo')
        for linea in instance.temas.splitlines():
            self.insertar('- ' + linea, 'texto')
        self.story.append(PageBreak())
        alto = 20
        alto += self.insertar(instance.nombre, 'titulo')
        alto += self.insertar(u'Versículo Para Memorizar', 'subtitulo')
        estilo = 'texto'
        for linea in instance.memorizar.splitlines():
            alto += self.insertar(linea, estilo)
            if estilo == 'texto':
                estilo = 'versiculo'
            else:
                estilo = 'texto'
        alto += self.insertar('Ejercicios Espirituales', 'subtitulo')        
        for linea in instance.ejercicios.splitlines():
            alto += self.insertar('- ' + linea, 'texto')
        ej = instance.ejercicios
        ruta_logo = instance.imagen
        url = ruta_logo.path
        img = utils.ImageReader(url)
        iw, ih = img.getSize()
        aspect = ih / float(iw)
        resta = int(height) - alto - 10
        logo = Image(url, width=(resta / aspect), height=resta)
        self.story.append(logo)
        logo.hAlign = 'CENTER'
        logo.vAlign = 'BOTTOM'
        self.insertar('Preguntas', 'subtitulo')
        i = 0
        for linea in instance.preguntas.splitlines():
            i += 1
            self.insertar(str(i) +'.- ' + linea, 'pregunta')
            self.insertar(97 * '. ', 'puntos')
            self.insertar(97 * '. ', 'puntos')
        self.insertar('Completa y Resuelve el Pupiletras', 'subtitulo')
        palabras = []
        for linea in instance.historia.splitlines():
            ps, l = self.parse(linea)
            palabras += ps
            self.insertar(l, 'texto')
        pupiletras = Pupiletras(palabras)
        pupi = unicode(pupiletras)
        self.story.append(Spacer(0, 20))
        for linea in pupi.splitlines():
            self.insertar(linea, 'pupiletras')
        NumberedCanvas(filename)
        self.build(self.story)

    def insertar(self, texto, estilo):
        self.story.append(Paragraph(unicode(texto), self.estilos[estilo]))
        return self.estilos[estilo].leading

    def cabecera(self, canvas):
        origen = Frame(self.MARGEN, A4[1] - 1.5 * cm,
            A4[0] - (2 * self.MARGEN), 1 * cm,
            id='cabecera', showBoundary=self.mostrar)
        story = []
        story.append(Paragraph(self.header, self.estilos['cabecera']))
        origen.addFromList(story, canvas)
        canvas.line(x1=self.MARGEN, y1=A4[1] - 1.2 * cm,
            x2=A4[0] - (self.MARGEN), y2=A4[1] - 1.2 * cm)

    def formato(self, canvas, doc):
        canvas.saveState()
        self.cabecera(canvas)
        canvas.restoreState()

    def parse(self, parrafo):
        palabras = []
        pp = parrafo.split('<')
        linea = pp[0]
        for p in pp[1:]:            
            ss = p.split('>')
            palabras.append(ss[0])
            linea += len(ss[0]) * 2 * '_'
            linea += ss[1]
        return palabras, linea


class NumberedCanvas(canvas.Canvas):
    def __init__(self, filename):
        canvas.Canvas.__init__(self, filename)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont('Helvetica', 10)
        self.drawString(10 * cm, 1 * cm, "{0} de {1}".
            format(self._pageNumber, page_count))


class Options(object):

    def __init__(self):
        self.DEFAULT_PUZZLE_SIZE = 10
        self.DEFAULT_PUZZLE_RESIZE = 2  # add 5 rows/columns to add more space.
        self.MAX_PUZZLE_SIZE = 80
        self.TRIES = 100  # number of attempts to place a word in puzzle,
            # no less than 100
        self.RANDOM_LETTERS = u"AAAÁÁABBCCDDEEEEÉÉFFGGHHIIIÍJJKKLLMMNNÑÑOOOOÓÓPPPQRRSSTUUUÚVVWXYYZZ"
        self.VERBOSE = True
        self.OUTPUT = "puzzle.txt"
        self.SOLUTION = "solution.txt"
        self.MODE = "w"


class Pupiletras(object):
    def __init__(self, words):
        self.size = 0  # overwritten by resize
        self.c = list()  # character table row, column, the resulting puzzle
        self.words = list()
        self.options = Options()
        self.resize(self.options.DEFAULT_PUZZLE_SIZE)
        self.add_words(words)
        self.fill()

    def resize(self, size):
        """Enlarges the puzzle."""
        #add rows, sometime at the beginning, sometimes at the end
        if random.random() > 0.5:
            for row in range(len(self.c), size):
                self.c.append(list())
        else:
            for row in range(len(self.c), size):
                self.c.insert(0, list())

    #add characters to rows, sometimes at the beginning, sometimes at the end
        if random.random() > 0.5:
            for row in range(len(self.c)):
                for col in range(len(self.c[row]), size):
                    self.c[row].append(False)
        else:
            for row in range(len(self.c)):
                for col in range(len(self.c[row]), size):
                    self.c[row].insert(0, False)
        self.size = size

    def add_words(self, words):
        for word in words:
            self.tries = 0  # counter increased by self.fits
            w = unicode(word.replace(' ', '')).upper()
            self.add_word(w)

    def add_word(self, word):
        while True:
            #TODO: try a crossed location
            row, col, rd, cd = self.get_crossed_position(word)
            if row >= 0:
                self.put(word, row, col, rd, cd)
                return
            #Try a random location
            for i in range(self.options.TRIES):
                row, col, rd, cd = self.get_random_position()
                if self.fits(word, row, col, rd, cd):
                    self.put(word, row, col, rd, cd)
                    return
            #attempt to enlarge the puzzle
            if self.size < self.options.MAX_PUZZLE_SIZE:
                self.resize(self.size + self.options.DEFAULT_PUZZLE_RESIZE)
            else:
                break
        raise Error("Error placing word!")

    def get_random_position(self):
        """return a random position: a tuple row, column, row delta,
            column delta deltas are always 1..-1"""
        col = random.randint(0, self.size)
        row = random.randint(0, self.size)
        #row delta. prefer readable directions
        rd = random.randint(-1, 2)
        if rd > 1:
            rd = random.randint(0, 1)
        #col delta. prefer readable directions
        cd = random.randint(-1, 2)
        if cd > 1:
            cd = random.randint(0, 1)
        #avoid deltas 0,0
        if rd == 0 and cd == 0:
            cd = 1
        return row, col, rd, cd

    def get_crossed_position(self, word):
        index = random.randint(0, len(word) - 1)
        letter = word[index]
        positions = list()
        for row in range(0, len(self.c)):
            for col in range(0, len(self.c)):
                if self.c[row][col] == letter:
                    positions.insert(random.randint(0,
                        len(positions)), (row, col))
        if not positions:
            return -1, -1, -1, -1
        for position in positions:
            #try left to right
            if ((position[1] + 1) < self.size and
                not self.c[position[0]][position[1] + 1]):
                #the letter to the right is empty, maybe this one fits here
                if self.fits(word, position[0], position[1] - index, 0, 1):
                    return position[0], position[1] - index, 0, 1
            #try top-bottom
            if ((position[0] + 1) < self.size and
                not self.c[position[0] + 1][position[1]]):
                if self.fits(word, position[0] - index, position[1], 1, 0):
                    return position[0] - index, position[1], 1, 0
        return -1, -1, -1, -1

    def fits(self, word, row, col, rd, cd):
        self.tries += 1
        r, c = row, col
        try:
            for char in word:
                if r < 0 or c < 0:
                    return False
                if not self.c[r][c] in (False, char):
                    return False
                r += rd
                c += cd
        except IndexError:
            return False
        #count the number of characters in the area, if there are too many,
        #this pos won't do
        limit = len(word) * 0.75
        areachars = 0
        minrow = min(row, row + rd * len(word))
        minrow = max(minrow - 1, 0)
        maxrow = max(row, row + rd * len(word))
        maxrow = min(maxrow + 1 + 1, self.size)
        mincol = min(col, col + cd * len(word))
        mincol = max(mincol - 1, 0)
        maxcol = max(col, col + cd * len(word))
        maxcol = min(maxcol + 1 + 1, self.size)
        for arearow in range(minrow, maxrow):
            for areacol in range(mincol, maxcol):
                if self.c[arearow][areacol]:
                    areachars += 1
                    if areachars > limit:
                        return False
        return True

    def put(self, word, row, col, rd, cd):
        """Puts a word in the jigsaw. Throws all errors. Use fits()
        before calling this."""
        r, c = row, col
        for char in word:
            self.c[r][c] = char
            r += rd
            c += cd
        #self.words.append(word.lower())
        self.words.insert(random.randint(0, len(self.words)), word.lower())

    def fill(self):
        """Add random letters to the puzzle."""
        size = len(self.options.RANDOM_LETTERS)
        for row in range(len(self.c)):
            for col in range(len(self.c[row])):
                if not self.c[row][col]:
                    self.c[row][col] = self.options.RANDOM_LETTERS[
                        random.randint(0, size - 1)]

    def __unicode__(self):
        result = ''
        for row in self.c:
            for col in row:
                if not col:
                    col = '.'
                try:
                    result += col + ' '
                except:
                    raise
            result += '\n'
        return result

    def read_words():
        words = list()
        for word in sys.argv[1:]:
            if word.startswith("-"):
                if word in ["-h", "--help"]:
                    sys.exit(0)
                elif word == "--silent":
                    self.options.VERBOSE = False
                elif word.startswith("--output="):
                    self.options.OUTPUT = word[len("--output="):]
                elif word.startswith("--solution="):
                    self.options.SOLUTION = word[len("--solution="):]
                elif word == "--append":
                    self.options.MODE = "a"
                else:
                    sys.exit(1)
            else:
                words.append(word)
        if not words:
            word = "true"
            while word:
                word = raw_input()
                if not word:
                    break
                words.append(word)
        return words



if __name__ == '__main__':
    Guia({'id': 1, 'nombre':'Jesús Purifica El Templo'})
