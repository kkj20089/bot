from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import json
import random
import string
import os
import sys
import asyncio
from datetime import datetime, timedelta
import pytz
import signal
import pyshorteners
import logging

# ✅ Configuration
TOKEN = "7722342816:AAEkrArt2FHmKCcKap32AyKgnRootmzlV3M"
TIMEZONE = pytz.timezone('Asia/Kolkata')
PID_FILE = "bot.pid"

# ✅ In-memory JSON storage
url_data = {}

# ✅ Channel Data (Stored inside the script)
channel_data = """
1 IN: Aastha SD = https://ninjatv-redtv.vercel.app/api/?id=354291 
2 Anjan SD = https://ninjatv-redtv.vercel.app/api/?id=355092 
3 Telugu: Aradana SD = https://ninjatv-redtv.vercel.app/api/?id=355093 
4 IN: Bharat 24 = https://ninjatv-redtv.vercel.app/api/?id=355094 
5 IN: Bharat Samachar SD = https://ninjatv-redtv.vercel.app/api/?id=355095 
6 IN: BIG MAGIC SD = https://ninjatv-redtv.vercel.app/api/?id=355253 
7 GUJ: Colors Gujarati Cinema SD = https://ninjatv-redtv.vercel.app/api/?id=355258 
8 IN: DD Chhattisgarh SD = https://ninjatv-redtv.vercel.app/api/?id=355263 
9 IN: Dangal 2 SD = https://ninjatv-redtv.vercel.app/api/?id=355278 
10 KIDS: ETV Bal Bharat SD = https://ninjatv-redtv.vercel.app/api/?id=355286 
11 Filamchi Bhojpuri SD = https://ninjatv-redtv.vercel.app/api/?id=355294 
12 IN: Goldmines_SD = https://ninjatv-redtv.vercel.app/api/?id=355478 
13 IN: INH 24X7 SD = https://ninjatv-redtv.vercel.app/api/?id=355487 
14 GUJ: India News Gujarat SD = https://ninjatv-redtv.vercel.app/api/?id=355493 
15 TELUGU: Kushi TV SD = https://ninjatv-redtv.vercel.app/api/?id=355504 
16 IN: News 24 SD = https://ninjatv-redtv.vercel.app/api/?id=355507 
17 IN: News India 24x7 SD = https://ninjatv-redtv.vercel.app/api/?id=355509 
18 IN: News State MP CG SD = https://ninjatv-redtv.vercel.app/api/?id=355510 
19 IN: News18 MP Chhattisgarh SD = https://ninjatv-redtv.vercel.app/api/?id=355511 
20 BD: 24 Ghanta SD = https://ninjatv-redtv.vercel.app/api/?id=355540 
21 IN: Aastha Bhajan = https://ninjatv-redtv.vercel.app/api/?id=355541 
22 IN: AlJazeera SD = https://ninjatv-redtv.vercel.app/api/?id=355542 
23 KAN: Ayush TV SD = https://ninjatv-redtv.vercel.app/api/?id=355543 
24 B4U Bhojpuri SD = https://ninjatv-redtv.vercel.app/api/?id=355544 
25 IN: B4U Kadak SD = https://ninjatv-redtv.vercel.app/api/?id=355545 
26 KAN: Chintu TV SD = https://ninjatv-redtv.vercel.app/api/?id=355546 
27 PB: Daily Post Punjab Haryana Himachal SD = https://ninjatv-redtv.vercel.app/api/?id=355552 
28 GUJ: Gujarat First SD = https://ninjatv-redtv.vercel.app/api/?id=355553 
29 IN: Khabarain Abhi Tak SD = https://ninjatv-redtv.vercel.app/api/?id=355554 
30 PB: Living India News SD = https://ninjatv-redtv.vercel.app/api/?id=355555 
31 IN: Manoranjan Grand SD = https://ninjatv-redtv.vercel.app/api/?id=355556 
32 IN: News18 Bihar Jharkhand SD = https://ninjatv-redtv.vercel.app/api/?id=355557 
33 ORI: Prarthana SD = https://ninjatv-redtv.vercel.app/api/?id=355558 
34 KAN: Raj News Kannada SD = https://ninjatv-redtv.vercel.app/api/?id=355559 
35 TM: SVBC 2 SD = https://ninjatv-redtv.vercel.app/api/?id=355560 
36 Sudarshan SD = https://ninjatv-redtv.vercel.app/api/?id=355561 
37 IN: Zee Bharat SD = https://ninjatv-redtv.vercel.app/api/?id=355562 
38 ORI: OTV SD = https://ninjatv-redtv.vercel.app/api/?id=356085 
39 CRI: Star 4K = https://ninjatv-redtv.vercel.app/api/?id=333368 
40 MARATHI: Saam Tv = https://ninjatv-redtv.vercel.app/api/?id=337784 
41 MARATHI: SHEMAROO MARATHI = https://ninjatv-redtv.vercel.app/api/?id=338882 
42 Tata Play Bollywood Masala = https://ninjatv-redtv.vercel.app/api/?id=108874 
43 Tata Play Hollywood Local = https://ninjatv-redtv.vercel.app/api/?id=108876 
44 Tata Play Zindgi = https://ninjatv-redtv.vercel.app/api/?id=108882 
45 Tata Play Hits = https://ninjatv-redtv.vercel.app/api/?id=108881 
46 Tata Play Fitness = https://ninjatv-redtv.vercel.app/api/?id=108880 
47 Telugu Classics = https://ninjatv-redtv.vercel.app/api/?id=108875 
48 Toons + Punjabi = https://ninjatv-redtv.vercel.app/api/?id=108873 
49 Tata Play Cooking = https://ninjatv-redtv.vercel.app/api/?id=3748 
50 Tata Play Ibaadat = https://ninjatv-redtv.vercel.app/api/?id=3749 
51 Tata Play Punjab De Rang = https://ninjatv-redtv.vercel.app/api/?id=7724 
52 Tata Play Beauty = https://ninjatv-redtv.vercel.app/api/?id=3745 
53 Tata Play Javed Akhtar = https://ninjatv-redtv.vercel.app/api/?id=3751 
54 Tata Play Videshi Kahaniyan = https://ninjatv-redtv.vercel.app/api/?id=7725 
55 Tata Play Romance = https://ninjatv-redtv.vercel.app/api/?id=44219 
56 Tata Play Seniors = https://ninjatv-redtv.vercel.app/api/?id=52493 
57 Tata Play ShortsTV = https://ninjatv-redtv.vercel.app/api/?id=52495 
58 Tata Play Classic Cinema = https://ninjatv-redtv.vercel.app/api/?id=52496 
59 Tata Play South Talkies = https://ninjatv-redtv.vercel.app/api/?id=108878 
60 Tata Play Gujarati Cinema = https://ninjatv-redtv.vercel.app/api/?id=108879 
61 KIDS-SPIDER MAN 2008 = https://ninjatv-redtv.vercel.app/api/?id=147720 
62 KIDS-SPIDER MAN 1981 = https://ninjatv-redtv.vercel.app/api/?id=147721 
63 KIDS-SPIDER MAN 1967 = https://ninjatv-redtv.vercel.app/api/?id=147722 
64 KIDS-SLUGTERRA = https://ninjatv-redtv.vercel.app/api/?id=147723 
65 KIDS-SHINCHAN = https://ninjatv-redtv.vercel.app/api/?id=147724 
66 KIDS-SHAPE RHYMES = https://ninjatv-redtv.vercel.app/api/?id=147725 
67 KIDS-SAMURAI JACK = https://ninjatv-redtv.vercel.app/api/?id=147726 
68 KIDS-POPEYE THE SAILOR MAN = https://ninjatv-redtv.vercel.app/api/?id=147727 
69 KIDS-PJ MASK = https://ninjatv-redtv.vercel.app/api/?id=147728 
70 KIDS-PEPPA PIG 2 = https://ninjatv-redtv.vercel.app/api/?id=147729 
71 KIDS-PEPPA PIG = https://ninjatv-redtv.vercel.app/api/?id=147730 
72 KIDS-FINGER FAMILY HD 3 = https://ninjatv-redtv.vercel.app/api/?id=147731 
73 KIDS-NURSERY RHYMES HD 4 = https://ninjatv-redtv.vercel.app/api/?id=147732 
74 KIDS-PAW PETROL UNBOXING TOY = https://ninjatv-redtv.vercel.app/api/?id=147733 
75 KIDS-PAW PETROL TOY STORY = https://ninjatv-redtv.vercel.app/api/?id=147734 
76 KIDS-PAW PETROL = https://ninjatv-redtv.vercel.app/api/?id=147735 
77 KIDS-PERMAN = https://ninjatv-redtv.vercel.app/api/?id=147736 
78 KIDS-LONNEY TUNES PLATINUM COLLECTION = https://ninjatv-redtv.vercel.app/api/?id=147737 
79 KIDS-KUNG FU PANDA = https://ninjatv-redtv.vercel.app/api/?id=147738 
80 KIDS-GENERTOX REX = https://ninjatv-redtv.vercel.app/api/?id=147740 
81 KIDS-FRUITS VEGETABLE RHYMES = https://ninjatv-redtv.vercel.app/api/?id=147741 
82 KIDS-FIVE LITTLE RHYMES = https://ninjatv-redtv.vercel.app/api/?id=147742 
83 KIDS-BEN 10 ULTIMATE ALIEN = https://ninjatv-redtv.vercel.app/api/?id=147743 
84 KIDS-DUCK TALES HD = https://ninjatv-redtv.vercel.app/api/?id=147744 
85 KIDS-DUCK TALES CLASSIC = https://ninjatv-redtv.vercel.app/api/?id=147745 
86 KIDS-DORAEMON = https://ninjatv-redtv.vercel.app/api/?id=147746 
87 KIDS-COLOUR RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147747 
88 KIDS-CHRISTMAS RHYMES = https://ninjatv-redtv.vercel.app/api/?id=147748 
89 KIDS-BEN 10 OMNIVERSE = https://ninjatv-redtv.vercel.app/api/?id=147749 
90 KIDS-BEN TEN CLASSIC = https://ninjatv-redtv.vercel.app/api/?id=147750 
91 KIDS-BEN 10 ALIEN FORCE HD = https://ninjatv-redtv.vercel.app/api/?id=147751 
92 KIDS-ART-FUN = https://ninjatv-redtv.vercel.app/api/?id=147752 
93 KIDS-AVATAR THE LAST AIRBENDER HD = https://ninjatv-redtv.vercel.app/api/?id=147753 
94 KIDS-ANIMAL RHMYES = https://ninjatv-redtv.vercel.app/api/?id=147754 
95 KIDS-ANGERY BIRDS TOONS HD = https://ninjatv-redtv.vercel.app/api/?id=147755 
96 KIDS-ABCD RHYMES HD 2 = https://ninjatv-redtv.vercel.app/api/?id=147756 
97 KIDS-ABBY HATCHER = https://ninjatv-redtv.vercel.app/api/?id=147757 
98 KIDS-NURSER RHYMES HD 4 = https://ninjatv-redtv.vercel.app/api/?id=147758 
99 KIDS-STORY = https://ninjatv-redtv.vercel.app/api/?id=147759 
100 KIDS-BABY TOOT = https://ninjatv-redtv.vercel.app/api/?id=147760 
101 KIDS-BIRTHDAY SONGS = https://ninjatv-redtv.vercel.app/api/?id=147761 
102 KIDS-HICKORY DICKORY DOCK = https://ninjatv-redtv.vercel.app/api/?id=147762 
103 KIDS-BOOM BUDDIES RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147763 
104 KIDS-BABAY BAO PANDA HD = https://ninjatv-redtv.vercel.app/api/?id=147769 
105 KIDS-BABAY RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147770 
106 KIDS-ANIMAL RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147771 
107 KIDS-A B C D RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147772 
108 KIDS-NURSERY RHYMES HD 3 = https://ninjatv-redtv.vercel.app/api/?id=147773 
109 KIDS-NUMBER RHMYES HD = https://ninjatv-redtv.vercel.app/api/?id=147774 
110 KIDS-BOB THE TRAIN HD = https://ninjatv-redtv.vercel.app/api/?id=147775 
111 KIDS-NURSERY RHYMES HD 2 = https://ninjatv-redtv.vercel.app/api/?id=147776 
112 KIDS-MR BEAN HD = https://ninjatv-redtv.vercel.app/api/?id=147777 
113 KIDS-RHYMES HD = https://ninjatv-redtv.vercel.app/api/?id=147778 
114 KIDS-MASH AND BEAR HD = https://ninjatv-redtv.vercel.app/api/?id=147779 
115 KIDS-CHU CHU TV HD = https://ninjatv-redtv.vercel.app/api/?id=147780 
116 KIDS-FINGER FAMILY HD = https://ninjatv-redtv.vercel.app/api/?id=147781 
117 BD: Zee24Ghanta = https://ninjatv-redtv.vercel.app/api/?id=144510 
118 Telugu: BHAKTI TV = https://ninjatv-redtv.vercel.app/api/?id=34581 
119 IN: Disney Junior = https://ninjatv-redtv.vercel.app/api/?id=35713 
120 IN: INDIA TODAY (News) = https://ninjatv-redtv.vercel.app/api/?id=35714 
121 IN: News18 Rajasthan = https://ninjatv-redtv.vercel.app/api/?id=37071 
122 IN: Colors Oria = https://ninjatv-redtv.vercel.app/api/?id=37073 
123 BD: ZEE BANGLA CINEMA = https://ninjatv-redtv.vercel.app/api/?id=49615 
124 PB: ZEE PUNJABI = https://ninjatv-redtv.vercel.app/api/?id=52082 
125 TELUGU:  RAJ NEWS = https://ninjatv-redtv.vercel.app/api/?id=52504 
126 IN: ROMEDY NOW HD = https://ninjatv-redtv.vercel.app/api/?id=179 
127 DANGAL = https://ninjatv-redtv.vercel.app/api/?id=53107 
128 KANNADA: Asianet Suvarna News = https://ninjatv-redtv.vercel.app/api/?id=56037 
129 TELUGU: Star Maa Music = https://ninjatv-redtv.vercel.app/api/?id=57772 
130 Telugu: GEMINI MOVIE (4K) = https://ninjatv-redtv.vercel.app/api/?id=23797 
131 IN: Dhinchaak = https://ninjatv-redtv.vercel.app/api/?id=77143 
132 Telugu: GEMINI MUSIC (4K) = https://ninjatv-redtv.vercel.app/api/?id=23796 
133 IN: DISNEY INTERNATIONAL (4K) = https://ninjatv-redtv.vercel.app/api/?id=20925 
134 IN: INVESTIGATION DISCOVERY (4K) = https://ninjatv-redtv.vercel.app/api/?id=23790 
135 Marathi: ZEE Marathi (FHD) = https://ninjatv-redtv.vercel.app/api/?id=85694 
136 Marathi: ZEE TALKIES (FHD) = https://ninjatv-redtv.vercel.app/api/?id=85695 
137 IN: COMEDY-CENTRAL (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23429 
138 IN: COMEDY CENTRAL HD = https://ninjatv-redtv.vercel.app/api/?id=186 
139 IN: MTV Beats HD. = https://ninjatv-redtv.vercel.app/api/?id=94498 
140 IN: MTV Plus (4K) = https://ninjatv-redtv.vercel.app/api/?id=94499 
141 Marathi: Pravah Picture (4K) = https://ninjatv-redtv.vercel.app/api/?id=96364 
142 IN: NDTV INDIA = https://ninjatv-redtv.vercel.app/api/?id=7430 
143 IN: India news = https://ninjatv-redtv.vercel.app/api/?id=7431 
144 IN: India TV = https://ninjatv-redtv.vercel.app/api/?id=7432 
145 IN: UTV Bindass = https://ninjatv-redtv.vercel.app/api/?id=7433 
146 IN: News18 News UP = https://ninjatv-redtv.vercel.app/api/?id=7435 
147 IN: News18 India (News) = https://ninjatv-redtv.vercel.app/api/?id=7436 
148 IN: NDTV Profit (news) = https://ninjatv-redtv.vercel.app/api/?id=7437 
149 IN: Nick+ FHD = https://ninjatv-redtv.vercel.app/api/?id=7438 
150 IN: Zee Hindustan = https://ninjatv-redtv.vercel.app/api/?id=7720 
151 BD: Star Jalsa (HD) = https://ninjatv-redtv.vercel.app/api/?id=8540 
152 Telugu: STAR MAA MOVIES HD = https://ninjatv-redtv.vercel.app/api/?id=9015 
153 Telugu: Zee Cinemalu HD = https://ninjatv-redtv.vercel.app/api/?id=9016 
154 Telugu: Etv HD = https://ninjatv-redtv.vercel.app/api/?id=9017 
155 TM: KALAIGNAR TV = https://ninjatv-redtv.vercel.app/api/?id=9018 
156 TM: ADITYA TV = https://ninjatv-redtv.vercel.app/api/?id=9019 
157 TM: VASANTH TV = https://ninjatv-redtv.vercel.app/api/?id=9020 
158 TM: J MOVIES = https://ninjatv-redtv.vercel.app/api/?id=9022 
159 TM: MALAI MURASU TV = https://ninjatv-redtv.vercel.app/api/?id=9023 
160 TM: RAJ MUSIX TAMIL = https://ninjatv-redtv.vercel.app/api/?id=9024 
161 Telugu: GEMINI COMEDY HD = https://ninjatv-redtv.vercel.app/api/?id=9042 
162 Telugu: STAR MAA GOLD = https://ninjatv-redtv.vercel.app/api/?id=9043 
163 Telugu: GEMINI LIFE HD = https://ninjatv-redtv.vercel.app/api/?id=9044 
164 Telugu: ETV Cinema HD = https://ninjatv-redtv.vercel.app/api/?id=9045 
165 Telugu: ETV AndhraPradesh = https://ninjatv-redtv.vercel.app/api/?id=9046 
166 Telugu: TV9 NEWS HD = https://ninjatv-redtv.vercel.app/api/?id=9047 
167 Telugu: Sakshi TV (News) = https://ninjatv-redtv.vercel.app/api/?id=9048 
168 Telugu: T News HD = https://ninjatv-redtv.vercel.app/api/?id=9049 
169 Telugu: ETV Telangana = https://ninjatv-redtv.vercel.app/api/?id=9050 
170 Telugu: ETV Life = https://ninjatv-redtv.vercel.app/api/?id=9052 
171 Telugu: ETV Abhiruchi = https://ninjatv-redtv.vercel.app/api/?id=9053 
172 Telugu: SVBC HD = https://ninjatv-redtv.vercel.app/api/?id=9054 
173 IN:Republic TV (English) = https://ninjatv-redtv.vercel.app/api/?id=9056 
174 IN: 9X Jalwa HD = https://ninjatv-redtv.vercel.app/api/?id=9057 
175 IN: Republic TV HD = https://ninjatv-redtv.vercel.app/api/?id=9080 
176 IN: CNBC Awaaz (News) HD = https://ninjatv-redtv.vercel.app/api/?id=9116 
177 IN: CNBC Tv 18 (News) = https://ninjatv-redtv.vercel.app/api/?id=9117 
178 IN: & PRIVE (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9379 
179 IN: SONY PIX (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9381 
180 IN: MN+ (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9383 
181 IN: STAR MOVIES (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9384 
182 IN: STAR Life (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9387 
183 IN: TLC (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9388 
184 IN: ZEE Cafe (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9389 
185 IN: Colors INFINITY (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9390 
186 IN: ANIMAL PLANET (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9391 
187 IN: HISTORY TV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9392 
188 IN: DISCOVERY (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9393 
189 IN: National GEO (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9394 
190 IN: NAT Geo Wild (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9395 
191 IN: Sony BBC EARTH (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9396 
192 IN: Star Sports Select 1 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9400 
193 IN: Star Sports Select 2 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9401 
194 IN: Sony Ten 1 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9402 
195 IN: Sony Ten 2 (4K) = https://ninjatv-redtv.vercel.app/api/?id=9403 
196 IN: Sony Ten 3 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9404 
197 Kand:Ayush TV HD = https://ninjatv-redtv.vercel.app/api/?id=9439 
198 Kand:Colors Kannada Cinema HD = https://ninjatv-redtv.vercel.app/api/?id=9440 
199 Kand: News18 Kannada HD = https://ninjatv-redtv.vercel.app/api/?id=9441 
200 Kand: Prajaa TV HD = https://ninjatv-redtv.vercel.app/api/?id=9442 
201 Kand: Public_TV = https://ninjatv-redtv.vercel.app/api/?id=9443 
202 Kand: Suvarna News HD = https://ninjatv-redtv.vercel.app/api/?id=9444 
203 Kand: TV5 News HD = https://ninjatv-redtv.vercel.app/api/?id=9445 
204 Kand: Tv9 Kannada (News) = https://ninjatv-redtv.vercel.app/api/?id=9446 
205 Kand: UDAYA COMEDY FHD = https://ninjatv-redtv.vercel.app/api/?id=9447 
206 Kand: UDAYA MOVIES FHD = https://ninjatv-redtv.vercel.app/api/?id=9448 
207 Kand: UDAYA TV FHD = https://ninjatv-redtv.vercel.app/api/?id=9449 
208 Kand: UDAYA TV FHD = https://ninjatv-redtv.vercel.app/api/?id=9450 
209 Kand: UDAYA TV FHD-(usa) = https://ninjatv-redtv.vercel.app/api/?id=9451 
210 Kand: ZEE Picchar (4K) = https://ninjatv-redtv.vercel.app/api/?id=9452 
211 Kand: Zee Kannada HD = https://ninjatv-redtv.vercel.app/api/?id=9453 
212 IN: ET Now = https://ninjatv-redtv.vercel.app/api/?id=9485 
213 IN: E24 = https://ninjatv-redtv.vercel.app/api/?id=9487 
214 IN: Zoom = https://ninjatv-redtv.vercel.app/api/?id=9488 
215 IN: Zee MP (News) = https://ninjatv-redtv.vercel.app/api/?id=9725 
216 IN: SONY HD = https://ninjatv-redtv.vercel.app/api/?id=9885 
217 IN: 1st India (News) = https://ninjatv-redtv.vercel.app/api/?id=9974 
218 IN: Food Food = https://ninjatv-redtv.vercel.app/api/?id=9975 
219 IN: CNN_NEWS_18 (NEWS) = https://ninjatv-redtv.vercel.app/api/?id=9976 
220 IN: SONY TEN 5 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=17565 
221 Kids: PAW Patrol FHD = https://ninjatv-redtv.vercel.app/api/?id=18455 
222 Kids: Hungama = https://ninjatv-redtv.vercel.app/api/?id=18456 
223 Kids: Nick Pakistan = https://ninjatv-redtv.vercel.app/api/?id=18457 
224 GUJ:ABP Asmita HD = https://ninjatv-redtv.vercel.app/api/?id=5832 
225 GuJ:Zee 24 Kalak HD = https://ninjatv-redtv.vercel.app/api/?id=5833 
226 GUJ:SANSKAR TV HD = https://ninjatv-redtv.vercel.app/api/?id=5834 
227 GUJ:NEWS 18 GUJARATI HD = https://ninjatv-redtv.vercel.app/api/?id=5836 
228 GUJ: TV9 GUJARATI HD = https://ninjatv-redtv.vercel.app/api/?id=5837 
229 GUJ:CNBC Bajar GUJRATI HD = https://ninjatv-redtv.vercel.app/api/?id=5838 
230 Guj: GSTV HD = https://ninjatv-redtv.vercel.app/api/?id=5840 
231 Guj:Sandesh News HD = https://ninjatv-redtv.vercel.app/api/?id=5844 
232 GUJ:India News Gujrat(lk) = https://ninjatv-redtv.vercel.app/api/?id=5847 
233 GUJ:Mantavya News Gujrat = https://ninjatv-redtv.vercel.app/api/?id=5848 
234 Guj:Colors Gujarati = https://ninjatv-redtv.vercel.app/api/?id=5850 
235 Guj:VTV NEWS = https://ninjatv-redtv.vercel.app/api/?id=5853 
236 US: Universal Kids = https://ninjatv-redtv.vercel.app/api/?id=5855 
237 Marathi: Sony Marathi HD = https://ninjatv-redtv.vercel.app/api/?id=5856 
238 Marathi:9x Jhakaas  HD = https://ninjatv-redtv.vercel.app/api/?id=5858 
239 Marathi:ABP Majha = https://ninjatv-redtv.vercel.app/api/?id=5859 
240 Marathi:DD Sahyadri HD(lk) = https://ninjatv-redtv.vercel.app/api/?id=5860 
241 Marathi:Fakt marathi = https://ninjatv-redtv.vercel.app/api/?id=5861 
242 Marathi:News18 Lokmat = https://ninjatv-redtv.vercel.app/api/?id=5862 
243 Marathi:TV9 Marathi HD = https://ninjatv-redtv.vercel.app/api/?id=5863 
244 Marathi:Sangeet Marathi(lk) = https://ninjatv-redtv.vercel.app/api/?id=5864 
245 Marathi:Zee Yuva = https://ninjatv-redtv.vercel.app/api/?id=5866 
246 Marathi:Zee Marathi HD = https://ninjatv-redtv.vercel.app/api/?id=5867 
247 Marathi:Zee  24 Taas = https://ninjatv-redtv.vercel.app/api/?id=5868 
248 Marathi: ZEE Marathi (usa) = https://ninjatv-redtv.vercel.app/api/?id=5869 
249 Marathi:Zee Talkies HD = https://ninjatv-redtv.vercel.app/api/?id=5871 
250 Marathi:Colors:Marathi = https://ninjatv-redtv.vercel.app/api/?id=5872 
251 Marathi:Star Parvaha FHD = https://ninjatv-redtv.vercel.app/api/?id=5874 
252 IN: MANORANJAN TV = https://ninjatv-redtv.vercel.app/api/?id=2433 
253 IN: MANORANJAN MOVIES = https://ninjatv-redtv.vercel.app/api/?id=2434 
254 IN: NEWS 18 INDIA = https://ninjatv-redtv.vercel.app/api/?id=2436 
255 PB: 5aabTV kabaddi = https://ninjatv-redtv.vercel.app/api/?id=1903 
256 PB: 5aabTV Gurbani HD = https://ninjatv-redtv.vercel.app/api/?id=1904 
257 IN: Pogo_Hindi = https://ninjatv-redtv.vercel.app/api/?id=1918 
258 IN: SONY HD = https://ninjatv-redtv.vercel.app/api/?id=144 
259 IN: SONY TV HD = https://ninjatv-redtv.vercel.app/api/?id=224 
260 IN: SONY (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9365 
261 IN: STAR PLUS HD = https://ninjatv-redtv.vercel.app/api/?id=221 
262 IN: STAR PLUS FHD = https://ninjatv-redtv.vercel.app/api/?id=167 
263 IN: STAR PLUS (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9366 
264 IN: COLOR HD = https://ninjatv-redtv.vercel.app/api/?id=219 
265 IN: COLORS FHD = https://ninjatv-redtv.vercel.app/api/?id=195 
266 IN: Colors (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9370 
267 IN: STAR BHARAT HD = https://ninjatv-redtv.vercel.app/api/?id=199 
268 IN: STAR BHARAT (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9367 
269 IN: SONY SAB HD = https://ninjatv-redtv.vercel.app/api/?id=145 
270 IN: SAB (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9368 
271 IN: & TV HD = https://ninjatv-redtv.vercel.app/api/?id=232 
272 IN: &TV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9369 
273 IN: ZEE TV HD = https://ninjatv-redtv.vercel.app/api/?id=161 
274 IN: ZEE TV FHD = https://ninjatv-redtv.vercel.app/api/?id=220 
275 IN: ZEE TV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9371 
276 IN: SONY MAX HD = https://ninjatv-redtv.vercel.app/api/?id=151 
277 IN: SONY MAX (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9373 
278 IN: STAR GOLD HD = https://ninjatv-redtv.vercel.app/api/?id=194 
279 IN: Star GOLD (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9375 
280 IN: STAR GOLD 2 (4K) = https://ninjatv-redtv.vercel.app/api/?id=157081 
281 IN: STAR GOLD SELECT HD = https://ninjatv-redtv.vercel.app/api/?id=210 
282 IN: Star Gold SELECT (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9376 
283 IN: ZEE CINEMA HD = https://ninjatv-redtv.vercel.app/api/?id=230 
284 IN: & PICTURES HD = https://ninjatv-redtv.vercel.app/api/?id=231 
285 IN: CINEPLEX HD = https://ninjatv-redtv.vercel.app/api/?id=867 
286 IN: Colors Cineplex (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9378 
287 IN: COLORS CINEPLEX SUPERHITS = https://ninjatv-redtv.vercel.app/api/?id=172368 
288 IN: Colors Cineplex Bollywood = https://ninjatv-redtv.vercel.app/api/?id=37074 
289 IN: MINIPLEX (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23427 
290 IN: &XPLOR (4K) = https://ninjatv-redtv.vercel.app/api/?id=4082 
291 IN: & XPLOR (FHD) = https://ninjatv-redtv.vercel.app/api/?id=20648 
292 IN: MOVIES ACTIVE HD D2H = https://ninjatv-redtv.vercel.app/api/?id=7336 
293 IN: MBC BOLLYWOOD (FHD) = https://ninjatv-redtv.vercel.app/api/?id=20512 
294 IN: B FLIX = https://ninjatv-redtv.vercel.app/api/?id=4081 
295 IN: STAR MOVIES HD = https://ninjatv-redtv.vercel.app/api/?id=979 
296 IN: STAR MOVIES SELECT HD = https://ninjatv-redtv.vercel.app/api/?id=218 
297 IN: SONY PIX HD = https://ninjatv-redtv.vercel.app/api/?id=147 
298 IN: MN PLUS = https://ninjatv-redtv.vercel.app/api/?id=178 
299 IN: MNX HD = https://ninjatv-redtv.vercel.app/api/?id=191 
300 IN: & PRIVE HD = https://ninjatv-redtv.vercel.app/api/?id=201 
301 IN: & FLIX HD = https://ninjatv-redtv.vercel.app/api/?id=253 
302 IN: HBO 2 HD = https://ninjatv-redtv.vercel.app/api/?id=185 
303 IN: COLORS INFINITY HD = https://ninjatv-redtv.vercel.app/api/?id=187 
304 IN: ZEECAFE HD = https://ninjatv-redtv.vercel.app/api/?id=196 
305 IN: FYI TV18 HD = https://ninjatv-redtv.vercel.app/api/?id=152 
306 IN: STAR LIFE = https://ninjatv-redtv.vercel.app/api/?id=2115 
307 IN: HISTORY HD = https://ninjatv-redtv.vercel.app/api/?id=180 
308 IN: HISTORY 18 (HINDI) = https://ninjatv-redtv.vercel.app/api/?id=5252 
309 IN: DISCOVERY WORLD HD = https://ninjatv-redtv.vercel.app/api/?id=156 
310 IN: NATIONAL GEOGRAPHIC INDIA = https://ninjatv-redtv.vercel.app/api/?id=7342 
311 IN: NATIONAL GEOGRAPHIC = https://ninjatv-redtv.vercel.app/api/?id=7343 
312 IN: NATGEO WILD HD = https://ninjatv-redtv.vercel.app/api/?id=7344 
313 IN: SONY BBC EARTH HD (ENG) = https://ninjatv-redtv.vercel.app/api/?id=174 
314 IN: SONY BBC EARTH HD (HINDI) = https://ninjatv-redtv.vercel.app/api/?id=7721 
315 IN: SONY BBC EARTH HD (ENGLISH) = https://ninjatv-redtv.vercel.app/api/?id=190 
316 IN: TRAVEL XP HD (HINDI) = https://ninjatv-redtv.vercel.app/api/?id=181 
317 IN: TRAVEL XP HD = https://ninjatv-redtv.vercel.app/api/?id=1623 
318 IN: ANIMAL PLANET HD = https://ninjatv-redtv.vercel.app/api/?id=182 
319 IN: MTV BEATS HD = https://ninjatv-redtv.vercel.app/api/?id=153 
320 IN: MTV HD PLUS = https://ninjatv-redtv.vercel.app/api/?id=4029 
321 MY: ASIANET (4K). = https://ninjatv-redtv.vercel.app/api/?id=98891 
322 MY: Asianet HD = https://ninjatv-redtv.vercel.app/api/?id=166 
323 MY: ASIANET (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23307 
324 MY: SURYA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98888 
325 MY: Surya_HD = https://ninjatv-redtv.vercel.app/api/?id=193 
326 MY: SURYA (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23309 
327 MY: MAZHAVIL (4K). = https://ninjatv-redtv.vercel.app/api/?id=98912 
328 MY: MANORAMA NEWS _HD = https://ninjatv-redtv.vercel.app/api/?id=226 
329 MY: MAZHAVIL (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23311 
330 MY: ZEE KERALAM (4K). = https://ninjatv-redtv.vercel.app/api/?id=98895 
331 MY: ZEE KERALAM = https://ninjatv-redtv.vercel.app/api/?id=4226 
332 MY: ZEE KERALAM (FHD) = https://ninjatv-redtv.vercel.app/api/?id=10094 
333 MY: ZEE KERALAM (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23310 
334 MY: Flowers TV = https://ninjatv-redtv.vercel.app/api/?id=9030 
335 MY: Asianet Movies (4K) = https://ninjatv-redtv.vercel.app/api/?id=177842 
336 MY: Asianet Movies SD = https://ninjatv-redtv.vercel.app/api/?id=9031 
337 Malayalam: Surya Movies HD = https://ninjatv-redtv.vercel.app/api/?id=9034 
338 MY: Amrita TV = https://ninjatv-redtv.vercel.app/api/?id=9028 
339 MY: Kairali HD = https://ninjatv-redtv.vercel.app/api/?id=9026 
340 MY: Asianet Plus = https://ninjatv-redtv.vercel.app/api/?id=9027 
341 MY: SURYA MUSIC = https://ninjatv-redtv.vercel.app/api/?id=9038 
342 MY: Raj Music Malayalam = https://ninjatv-redtv.vercel.app/api/?id=245 
343 MY: SURYA COMEDY HD = https://ninjatv-redtv.vercel.app/api/?id=9033 
344 MY: REPORTER News HD = https://ninjatv-redtv.vercel.app/api/?id=166615 
345 MY: REPORTER News = https://ninjatv-redtv.vercel.app/api/?id=56032 
346 MY: News 24 Malayalam HD = https://ninjatv-redtv.vercel.app/api/?id=166612 
347 MY: News 24 Malayalam = https://ninjatv-redtv.vercel.app/api/?id=248 
348 MY: Media One HD = https://ninjatv-redtv.vercel.app/api/?id=169796 
349 MY: Media One = https://ninjatv-redtv.vercel.app/api/?id=9035 
350 MY: Mathrubhumi News HD = https://ninjatv-redtv.vercel.app/api/?id=169786 
351 MY: Mathrubhumi News = https://ninjatv-redtv.vercel.app/api/?id=9032 
352 MY: Asianet News HD = https://ninjatv-redtv.vercel.app/api/?id=166605 
353 MY : Asianet News = https://ninjatv-redtv.vercel.app/api/?id=165 
354 MY: Kairali News HD = https://ninjatv-redtv.vercel.app/api/?id=169797 
355 MY: Kairali News = https://ninjatv-redtv.vercel.app/api/?id=85929 
356 MY: AsianetMiddleEast = https://ninjatv-redtv.vercel.app/api/?id=85926 
357 MY: Kairali We = https://ninjatv-redtv.vercel.app/api/?id=150128 
358 MY: Manorama News HD = https://ninjatv-redtv.vercel.app/api/?id=169776 
359 MY: Manorama News Malayalam = https://ninjatv-redtv.vercel.app/api/?id=249 
360 MY: News 18 Kerala HD = https://ninjatv-redtv.vercel.app/api/?id=169837 
361 MY: News 18 Kerala = https://ninjatv-redtv.vercel.app/api/?id=9036 
362 MY: DD Malayalam = https://ninjatv-redtv.vercel.app/api/?id=4051 
363 MY: Raj News Malayalam = https://ninjatv-redtv.vercel.app/api/?id=9037 
364 MY: JeevanTV = https://ninjatv-redtv.vercel.app/api/?id=85920 
365 MY: Kappa_TV = https://ninjatv-redtv.vercel.app/api/?id=9039 
366 MY: SAFARI TV = https://ninjatv-redtv.vercel.app/api/?id=4067 
367 MY: Kaumudy TV HD = https://ninjatv-redtv.vercel.app/api/?id=169822 
368 MY: Kaumudy_TV = https://ninjatv-redtv.vercel.app/api/?id=169 
369 MY: Jai Hind tv HD = https://ninjatv-redtv.vercel.app/api/?id=169798 
370 MY: Jai Hind_tv = https://ninjatv-redtv.vercel.app/api/?id=172 
371 MY: WE TV = https://ninjatv-redtv.vercel.app/api/?id=53199 
372 MY: Janam TV HD = https://ninjatv-redtv.vercel.app/api/?id=169807 
373 MY: Janam TV = https://ninjatv-redtv.vercel.app/api/?id=9029 
374 MY: Kochu TV = https://ninjatv-redtv.vercel.app/api/?id=37450 
375 MY: KairaliArabia = https://ninjatv-redtv.vercel.app/api/?id=85928 
376 MY: Shalom HD = https://ninjatv-redtv.vercel.app/api/?id=169838 
377 MY: Shalom = https://ninjatv-redtv.vercel.app/api/?id=9040 
378 MY: Power Vesion HD = https://ninjatv-redtv.vercel.app/api/?id=169867 
379 MY: Power Vesion Malayalam = https://ninjatv-redtv.vercel.app/api/?id=252 
380 MY: Kerala Vision News HD = https://ninjatv-redtv.vercel.app/api/?id=169850 
381 MY: GoodnessTV = https://ninjatv-redtv.vercel.app/api/?id=85915 
382 IN: Good news TV = https://ninjatv-redtv.vercel.app/api/?id=9041 
383 MY: Harvest24x7 = https://ninjatv-redtv.vercel.app/api/?id=85917 
384 MY: Magnavision TV = https://ninjatv-redtv.vercel.app/api/?id=127305 
385 MY: Sakhi Tv = https://ninjatv-redtv.vercel.app/api/?id=85922 
386 MY: DarshanaTV = https://ninjatv-redtv.vercel.app/api/?id=85924 
387 MY: Pulari Tv HD = https://ninjatv-redtv.vercel.app/api/?id=131454 
388 Malayalam: Nicklodean Sonic = https://ninjatv-redtv.vercel.app/api/?id=127762 
389 Kand:  Colors Kannada HD = https://ninjatv-redtv.vercel.app/api/?id=162 
390 Kand:  Colors Super = https://ninjatv-redtv.vercel.app/api/?id=163 
391 Kand: Udaya TV HD = https://ninjatv-redtv.vercel.app/api/?id=164 
392 Telugu: TV 5 News = https://ninjatv-redtv.vercel.app/api/?id=170 
393 Telugu: STAR MAA TV HD = https://ninjatv-redtv.vercel.app/api/?id=168 
394 PB: PTC PUNJABI = https://ninjatv-redtv.vercel.app/api/?id=171 
395 BD: CHANNEL I = https://ninjatv-redtv.vercel.app/api/?id=34665 
396 BD: ZEE BANGLA HD = https://ninjatv-redtv.vercel.app/api/?id=435 
397 BD: BANGLA VISION = https://ninjatv-redtv.vercel.app/api/?id=426 
398 BD_NTV Bangla HD = https://ninjatv-redtv.vercel.app/api/?id=424 
399 BD_RTV HD = https://ninjatv-redtv.vercel.app/api/?id=401 
400 BD:Ekattor tv = https://ninjatv-redtv.vercel.app/api/?id=428 
401 BD_Somoy TV = https://ninjatv-redtv.vercel.app/api/?id=422 
402 BD_Independent TV = https://ninjatv-redtv.vercel.app/api/?id=423 
403 BD_DBC HD = https://ninjatv-redtv.vercel.app/api/?id=420 
404 BD:DEEPTO TV = https://ninjatv-redtv.vercel.app/api/?id=1331 
405 BD: News 24 Tv = https://ninjatv-redtv.vercel.app/api/?id=3810 
406 BD: Nagorik Tv HD = https://ninjatv-redtv.vercel.app/api/?id=3802 
407 BD : Star Jalsa HD = https://ninjatv-redtv.vercel.app/api/?id=198 
408 IN: Colors_Bengali_HD = https://ninjatv-redtv.vercel.app/api/?id=183 
409 BD : SUN Bangla (4K) = https://ninjatv-redtv.vercel.app/api/?id=3753 
410 BD: ABP Ananda = https://ninjatv-redtv.vercel.app/api/?id=5436 
411 BD_Aakaash Aath = https://ninjatv-redtv.vercel.app/api/?id=396 
412 BD: TIME TV = https://ninjatv-redtv.vercel.app/api/?id=2882 
413 IN: Zee Anmol = https://ninjatv-redtv.vercel.app/api/?id=203 
414 IN: Sony_Yay_Hindi = https://ninjatv-redtv.vercel.app/api/?id=204 
415 IN:  Nick_Hindi = https://ninjatv-redtv.vercel.app/api/?id=205 
416 IN: Nick_Junior = https://ninjatv-redtv.vercel.app/api/?id=206 
417 IN: sonic_Hindi = https://ninjatv-redtv.vercel.app/api/?id=207 
418 IN: Discovery_Kids_1 = https://ninjatv-redtv.vercel.app/api/?id=208 
419 Telugu: Gemini_Movies_HD = https://ninjatv-redtv.vercel.app/api/?id=212 
420 Telugu: Gemini_Music_HD = https://ninjatv-redtv.vercel.app/api/?id=213 
421 Telugu: Gemini_TV_HD = https://ninjatv-redtv.vercel.app/api/?id=214 
422 Telugu: Sony_BBC_Earth_HD_Telugu = https://ninjatv-redtv.vercel.app/api/?id=223 
423 PB :  Pitaara = https://ninjatv-redtv.vercel.app/api/?id=227 
424 Telugu:  V6_News = https://ninjatv-redtv.vercel.app/api/?id=228 
425 Telugu:  Sri_Venkateshwar_Bhakti = https://ninjatv-redtv.vercel.app/api/?id=233 
426 Telugu:  ABN_Andhra_Jyothi = https://ninjatv-redtv.vercel.app/api/?id=234 
427 Telugu: NTV TELUGU = https://ninjatv-redtv.vercel.app/api/?id=235 
428 Kand:  Suvarna_News = https://ninjatv-redtv.vercel.app/api/?id=236 
429 IN : Colors Rishtey TV = https://ninjatv-redtv.vercel.app/api/?id=241 
430 Telugu: ETV Plus = https://ninjatv-redtv.vercel.app/api/?id=242 
431 IN: Raj Music Telugu = https://ninjatv-redtv.vercel.app/api/?id=243 
432 Telugu: Vissa TV = https://ninjatv-redtv.vercel.app/api/?id=244 
433 IN: NDTV 24x7 = https://ninjatv-redtv.vercel.app/api/?id=247 
434 IN: Food Food = https://ninjatv-redtv.vercel.app/api/?id=250 
435 IN: SONY (4K). = https://ninjatv-redtv.vercel.app/api/?id=98854 
436 IN: SONY SAB (4K). = https://ninjatv-redtv.vercel.app/api/?id=98853 
437 IN: COLORS (4K). = https://ninjatv-redtv.vercel.app/api/?id=98851 
438 IN: STAR PLUS (4K). = https://ninjatv-redtv.vercel.app/api/?id=98849 
439 IN: STAR BHARAT (4K). = https://ninjatv-redtv.vercel.app/api/?id=98855 
440 IN: &TV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98852 
441 IN: ZEETV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98850 
442 IN: SONY MAX (4K). = https://ninjatv-redtv.vercel.app/api/?id=98857 
443 IN: &PICTURE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98856 
444 IN: STAR GOLD (4K). = https://ninjatv-redtv.vercel.app/api/?id=98858 
445 IN: STAR GOLD SELECT (4K). = https://ninjatv-redtv.vercel.app/api/?id=98859 
446 IN: ZEE CINEMA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98860 
447 IN: Colors Cineplex (4K). = https://ninjatv-redtv.vercel.app/api/?id=98908 
448 IN: STAR MOVIE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98842 
449 IN: STAR MOVIE SELECT (4K). = https://ninjatv-redtv.vercel.app/api/?id=98843 
450 IN: &PRIVE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98840 
451 IN: &FLIX (4K). = https://ninjatv-redtv.vercel.app/api/?id=98841 
452 IN: SONY PIX (4K). = https://ninjatv-redtv.vercel.app/api/?id=98846 
453 IN: MN+ (4K). = https://ninjatv-redtv.vercel.app/api/?id=98847 
454 IN: ZEE CAFE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98848 
455 IN: Colors INFINITY (4K). = https://ninjatv-redtv.vercel.app/api/?id=98879 
456 IN: STAR LIFE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98876 
457 IN: AXN (4K). = https://ninjatv-redtv.vercel.app/api/?id=98915 
458 IN: TLC (4K). = https://ninjatv-redtv.vercel.app/api/?id=98878 
459 IN: DISCOVERY (4K). = https://ninjatv-redtv.vercel.app/api/?id=98872 
460 IN: ANIMAL PLANET (4K). = https://ninjatv-redtv.vercel.app/api/?id=98873 
461 IN: National GEO (4K). = https://ninjatv-redtv.vercel.app/api/?id=98874 
462 IN: NAT Geo Wild (4K). = https://ninjatv-redtv.vercel.app/api/?id=98875 
463 IN: Sony BBC EARTH (4K). = https://ninjatv-redtv.vercel.app/api/?id=98871 
464 IN: HISTORY TV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98877 
465 IN: NICK (4K). = https://ninjatv-redtv.vercel.app/api/?id=98880 
466 BD: ZEE BANGLA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98881 
467 BD: COLORS BANGLA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98882 
468 BD: JALSHA MOVIES (4K). = https://ninjatv-redtv.vercel.app/api/?id=98884 
469 BD: STAR JALSHA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98883 
470 TG: BIGG BOSS 24X7 FHD = https://ninjatv-redtv.vercel.app/api/?id=393899 
471 BIGG BOSS 24X7 HD = https://ninjatv-redtv.vercel.app/api/?id=393900 
472 Telugu: ETV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98885 
473 Telugu: STAR-MAA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98886 
474 Telugu: STAR-MAA-MOVIE (4K). = https://ninjatv-redtv.vercel.app/api/?id=98887 
475 Telugu: GEMINI (4K). = https://ninjatv-redtv.vercel.app/api/?id=98892 
476 Telugu: ZEE-TELUGU (4K). = https://ninjatv-redtv.vercel.app/api/?id=98894 
477 Telugu: ZEE-CINEMALU (4K). = https://ninjatv-redtv.vercel.app/api/?id=98896 
478 Marathi: STAR-PRAVAH (4K). = https://ninjatv-redtv.vercel.app/api/?id=98902 
479 Marathi: ZEE Marathi (4K). = https://ninjatv-redtv.vercel.app/api/?id=98903 
480 Marathi: ZEE TALKIES (4K). = https://ninjatv-redtv.vercel.app/api/?id=98904 
481 MARATHI: COLORS MARATHI (4K). = https://ninjatv-redtv.vercel.app/api/?id=98905 
482 Kannada: UDAYA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98889 
483 Kannada: STAR-SUVARNA (4k). = https://ninjatv-redtv.vercel.app/api/?id=98901 
484 Kannada: ZEE-KANNADA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98890 
485 Kannada: COLORS_KANNADA (4K). = https://ninjatv-redtv.vercel.app/api/?id=98907 
486 IN: STAR SPORTS 1 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98864 
487 IN: STAR SPORTS 2 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98865 
488 IN: STAR SPORTS 1 HINDI (4K). = https://ninjatv-redtv.vercel.app/api/?id=98866 
489 IN: STAR SPORTS SELECT 1 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98867 
490 IN: START SPORTS SELECT 2 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98868 
491 IN: TEN 1 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98861 
492 IN: TEN 2 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98862 
493 IN: TEN 3 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98863 
494 IN: SONY TEN 5 (4K). = https://ninjatv-redtv.vercel.app/api/?id=98870 
495 CRI: STARZPLAY CricLife 1 (FHD) = https://ninjatv-redtv.vercel.app/api/?id=122979 
496 CRI: STARZPLAY CricLife 2 FHD = https://ninjatv-redtv.vercel.app/api/?id=122980 
497 CRI: FOX CRICKET 501 = https://ninjatv-redtv.vercel.app/api/?id=1856 
498 CRI: SUPER SPORTS CRICKET (4K) = https://ninjatv-redtv.vercel.app/api/?id=158442 
499 CRI: SUPER SPORTS (CRICKET) = https://ninjatv-redtv.vercel.app/api/?id=2496 
500 CRI: SKY SPORTS CRICKET = https://ninjatv-redtv.vercel.app/api/?id=12 
501 CRI: SKY SPORTS CRICKET (4K) = https://ninjatv-redtv.vercel.app/api/?id=23566 
502 CRI: SKY SPORTS CRICKET (4K). = https://ninjatv-redtv.vercel.app/api/?id=114479 
503 CRI: SKY SPORTS CRICKET (4K) = https://ninjatv-redtv.vercel.app/api/?id=124269 
504 CRI:ASTRO CRICKET HD = https://ninjatv-redtv.vercel.app/api/?id=2494 
505 CRI: WILLOW CRICKET = https://ninjatv-redtv.vercel.app/api/?id=215 
506 CRI: WILLOW CRICKET. = https://ninjatv-redtv.vercel.app/api/?id=23943 
507 CRI: WILLOW CRICKET XTRA = https://ninjatv-redtv.vercel.app/api/?id=5040 
508 CRI: TNT Sports 3 FHD = https://ninjatv-redtv.vercel.app/api/?id=148090 
509 CRI: PTV SPORTS = https://ninjatv-redtv.vercel.app/api/?id=89 
510 CRI: PTV SPORTS (4K) = https://ninjatv-redtv.vercel.app/api/?id=61674 
511 CRI: A Sports ARY = https://ninjatv-redtv.vercel.app/api/?id=43444 
512 CRI: A SPORTS ARY (4K) = https://ninjatv-redtv.vercel.app/api/?id=43447 
513 CRI: GEO SUPER = https://ninjatv-redtv.vercel.app/api/?id=101 
514 CRI: TEN SPORTS = https://ninjatv-redtv.vercel.app/api/?id=98 
515 CRI: TEN CRICKET (FHD) = https://ninjatv-redtv.vercel.app/api/?id=196594 
516 CRI: TEN CRICKET = https://ninjatv-redtv.vercel.app/api/?id=9886 
517 CRI: STAR SPORT 1 HD = https://ninjatv-redtv.vercel.app/api/?id=148 
518 CRI: Star Sport-1  (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9397 
519 CRI: STAR SPORTS 1 (4K) = https://ninjatv-redtv.vercel.app/api/?id=124281 
520 CRI: STAR SPORTS 2 HD = https://ninjatv-redtv.vercel.app/api/?id=239 
521 CRI: Star Sport-2  (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9398 
522 CRI: STAR SPORTS 2 (4K) = https://ninjatv-redtv.vercel.app/api/?id=124284 
523 CRI: STAR SPORTS HINDI HD = https://ninjatv-redtv.vercel.app/api/?id=211 
524 CRI: Star Sport 1 HINDI (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9399 
525 CRI: STAR SPORTS 1 HINDI (4K) = https://ninjatv-redtv.vercel.app/api/?id=124287 
526 CRI: STAR SPORTS SELECT 1 HD = https://ninjatv-redtv.vercel.app/api/?id=238 
527 CRI: STAR SPORTS SELECT 2 HD = https://ninjatv-redtv.vercel.app/api/?id=148801 
528 CRI: STAR SPORTS TAMIL 1 HD = https://ninjatv-redtv.vercel.app/api/?id=9722 
529 CRI: STAR SPORTS TELUGU 1 (4K) = https://ninjatv-redtv.vercel.app/api/?id=177843 
530 CRI: STAR SPORTS 3 = https://ninjatv-redtv.vercel.app/api/?id=1080 
531 CRI: T SPORTS FHD = https://ninjatv-redtv.vercel.app/api/?id=18452 
532 CRI: T SPORTS. = https://ninjatv-redtv.vercel.app/api/?id=130714 
533 CRI: RTA Sports = https://ninjatv-redtv.vercel.app/api/?id=1039 
534 CRI: SONY TEN 1 HD = https://ninjatv-redtv.vercel.app/api/?id=154 
535 CRI: SONY Ten 2 HD. = https://ninjatv-redtv.vercel.app/api/?id=31314 
536 CRI: SONY TEN 3 HD = https://ninjatv-redtv.vercel.app/api/?id=146 
537 CRI: SONY TEN 4 (4K) = https://ninjatv-redtv.vercel.app/api/?id=29469 
538 CRI: SONY 5 HD = https://ninjatv-redtv.vercel.app/api/?id=176 
539 CRI: SONY ESPN HD = https://ninjatv-redtv.vercel.app/api/?id=155 
540 CRI: Jio Cricket HD = https://ninjatv-redtv.vercel.app/api/?id=158899 
541 CRI: Sky Sport 1 HD = https://ninjatv-redtv.vercel.app/api/?id=150854 
542 CRI: Sky Sport 3 CRICKET FHD. = https://ninjatv-redtv.vercel.app/api/?id=24018 
543 CRI: Carib SportsMax Cricket = https://ninjatv-redtv.vercel.app/api/?id=142048 
544 CRI: FLOW SPORTS = https://ninjatv-redtv.vercel.app/api/?id=34489 
545 CRI: ATN Plus Cricket = https://ninjatv-redtv.vercel.app/api/?id=85829 
546 CRI: EUROSPORTS = https://ninjatv-redtv.vercel.app/api/?id=216 
547 Tamil: VIJAY TV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98898 
548 Tamil: VIJAY TV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9969 
549 TM: STAR VIJAY INDIA FHD = https://ninjatv-redtv.vercel.app/api/?id=5916 
550 TM: STAR VIJAY HD = https://ninjatv-redtv.vercel.app/api/?id=157 
551 TM: VIJAY TV HD = https://ninjatv-redtv.vercel.app/api/?id=1634 
552 TM: STAR VIJAY HD = https://ninjatv-redtv.vercel.app/api/?id=5915 
553 TM: STAR VIJAY HD (Vip) = https://ninjatv-redtv.vercel.app/api/?id=5917 
554 Tamil: Zee Tamil (4K). = https://ninjatv-redtv.vercel.app/api/?id=98897 
555 Tamil: Zee Tamil (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9971 
556 TM: ZEE TAMIL = https://ninjatv-redtv.vercel.app/api/?id=225 
557 Tamil: Colors Tamil (4K). = https://ninjatv-redtv.vercel.app/api/?id=98911 
558 Tamil: Colors Tamil (FHD) = https://ninjatv-redtv.vercel.app/api/?id=9970 
559 TM: COLORS TAMIL HD = https://ninjatv-redtv.vercel.app/api/?id=5886 
560 TM: COLOR TAMIL HD = https://ninjatv-redtv.vercel.app/api/?id=57 
561 Tamil: KTV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98893 
562 Tamil: KTV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23318 
563 TM: KTV HD = https://ninjatv-redtv.vercel.app/api/?id=160 
564 TM: KTV HD = https://ninjatv-redtv.vercel.app/api/?id=5900 
565 TM: KTV FHD (IND) = https://ninjatv-redtv.vercel.app/api/?id=5899 
566 Tamil: SUNTV (4K). = https://ninjatv-redtv.vercel.app/api/?id=98899 
567 Tamil: SUNTV (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23320 
568 TM: SUN TV HD = https://ninjatv-redtv.vercel.app/api/?id=158 
569 TM: SUN TV HD = https://ninjatv-redtv.vercel.app/api/?id=5921 
570 TM: SUN TV HD = https://ninjatv-redtv.vercel.app/api/?id=5922 
571 TM: SUN TV HD = https://ninjatv-redtv.vercel.app/api/?id=5923 
572 Tamil: SUN-MUSIC (4K). = https://ninjatv-redtv.vercel.app/api/?id=98900 
573 Tamil: SUN-MUSIC (FHD) = https://ninjatv-redtv.vercel.app/api/?id=23321 
574 TM: SUN MUSIC HD = https://ninjatv-redtv.vercel.app/api/?id=159 
575 TM: VIJAY SUPER (4K) = https://ninjatv-redtv.vercel.app/api/?id=1614 
576 TAMIL: VIJAY MUSIC = https://ninjatv-redtv.vercel.app/api/?id=23869 
577 TAMIL: ZEE THIRAI HD = https://ninjatv-redtv.vercel.app/api/?id=181966 
578 TAMIL: Zee Thirai = https://ninjatv-redtv.vercel.app/api/?id=144636 
579 TM: SUN LIFE HD = https://ninjatv-redtv.vercel.app/api/?id=5919 
580 TM: SUN LIFE HD = https://ninjatv-redtv.vercel.app/api/?id=5918 
581 TM: SUN LIFE = https://ninjatv-redtv.vercel.app/api/?id=1612 
582 TM: SUN NEWS = https://ninjatv-redtv.vercel.app/api/?id=1613 
583 TM: SUN NEWS = https://ninjatv-redtv.vercel.app/api/?id=5924 
584 TM: POLIMER NEWS = https://ninjatv-redtv.vercel.app/api/?id=5911 
585 TM: POLIMER NEWS = https://ninjatv-redtv.vercel.app/api/?id=237 
586 TM: POLIMER TV = https://ninjatv-redtv.vercel.app/api/?id=1617 
587 TM: KAIRALI NEWS HD = https://ninjatv-redtv.vercel.app/api/?id=5896 
588 TM: Kalaignar TV News = https://ninjatv-redtv.vercel.app/api/?id=5897 
589 Tamil: Sathiyam Tv news = https://ninjatv-redtv.vercel.app/api/?id=256457 
590 TM: JAYA TV (4K) = https://ninjatv-redtv.vercel.app/api/?id=188 
591 TM: JAYA TV = https://ninjatv-redtv.vercel.app/api/?id=5895 
592 TM: JAYA MAX = https://ninjatv-redtv.vercel.app/api/?id=240 
593 TM: JAYA PLUS = https://ninjatv-redtv.vercel.app/api/?id=1615 
594 TM: JAYA MOVIES = https://ninjatv-redtv.vercel.app/api/?id=1618 
595 TM: VENDHAR TV = https://ninjatv-redtv.vercel.app/api/?id=1624 
596 TM: VENDHAR TV HD = https://ninjatv-redtv.vercel.app/api/?id=5931 
597 TM: RAJ TV HD = https://ninjatv-redtv.vercel.app/api/?id=5913 
598 TM: RAJ TV = https://ninjatv-redtv.vercel.app/api/?id=1619 
599 TM: RAJ DIGITAL PLUS = https://ninjatv-redtv.vercel.app/api/?id=1616 
600 TM: NEWS 18 TAMIL NADU HD = https://ninjatv-redtv.vercel.app/api/?id=5906 
601 TM: PUTHIYA THALAIMURAI TV HD = https://ninjatv-redtv.vercel.app/api/?id=5910 
602 TM: PUTHU YUGAmM TV = https://ninjatv-redtv.vercel.app/api/?id=5912 
603 TM: SIRIPPOLI TV = https://ninjatv-redtv.vercel.app/api/?id=5932 
604 Tamil: MEGA TV = https://ninjatv-redtv.vercel.app/api/?id=28141 
605 Tamil: MEGA 24 = https://ninjatv-redtv.vercel.app/api/?id=26163 
606 Tamil: MEGA MUSIQ = https://ninjatv-redtv.vercel.app/api/?id=26164 
607 Tamil: ISAI ARUVI = https://ninjatv-redtv.vercel.app/api/?id=26165 
608 TAMIL: MURASU TV = https://ninjatv-redtv.vercel.app/api/?id=29086 
609 Tamil: D TAMIL = https://ninjatv-redtv.vercel.app/api/?id=26162 
610 TAMIL: TRAVEL XP = https://ninjatv-redtv.vercel.app/api/?id=9972 
611 TM: SONY BBC EARTH HD = https://ninjatv-redtv.vercel.app/api/?id=222 
612 TM: NEWS 7 TAMIL HD = https://ninjatv-redtv.vercel.app/api/?id=5907 
613 TM: NEWS J = https://ninjatv-redtv.vercel.app/api/?id=5908 
614 Tamil: THANTHI TV = https://ninjatv-redtv.vercel.app/api/?id=111034 
615 Tamil : Sri Sankara TV = https://ninjatv-redtv.vercel.app/api/?id=153205 
616 TAMIL: News Tamil 24x7 = https://ninjatv-redtv.vercel.app/api/?id=160589 
617 TM: PEPPERS TV = https://ninjatv-redtv.vercel.app/api/?id=5909 
618 TM: TAMIL VISION HD = https://ninjatv-redtv.vercel.app/api/?id=5926 
619 TAMIL: SRI SHANKARA TAMIL = https://ninjatv-redtv.vercel.app/api/?id=36653 
620 TAMIL: CHITHIRAM = https://ninjatv-redtv.vercel.app/api/?id=46743 
621 KIDS: SUPER HUNGAMA = https://ninjatv-redtv.vercel.app/api/?id=66162 
622 TAMIL: NICK = https://ninjatv-redtv.vercel.app/api/?id=66163 
623 TAMIL: DISCOVERY KIDS = https://ninjatv-redtv.vercel.app/api/?id=66164 
624 TAMIL: POGO = https://ninjatv-redtv.vercel.app/api/?id=66165 
625 Tamil: Chutti Tv = https://ninjatv-redtv.vercel.app/api/?id=85931 
626 TM: 7 STAR TV HD = https://ninjatv-redtv.vercel.app/api/?id=5876 
627 TM: AASTHA TAMIL HD = https://ninjatv-redtv.vercel.app/api/?id=5877 
628 TM: ANGEL TV HD = https://ninjatv-redtv.vercel.app/api/?id=5881 
629 TM: ANGEL TV HD = https://ninjatv-redtv.vercel.app/api/?id=189 
630 TM: ANGEL TV HD = https://ninjatv-redtv.vercel.app/api/?id=5882 
631 TM: ANGEL TV HD = https://ninjatv-redtv.vercel.app/api/?id=5883 
632 TM: DD PODHIGAI = https://ninjatv-redtv.vercel.app/api/?id=5887 
633 TM: IBC COMEDY = https://ninjatv-redtv.vercel.app/api/?id=1633 
634 TM: IBC CANADA HD = https://ninjatv-redtv.vercel.app/api/?id=5890 
635 TM: IBC COMEDY = https://ninjatv-redtv.vercel.app/api/?id=5891 
636 TM: IBC MUSIC HD = https://ninjatv-redtv.vercel.app/api/?id=5892 
637 TM: IBC TAMIL HD = https://ninjatv-redtv.vercel.app/api/?id=5894 
638 TM: MADHA TV = https://ninjatv-redtv.vercel.app/api/?id=5902 
639 TM: MAKKAL TV HD = https://ninjatv-redtv.vercel.app/api/?id=5903 
640 TAMIL: MK TV = https://ninjatv-redtv.vercel.app/api/?id=37451 
641 TAMIL: MK Tunes = https://ninjatv-redtv.vercel.app/api/?id=37452 

642 devang s2 Bandish Bandits episode 1 = de to diya tha bhai 
643 devang s2 Bandish Bandits episode 2 = de to diya tha bhai 
644 devang s2 Bandish Bandits episode 3 = de to diya tha bhai 
645 devang s2 Bandish Bandits episode 4 = https://www.tgxdl.workers.dev/dl/67b8804f905d7ae32b6cad2e
646 devang s2 Bandish Bandits episode 5 = https://www.tgxdl.workers.dev/dl/67b8804e905d7ae32b6cad2d
647 devang s2 Bandish Bandits episode 6 = https://www.tgxdl.workers.dev/dl/67b8804f905d7ae32b6cad30
648 devang s2 Bandish Bandits episode 7 = https://www.tgxdl.workers.dev/dl/67b88050905d7ae32b6cad31
649 devang s2 Bandish Bandits episode 8 = https://www.tgxdl.workers.dev/dl/67b88050905d7ae32b6cad32
650 devang s2 Bandish Bandits episode 9 = chahiye bas 70 gb ki hai best of the best quality aasi quality nahi milegi kahi bhi 8k se bhi jada 
"""

