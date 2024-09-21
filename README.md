<h1 align="center">
    <a> 🦖 Treinamento do Dinossauro Dino Game Usando Algoritmos Genéticos 🦖 </a>
</h1>


### 🔹 Sobre o projeto
Este projeto utiliza algoritmos genéticos para treinar dinossauros no jogo Dino Game, simulando a evolução de agentes (dinossauros) ao longo de várias gerações para melhorar seu desempenho no jogo.

---

### 🔹 Objetivo
Evoluir agentes dinossauros para maximizar sua performance no jogo Dino Game ao longo das gerações, utilizando os conceitos de **seleção natural**,**mutação genética** e **crossover** conforme ilustrado nas imagens abaixo:


🔸**3ª Geração:**

![alt text](image-2.png)

🔸**7ª Geração:**

![alt text](image-3.png)

🔸**Exibição das informações que acontecem nas partidas:**

![alt text](image-4.png)
![alt text](image-5.png)

---

### 🔹 Requisitos e Instalação
🔸**Requisitos:**
- Python 3
- Bibliotecas necessárias:
    - ``` git clone https://github.com/GrupoTuringCodes/chrome-trex-rush ``` 
    - ``` cd chrome-trex-rush  ``` 
    - ``` pip install chrome-trex-rush/  ```

<br>

🔸**Instalação:**
1. Clone o repositório:
``` git clone https://github.com/natalia-martins/TrainingTAIC.git ```

2. Navegue até o diretório do projeto:
``` cd TrainingTAIC ```

3. Instale as dependências:
``` pip install -r requirements.txt ```

---

### 🔹 Estrutura do Projeto
- ``` src/ ```
    - ``` genetic_algorithm.py ```: Implementação do algoritmo genético.
    - ``` dino_agent.py ```: Definição da classe ``` DinoAgent ```.
- ``` tests/ ```
    - Testes unitários para o código.
- ``` docs/ ```
    - Documentação do projeto e instruções de uso.

---

### 🔹 Algoritmos Genéticos Utilizados
No projeto, foram utilizados diversos algoritmos genéticos para evoluir os dinossauros ao longo das gerações. 

Os principais são:

**1. Seleção Proporcional ao Fitness**

🔸 **Como funciona:** 

Utilizamos um algoritmo de seleção proporcional ao fitness. Dinossauros com maior pontuação têm mais chances de serem selecionados para reprodução. A pontuação de cada dinossauro é elevada ao quadrado para enfatizar a diferença entre os mais aptos e os menos aptos.

🔸 **Código:**
![alt text](image-6.png)

🔸 **Diferencial:** 

Testamos outros métodos de seleção, mas a seleção proporcional proporcionou uma maior diversidade inicial, garantindo que dinossauros com pequenas vantagens evoluíssem mais rápido.

<br>

**2. Crossover Genético**

🔸 **Como funciona:** 

Durante o crossover, genes de dois pais são combinados para gerar um novo indivíduo (filho). A chance de herdar genes de um dos pais é controlada por uma porcentagem de herança, sorteada aleatoriamente.

🔸 **Código:**
![alt text](image-7.png)

🔸 **Diferencial:** 

O uso de um crossover com variação aleatória na herança (entre 0% a 100%) garantiu que os indivíduos tivessem uma mistura equilibrada de genes.

<br>

**3. Mutação**

🔸 **Como funciona:** 

Após o crossover, cada gene pode sofrer mutação com uma taxa de mutação de 5%. A mutação altera aleatoriamente os pesos da rede neural, adicionando variação ao pool genético.

🔸 **Código:**

![alt text](image-8.png)

🔸 **Diferencial:** 

Testamos diferentes taxas de mutação. Concluímos que uma taxa de 5% com magnitude de 0.1 trouxe o equilíbrio ideal entre diversidade e estabilidade no treinamento.

--- 

### 🔹 Processos de Treinamento

**1. Início do Treinamento**
   * O treinamento começa com uma população de dinossauros gerada aleatoriamente. Cada dinossauro tenta pular obstáculos, e sua performance determina sua pontuação e fitness.

