from langdetect import detect
from pymongo import MongoClient
import sys


def get_repository_projects():
    client = MongoClient('localhost', 27017)
    db = client.github
    return db.projects


def detect_language(project):
    language = None
    try:
        if len(project['readme_txt']):
            language = detect(project['readme_txt'])
    except:
        pass
    return (language)


repository_projects = get_repository_projects()

no_readme = 0
en = 0
no_en = 0
errors = 0

px = list(repository_projects.find())

projects = [project for project in px if detect_language(project) == 'en']

# for project in repository_projects.find({'pipeline_status': 'PROCESSED'}):
for project in repository_projects.find():
    try:
        if len(project['readme_txt']):
            lang = detect(project['readme_txt'])
            if lang == 'en':
                en += 1
            else:
                no_en += 1
        else:
            no_readme += 1
    except:
        errors += 1
        print("Error procesing project {0} [{1}] - {2}".format(project['id'], project['name'], sys.exc_info()[0]))

print('en', en)
print('len', len(projects))
print('noreadme', no_readme)
print('otros', no_en)
print('errors', errors)

exit()

text1 = '''
There's a passage I got memorized. Ezekiel 25:17. "The path of the righteous man is beset on all sides\
by the inequities of the selfish and the tyranny of evil men. Blessed is he who, in the name of charity\
and good will, shepherds the weak through the valley of the darkness, for he is truly his brother's keeper\
and the finder of lost children. And I will strike down upon thee with great vengeance and furious anger\
those who attempt to poison and destroy My brothers. And you will know I am the Lord when I lay My vengeance\
upon you." Now... I been sayin' that shit for years. And if you ever heard it, that meant your ass. You'd\
be dead right now. I never gave much thought to what it meant. I just thought it was a cold-blooded thing\
to say to a motherfucker before I popped a cap in his ass. But I saw some shit this mornin' made me think\
twice. See, now I'm thinking: maybe it means you're the evil man. And I'm the righteous man. And Mr.\
9mm here... he's the shepherd protecting my righteous ass in the valley of darkness. Or it could mean\
you're the righteous man and I'm the shepherd and it's the world that's evil and selfish. And I'd like\
that. But that shit ain't the truth. The truth is you're the weak. And I'm the tyranny of evil men.\
But I'm tryin', Ringo. I'm tryin' real hard to be the shepherd.
'''
text2 = '''
   Il y a un passage que j'ai mémorisé. Ézéchiel 25:17. "Le chemin de l'homme juste est assailli de tous côtés"
    par les iniquités de l'égoïsme et la tyrannie des hommes mauvais. Béni soit celui qui, au nom de la charité
    et bonne volonté, bergers les faibles à travers la vallée des ténèbres, car il est vraiment le gardien de son frère
    et le trouveur d'enfants perdus. Et je frapperai sur toi avec une grande vengeance et une colère furieuse.
    ceux qui tentent d'empoisonner et de détruire Mes frères. Et vous saurez que je suis le Seigneur quand je mets ma vengeance
    Maintenant ... Je disais cette merde depuis des années et si tu l'avais jamais entendu, ça voulait dire ton cul.
    être mort maintenant. Je n'ai jamais beaucoup réfléchi à ce que cela voulait dire. Je pensais juste que c'était une chose de sang-froid
    dire à un enfoiré avant que je lui ai sauté une casquette dans le cul. Mais j'ai vu de la merde ce matin m'a fait penser \
    deux fois. Vous voyez, maintenant je pense: peut-être que cela signifie que vous êtes l'homme diabolique. Et je suis l'homme juste. Et M. \
    9mm ici ... il est le berger protégeant mon âne juste dans la vallée des ténèbres. Ou cela pourrait signifier \
    vous êtes l'homme juste et je suis le berger et c'est le monde qui est mauvais et égoïste. Et je voudrais \
    cette. Mais cette merde n'est pas la vérité. La vérité est que vous êtes le faible. Et je suis la tyrannie des hommes méchants.
    Mais j'essaye, Ringo. J'essaye vraiment d'être le berger.
'''

