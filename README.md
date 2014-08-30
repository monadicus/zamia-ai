Links
=====

Data / Exports: http://goofy.zamia.org/voxforge/

Code: https://github.com/gooofy/voxforge

Dictionary
==========

check dictionary for missing words from submissions:

    [guenter@dagobert speech]$ ./lex-todo.py 
    loading transcripts... done. 9891 unique words found.
    Looking up words in dictionary... done

    STATS: 32 of 9891 words have no entry yet => 99% done.

add missing pronounciations:

    ./lex-edit.py `./lex-prompts.py`

export dictionary:

    [guenter@dagobert speech]$ ./lm-export-dict.py -c

    Fetching dict entries for transcript words from db...

    Found 2070 entries.

    /home/ai/voxforge/de/lm/wlist.txt written.
    /home/ai/voxforge/de/lm/dict-julius.txt written.

CMUCLMTK Language Model
=======================

extract prompts from db:

    ./lm-prompts.py

prepare sentences, vocabulary:

    pushd /home/ai/voxforge/de/lm

    cat prompts.sent parole.sent > all.sent

    sed 's/^/<s> /' all.sent | sed 's/$/ <\/s>/' >all.txt

    echo '</s>' > all.vocab
    echo '<s>' >> all.vocab
    cat wlist.txt >>all.vocab

generate model:

    text2idngram -vocab all.vocab -idngram voxforge.idngram < all.txt
    idngram2lm -vocab_type 0 -idngram voxforge.idngram -vocab all.vocab -arpa voxforge.arpa
    sphinx_lm_convert -i voxforge.arpa -o voxforge.lm.DMP

Audio Model
===========

Record Audio, Create Dictionary Entries, Review + Transcribe
------------------------------------------------------------

record:

    ./audio-record-init.py /home/ai/corpora/de/chat/conversation_starters.txt 
    ./audio-record.py /home/ai/voxforge/de/audio/guenter-20131123-qah

import into db:

    ./audio-import.py

transcribe, rate:

    ./audio-transcribe.py 
    point web browser to: http://localhost:8000/

optional: auto-transcribe prompts accepted by the current model:

    ./audio-sphinx-transcribe.py -p 1 -a 1 -n 1 Manu

export dictionary:

    ./lm-export-dict.py -c

Compute Sphinx Model
--------------------

verify:
    ./check-consistency.py 
    ./lex-spellcheck.py

compute model:

    ./audio-gen-sphinx-model.py -c

collect results:

    datum=`date +%Y%m%d`

    AMNAME="voxforge-de-r$datum"

    mkdir "output/$AMNAME"
    mkdir "output/$AMNAME/model_parameters"

    cp -r /home/ai/voxforge/de/work/model_parameters/voxforge.cd_cont_4000 "output/$AMNAME/model_parameters"
    cp -r /home/ai/voxforge/de/work/etc "output/$AMNAME"
    cp -r /home/ai/voxforge/de/work/result "output/$AMNAME"
    cp /home/ai/voxforge/de/work/voxforge.html "output/$AMNAME"
    cp /home/ai/voxforge/de/work/voxforge.html "output/"

    cp input_files/run-pocketsphinx.sh "output/$AMNAME"
    cp input_files/sphinx-model-README "output/$AMNAME/README"

    pushd output
    tar cfvz "$AMNAME.tgz" $AMNAME
    popd

    rm -r "output/$AMNAME"

produce stats overview text file:

    ./audio-stats.py >output/audio-stats.txt

Running pocketsphinx
--------------------

just a sample invocation for live audio from mic:

    pocketsphinx_continuous \
        -hmm model_parameters/voxforge.cd_cont_4000 \
        -lw 10 -feat 1s_c_d_dd -beam 1e-80 -wbeam 1e-40 \
        -dict etc/voxforge.dic \
        -lm etc/voxforge.lm.DMP \
        -wip 0.2 \
        -agc none -varnorm no -cmn current

Expanding the Dictionary
------------------------

