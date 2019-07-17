#!/usr/bin/env python
# encoding: utf8

# Aligns OCR output with a gold standard text, inserting linebreaks
# and hyphenatation into the gold standard if needed.
#
# The switches
#   -sb (strip beginning) and
#   -se (strip end),
# allow stripping lines at the beginning resp the end of the OCR
# text. NB! The amount of stripped material may vary with the quality
# of the alignment, so use with some care.
#
# A mismatching aligned character counts as a character error (with
# exceptions for newlines and hyphens), a word containing a character
# error -- including a misaligned whitespace marking the end of the
# word -- counts as a word error. Total character and word counts are
# based on the manual string. This means that if the ocr string
# contains many characters without counterparts in the manual string,
# the error rates may be more than 100%.
#


punct = ('.',',','!','?',':',';','\'','"','-','/')

import sys
import codecs
import pickle
import constants as c

def save_obj(obj, name ):
    with open('models/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('models/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

def worderrors(ocrdrec,mandrec):

#   #print ocrdrec
#   #print mandrec

    def ocrdwordgenerator(ocrd):
        ocrdlines = ocrd.split('\n')
        halfword = ''
        for l in ocrdlines:
            l = l.strip()
            if not l:
                continue

            words = l.replace('\t',' ').split(' ')
            words[0] = halfword+'\n'+words[0]
            if (words[-1].endswith('-') or words[-1].endswith('\xad')) and len(words[-1])>1:
                halfword = words[-1]
                del words[-1]
            else:
                halfword = ''

            for w in words:
                yield w

    mandwords = [w for w in ''.join(mandrec).replace('\t',' ').replace('\n',' ').replace('\u00ad','-').split() if w]
    ocrdwords = [w for w in ocrdwordgenerator(''.join(ocrdrec))]

    x = len(ocrdwords)+1
    y = len(mandwords)+1
    Tot = [0 for _ in range(x*y)]
    Noo = [0 for _ in range(x*y)]
    Sub = [0 for _ in range(x*y)]
    Ins = [0 for _ in range(x*y)]
    Del = [0 for _ in range(x*y)]

#   #print ocrdwords
#   #print mandwords

    for i in range(1,x):
        Del[i] = Del[i-1]+1
        Tot[i] = Tot[i-1]+1

    for j in range(1,y):
        Ins[x*j] = Ins[x*(j-1)]+1
        Tot[x*j] = Tot[x*(j-1)]+1

    for j in range(1,y):
        for i in range(1,x):
            mandword = mandwords[j-1]
            ocrdword = ocrdwords[i-1]

            if mandword == ocrdword or mandword == ocrdword.replace('-\n','') or mandword == ocrdword.replace('\xad\n','') or mandword == ocrdword.replace('\n',''):
                ntot = Tot[(i-1)+x*(j-1)]
                nnoo = Noo[(i-1)+x*(j-1)]+1
                nsub = Sub[(i-1)+x*(j-1)]
                nins = Ins[(i-1)+x*(j-1)]
                ndel = Del[(i-1)+x*(j-1)]
            else:
                ntot = Tot[(i-1)+x*(j-1)]+1
                nnoo = Noo[(i-1)+x*(j-1)]
                nsub = Sub[(i-1)+x*(j-1)]+1
                nins = Ins[(i-1)+x*(j-1)]
                ndel = Del[(i-1)+x*(j-1)]

            # inserts
            down = Tot[i+x*(j-1)]+1
            if down < ntot:
                ntot = down
                nnoo = Noo[i+x*(j-1)]
                nsub = Sub[i+x*(j-1)]
                nins = Ins[i+x*(j-1)]
                ndel = Del[i+x*(j-1)]+1

            # deletes
            rght = Tot[(i-1)+x*j]+1
            if rght < ntot:
                ntot = rght
                nnoo = Noo[(i-1)+x*j]
                nsub = Sub[(i-1)+x*j]
                nins = Ins[(i-1)+x*j]+1
                ndel = Del[(i-1)+x*j]

            Tot[i+x*j] = ntot
            Noo[i+x*j] = nnoo
            Sub[i+x*j] = nsub
            Del[i+x*j] = ndel
            Ins[i+x*j] = nins

    return Tot[-1],Noo[-1],Sub[-1],Del[-1],Ins[-1], len(mandwords)

def charalign(ocrd,mand):
    # Align an ocr string and a manual (gold standard) string

    # First fill in the edit distance matrix
    # Operations, each may be associated with special costs/circumstances
    #
    # z: potential alternative startpoint for the alignment (directly
    #    after a newline in the ocr string at the start of the manual
    #    string)
    # d: delete
    # i: insert
    # n: no operation (direct match)
    # w: matching whitespace
    # h: matching hyphens
    # t: substitute
    # -: delete a hyphen at the end of the line
    # r: deleta a return

    x = len(ocrd)+1
    y = len(mand)+1
    M = [0 for _ in range(x*y)]         # matrix (as list) holding scores
    O = ['' for _ in range(x*y)]        # matrix (as list) holding operations/backpointers

    M[0] = 0
    for i in range(1,x):
        # fill in the X-margin, mark positions after a newline
        if i > 1 and ocrd[i-1]=='\n':
            M[i] = 0
            O[i] = 'z'
        else:
            M[i] = M[i-1]+1
            O[i] = 'd'

    for j in range(1,y):
        # fill in the Y-margin
        M[x*j] = M[x*(j-1)] + 1
        O[x*j] = 'i'

    for j in range(1,y):
        for i in range(1,x):
            # Fill in the rest of the matrix
            # NOTE: the matrix indices i,j correspond to string indices i-1, j-1, because of the added initial row/column

            # substitutions
            mandchar = mand[j-1]
            ocrdchar = ocrd[i-1]
            if mandchar == ocrdchar:
                diag = M[(i-1)+x*(j-1)]
                ops = 'n' # no-op
            elif mandchar in ' \t\n' and ocrdchar in ' \t\n':
                diag = M[(i-1)+x*(j-1)]
                ops = 'w' # match whitespace
            elif mandchar in '-\u2014\u00ad' and ocrdchar in '-\u2014\xad':
                diag = M[(i-1)+x*(j-1)]
                ops = 'h' # match hyphens
            elif mandchar not in '\t \n' and ocrdchar not in ' \t\n':
                if mandchar in punct and ocrdchar in punct:
                    diag = M[(i-1)+x*(j-1)]+0.999 # if it's all the same, prefer to substitute punktuation for punktuation
                elif mandchar not in punct and ocrdchar not in punct:
                    diag = M[(i-1)+x*(j-1)]+0.999 #                       or substitute nonpunktuation for nonpunktuation
                else:
                    diag = M[(i-1)+x*(j-1)]+1
                ops = 't' # substitute, only non-whitespace
            else:
                ops = 'x'
                diag = M[(i-1)+x*(j-1)]+100000
            bst = diag

            # inserts
            down = M[i+x*(j-1)]+1
            if down < bst:
                ops = 'i' # insert
                bst = down
            elif down == bst:
                ops += 'i'

            # deletes
            if ocrd[i-1] in ('-','\xad') and (i==x-1 or (i < x-1 and ocrd[i]=='\n')):
                rght = M[(i-1)+x*j]
                dops = '-' # delete a hyphen at the end of the line = free
            elif ocrd[i-1] == '\n':
                rght = M[(i-1)+x*j]
                dops = 'r' # delete a newline ('r'eturn) = free
            else:
                rght = M[(i-1)+x*j]+1
                dops = 'd' # delete

            if rght < bst:
                ops = dops
                bst = rght
            elif rght == bst:
                ops += dops

            # enter the best score and operations/backpointers in the matrices
            M[i+x*j] = bst
            O[i+x*j] = ops



    # Reconstruct one of the optimal alignments. There is no explicit
    # control over which alignment is chosen in case of multiple
    # alignments with the same, optimatal score.

    # Alignment endpoint logic, depends on -se switch (=OPTstripend)
    j = y-1
    if OPTstripend and '\n' in ocrd:
        # endpoint is cheapest cell on bottom row that corresponds to a newline in the ocr string
        i = -min((M[(i+1)+x*j],-(i+1)) for i,ch in enumerate(ocrd) if ch=='\n' or i==x-2)[1]
    else:
        i = x-1

    ocrdrec = []
    mandrec = []

    while i or j:
        op = O[i+x*j][-1]
        if OPTstripbeg and op == 'z': # ztartpoint of the alignment, see also endpoint logic
                                      # depends on -sb switch (=OPTstripbeg)
            break
        elif op in 'ntwh':
            ocrdrec.append(ocrd[i-1])
            mandrec.append(mand[j-1])
            i -= 1
            j -= 1
        elif op in 'dz': # case for z when stripping of initial lines is not allowed
            ocrdrec.append(ocrd[i-1])
            mandrec.append('') # u'\u03F5')
            i -= 1
        elif op=='e':
            i -= 1
        elif op in 'r-':
            ocrdrec.append(ocrd[i-1])
            mandrec.append('') # %
            i -= 1
        elif op == 'i':
            ocrdrec.append('') # u'\u03F5')
            mandrec.append(mand[j-1])
            j -= 1

#    for p in zip(reversed(mandrec),reversed(ocrdrec)):
#       #print "[%s]\t[%s]" % p

    return list(reversed(ocrdrec)),list(reversed(mandrec))


def markerror(listofstrings,index):
    # Mark the character(s) at location index as an error, to give some visual feedback
    # '\x1b[44;1m' and '\x1b[0m' are ANSI escape codes that change the color and fontstyle
    # See e.g. https://en.wikipedia.org/wiki/ANSI_escape_code
    listofstrings[index] = '°°'+listofstrings[index]+'°°'





def score_and_print(ocrdrec,mandrec):
    # With the alignment, go through line by line, character by character to count errors, characters, words, etc.
    # Also marks the errors in a#printable way and#prints the alignment and scores to the screen

    if ocrdrec == []:
        return 0, 0, 0, 0, 0, 0, 0
#        return charactererrors, characters, worderrors, words, unaligned_ocr_whitespaces, unaligned_man_whitespaces, aligned_whitespaces

    newlines = [i for i,char in enumerate(ocrdrec) if char=='\n']
    if not newlines or not newlines[-1] == len(ocrdrec)-1:
        newlines.append(len(ocrdrec)-1)
    i0 = 0
    charactererrors = 0
    characters = 0
    worderrors = 0 # number of words containing
    words = 0
    unaligned_ocr_whitespaces = 0
    unaligned_man_whitespaces = 0
    aligned_whitespaces = 0
    output=''

    errors_in_current_word = False
    characters_in_mandword = False

    for i in newlines:
        ocrdline = ocrdrec[i0:i+1]
        mandline = mandrec[i0:i+1]
        i0 = i+1

        try:
            ignorable_prefix = next(i for i,(o,m) in enumerate(zip(ocrdline,mandline))
                                    if o not in ('','\n','\t',' ') or m not in ('','\n','\t',' '))
        except StopIteration:
            ignorable_prefix = len(ocrdline)

        try:
            ignorable_suffix = len(ocrdline)-next(i for i,(o,m) in enumerate(reversed(list(zip(ocrdline,mandline))))
                                                  if o not in ('','\n','\t',' ','-','\xad') or m not in ('','\n','\t',' '))
        #                                                                       ^^^^ End of line hyphens are ignorable in the OCR.
        #                                                                            BUG! may ignore several line-final hyphens in a row
        except StopIteration:
            ignorable_suffix = 0

        for i,o in enumerate(ocrdline):
            if o == '\n':
                ocrdline[i] = '\u2424' # unicode ␤  (newline)
            elif o == '\t':
                ocrdline[i] = '\u2409' # unicode ␉  ([horizontal] tab)

        for i,m in enumerate(mandline):
            if m == '\n':
                mandline[i] = '\u2424'
            elif m == '\t':
                mandline[i] = '\u2409'

        # compare line on character basis
        for i,(o,m) in enumerate(zip(ocrdline,mandline)):

            # All the `pass' cases are considered correct
            if ignorable_suffix <= i or i < ignorable_prefix:
                if not o:
                    ocrdline[i] = '\u03F5' # unicode epsilon
                if not m:
                    mandline[i] = '\u03F5'
                pass
            elif o and o in '-\u2014\xad' and m and m in '-\u2014\xad': # (soft-)hyphen and m-dash considered equal
                pass
            elif o in ('\u2424','\u2409',' ') and m in ('\u2409',' '):
                aligned_whitespaces += 1
                pass
            elif OPTnewlines_in_man and m=='\u2424' and o in ('\u2424','\u2409',' '):
                aligned_whitespaces += 1
                pass
            elif o == '-' and m == '\u00ad': # hyphen and soft hyphen considered equal
                pass
# Special cases if certain characters are to be ignored in the total count
#            elif o == '*':
#                characters -= 1
#            elif m and m in u'åöäÅÖÄëË':
#                characters -= 1
            elif o==m:

                pass

            # The rest constitutes an error case
            else:
                charactererrors += 1

                if not o:
                    ocrdline[i] = '\u03F5' # unicode epsilon
                if not m:
                    mandline[i] = '\u03F5'

                markerror(ocrdline,i)
                markerror(mandline,i)

                if o in (' ','\u2424','\u2409'):
                    unaligned_ocr_whitespaces += 1

                if m in (' ','\u2424','\u2409'):
                    unaligned_man_whitespaces += 1
                else:
                    errors_in_current_word = True

            if m:
                characters +=1

            # rather rudimentary word counting, only segments at ' ' (space).
            if m in ('\u2424','\u2409',' '):
                if characters_in_mandword:
                    words += 1
                    if errors_in_current_word:
                        worderrors += 1
                characters_in_mandword = False
                errors_in_current_word = False
            elif m:
                characters_in_mandword = True

        output+=''.join(char for char in ocrdline)
        #print the alignment with markup to the screen, with a running score counter for this page
        # print(''.join(char for char in ocrdline))#, '\tce: %s, #c: %s, we: %s, #w: %s' % (charactererrors, characters, worderrors, words))
        # print(''.join(char for char in mandline))
        # print()

    if characters_in_mandword:
        words += 1
    if errors_in_current_word:
        worderrors += 1

    return charactererrors, characters, worderrors, words, unaligned_ocr_whitespaces, unaligned_man_whitespaces, aligned_whitespaces,output



# Options to control the stripping of lines at the beginning resp end
# Options to control the stripping of lines at the beginning resp end
OPTstripbeg = False
OPTstripend = False
OPTnewlines_in_man = False
def main(mode, pairOfPaths):
    error_words = []
    if mode == '-sb':
        OPTstripbeg = True
    elif mode == '-se':
        OPTstripend = True
    elif mode == '-nm':
        OPTnewlines_in_man = True

    totalchrs = totalchrerrs = totalwrds = totalwrderrs = totalua_m_wh = totalua_o_wh = totala_wh = 0
    tWErrors = tWNoos = tWSubs = tWDels = tWIns = tWCount = 0

    count=0
    number_of_files=len(pairOfPaths)
    for ocrdfile, mandfile in pairOfPaths:
        with codecs.open(ocrdfile,'r','utf8') as f:
            # codecs.open('utf8') no gusto universal newlines???
            ocrd = f.read().replace('\r\n','\n').replace('\r','\n').strip()
        with codecs.open(mandfile,'r','utf8') as f:
            mand = f.read().replace('\r\n','\n').replace('\r','\n').strip()

        ocrdrec,mandrec = charalign(ocrd,mand)
        chrerrs, chrs, wrderrs, wrds, ua_o_wh, ua_m_wh, a_wh, ocr = score_and_print(ocrdrec,mandrec)
        WErrors, WNoos, WSubs, WDels, WIns, WCount = worderrors(ocrdrec,mandrec)

        if(c.verbose):
            count+=1
            print("Evaluated file: %i/%i"%(count,number_of_files))

        totalchrerrs += chrerrs
        totalchrs += chrs
        totalwrderrs += wrderrs
        totalwrds += wrds
        totalua_m_wh += ua_m_wh
        totalua_o_wh += ua_o_wh
        totala_wh += a_wh

        tWErrors += WErrors
        tWNoos += WNoos
        tWSubs += WSubs
        tWDels += WDels
        tWIns += WIns
        tWCount += WCount
        if(totalchrs == 0 or tWCount == 0):
            return(0,0)

    return(float(totalchrerrs/totalchrs), tWErrors/tWCount)
