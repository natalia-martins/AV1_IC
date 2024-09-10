# Treinamento do Dinossauro do Jogo T-Rex com Algoritmos Genéticos
Este projeto visa treinar o dinossauro do jogo T-Rex do Google usando algoritmos genéticos. O objetivo é evoluir agentes (dinossauros) para melhorar seu desempenho no jogo ao longo de várias gerações.

![image](https://github.com/user-attachments/assets/a8247deb-dd7e-4318-a677-941fda254ef7)

![image](https://github.com/user-attachments/assets/379ecd26-e7c5-4180-82cb-7a03d7b7cd1d)


### Requisitos
- Python 3
- Bibliotecas necessárias:
    - ``` chrome-trex-rush ``` (para interação com o jogo T-Rex)
    - ``` numpy ``` (para operações matemáticas)

### Estrutura do Projeto
- ``` src/ ```
    - ``` genetic_algorithm.py ```: Implementação do algoritmo genético.
    - ``` dino_agent.py ```: Definição da classe ``` DinoAgent ```.
- ``` tests/ ```
    - Testes unitários para o código.
- ``` docs/ ```
    - Documentação do projeto e instruções de uso.

### Instalação
1. Clone o repositório:
``` git clone https://github.com/natalia-martins/TrainingTAIC.git ```

2. Navegue até o diretório do projeto:
``` cd TrainingTAIC ```

3. Instale as dependências:
``` pip install -r requirements.txt ```

### Uso
#### Configuração Inicial
Antes de executar o algoritmo genético, certifique-se de que a biblioteca chrome-trex-rush está corretamente configurada. Consulte a documentação da biblioteca para obter detalhes sobre a configuração.

#### Executando o Algoritmo Genético
1. Execute o script principal para iniciar o treinamento:
``` python src/genetic_algorithm.py ```

2. O algoritmo genético começará a treinar os agentes (dinossauros). Você verá a evolução dos agentes ao longo das gerações, conforme medido pela função de aptidão.

#### Funções
- ``` DinoAgent ```: Classe que representa um dinossauro no jogo T-Rex. Possui genes que determinam seu comportamento e uma função de aptidão que avalia seu desempenho.
- ``` genetic_algorithm ```: Função principal que executa o algoritmo genético, incluindo seleção, cruzamento e mutação de agentes.

#### Testes
Execute os testes unitários para garantir que o código esteja funcionando corretamente:
``` pytest ```

#### Contribuição
Se desejar contribuir para o projeto, siga estes passos:
1. Faça um fork do repositório.
2. Crie uma branch para sua feature ou correção.
3. Faça suas alterações e adicione testes, se aplicável.
4. Envie um pull request descrevendo suas mudanças.

### Links Importantes:
Repositório T-Rex: https://github.com/turing-usp/chrome-trex-rush/blob/master/README.md
Template de repositório: https://github.com/ArielMAJ/python-repository-template

### Contato
Para dúvidas ou sugestões, entre em contato com natalia.santos@aln.senaicimetec.edu.br
