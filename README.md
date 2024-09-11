# Registro de Nuvens de Pontos com ICP (Iterative Closest Point)

Este projeto utiliza a biblioteca Open3D para realizar o registro de nuvens de pontos 3D, aplicando transformações geométricas e o algoritmo Iterative Closest Point (ICP) para alinhar as nuvens de pontos.

## Requisitos

Para rodar este projeto, você precisará ter o seguinte instalado:

- Python 3.8+
- Open3D
- NumPy

### Instalação das dependências

Para instalar as dependências necessárias, execute:

```bash
pip install open3d numpy
```

## Estrutura do Projeto

```plaintext
.
├── point_clouds/                # Diretório contendo os arquivos de nuvens de pontos em formato .ply
│   ├── bunny2_up.ply            # Nuvem de pontos de referência
│   └── bunny2_down.ply          # Nuvem de pontos a ser alinhada
├── main.py                      # Script principal do projeto
└── README.md                    # Documentação do projeto
```

## Funcionalidades

- **Carregamento de Nuvens de Pontos**: O projeto permite o carregamento de nuvens de pontos no formato `.ply` para serem processadas e alinhadas.
- **Registro por ICP**: O algoritmo ICP é aplicado para alinhar duas nuvens de pontos. O critério de convergência é baseado no erro quadrático médio relativo (RMSE).
- **Visualização**: A função de visualização exibe as nuvens de pontos durante o processo de registro em diferentes iterações.
- **Salvamento de Resultados**: As nuvens de pontos resultantes podem ser salvas no diretório `point_clouds/` após o registro.

## Como Executar

1. **Pré-requisitos**: Certifique-se de ter o Python instalado, juntamente com as bibliotecas `open3d` e `numpy`.

2. **Carregar Nuvens de Pontos**: As nuvens de pontos estão localizadas no diretório `point_clouds`. Elas são carregadas automaticamente pelo script.

3. **Executar o Script**: Para rodar o processo de registro, basta executar o seguinte comando no terminal:

```bash
python main.py
```

Durante a execução, o script aplicará o algoritmo ICP em iterações e exibirá as nuvens de pontos registradas. Se o critério de convergência for atingido, as nuvens de pontos serão salvas.

## Funções Principais

### `result_register(directory, font, target, transform, inter=0, salve=False)`

Aplica uma transformação a uma nuvem de pontos de origem e visualiza o resultado do registro. Se a opção `salve` for definida como `True`, salva as nuvens de pontos transformadas em arquivos `.ply`.

- **Parâmetros**:
  - `directory (str)`: Diretório onde se encontram as nuvens de pontos.
  - `font (o3d.geometry.PointCloud)`: Nuvem de pontos de origem.
  - `target (o3d.geometry.PointCloud)`: Nuvem de pontos alvo.
  - `transform (numpy.ndarray)`: Matriz de transformação a ser aplicada à nuvem de pontos de origem.
  - `inter (int, opcional)`: Iteração atual do processo de registro. Exibe visualização na iteração 9.
  - `salve (bool, opcional)`: Se `True`, salva as nuvens de pontos transformadas.

### `load_point_cloud(direct, figure)`

Carrega uma nuvem de pontos a partir de um arquivo no diretório especificado.

- **Parâmetros**:
  - `direct (str)`: Diretório onde o arquivo da nuvem de pontos está localizado.
  - `figure (str)`: Nome do arquivo da nuvem de pontos a ser carregado.

- **Retorno**:
  - `pcd (o3d.geometry.PointCloud)`: Nuvem de pontos carregada.

### `icp_point_to_point(pcd_up, pcd_down, transform, dist, relative_tol)`

Aplica o algoritmo ICP para alinhar duas nuvens de pontos, retornando a transformação resultante e o erro médio quadrático.

- **Parâmetros**:
  - `pcd_up (o3d.geometry.PointCloud)`: Nuvem de pontos de referência.
  - `pcd_down (o3d.geometry.PointCloud)`: Nuvem de pontos a ser alinhada.
  - `transform (numpy.ndarray)`: Matriz de transformação inicial.
  - `dist (float)`: Potência da base 10 que define a distância máxima para a correspondência de pontos.
  - `relative_tol (float)`: Critério de convergência para o RMSE relativo.

- **Retorno**:
  - `transformation (numpy.ndarray)`: Matriz de transformação resultante após a aplicação do ICP.
  - `inlier_rmse (float)`: Erro médio quadrático das correspondências válidas (inliers).

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um pull request ou enviar sugestões.

## Licença

Este projeto está licenciado sob a [MIT License](LICENSE).