text3 = '''
Там есть проход, который я запомнил. Иезекииль 25:17. «Путь праведника окружен со всех сторон \
    по неравенствам эгоизма и тирании злых людей. Блажен тот, кто во имя милосердия \
    и доброй воли, пастухи слабы в долине тьмы, потому что он действительно хранитель своего брата \
    и искатель потерянных детей. И Я поражу тебя с великой мести и яростью гнева \
    тех, кто пытается отравить и уничтожить Мои братья. И ты узнаешь, что я Господь, когда я возлагаю Мою мести \
    на вас ». Теперь ... Я говорил это дерьмо в течение многих лет. И если вы когда-либо слышали это, это означало вашу задницу.
    быть мертвым прямо сейчас. Я никогда не думал о том, что это значит. Я просто подумал, что это хладнокровная вещь \
    чтобы сказать ублюдку, прежде чем я вытащил шапку в его задницу. Но я видел какое-то дерьмо, это заставил меня думать,
    дважды. Понимаете, теперь я думаю: может быть, это означает, что вы злой человек. И я - праведник. И г-н \
    Здесь 9 мм ... он - пастух, защищающий мою праведную задницу в долине тьмы. Или это может означать \
    вы праведник, и я пастух, и это мир злой и эгоистичный. И я хотел бы \
    что. Но это дерьмо не правда. Правда в том, что вы слабы. И я тирания злых людей. \
    Но я пытаюсь, Ринго. Я очень стараюсь быть пастухом.
'''
text4 = '''
Hay un pasaje que obtuve memorizado. Ezequiel 25:17. "El camino del hombre justo está asediado por todos lados"
    por las desigualdades de los egoístas y la tiranía de los hombres malvados. Bienaventurado el que, en nombre de la caridad \
    y buena voluntad, pastorea a los débiles a través del valle de la oscuridad, porque él es verdaderamente el guardián de su hermano \
    y el buscador de niños perdidos. Y voy a atacar a ti con gran venganza y enojo furioso \
    aquellos que intentan envenenar y destruir a Mis hermanos. Y sabrás que soy el Señor cuando pongo Mi venganza \
    sobre ti. "Ahora ... He estado diciendo esa mierda durante años. Y si alguna vez lo escuchaste, eso significaba tu culo.
    estar muerto ahora mismo Nunca pensé mucho sobre lo que significaba. Solo pensé que era una cosa de sangre fría
    decirle a un hijo de puta antes de que le estallara una gorra en el culo. Pero vi algo de mierda esta mañana me hizo pensar \
    dos veces. Mira, ahora estoy pensando: tal vez significa que eres el hombre malo. Y yo soy el hombre justo. Y el Sr. \
    9mm aquí ... él es el pastor que protege mi culo justo en el valle de la oscuridad. O podría significar \
    eres el hombre justo y yo el pastor, y el mundo es malvado y egoísta. Y me gustaría \
    ese. Pero esa mierda no es la verdad. La verdad es que eres el débil Y yo soy la tiranía de los hombres malvados.
    Pero lo estoy intentando, Ringo. Estoy tratando de ser el pastor.
'''

text5 = '''
Da ist eine Passage, die ich auswendig gelernt habe. Hesekiel 25,17. "Der Weg des Gerechten ist von allen Seiten bedrängt.
    durch die Ungerechtigkeiten des Egoismus und der Tyrannei der bösen Menschen. Gesegnet ist er, der im Namen der Nächstenliebe
    und guten Willens, hütet die Schwachen durch das Tal der Finsternis, denn er ist wirklich der Hüter seines Bruders.
    und der Finder von verlorenen Kindern. Und ich werde mit großer Rache und wütendem Zorn auf dich herabstoßen.
    diejenigen, die versuchen, meine Brüder zu vergiften und zu zerstören. Und du wirst wissen, dass ich der Herr bin, wenn ich meine Rache lege.
    auf dich. "Nun ... ich habe diesen Scheiß seit Jahren gesagt. Und wenn du es je gehört hast, dann war das dein Arsch.
    sei jetzt tot. Ich habe nie darüber nachgedacht, was es bedeutete. Ich dachte nur, es sei ein kaltblütiges Ding.
    zu einem Motherfucker zu sagen, bevor ich ihm eine Mütze in den Arsch steckte. Aber ich sah etwas Scheiße an diesem Morgen 'machte mich zu denken
    zweimal. Sehen Sie, jetzt denke ich: Vielleicht heißt das, dass Sie der böse Mann sind. Und ich bin der Gerechte. Und Herr \
    9mm hier ... er ist der Hirte, der meinen gerechten Esel im Tal der Dunkelheit beschützt. Oder es könnte bedeuten \
    Du bist der Gerechte und ich bin der Hirte und es ist die Welt, die böse und selbstsüchtig ist. Und ich würde gerne
    dass. Aber das ist nicht die Wahrheit. Die Wahrheit ist, du bist der Schwache. Und ich bin die Tyrannei böser Männer.
    Aber ich versuche es, Ringo. Ich versuche wirklich sehr, der Hirte zu sein.
'''

text6 = '''QQ空间爬虫，一小时20万数据'''

print("Text1:", detect(text1))
print("Text2:", detect(text2))
print("Text3:", detect(text3))
print("Text4:", detect(text4))
print("Text5:", detect(text5))
print("Text6:", detect(text6))
