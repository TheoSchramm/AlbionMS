# __📊 Albion Market Search__
Um programa feito em Python usando a biblioteca Tkinter. Permite que o usuário pesquise o preço de itens no jogo Albion Online e exiba os resultados em um formato semelhante a uma tabela.

# __👨‍💻 Como funciona__
O usuário pode inserir o nome do item, a qualidade e o nível de encantamento para pesquisar e o programa irá recuperar dados de uma API externa e exibir no janela de resultado. O script também inclui recursos adicionais, como classificar a tabela por diferentes colunas, salvar a pesquisa como favorita e copiar os dados do item selecionado para a área de transferência.

# __📷 Exemplo__
![](/img_exemplo.png?raw=true "Exemplo")

# __🤔 Como utilizar?__
Através da interface gráfica, o usuário pode inserir o nome do item, a qualidade e o encantamento desejado e, em seguida, clicar no botão "Pesquisar" para iniciar a busca. Os resultados da busca serão exibidos em uma janela de resultados, onde o usuário pode classificar e copiar informações para a área de transferência. Ele também pode salvar a pesquisa como favorito pressionando F1-F12. <br>

# __📌 Perguntas Frequentes__
__Os preços estão desatualizados! Como faço para atualizar?__<br>
      R: Caso você queira os dados em tempo real, [baixe](https://github.com/BroderickHyman/albiondata-client/releases) o client do Albion Data Project, que vai monitorar o tráfego da sua conexão com o Albion Online, fazendo com que as informações relevantes sejam enviadas para um servidor central que as distribui para quem quiser.

__Preciso baixar mais alguma coisa além desse client?__<br>
      R: É necessário ter [Python](https://www.python.org/downloads/) instalado na sua máquina e uma conexão com a Internet.

__Como vou saber o nome de X item?__<br>
      R: O arquivo JSON deste repositório contém uma lista em inglês e em português com o nome de todos os itens do jogo.

__Devo colocar acentuação no nome dos itens?__<br>
      R: Não!

__Meus favoritos pararam de funcionar, como prosseguir?__<br>
      R: Você provavelmente moveu/apagou o arquivo fav.json, restaure ele e seus favoritos irão reaparecer.


# __⏳ Atalhos__
- Começar pesquisa: `Enter`
- Fechar janela dos resultados: `Esc`
- Copiar dados da tabela: `Clique na linha desejada`
- Mudar a ordem da classificação: `Clique na coluna desejada`
- Salvar item como favorito: `F1-F12 na janela dos resultados`
- Abrir item favoritado: `F1-F12 na janela de pesquisa`