# ✅ Load channels into a dictionary
def load_channels():
    channels = {}
    for line in channel_data.strip().split("\n"):
        if " = " in line:
            parts = line.strip().split(" = ")
            name = parts[0].lstrip("0123456789 ").strip()
            link = parts[1].strip()
            channels[name.lower()] = {"name": name, "link": link}
    return channels

# ✅ Shorten URLs
def shorten_url(long_url):
    try:
        shortener = pyshorteners.Shortener()
        return shortener.tinyurl.short(long_url)
    except Exception as e:
        print(f"Error shortening URL: {e}")
        return long_url

# ✅ Delete messages after 15 minutes
async def delete_after_delay(messages, selection_message=None):
    await asyncio.sleep(480)
    for msg in messages:
        try:
            await msg.edit_text("Deleted for avoiding copyright. Tap /start to restart.")
        except:
            pass
    if selection_message:
        try:
            await selection_message.edit_text("Deleted. Tap /start to restart.", reply_markup=None)
        except:
            pass


# ✅ Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pdf_path = "D:\\my creation\\roo\\z our\\cleaned_data_columns (2).pdf"

    # Send a message first
    await update.message.reply_text('''
📜 We currently have these channels available.Please check the attached list , 
find your favorate channel type name here  ,
you  will get a link , to play you need vlc player , 
copy link go to vlc player then on bottom 
there will be a button named as more tap there at there a button or place written with 
new sream click there paste link and just wait few seconds nd boom , enjoy ''')

    # Send the PDF file
    with open(pdf_path, "rb") as pdf_file:
        await update.message.reply_document(document=pdf_file, filename="Channel_List.pdf")