The idea here is to generate lists of frequently used words (according to our
text corpora) currently not covered by prompts and/or our dictionary.

    ./lm-topwords.py 
    Reading /home/ai/voxforge/de/lm/prompts.sent...
      10000 sentences.   9700 unique words.
      20000 sentences.  11765 unique words.
    Reading /home/ai/voxforge/de/lm/parole.sent...
      10000 sentences.  30165 unique words.
    [...]
    Got 602300 unique words from corpora.

    Computed top 7000 words.
    output/topwords.txt written.

    Already covered by submissions: 12832 words.


    Words not covered: 999
    output/missingwords.txt written.

now compose sentences using as many words as possible from output/missingwords and read them.

Audiobooks
----------

(1/9) Convert Audio to Wav:

    for i in mp3/*.mp3 ; do mpg123 -w wav/`basename $i`.wav $i ; done

(2/9) Check Audio, add prolog/epilog of chapters to transcripts, if necessary.

(3/9) Spellcheck, convert to prompts:

    ./abook-spellcheck.py abook/janeeyre/txt/abschnitt1.txt abook/janeeyre/prompts/abschnitt1.txt

(4/9) segment

    ./abook-segment.py Karlsson abook/das_alte_haus/wav/altehaus_01_gerstaecker_64kb.mp3.wav

make sure to check the last segment generated, usually it is empty. If so, delete it.

(5/9) align prompts

automatically:

    ./abook-align-sphinx.py /home/ai/voxforge/de/audio/Hokuspokus-20140826-qah abook/janeeyre/prompts/abschnitt1.txt 

or manually:

    ./abook-align.py /home/ai/voxforge/de/audio/Karlsson-20140718-qah abook/das_alte_haus/prompts/abschnitt1.txt 

(6/9) import

    ./audio-import.py

(7/9) add missing words to dictionary:

    ./lex-auto.py
    ./lex-edit.py `./lex-prompts.py`

(8/9) transcribe

    ./audio-sphinx-align.py Hokuspokus

(9/9) export

    ./audio-export-submission.py Hokuspokus-20140826-qah



Compute HTK Model (currently not used)
--------------------------------------

    ./audio-gen-model.py

    [guenter@dagobert speech]$ ./audio-gen-model.py
    
    Step 1 - Preparation
    
    Loading dict...
    30222 words found in dictionary.
    
    Step 2 - Collect Prompts, generate words.mlf, convert audio
    
    ...
    
    Step 10 - Making Tied-State Triphones
    
    cd /home/ai/voxforge/de/work ; HDMan -A -D -T 1 -b sp -n fulllist -g ./input_files/global.ded dict-tri dict.txt > logs/Step10_HDMan.log
    making hmm13
    cd /home/ai/voxforge/de/work ; HHEd -A -D -T 1 -H hmm12/macros -H hmm12/hmmdefs -M hmm13 tree.hed triphones1 > logs/Step10_HHed_hmm13.log
    making hmm14
    cd /home/ai/voxforge/de/work ; HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm13/macros -H hmm13/hmmdefs -M hmm14 tiedlist > logs/Step10_HERest_hmm14.log
    making hmm15
    cd /home/ai/voxforge/de/work ; HERest -A -D -T 1 -T 1 -C ./input_files/config -I wintri.mlf -t 250.0 150.0 3000.0 -s stats -S train.scp -H hmm14/macros -H hmm14/hmmdefs -M hmm15 tiedlist > logs/Step11_HERest_hmm15.log
    
    *** completed ***

    Final model copied to: /home/ai/voxforge/de/work/acoustic_model_files

collect final model:

    cp -r /home/ai/voxforge/de/work/acoustic_model_files output/
    cp /home/ai/voxforge/de/work/dict.txt output/dict
    cp /home/ai/voxforge/de/lm/dict-julius.txt output/dict
    cp /home/ai/voxforge/de/work/logs/Step* output/logs

SRILM / MITLM Language Models (currently not used)
==================================================

SRILM Language Model Generation
-------------------------------

workdir: /home/ai/voxforge/de/lm

References:
* http://julius.sourceforge.jp/forum/viewtopic.php?f=5&t=132&p=783&hilit=reverse+model#p783
* http://www.speech.sri.com/projects/srilm/download.html
* http://trulymadlywordly.blogspot.de/2011/03/creating-text-corpus-from-wikipedia.html
* HTK Book

SRILM Installation:
* unpack
* export SRILM=`pwd`
* make MACHINE_TYPE=i686-m64-rhel World

Download from http://www.statmt.org/europarl/

Export dictionary, generate wordlist:

    ./lm-export-dict.py

Generate corpus:

    #./lm-europarl.py
    ./lm-prompts.py 

Generate reverse corpus:

    #~/projects/ai/speech/lm-reverse.pl conversation_starters.sent >conversation_starters.rev
    #~/projects/ai/speech/lm-reverse.pl europarl.sent >europarl.rev
    ~/projects/ai/speech/lm-reverse.pl prompts.sent > prompts.rev

Train forward 2-gram in ARPA format:

    #ngram-count -order 2 -text prompts.sent -text conversation_starters.sent -text europarl.sent -unk -lm german.arpa -vocab wlist.txt
    ngram-count -order 2 -text prompts.sent -unk -lm german.arpa -vocab wlist.txt

Train backward N-gram:

    #ngram-count -order 4 -text prompts.rev -text conversation_starters.rev -text europarl.rev -unk -lm german-rev.arpa -vocab wlist.txt
    ngram-count -order 4 -text prompts.rev -unk -lm german-rev.arpa -vocab wlist.txt

Combine the two ARPA N-grams and convert into binary format for Julius:

    mkbingram -nlr german.arpa -nrl german-rev.arpa german.bingram

collect results:

    cp /home/ai/voxforge/de/lm/german.bingram output/lm
    cp /home/ai/voxforge/de/lm/wlist.txt output/lm

test julius:

    ./run-julius.sh

if fail:

    ./run-julius.sh &>t.log
    ./lm-export-dict.py t.log
    cp /home/ai/voxforge/de/lm/dict-julius.txt /home/guenter/projects/ai/speech/output/


MITLM Language Model Generation
-------------------------------

workdir: /home/ai/voxforge/de/lm

References:

* http://trulymadlywordly.blogspot.de/2011/03/creating-text-corpus-from-wikipedia.html
* HTK Book

Download from http://www.statmt.org/europarl/

    ./lm-europarl.py
    ./lm-export-dict.py

estimate-ngram -vocab wlist.txt -text europarl.sent -write-lm german.lm

    ./lm-collect-sentences.py /home/ai/corpora/de/chat/conversation_starters.txt > /home/ai/voxforge/de/lm/conversation_starters.sent

    estimate-ngram -vocab wlist.txt -text conversation_starters.sent,europarl.sent -write-lm german.lm

    cp /home/ai/voxforge/de/lm/german.lm /home/guenter/projects/ai/speech/output/
    cp /home/ai/voxforge/de/lm/dict-julius.txt /home/guenter/projects/ai/speech/output/


test julius:

    ./run-julius.sh

if fail:

    ./run-julius.sh &>t.log
    ./lm-export-dict.py t.log


Grammar Generation:
===================

edit 

    grammar/starter.grammar
    grammar/starter.voca

compute

    cd grammar
    [guenter@dagobert grammar]$ mkdfa.pl starter
    starter.grammar has 3 rules
    starter.voca    has 8 categories and 8 words
    ---
    Now parsing grammar file
    Now modifying grammar to minimize states[-1]
    Now parsing vocabulary file
    Now making nondeterministic finite automaton[11/11]
    Now making deterministic finite automaton[11/11] 
    Now making triplet list[11/11]
    8 categories, 11 nodes, 11 arcs
    -> minimized: 9 nodes, 9 arcs
    ---
    generated: starter.dfa starter.term starter.dict


Running Julius
==============

    julius -input pulseaudio -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -nlr output/german.lm -v output/dict-julius.txt

    julius -input file -filelist files.txt -h output/acoustic_model_files/hmmdefs -hlist output/acoustic_model_files/tiedlist -dfa grammar/starter.dfa -v grammar/starter.dict -smpFreq 48000

    julius -input rawfile -realtime -filelist $sndfile -h $mmf -gramlist julius/gramlist.txt -multipath -lv 2500 -rejectshort 70 -headmargin 50 -tailmargin 50 -progout -sp sil -b 0

