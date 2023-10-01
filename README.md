## ● Equipe 4:

1. Guilherme Siqueira (gcms2)
2. Ivo Neto (ilsn)
3. Niltton Szpak (nrcsf)
4. Pedro Fischer (palfl)
5. Walter Crasto (wcm)

---

## ● Arquitetura do Projeto:

### Ideia Geral:

- Interface: 2D - Visão superior
- Jogabilidade:
- Movimentação em vetores simples (cima, baixo, direita e esquerda) e compostos.
- Sistema de mira com o mouse, atirando projéteis que atingem o primeiro zumbi na linha de tiro.
- Zumbis andam na direção do jogador e ao encostarem nele tiram 1 vida. Cada zumbi tem 3 de vida e cada projétil que o atinge tira 1 de vida.
- Jogo organizado em 5 rounds em que o número de zumbis por round varia, aumentando a medida que o jogador avança.
- Condição de Derrota: Perder todas as vidas (3 vidas).
- Condição de Vitória: Matar o Zumbi Boss no último round (5) e pegar seu drop (Bomba).
- Interação de Objetos:
    - Contagem do número de Vidas
    - Contagem da munição
    - Contagem do número de abates de zumbis
    - Coleta de Medkits
    - Projétil colidindo com o Zumbi
    - Zumbi colidindo com o Sobrevivente

---

## ● Capturas de Tela:

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/8543ac43-7561-4a17-bb50-c03e6d0d58a0/0ec14fa4-a712-437a-82a6-450eaa536b84/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/8543ac43-7561-4a17-bb50-c03e6d0d58a0/bce94643-e558-4d2a-b7b8-f06c405cbea4/Untitled.png)

![Untitled](https://prod-files-secure.s3.us-west-2.amazonaws.com/8543ac43-7561-4a17-bb50-c03e6d0d58a0/f48ca373-1771-4d81-a6b1-786b43da1c11/Untitled.png)

![Captura_de_tela_2023-09-29_142005.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/8543ac43-7561-4a17-bb50-c03e6d0d58a0/141094af-188c-42e9-a338-88cfe0446b4e/Captura_de_tela_2023-09-29_142005.png)

---

● Auxiliares do Projeto:

### Ferramentas:

### Bibliotecas:

- Pygame - Biblioteca base para a criação de jogos com Python:
- Criação das mecânicas do jogo (ex; andar, atirar, recarregar)
- Interação entre os objetos (ex: colisão e contagem)
- Criação de efeitos visuais do jogo
- Random - Utilizada para sortear números que caso batessem com os números especiais do jogador, o zumbi derruba um MedKit ao morrer.

### Frameworks:

---

## ● Divisão de Trabalho:

1º Semana:

Niltton e Walter - Estudo da Dinâmica de Movimento e Interações entre Objetos no Pygame

Ivo, Guilherme e Pedro - Arquitetura do Projeto (conceitos base do jogo)

2º Semana:

Estudo coletivo de POO com início desenvolvimento das classes.

Reuniões para tirar dúvidas em conjunto

Início da conversão do código sem POO para a utilização desse conceito

3º Semana:

Criação de todas as classes de forma separada:

- Niltton, Pedro e Ivo: Sobrevivente, Zumbi, Projétil
- Walter e Guilherme: Kit Médico, Bomba Nuclear e Obstáculo

Niltton - Adição de Mecânicas novas: Rounds com número de zumbis aumentando, o Boss final aparecendo no 5º round, arma com número de balas limitadas no pente, recarga da arma e a parada de sobreposição de objetos no mapa (zumbis e sobreviventes não podem cruzar seus corpos). 

4º Semana:

Ajustes finais nas mecânicas do jogo

Guilherme e Niltton - Adição de Sprites no Jogo

Walter, Pedro e Ivo - Desenvolvimento do relatório e da apresentação

---

## ● Conceitos Python:

- Utilização de listas, funções e loops para otimização e organização do código. Muitas linhas repetidas puderam ser substituídas com a criação de loops e o armazenamento do conjunto de zumbis em listas. Além disso, a criação de funções permitiu a falta de repetição das mesmas linhas de código em diversas partes do projeto, permitindo apenas a chamada desses métodos.
- Além disso, a utilização da Programação Orientada Ao Objeto possibilitou a criação de um código com classes, de forma que ele era modular e podia ter seu desenvolvimento em diversos locais independentes, facilitando o trabalho coletivo sobre o código. Além de que a busca de erros era mais evidente, visto que cada classe tem seu arquivo separado e o erro aparece de forma isolada, mostrando em que pedaço do projeto é necessário o ajuste.

---

## ● Perguntas Projeto:

### Qual foi o maior erro cometido durante o projeto? Como vocês lidaram com ele?

O maior erro cometido pelo grupo foi a má administração da utilização do GitHub, de forma que, no início do projeto, o desenvolvimento do código se dava de forma independente e era apenas atualizado depois que houvesse uma conversa entre os integrantes do grupo. Para lidar com isso, aprendemos a utilizar o Github (”git clone”, “git add .”, “git commit -m” e “git push”) e passamos a atualizar nosso código com mais frequência, de forma que o desenvolvimento do projeto ocorreu com uma maior inclusão de todos os integrantes no processo de criação do jogo.

### Qual foi o maior desafio enfrentado durante o projeto? Como vocês lidaram com ele?

Além do aprendizado do GitHub que foi citado anteriormente, a implementação de Sprite Sheets foi o maior desafio encontrado pelo grupo. Além de não termos conhecimento sobre esse tópico, achamos a sua implementação complicada: iniciando já pela procura de um que fosse ideal para nosso código (sendo: gratuito, detalhado, com boa resolução e com as animações que existem no nosso jogo - andar, atirar e recarregar) e em seguida formatar para incluí-lo no nosso jogo, pois podem existir vários tipos de resolução em uma mesma Sprite Sheet e foi necessário uniformizar todas as imagens. Para resolver isso, procuramos na internet diversos Sprite Sheets, de forma que achamos um para o Zumbi e um para o Sobrevivente que atendiam as nossas necessidades. Em seguida, realizamos o tratamento das imagens de cada ação para todas se encaixarem na mesma formatação e as animações do jogo acontecerem de forma suave e sem bugs visuais.

### Quais as lições aprendidas durante o projeto?

Aprendemos bastante sobre a importância da Programação Orientada ao Objeto, de forma que tornamos o nosso código modularizado, diminuindo a dependência das funções do nosso programa, sendo mais fácil identificar erros isolados e tornando o código mais organizado.

Além disso, tivemos um problema na repetição de linhas de código, de modo que nosso código não estava otimizado. Com ajuda do nosso professor, tivemos indicações de como melhorar a estrutura do código, como por exemplo a utilização de loops e a criação de listas para variáveis repetidas em locais específicos do código, assim, tirando como lição a importância de um código com uma disposição organizada e otimizada.

Também aprendemos a importância de buscar o conteúdo por conta própria, visto que muitos recursos do nosso jogo foram acrescentados a partir do estudo independente do grupo, como por exemplo a utilização de Sprite Sheets e a interação de objetos utilizando os pixels do Hitbox. Ou seja, com a vasta quantidade de conteúdo disponível para o aprendizado na internet, sempre vai existir a possibilidade de aprender coisas importantes de forma rápida e prática.