# ✅ Search Function
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.lower()
    channels = load_channels()

    if not channels:
        await update.message.reply_text("Error: Channel list is empty.")
        return

    matches = [channels[name] for name in channels if query in name]

    if not matches:
        await update.message.reply_text("No channels found. Try another keyword.")
        return

    buttons = [[InlineKeyboardButton(ch["name"], callback_data=ch["name"])] for ch in sorted(matches, key=lambda x: x["name"])[:20]]
    reply_markup = InlineKeyboardMarkup(buttons)

    selection_msg = await update.message.reply_text("Select channel:", reply_markup=reply_markup)
    asyncio.create_task(delete_after_delay([], selection_message=selection_msg))

# ✅ Handle Button Clicks
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    channel_name = query.data
    channels = load_channels()
    now = datetime.now(TIMEZONE)

    if channel_name.lower() not in channels:
        await query.message.reply_text("Channel not found.")
        return

    channel = channels[channel_name.lower()]

    # ✅ Check if link already exists in memory
    if channel_name in url_data:
        try:
            expiry = datetime.strptime(url_data[channel_name]["expiry"], "%Y-%m-%d %H:%M:%S")
            expiry = TIMEZONE.localize(expiry)
            if expiry > now and not url_data[channel_name]["link"].startswith("DELETED"):
                msg1 = await query.message.reply_text(f"Channel link for {channel_name}:")
                msg2 = await query.message.reply_text(url_data[channel_name]["link"])
                asyncio.create_task(delete_after_delay([msg1, msg2], selection_message=query.message))
                return
        except:
            pass

    # ✅ Generate new short URL
    short_link = shorten_url(channel["link"])

    url_data[channel_name] = {
        "link": short_link,
        "expiry": (now + timedelta(hours=17)).strftime("%Y-%m-%d %H:%M:%S")
    }

    msg1 = await query.message.reply_text(f"Channel link for {channel_name}:")
    msg2 = await query.message.reply_text(short_link)
    asyncio.create_task(delete_after_delay([msg1, msg2], selection_message=query.message))

