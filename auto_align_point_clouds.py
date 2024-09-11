""" Curso IDASE
    Disciplina de Visão Computacional
    Doscente: Dr. Vinicius Ferreira Vidal,
    Discente: Giovani Santiago Junqueira

    O objetivo é encontrar um alinhamento bom e automático entre as duas point clouds utilizadas de
    exemplo para o bunny.
"""
import os
import copy
import open3d as o3d
import numpy as np

# pylint: disable=no-member

def result_register(directory, font, target, transform, inter=0, salve=False):
    """ Aplica uma transformação a uma nuvem de pontos de origem e visualiza o resultado do
    registro.

    Args:
        - directory (str): DirectoryDiretório onde se encontram as nuvens de pontos
        - font (o3d.geometry.PointCloud): Nuvem de pontos de origem.
        - target (o3d.geometry.PointCloud): Nuvem de pontos alvo.
        - transform (numpy.ndarray): Matriz de transformação a ser aplicada à nuvem de pontos de
        origem.
        - inter (int, opcional): Iteração atual do processo de registro. Se `inter` for igual a 9,
        a função exibe uma visualização das nuvens de pontos registradas. Padrão é 0.
        - salve (bool, opcional): Se `True`, salva as nuvens de pontos transformadas em arquivos
        PLY. Padrão é `False`.
    """
    font_temp = copy.deepcopy(font)
    target_temp = copy.deepcopy(target)
    font_temp.paint_uniform_color([1, 0.706, 0])
    target_temp.paint_uniform_color([0, 0.651, 0.929])
    font_temp.transform(transform)
    if inter == 9:
        o3d.visualization.draw_geometries([font_temp, target_temp],
                                          window_name=f"Nuvens de Pontos iteração: {inter}")
    if salve:
        o3d.io.write_point_cloud(os.path.join(directory, 'point_clouds/bunny_fon"_icp.ply'),
                                 font_temp, write_ascii=False)
        o3d.io.write_point_cloud(os.path.join(directory, 'point_clouds/bunny_target_icp.ply'),
                                 target_temp, write_ascii=False)


def load_point_cloud(direct, figure):
    """ Carrega uma nuvem de pontos de um arquivo.

    Args:
        - direct (str): Diretório onde o arquivo da nuvem de pontos está localizado.
        - figure (str): Nome do arquivo da nuvem de pontos a ser carregado.

    Return:
        - pcd (o3d.geometry.PointCloud): A nuvem de pontos carregada.
    """
    pcd = o3d.io.read_point_cloud(os.path.join(direct, f'{figure}'))
    return pcd


def icp_point_to_point(pcd_up, pcd_down, transform, dist, relative_tol):
    """ Aplica o algoritmo ICP (Iterative Closest Point) para alinhar duas nuvens de pontos.

    Args:
        - pcd_up (o3d.geometry.PointCloud): Nuvem de pontos de referência.
        - pcd_down (o3d.geometry.PointCloud): Nuvem de pontos a ser alinhada.
        - transform (numpy.ndarray): Matriz de transformação inicial.
        - dist (float): Potência da base 10 que define a distância máxima para a correspondência
        de pontos.
        - relative_tol (float): Critério de convergência para o RMSE relativo.

    Return:
        - transformation (numpy.ndarray): Matriz de transformação resultante após a aplicação do
        ICP.
        - inlier_rmse (float): Erro médio quadrático das correspondências válidas (inliers).
    """
    max_dist_corresp = 10 ** (- dist)
    reg_p2p = o3d.pipelines.registration.registration_icp(
        pcd_up, pcd_down, max_dist_corresp, transform,
        o3d.pipelines.registration.TransformationEstimationPointToPoint(),
        # o3d.pipelines.registration.TransformationEstimationPointToPlane(),
        o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=1500,
                                                          relative_rmse=relative_tol))
    print(f"Aplicar ICP ponto a ponto iteração {dist}")
    print(reg_p2p)
    print(reg_p2p.transformation)
    return reg_p2p.transformation, reg_p2p.inlier_rmse


if __name__ == "__main__":
    # Carregar as nuvens de pontos
    dir_path = os.path.dirname(os.path.realpath(__file__))
    figures = ["point_clouds/bunny2_up.ply", "point_clouds/bunny2_down.ply"]
    pcd_s = []
    for i, fig in enumerate(figures):
        pcd_s.append(load_point_cloud(dir_path, fig))
        pcd_s[i].estimate_normals()  # Cálculo da normal da nuvem de pontos

    # Alinhamento inicial
    transform_reference = np.identity(4)
    print(transform_reference)
    result_register(dir_path, pcd_s[0], pcd_s[1], transform_reference)
    TOLERANCE = 0.001

    # processo interativo para aplicação do ICP
    for i in range(1, 10):
        # Aplicar ICP para registro
        transform_reference, tol = icp_point_to_point(pcd_s[0], pcd_s[1], transform_reference,
                                                      i, TOLERANCE)
        print(tol, TOLERANCE)
        if tol < TOLERANCE:
            TOLERANCE = 1/(10 ** (int(str(tol).split('-')[1]) + 3))
        if i == 9:
            result_register(dir_path, pcd_s[0], pcd_s[1], transform_reference, inter=i, salve=True)
        else:
            result_register(dir_path, pcd_s[0], pcd_s[1], transform_reference, inter=i)
