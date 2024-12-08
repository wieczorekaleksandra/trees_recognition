import sqlite3
import json

# Sample JSON data
data = {
    "1": [
        "Pelargonium graveolens L'H\u0102\u00a9r.",
        "1355932"
    ],
    "2": [
        "Cirsium arvense (L.) Scop.",
        "1355936"
    ],
    "3": [
        "Cirsium vulgare (Savi) Ten.",
        "1355937"
    ],
    "4": [
        "Pelargonium zonale (L.) L'H\u0102\u00a9r.",
        "1355978"
    ],
    "5": [
        "Mercurialis annua L.",
        "1355990"
    ],
    "6": [
        "Hypericum perforatum L.",
        "1356022"
    ],
    "7": [
        "Tradescantia fluminensis Vell.",
        "1356075"
    ],
    "8": [
        "Lamium amplexicaule L.",
        "1356111"
    ],
    "9": [
        "Lavandula dentata L.",
        "1356126"
    ],
    "10": [
        "Melilotus albus Medik.",
        "1356257"
    ],
    "11": [
        "Dryopteris filix-mas (L.) Schott",
        "1356382"
    ],
    "12": [
        "Nephrolepis cordifolia (L.) C. Presl",
        "1356420"
    ],
    "13": [
        "Nephrolepis exaltata (L.) Schott",
        "1356421"
    ],
    "14": [
        "Osmunda regalis L.",
        "1356428"
    ],
    "15": [
        "Lithodora fruticosa (L.) Griseb.",
        "1356692"
    ],
    "16": [
        "Humulus lupulus L.",
        "1356781"
    ],
    "17": [
        "Vaccaria hispanica (Mill.) Rauschert",
        "1356816"
    ],
    "18": [
        "Calendula officinalis L.",
        "1357330"
    ],
    "19": [
        "Carthamus lanatus L.",
        "1357379"
    ],
    "20": [
        "Helminthotheca echioides (L.) Holub",
        "1357635"
    ],
    "21": [
        "Lactuca muralis (L.) Gaertn.",
        "1357677"
    ],
    "22": [
        "Limbarda crithmoides (L.) Dumort.",
        "1357705"
    ],
    "23": [
        "Sedum acre L.",
        "1358094"
    ],
    "24": [
        "Sedum album L.",
        "1358095"
    ],
    "25": [
        "Sedum dasyphyllum L.",
        "1358105"
    ],
    "26": [
        "Sedum sediforme (Jacq.) Pau",
        "1358133"
    ],
    "27": [
        "Mercurialis perennis L.",
        "1358605"
    ],
    "28": [
        "Hypericum androsaemum L.",
        "1358689"
    ],
    "29": [
        "Lamium purpureum L.",
        "1358752"
    ],
    "30": [
        "Lavandula stoechas L.",
        "1358766"
    ],
    "31": [
        "Galega officinalis L.",
        "1359197"
    ],
    "32": [
        "Trifolium angustifolium L.",
        "1359483"
    ],
    "33": [
        "Trifolium arvense L.",
        "1359485"
    ],
    "34": [
        "Trifolium campestre Schreb.",
        "1359488"
    ],
    "35": [
        "Trifolium incarnatum L.",
        "1359498"
    ],
    "36": [
        "Trifolium pratense L.",
        "1359517"
    ],
    "37": [
        "Trifolium stellatum L.",
        "1359525"
    ],
    "38": [
        "Punica granatum L.",
        "1359616"
    ],
    "39": [
        "Alcea rosea L.",
        "1359620"
    ],
    "40": [
        "Althaea officinalis L.",
        "1359625"
    ],
    "41": [
        "Nymphaea alba L.",
        "1359669"
    ],
    "42": [
        "Anemone coronaria L.",
        "1360153"
    ],
    "43": [
        "Hyoscyamus albus L.",
        "1360550"
    ],
    "44": [
        "Hyoscyamus niger L.",
        "1360555"
    ],
    "45": [
        "Daphne gnidium L.",
        "1360588"
    ],
    "46": [
        "Daphne laureola L.",
        "1360590"
    ],
    "47": [
        "Chaerophyllum temulum L.",
        "1360671"
    ],
    "48": [
        "Thapsia villosa L.",
        "1360811"
    ],
    "49": [
        "Pancratium maritimum L.",
        "1360978"
    ],
    "50": [
        "Anthericum liliago L.",
        "1360998"
    ],
    "51": [
        "Butomus umbellatus L.",
        "1361024"
    ],
    "52": [
        "Ophrys apifera Huds.",
        "1361656"
    ],
    "53": [
        "Ophrys lutea Cav.",
        "1361663"
    ],
    "54": [
        "Cirsium palustre (L.) Scop.",
        "1361759"
    ],
    "55": [
        "Lamium galeobdolon (L.) L.",
        "1361823"
    ],
    "56": [
        "Lavandula angustifolia Mill.",
        "1361824"
    ],
    "57": [
        "Epipactis helleborine (L.) Crantz",
        "1362294"
    ],
    "58": [
        "Sedum rupestre L.",
        "1362490"
    ],
    "59": [
        "Cenchrus setaceus (Forssk.) Morrone",
        "1363021"
    ],
    "60": [
        "Anemone hortensis L.",
        "1363110"
    ],
    "61": [
        "Papaver rhoeas L.",
        "1363128"
    ],
    "62": [
        "Papaver somniferum L.",
        "1363130"
    ],
    "63": [
        "Daucus carota L.",
        "1363227"
    ],
    "64": [
        "Smilax aspera L.",
        "1363336"
    ],
    "65": [
        "Secale cereale L.",
        "1363451"
    ],
    "66": [
        "Phalaris arundinacea L.",
        "1363490"
    ],
    "67": [
        "Lupinus angustifolius L.",
        "1363699"
    ],
    "68": [
        "Trifolium dubium Sibth.",
        "1363737"
    ],
    "69": [
        "Trifolium repens L.",
        "1363740"
    ],
    "70": [
        "Acacia dealbata Link",
        "1363764"
    ],
    "71": [
        "Acacia retinodes Schltdl.",
        "1363778"
    ],
    "72": [
        "Fragaria vesca L.",
        "1363991"
    ],
    "73": [
        "Centranthus ruber (L.) DC.",
        "1364099"
    ],
    "74": [
        "Tagetes patula L.",
        "1364159"
    ],
    "75": [
        "Lapsana communis L.",
        "1364164"
    ],
    "76": [
        "Lactuca sativa L.",
        "1364172"
    ],
    "77": [
        "Lactuca serriola L.",
        "1364173"
    ],
    "78": [
        "Lupinus polyphyllus Lindl.",
        "1367432"
    ],
    "79": [
        "Trachelospermum jasminoides (Lindl.) Lem.",
        "1369887"
    ],
    "80": [
        "Tradescantia spathacea Sw.",
        "1369960"
    ],
    "81": [
        "Morinda citrifolia L.",
        "1372016"
    ],
    "82": [
        "Tagetes erecta L.",
        "1374048"
    ],
    "83": [
        "Cucurbita pepo L.",
        "1384485"
    ],
    "84": [
        "Zamioculcas zamiifolia (Lodd.) Engl.",
        "1385937"
    ],
    "85": [
        "Cereus jamacaru DC.",
        "1389297"
    ],
    "86": [
        "Aegopodium podagraria L.",
        "1389510"
    ],
    "87": [
        "Cirsium eriophorum (L.) Scop.",
        "1391192"
    ],
    "88": [
        "Cirsium oleraceum (L.) Scop.",
        "1391226"
    ],
    "89": [
        "Daphne mezereum L.",
        "1391652"
    ],
    "90": [
        "Dryas octopetala L.",
        "1391797"
    ],
    "91": [
        "Epipactis atrorubens (Hoffm.) Besser",
        "1391953"
    ],
    "92": [
        "Epipactis palustris (L.) Crantz",
        "1391963"
    ],
    "93": [
        "Alliaria petiolata (M.Bieb.) Cavara & Grande",
        "1392475"
    ],
    "94": [
        "Gomphocarpus physocarpus E.Mey.",
        "1392654"
    ],
    "95": [
        "Hebe salicifolia (G.Forst.) Pennell",
        "1392695"
    ],
    "96": [
        "Hippophae rhamnoides L.",
        "1392777"
    ],
    "97": [
        "Hypericum calycinum L.",
        "1393241"
    ],
    "98": [
        "Kniphofia uvaria (L.) Hook.",
        "1393393"
    ],
    "99": [
        "Lactuca alpina (L.) Benth. & Hook.f.",
        "1393414"
    ],
    "100": [
        "Lamium album L.",
        "1393423"
    ],
    "101": [
        "Lamium maculatum (L.) L.",
        "1393425"
    ],
    "102": [
        "Lathraea clandestina L.",
        "1393449"
    ],
    "103": [
        "Lathraea squamaria L.",
        "1393450"
    ],
    "104": [
        "Liriodendron tulipifera L.",
        "1393614"
    ],
    "105": [
        "Maianthemum bifolium (L.) F.W.Schmidt",
        "1393725"
    ],
    "106": [
        "Melilotus officinalis (L.) Lam.",
        "1393792"
    ],
    "107": [
        "Neotinea ustulata (L.) R.M.Bateman, Pridgeon & M.W.Chase",
        "1393946"
    ],
    "108": [
        "Ophrys aranifera Huds.",
        "1394073"
    ],
    "109": [
        "Ophrys fuciflora (F.W.Schmidt) Moench",
        "1394120"
    ],
    "110": [
        "Anemone alpina L.",
        "1394382"
    ],
    "111": [
        "Papaver alpinum L.",
        "1394399"
    ],
    "112": [
        "Papaver orientale L.",
        "1394404"
    ],
    "113": [
        "Anemone hepatica L.",
        "1394420"
    ],
    "114": [
        "Anemone nemorosa L.",
        "1394460"
    ],
    "115": [
        "Anemone pulsatilla L.",
        "1394489"
    ],
    "116": [
        "Angelica sylvestris L.",
        "1394591"
    ],
    "117": [
        "Pyracantha coccinea M.Roem.",
        "1394994"
    ],
    "118": [
        "Metasequoia glyptostroboides Hu & W.C.Cheng",
        "1396708"
    ],
    "119": [
        "Telekia speciosa (Schreb.) Baumg.",
        "1396713"
    ],
    "120": [
        "Tradescantia virginiana L.",
        "1396824"
    ],
    "121": [
        "Trifolium alpinum L.",
        "1396843"
    ],
    "122": [
        "Anemone hupehensis (Lemoine) Lemoine",
        "1397268"
    ],
    "123": [
        "Adenostyles alpina (L.) Bluff & Fingerh.",
        "1397303"
    ],
    "124": [
        "Anemone narcissiflora L.",
        "1397311"
    ],
    "125": [
        "Anemone ranunculoides L.",
        "1397312"
    ],
    "126": [
        "Cirsium acaulon (L.) Scop.",
        "1397351"
    ],
    "127": [
        "Cirsium spinosissimum (L.) Scop.",
        "1397352"
    ],
    "128": [
        "Cymbalaria muralis P.Gaertn., B.Mey. & Scherb.",
        "1397364"
    ],
    "129": [
        "Lactuca perennis L.",
        "1397420"
    ],
    "130": [
        "Sedum palmeri S.Watson",
        "1398128"
    ],
    "131": [
        "Tradescantia zebrina Bosse",
        "1398178"
    ],
    "132": [
        "Calycanthus floridus L.",
        "1398326"
    ],
    "133": [
        "Anemone blanda Schott & Kotschy",
        "1398444"
    ],
    "134": [
        "Hypericum x hidcoteense Hilling ex Geerinck",
        "1398515"
    ],
    "135": [
        "Perovskia atriplicifolia Benth.",
        "1398592"
    ],
    "136": [
        "Barbarea vulgaris R.Br.",
        "1400100"
    ],
    "137": [
        "Peperomia serpens (Sw.) Loudon",
        "1402926"
    ],
    "138": [
        "Acalypha wilkesiana M\u0102\u013dll.Arg.",
        "1405685"
    ],
    "139": [
        "Alocasia macrorrhizos (L.) G.Don",
        "1408045"
    ],
    "140": [
        "Tradescantia pallida (Rose) D.R.Hunt",
        "1408774"
    ],
    "141": [
        "Schefflera arboricola (Hayata) Merr.",
        "1408961"
    ],
    "142": [
        "Aphelandra squarrosa Nees",
        "1409185"
    ],
    "143": [
        "Peperomia caperata Yunck.",
        "1409215"
    ],
    "144": [
        "Anthurium andraeanum Linden ex Andr\u0102\u00a9",
        "1409238"
    ],
    "145": [
        "Dendrobium nobile Lindl.",
        "1409292"
    ],
    "146": [
        "Nandina domestica Thunb.",
        "1409295"
    ],
    "147": [
        "Fittonia albivenis (Lindl. ex Veitch) Brummitt",
        "1418146"
    ],
    "148": [
        "Sedum morganianum E.Walther",
        "1418547"
    ],
    "149": [
        "Liriope muscari (Decne.) L.H.Bailey",
        "1419334"
    ],
    "150": [
        "Alocasia sanderiana W.Bull",
        "1420795"
    ],
    "151": [
        "Tradescantia sillamontana Matuda",
        "1497667"
    ],
    "152": [
        "Sedum adolphii Raym.-Hamet",
        "1529081"
    ]
}

conn = sqlite3.connect('flowers.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS plants (
    id INTEGER PRIMARY KEY,
    scientific_name TEXT NOT NULL,
    code TEXT NOT NULL
)
''')

for key, value in data.items():
    cursor.execute('''
    INSERT INTO plants (id, scientific_name, code)
    VALUES (?, ?, ?)
    ''', (int(key), value[0], value[1]))

conn.commit()
conn.close()

print("Data successfully inserted into the SQLite database!")
