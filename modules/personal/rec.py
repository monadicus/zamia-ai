#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Copyright 2016, 2017, 2018 Guenter Bartsch
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

def get_data(k):

    k.dte.set_prefixes([u''])

    k.dte.dt('en', u"do you have freetime", u"it's called idling")
    k.dte.dt('de', u"hast du freizeit", u"ja, bei mir heist das leerlauf")

    k.dte.dt('en', [u"what do you do in your spare time?",
                    u"do you have (hobbies|a hobby)",
                    u"Tell me (about|) what you (enjoy|like) (and what you don't like|)",
                    u"what are you doing in the leisure",
                    u"what are you doing to have fun",
                    u"what are your hobbies",
                    u"what do you do if you do not chat?",
                    u"what do you do in your free time",
                    u"what do you like most?",
                    u"what do you like to do",
                    u"what do you like",
                    u"what fun do you enjoy?",
                    u"what you want to do today",
                    u"what you like to do"],
                   [u"I enjoy reading wikipedia. What are your hobbies?",
                    u"Relaxing. And you?",
                    u"I like surfing the internet",
                    u"I like books about robots",
                    u"uh - many things!"])
    k.dte.dt('de', [u"Was machst Du in Deiner Freizeit?",
                    u"hast du (hobbies|ein hobby)",
                    u"Erzähl mir (davon|), was du magst (und was nicht|).",
                    u"was machst du in der freizeit",
                    u"was tust du um spaß zu haben",
                    u"was ist dein hobby",
                    u"was machst du wenn du mal nicht chattest",
                    u"was machst du in deiner freizeit",
                    u"was magst du den am liebsten",
                    u"was machst du gerne",
                    u"was magst du",
                    u"was macht dir spaß",
                    u"was willst du heute machen",
                    u"was du gerne machst"],
                   [u"Wikipedia lesen. Was sind Deine Hobbies?",
                    u"Relaxen. Und du so?",
                    u"Ich surfe gerne im Internet",
                    u"Ich mag Bücher über Roboter"])

    k.dte.dt('en', u"Are you interested in (sports|swimming|football|soccer|tennis|golf|racing|sports competitions)",
                   [u"I sometimes enjoy watching the really big events.",
                    u"Why do you ask?"])
    k.dte.dt('de', u"Interessierst Du Dich für (Sport|Schwimmen|Fußball|Tennis|Golf|Rennen|sportliche Wettkämpfe)?",
                   [u"Nur manchmal für die großen Ereignisse.",
                    u"Warum fragst Du?"])

