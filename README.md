# __📊 Albion Market Search__
Um programa feito em Python  que utilizando a interface gráfica da biblioteca Tkinter e uma API, Permite que o usuário pesquise o preço de itens do jogo Albion Online e exiba seus resultados.

# __👨‍💻 Como funciona__
O usuário deve inserir o nome do item, sua qualidade e o nível de encantamento para pesquisar e o programa irá recuperar dados de uma API externa e exibir no janela de resultados. Também é possível ordenar as tabelas do resultado por diferentes colunas (Eg. Preço, Cidade, Etc), salvar a pesquisa como favorita e copiar os dados do item selecionado para a área de transferência.

# __📷 Exemplo__
![](/img_exemplo.png?raw=true "Exemplo")

# __📌 Dependências__
1. [Python](https://www.python.org/downloads/)

# __🙋 Perguntas Frequentes__
__Os preços estão desatualizados! Como faço para atualizar?__<br>
      R: Caso você queira os dados em tempo real, [baixe](https://github.com/BroderickHyman/albiondata-client/releases) o client do Albion Data Project, que vai monitorar o tráfego da sua conexão com o Albion Online, fazendo com que as informações relevantes sejam enviadas para um servidor central que as distribui para quem quiser.

__Como vou saber o nome de X item?__<br>
      R: O arquivo JSON deste repositório contém uma lista em inglês e em português com o nome de todos os itens do jogo.

__O item que eu procuro está sempre inválido!__<br>
      R: Verifique sua conexão com a Internet e certifique-se de não utilizar nenhum acento.

__Meus favoritos sumiram!__<br>
      R: Você provavelmente moveu/apagou o arquivo fav.json, restaure ele e seus favoritos irão voltar.


# __⏳ Atalhos__
- Começar pesquisa: `Enter`
- Fechar janela dos resultados: `Esc`
- Copiar dados da tabela: `Clique na linha desejada`
- Mudar a ordem da classificação: `Clique na coluna desejada`
- Salvar item como favorito: `F1-F12 na janela dos resultados`
- Abrir item favoritado: `F1-F12 na janela de pesquisa`
