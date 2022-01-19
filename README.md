Polonium
========
Polonium é um complemento à biblioteca selenium a fim de facilitar a sua utilização.
Selenium é uma ferramenta desenvolvida com o intuito de automatizar aplicações web 
usando navegadores como Firefox, Safari, Edge, Chrome, Internet Explorer e Opera.
Polonium é uma classe desenvolvida em Python 3.x que simplifica a inicialização dos
webdrivers e não só a busca por um elemento dentro da página como também o clique, 
o envio de um texto para uma caixa de texto na página e a extração do conteúdo de
um elemento.

## 1. Usabilidade
Um exemplo de aplicação é a extração dos primeiros links referentes a uma busca no
google sobre a palavra "Polonium".

```python
# Código
from polonium import Polonium

po = Polonium()
driver = po.init_driver('chrome', 'C:/WebDrivers/chrome', 'User1')
driver.get('http://www.google.com')

po.send_keys('polonium', 'input', name='q')
po.click('input', name='btnK')
po.wait(2)

print('\nTexto:')
print(po.text('div/div/div/div/div/span/span'))
print('\nLinks:')
for a in po.find_all("cite"):
    if (a.text):
        print('-', a.text)
```

```
# Output
Texto:
O polônio ou polónio é um elemento químico de símbolo Po e de número atómico igual a 84 (84 prótons e 84 elétrons), com massa atómica 209 u. ... À temperatura ambiente, o polônio encontra-se no estado sólido. O polônio quando misturado ou em liga com o berílio pode ser empregado como uma fonte de nêutrons.

Links:
- https://pt.wikipedia.org › wiki › Polônio
- https://en.wikipedia.org › wiki › Po...
- https://www.rsc.org › periodic-table
- https://www.britannica.com › science
- https://www.livescience.com › 394...
- https://www.medicalnewstoday.com › ...
- https://www.lenntech.com › elements
- https://www.magazineluiza.com.br › busca › polonium...
- https://pubchem.ncbi.nlm.nih.gov › ...
- https://www.cdc.gov › isotopes › p...
```

