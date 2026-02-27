SEX
before: sex
M        5588
F         800
NaN       564
M           4
F           2
N           2
 M          1
m           1
lli         1
?           1
M x 2       1
.           1
Name: count, dtype: int64
after : sex
M    5596
F     802
O     569
Name: count, dtype: int64

=========
TYPE
I manually filled up the empty fields


before type counts:
type
Unprovoked             5157
Provoked                636
Invalid                 553
Watercraft              348
Sea Disaster            234
Questionable             26
Boat                      7
 Provoked                 2
unprovoked                1
Unconfirmed               1
Unverified                1
Under investigation       1
Name: count, dtype: int64

after type counts:
type
unprovoked      5159
provoked         638
invalid          581
watercraft       355
sea disaster     234
Name: count, dtype: int64

======
FATAL 
before counts:
fatal_y_n
N          4884
Y          1441
NaN         553
UNKNOWN      68
 N            7
F             5
M             2
Y x 2         2
n             1
Nq            1
2017          1
N             1
y             1
Name: count, dtype: int64

after counts:
fatal_y_n
N          4896
Y          1449
Unknown     622
Name: count, dtype: int64

=======
COUNTRIES
countries before normalization
 ['Brazil',
 'Australia',
 'USA',
 'US Virgin Islands',
 'New Caledonia',
 'French Polynesia',
 'Samoa',
 'Columbia',
 'Costa Rica',
 'Bahamas',
 'Puerto Rico',
 'Spain',
 'Canary Islands',
 'South Africa',
 'Vanuatu',
 'Jamaica',
 'Israel',
 'Mexico',
 'Maldives',
 'Philippines',
 'Turks and Caicos',
 'Mozambique',
 'Egypt',
 'Thailand',
 'New Zealand',
 'Hawaii',
 'Honduras',
 'Indonesia',
 'Morocco',
 'Belize',
 'Maldive Islands',
 'Tobago',
 'AUSTRALIA',
 'INDIA',
 'TRINIDAD',
 'BAHAMAS',
 'SOUTH AFRICA',
 'MEXICO',
 'NEW ZEALAND',
 'EGYPT',
 'BELIZE',
 'PHILIPPINES',
 'Coral Sea',
 'SPAIN',
 'PORTUGAL',
 'SAMOA',
 'COLOMBIA',
 'ECUADOR',
 'FRENCH POLYNESIA',
 'NEW CALEDONIA',
 'TURKS and CaICOS',
 'CUBA',
 'BRAZIL',
 'SEYCHELLES',
 'ARGENTINA',
 'FIJI',
 'MeXICO',
 'ENGLAND',
 'JAPAN',
 'INDONESIA',
 'JAMAICA',
 'MALDIVES',
 'THAILAND',
 'COLUMBIA',
 'COSTA RICA',
 'British Overseas Territory',
 'CANADA',
 'JORDAN',
 'ST KITTS / NEVIS',
 'ST MARTIN',
 'PAPUA NEW GUINEA',
 'REUNION ISLAND',
 'ISRAEL',
 'CHINA',
 'IRELAND',
 'ITALY',
 'MALAYSIA',
 'LIBYA',
 nan,
 'MAURITIUS',
 'SOLOMON ISLANDS',
 'ST HELENA, British overseas territory',
 'COMOROS',
 'REUNION',
 'UNITED KINGDOM',
 'UNITED ARAB EMIRATES',
 'CAPE VERDE',
 'Fiji',
 'DOMINICAN REPUBLIC',
 'CAYMAN ISLANDS',
 'ARUBA',
 'MOZAMBIQUE',
 'PUERTO RICO',
 'ATLANTIC OCEAN',
 'GREECE',
 'ST. MARTIN',
 'FRANCE',
 'TRINIDAD & TOBAGO',
 'KIRIBATI',
 'DIEGO GARCIA',
 'TAIWAN',
 'PALESTINIAN TERRITORIES',
 'GUAM',
 'NIGERIA',
 'TONGA',
 'SCOTLAND',
 'CROATIA',
 'SAUDI ARABIA',
 'CHILE',
 'ANTIGUA',
 'KENYA',
 'RUSSIA',
 'TURKS & CAICOS',
 'UNITED ARAB EMIRATES (UAE)',
 'AZORES',
 'SOUTH KOREA',
 'MALTA',
 'VIETNAM',
 'MADAGASCAR',
 'PANAMA',
 'SOMALIA',
 'NEVIS',
 'BRITISH VIRGIN ISLANDS',
 'NORWAY',
 'SENEGAL',
 'YEMEN',
 'GULF OF ADEN',
 'Sierra Leone',
 'ST. MAARTIN',
 'GRAND CAYMAN',
 'Seychelles',
 'LIBERIA',
 'VANUATU',
 'MEXICO ',
 'HONDURAS',
 'VENEZUELA',
 'SRI LANKA',
 ' TONGA',
 'URUGUAY',
 'MICRONESIA',
 'CARIBBEAN SEA',
 'OKINAWA',
 'TANZANIA',
 'MARSHALL ISLANDS',
 'EGYPT / ISRAEL',
 'NORTHERN ARABIAN SEA',
 'HONG KONG',
 'EL SALVADOR',
 'ANGOLA',
 'BERMUDA',
 'MONTENEGRO',
 'IRAN',
 'TUNISIA',
 'NAMIBIA',
 'NORTH ATLANTIC OCEAN',
 'SOUTH CHINA SEA',
 'BANGLADESH',
 'PALAU',
 'WESTERN SAMOA',
 'PACIFIC OCEAN ',
 'BRITISH ISLES',
 'GRENADA',
 'IRAQ',
 'TURKEY',
 'SINGAPORE',
 'NEW BRITAIN',
 'SUDAN',
 'JOHNSTON ISLAND',
 'SOUTH PACIFIC OCEAN',
 'NEW GUINEA',
 'NORTH PACIFIC OCEAN',
 'FEDERATED STATES OF MICRONESIA',
 'MID ATLANTIC OCEAN',
 'ADMIRALTY ISLANDS',
 'BRITISH WEST INDIES',
 'SOUTH ATLANTIC OCEAN',
 'PERSIAN GULF',
 'RED SEA / INDIAN OCEAN',
 'PACIFIC OCEAN',
 'NORTH SEA',
 'NICARAGUA ',
 'MALDIVE ISLANDS',
 'AMERICAN SAMOA',
 'ANDAMAN / NICOBAR ISLANDAS',
 'GABON',
 'MAYOTTE',
 'NORTH ATLANTIC OCEAN ',
 'THE BALKANS',
 'SUDAN?',
 'MARTINIQUE',
 'INDIAN OCEAN',
 'GUATEMALA',
 'NETHERLANDS ANTILLES',
 'NORTHERN MARIANA ISLANDS',
 'IRAN / IRAQ',
 'JAVA',
 'SIERRA LEONE',
 ' PHILIPPINES',
 'NICARAGUA',
 'CENTRAL PACIFIC',
 'SOLOMON ISLANDS / VANUATU',
 'BAY OF BENGAL',
 'MID-PACIFC OCEAN',
 'SOUTHWEST PACIFIC OCEAN',
 'SLOVENIA',
 'CURACAO',
 'ICELAND',
 'ITALY / CROATIA',
 'BARBADOS',
 'GUYANA',
 'HAITI',
 'SAN DOMINGO',
 'KUWAIT',
 'YEMEN ',
 'FALKLAND ISLANDS',
 'CYPRUS',
 'EGYPT ',
 'WEST INDIES',
 'CRETE',
 'BURMA',
 'LEBANON',
 'PARAGUAY',
 'BRITISH NEW GUINEA',
 'CEYLON',
 'OCEAN',
 'GEORGIA',
 'SYRIA',
 'TUVALU',
 'INDIAN OCEAN?',
 'GUINEA',
 'ANDAMAN ISLANDS',
 'EQUATORIAL GUINEA / CAMEROON',
 'COOK ISLANDS',
 'TOBAGO',
 'PERU',
 'AFRICA',
 'Coast of AFRICA',
 'TASMAN SEA',
 'GREENLAND',
 'MEDITERRANEAN SEA',
 'SWEDEN',
 'ROATAN',
 'DJIBOUTI',
 'ASIA?',
 'CEYLON (SRI LANKA)']
 countries after normalization