# ✅ Auto-Refresh Expired Codes
async def refresh_codes(context: ContextTypes.DEFAULT_TYPE):
    try:
        now = datetime.now(TIMEZONE)

        for channel in url_data:
            try:
                expiry = datetime.strptime(url_data[channel]["expiry"], "%Y-%m-%d %H:%M:%S")
                expiry = TIMEZONE.localize(expiry)
                if now > expiry or now > expiry + timedelta(days=30):
                    url_data[channel]["link"] = "DELETED_" + shorten_url("https://expired-url.com")
                    url_data[channel]["expiry"] = now.strftime("%Y-%m-%d %H:%M:%S")
            except:
                url_data[channel]["link"] = "DELETED_" + shorten_url("https://expired-url.com")
                url_data[channel]["expiry"] = now.strftime("%Y-%m-%d %H:%M:%S")

        print("Codes refreshed")
    except Exception as e:
        print(f"Error refreshing codes: {e}")

# ✅ Run Bot
def main():
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, signal.SIGTERM)
            print(f"Terminated existing bot instance (PID: {old_pid})")
        except:
            pass
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))

    print("Initializing bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search))
    app.add_handler(CallbackQueryHandler(button))

    app.job_queue.run_repeating(refresh_codes, interval=17*60*60, first=17*60*60)
    
    print("Starting bot...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    try:
        signal.signal(signal.SIGINT, lambda s, f: (os.remove(PID_FILE), sys.exit(0)))
        signal.signal(signal.SIGTERM, lambda s, f: (os.remove(PID_FILE), sys.exit(0)))
        main()
    except KeyboardInterrupt:
        print("\nStopping bot...")
        os.remove(PID_FILE)
    except Exception as e:
        print(f"Fatal error: {e}")
        os.remove(PID_FILE)
        sys.exit(1)
