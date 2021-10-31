from osnova import Kalorije

kalorije1 = Kalorije.nalozi_seznam('seznam.json')

print(kalorije1.jedi[2].ogljikovi_hidrati)

def tabela(tabela):
    for line in tabela:        
        print(line)
        print(
            line.ime,
            line.ogljikovi_hidrati,
            line.beljakovine,
            line.mascobe,
            kalorije1.izracun_kalorij(line.ogljikovi_hidrati, line.beljakovine, line.mascobe),  
            )
    print(sum(jed.beljakovine for jed in tabela))

tabela(kalorije1.jedi)