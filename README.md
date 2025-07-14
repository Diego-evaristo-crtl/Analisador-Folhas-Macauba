# Script para Evaluação do Quanto uma Planta de Macauba esta Afetada


## Como usar

1. Instale o repositorio usando `git clone`, ou instale pelo no própio github
2. verifique se você tem o [python](https://www.python.org/downloads/) instalado com o seguinte commando `python --version`
3. instale o `tkinter` com `pip install tk`
4. execute `main.py` com o comando `python C:\caminho\para\main.py` (ou o equivalente em seu sistema operacional)

Coloque o caminho para a pasta na entrada superior, o nome do arquivo na entrada logo abaixo, 
e as dimensões da foto na entrada mais abaixo, estas devem estar formatadas em uma das seguintes
formas: `<altura>,<comprimento>` ou `<comprimento>,<altura>`. Os resultados serão devolvidos na 
mesma medida que está porem ao quadrado, portanto, `20,20` retornará algo como: `2.5`, 
caso `20,20` sejam medidas em `cm`, `2.5` estará em `2.5cm^2`. O mesmo vale para qualquer medida.

Clique no Botão "scanear imagem", e espere os resultados ao lado direito.
Clique em "mostrar imagem" para ver a representação visual da analise.


## Como o algoritimo funciona (METODOLOGIA)

O programa itera entre todos os pixeis da imagem escolhida e faz a seguinte decisão:
`R`: (`R`GB), `G`: (R`G`B), `B`: (RG`B`), `H`: (`H`SL)

se `G` > `R`-10 e `G` > `B`-10 e `H` < 150 `==>` saúdavel
se `R` > `G` e `R` > `B` `==>` Doente

Caso nenhuma das condicionais seja validada, o pixel é considerado
parte do fundo da foto. 

Todas as fotos testadas continham um fundo Azul, portanto, só podemos garantir a funcionalidade nessas circunstanceas.
Verifique os resultados regularmente com a opção "mostrar imagem".
