<h1 align="center">
    <a> 🦖 Treinamento do Dinossauro no T-Rex Rush Usando Algoritmos Genéticos 🦖 </a>
</h1>


### 🔹 Sobre o projeto
Este projeto utiliza algoritmos genéticos para treinar o dinossauro no jogo T-Rex Rush, simulando a evolução de agentes (dinossauros) ao longo de várias gerações para melhorar seu desempenho no jogo.

<br>

### 🔹 Objetivo
Evoluir agentes dinossauros para maximizar sua performance no jogo T-Rex Rush ao longo das gerações, conforme ilustrado no exemplo abaixo:

[IMAGEM]

[IMAGEM]

<br>

### 🔹 Requisitos
- Python 3
- Bibliotecas necessárias para interação com o jogo R-Rex:
    - ``` git clone https://github.com/GrupoTuringCodes/chrome-trex-rush ``` 
    - ``` cd chrome-trex-rush  ``` 
    - ``` pip install chrome-trex-rush/  ```

<br>

### 🔹 Estrutura do Projeto
- ``` src/ ```
    - ``` genetic_algorithm.py ```: Implementação do algoritmo genético.
    - ``` dino_agent.py ```: Definição da classe ``` DinoAgent ```.
- ``` tests/ ```
    - Testes unitários para o código.
- ``` docs/ ```
    - Documentação do projeto e instruções de uso.

<br>

### 🔹 Instalação
1. Clone o repositório:
``` git clone https://github.com/natalia-martins/TrainingTAIC.git ```

2. Navegue até o diretório do projeto:
``` cd TrainingTAIC ```

3. Instale as dependências:
``` pip install -r requirements.txt ```

<br>

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

<br>

### 🔹 Links Importantes:
- [Biblioteca chrome-trex-rush](https://github.com/turing-usp/chrome-trex-rush/blob/master/README.md)
- [Template de Repositório](https://github.com/ArielMAJ/python-repository-template)

<br>

### 🔹 Contato
Para dúvidas ou sugestões, entre em contato com:
- 👩‍💻 natalia.santos@aln.senaicimetec.edu.br
- 👩‍💻 nathalia.leite@ba.estudante.senai.br
<h1 align="center">
