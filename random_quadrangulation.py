from random_tree import *
import numpy as np
import random
import math

def cvs(tree):
    edges = []
    faces_edges = []
    faces = []
    num_nodes = len(tree.nodes)
    min_label = math.inf
    for node in tree.nodes:
        if node.label < min_label:
            min_label = node.label
    infinity_node = TreeNode(str(num_nodes), min_label - 1)
    tree.edges.append((infinity_node, infinity_node))
    tree.nodes.append(infinity_node)
    num_edges = len(tree.corners)
    tree.corners.append(infinity_node)
    corners = tree.corners + tree.corners
    succesors = []


    for i in range(num_edges): 
        node = corners[i]
        label = node.label
        j = i + 1
        while True:
            if corners[j].label == (label - 1):
                edges.append((int(node.data), int(corners[j].data)))
                if j <= num_edges:
                    succesors.append(j)
                else:
                    succesors.append(j - (num_edges + 1))
                break
            j += 1


    for i in range(num_edges):
        edge = tree.edges[i]
        start_edge = edge[0]
        target_edge = edge[1]

        if start_edge.label - target_edge.label == 1:
            j = tree.edges.index((target_edge, start_edge))
            succ1 = succesors[(j+1) % num_edges]  
            succ2 = succesors[succ1]  
            edge_face = sorted([i, j, succ1, succ2])
            if edge_face not in faces_edges:
                faces_edges.append(edge_face)
                vertices_face = [int(start_edge.data), int(target_edge.data), int(tree.corners[succ2].data), int(tree.corners[succ1].data)]
                if vertices_face not in faces:
                    faces.append(vertices_face)

        elif start_edge.label - target_edge.label == -1:
            succ1 = succesors[(i+1) % num_edges] 
            succ2 = succesors[succ1]  
            edge_face = sorted([i, j, succ1, succ2])
            if edge_face not in faces_edges:
                faces_edges.append(edge_face)
                vertices_face = [int(target_edge.data), int(start_edge.data), int(tree.corners[succ2].data), int(tree.corners[succ1].data)]
                if vertices_face not in faces:
                    faces.append(vertices_face)

        elif start_edge.label - target_edge.label == 0:
            j = tree.edges.index((target_edge, start_edge))
            succ1 = succesors[(i + 1) % num_edges] 
            succ2 = succesors[(j + 1) % num_edges] 
            edge_face = sorted([i, j, succ1, succ2])
            if edge_face not in faces_edges:
                faces_edges.append(edge_face)
                vertices_face = [int(start_edge.data), int(tree.corners[succ1].data), int(target_edge.data), int(tree.corners[succ2].data)]
                if vertices_face not in faces:
                    faces.append(vertices_face)

    return edges, faces

def create_file_edges(edges):
    file = open("edges.dat", "w")
    for edge in edges:
        file.write(str(edge[0]) + " " + str(edge[1]) + "\n")
    file.close 

def create_file_faces(faces):
    file = open("faces.dat", "w")
    for face in faces:
        file.write(str(face[0]) + " " + str(face[1]) + " " + str(face[2]) + " " + str(face[3]) + "\n")
    file.close

if __name__ == "__main__":
    n = 15
    contour = random_contour(n)
    # contour = [0, 1, 2, 3, 4, 3, 2, 3, 4, 3, 4, 3, 2, 1, 2, 3, 2, 1, 0]
    tree = contour_to_tree(contour)
    edges, faces = cvs(tree)
    print(edges)
    print(faces)
    create_file_edges(edges)
    create_file_faces(faces)