TBA? Idk, the lists are very long
before country sample counts:
244

after country sample counts:
160


====
AGES

ages before normalization
TBA

ages after normalisation
[  13, <NA>,   39,   11,   27,   12,   26,   56,   55,   24,   25,   61,   40,
   14,   54,   48,   57,    8,   63,    9,   19,    7,   85,   69,   18,   66,
   21,   37,   16,   20,   42,   45,   30,   47,   29,   35,   58,   17,   36,
   23,   28,   38,   68,   33,   15,   41,   43,   44,   49,   46,   65,   64,
   32,   10,   62,   22,   52,   59,   50,   34,   77,   60,   73,   67,    6,
   53,   51,   31,   71,   75,   70,    4,   74,    3,   82,   72,    2,    5,
   86,   84,   87,    1,    0,   81,   78]


# Univariate

Build the heatmap correlation

What is the relation between eaten man and women
Does man die more frequently

Who provokates more?  man or woman

Is it more likely to die from shark attack if you provokate incident 

Do children die more frequently from shark attacks then adults

Is there any correlation between age and likelyhood of death

Any coorelation between coordinates and likelyhood of death? Maybe some ocean is more dangerous, or there leave more dangerous species

Amount of cases distributed with stacked box plot to man and women

Is there a correlation between time and death rate

Is there correlation between season (Winter, Spring, Summer, Fall) and number of cases
Season/death
Month/Cases
Month/Death

Crosscorrelate fatal and type
Type/sex
Type/Country

- **Bivariate — Categorical vs Categorical:**
  - Cross-tab: `type` vs `fatal_y_n`, `activity` vs `injury`, `sex` vs `fatal_y_n`
  - Stacked bar charts or heatmaps for co-occurrence

- **Bivariate — Categorical vs Numerical:**
  - `age` distribution by `fatal_y_n`, `sex`, `type`
  - Mean/median `age` per `activity` / `species`

- **Bivariate — Time series / Trends:**
  - Yearly trend by `type` and by `country`
  - Rolling averages (5- or 10-year) to smooth noise
  - Anomaly detection for spikes/sudden drops

- **Multivariate / Correlation:**
  - Correlation matrix for numeric columns
  - Pairplots for small numeric subsets
  - Logistic-style checks: predictors vs fatality (for simple modeling)
  

# Univariate

What is the country with the most invalid attacks 

What is the country with the most reported cases

Amount of reports per year

What is the most frequent time reported

Who are more reported women or man

What age is reported more (top 10)

# TODO

Categorize somehow injury to analyse it

Normalize and categorize species
Is any species more deadlier then other