**2. Momento Avançado do Treinamento**
   * Após várias gerações, os dinossauros começam a mostrar melhorias significativas. Dinossauros com bom desempenho sobrevivem, e sua inteligência evolui, ajustando melhor suas ações.
  
**3. Melhor Indivíduo**
   * O melhor dinossauro é salvo, com seus pesos sendo armazenados em um arquivo. Ele pode ser carregado posteriormente para testes e comparações.
  
--- 
### 🔹 Comportamento do Código
O código segue o ciclo clássico de um algoritmo genético:

  1. **Criação de uma população inicial** de dinossauros.
   
  2. **Avaliação:** Cada dinossauro joga e acumula uma pontuação.
   
  3. **Seleção:** Dinossauros mais aptos são selecionados.
   
  4. **Reprodução:** Realiza-se crossover e mutação para criar novos dinossauros.
   
  5. **Repetição:** O processo é repetido por várias gerações.
   
A cada nova geração, o comportamento do dinossauro melhora à medida que ele se adapta ao ambiente do jogo.

---
### 🔹 Resultados e Curiosidades

1. **Melhor Algoritmo:** O crossover com taxa de herança variável se mostrou mais eficiente do que outros métodos.
   
2. **Curiosidade:** No início, observamos que a mutação alta atrapalhava a convergência do treinamento. Após ajustar a magnitude da mutação, obtivemos uma evolução mais estável.

---

### 🔹 Salvar e Rodar o Melhor Dinossauro

O melhor dinossauro é salvo automaticamente no arquivo "pesos_melhor_individuo.json" após cada geração. 

Para rodar o melhor dinossauro:

![alt text](image-9.png)

Comando:  
-  ```python Melhor_Dino.py ```

---
### 🔹 Vídeos Demonstrativos

🔸 **1. Início do Treinamento:**

https://github.com/user-attachments/assets/05211b9b-a70b-4084-9baa-d01865ca3170




🔸 **2. Momento Avançado:**




🔸 **3. Melhor Dinossauro:**


--- 
### 🔹 Conclusão e Aprendizados

- Implementamos algoritmos genéticos para evoluir dinossauros no jogo T-Rex Rush.
  
- A mutação e o crossover foram ajustados para melhorar a convergência e estabilidade.
  
- O uso de uma seleção proporcional ao fitness aumentou a diversidade genética.

--- 

### 🔹 Uso
#### 🔸 Configuração Inicial
Antes de rodar o algoritmo genético, certifique-se de que a biblioteca chrome-trex-rush está corretamente instalada e configurada. Consulte a [documentação oficial](https://github.com/turing-usp/chrome-trex-rush/blob/master/README.md)  para obter detalhes sobre a configuração.

#### 🔸 Executando o Algoritmo Genético
1. Inicie o processo de treinamento executando o seguinte comando:
``` python src/genetic_algorithm.py ```

2. Durante o treinamento, os agentes evoluirão com base em uma função de aptidão, e você poderá observar sua melhoria ao longo das gerações.

#### 🔸 Funções Principais
- ``` DinoAgent ```: Classe que representa um dinossauro no jogo T-Rex. Os genes determinam seu comportamento e a função de aptidão mede seu desempenho.
- ``` genetic_algorithm ```: Função principal que executa o algoritmo genético, realizando as operações de seleção, cruzamento e mutação.

#### 🔸 Testes
Para garantir que o código está funcionando corretamente, rode os testes unitários:
``` pytest ```

#### 🔸 Contribuição
Contribuições são bem-vindas! Siga os passos abaixo para contribuir:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção.
3. Implemente suas mudanças e adicione testes (se necessário).
4. Envie um pull request com uma descrição clara das modificações.

---

### 🔹 Links Importantes:
- [Biblioteca chrome-trex-rush](https://github.com/turing-usp/chrome-trex-rush/blob/master/README.md)
- [Template de Repositório](https://github.com/ArielMAJ/python-repository-template)

---

### 🔹 Contato
Para dúvidas ou sugestões, entre em contato com:
- 👩‍💻 natalia.santos@aln.senaicimetec.edu.br
- 👩🏽‍💻 nathalia.leite@ba.estudante.senai.br
<h1 align="center">
