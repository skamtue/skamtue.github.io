import itertools
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation as animation

##Fixed parameters
n = 5
T = 20
T_buff = 25
nf = (n+2)*T_buff

def findsubsets(S,m):
    return set(itertools.combinations(S, m))

#dictionary of vertices of CP(4) x J(6,3) and their positions
def generateCPJ(): #
    n = 3
    N = range(2*n)
    S = findsubsets(N,n)

    ### johson graph
    posJ = {}
    count_layer = [0]*(n+1)
    poleJ = tuple(range(n))
    
    for subset in S:
        v = tuple(subset)
        x_axis = n - len(set(v) & set(poleJ))
        y_axis = count_layer[x_axis]
        #offset scale on y-axis (n=3) [-4,4]
        if x_axis == 1 or x_axis == 2:
            y_axis = y_axis-4
        posJ[v] =(x_axis,y_axis)
        count_layer[x_axis] +=1

    G = nx.Graph()
    G_vert = nx.Graph()
    #CP circle scale
    rx = 6
    ry = 10
    angle = [1, 0.75-0.05, 0.5, 0.25+0.02, 0, -0.25-0.02, -0.5, -0.75+0.05]  
    for i in range(8):
        for p in posJ.keys():
            x_axis = 6*np.cos(np.pi*angle[i])
            y_axis = 10*np.sin(np.pi*angle[i])
            position = np.add(posJ[p] , (x_axis,y_axis))
            G.add_node((i,p), pos= position)
            G_vert.add_node((i,p), pos= position)

##    for i in range(8):
##        for p in posJ.keys():
##            for q in posJ.keys():
##                if len((set(p) & set(q))) == n-1:
##                    G.add_edge((i,p),(i,q), weight=0) #vertical edges
##
##    for i in range(8):
##        for j in range(8):
##            if (j-i)%8 !=4:
##                for p in posJ.keys():
##                    G.add_edge((i,p),(j,p),weight=1) #horizontal edges


    for i in range(8):
        for j in range(8):
            if j == i:
                for p in posJ.keys():
                    for q in posJ.keys():
                        if len((set(p) & set(q))) == n-1:
                            G.add_edge((i,p),(i,q)) #vertical edges
                            G_vert.add_edge((i,p),(i,q))
            elif (j-i)%8 !=4:
                for p in posJ.keys():
                    G.add_edge((i,p),(j,p)) #horizontal edges
    return G, G_vert

def interpolate(posG,v0,v1,lamb):
    """Find the position of a convex combination of two nodes"""
    pos0 = np.array(posG[v0])
    pos1 = np.array(posG[v1])
    posip = (1-lamb)*pos0+ lamb*pos1
    return posip #np array of dim 2

def generate_labels():
    """Customize labels on the graph"""
    L = nx.Graph()
    labels = ["$v_0$", "$v_1$", "$v_2$", "$v_3$", "$v_4$", "$v_5$", ""]
    positions = [(-6,0.5), (-5,-0.5), (1,9.5), (2,9.5), (8,-0.5), (9,0.5), (-6,-15)]
    for i in range(len(labels)):
        L.add_node(labels[i], pos=positions[i])
    return L

def toggle_on(k):
    """Customize labels to appear in k-pause frame"""
    #k runs from -1 to n
    K = nx.Graph()
    labels = ["$\\bf{B_1(v_0)}$", "$\\bf{B_1(v_1)}$", "$\\bf{B_1(v_2)}$", "$\\bf{B_1(v_3)}$", "$\\bf{B_1(v_4)}$", "$\\bf{B_1(v_5)}$"]
    positions = [(-6,-0.5), (-5,-1.5), (1,8.5), (2,8.5), (8,-1.5), (9,-0.5)]

    if k != n: #ignore frames n
        K.add_node(labels[k+1], pos=positions[k+1])
    return K

def update_function(t, n, T, T_buff, G, G_vert, posG, posG_vert, geod):
    """
    G is networkx graph with positions posG. 
    geod is the list of vertices on the main geodesic. 
    """
    plt.clf() #Clear figure in the plot

    #Construct the list of edges along main geodesic
    geod_edges = []
    for edge in G.edges:
        for i in range(n):
            if (geod[i] in edge) and (geod[i+1] in edge):
                geod_edges.append(edge)
    #Construct the list of 1-balls around vertices along main geod
    balls = [0]*(n+1)
    for i in range(n+1):
        ball_i = list(G.adj[geod[i]])
        ball_i.append(geod[i])
        balls[i] = ball_i

    ##Draw base graph G
    nx.draw(G,posG,node_size=20, node_color = '0.7', edge_color = '0.7')
    nx.draw(G_vert,posG_vert,node_size=20, node_color = '0.5', edge_color = '0.5', with_labels=False)
    
    nx.draw_networkx_nodes(G, posG, nodelist=geod, node_color = '0', node_size=20, label = range(n+1))
    nx.draw_networkx_edges(G, posG, edgelist=geod_edges, width=2.0)

    
    TF = (n+2)*T_buff # total frames
    t = (t % TF) - T_buff

    k = t // T_buff #range from -1 to n
    t = t % T_buff  #range from 0 to T_buff-1

    L = generate_labels()
    posL = nx.get_node_attributes(L,'pos')
    nx.draw_networkx(L, posL, node_size=0, with_labels=True)
    
    if t > T:
        t = T
        K = toggle_on(k)
        posK = nx.get_node_attributes(K,'pos')
        nx.draw_networkx(K, posK, node_size=0, with_labels=True, font_color='darkgreen', font_size=12)
                
    lamb = float(t/T) #interpolation coefficient between 0 and 1

    ##Construct graph H of the moving ball
    H = nx.Graph()
    if k == -1:
        gamma = 0
        H.add_node(0, pos=posG[geod[0]]) #the moving centre
        u = {} #dictionary for positions of moving masses
        for a in balls[0]:
             u[a] = interpolate(posG,geod[0],a,lamb)
             H.add_node(a, pos=tuple(u[a]))
             H.add_edge(a,0)
    elif k == n:
        gamma = 1
        H.add_node(0, pos=posG[geod[n]])
        u = {}
        for a in balls[n]:
            u[a] = interpolate(posG,a,geod[n],lamb)
            H.add_node(a, pos=tuple(u[a]))
            H.add_edge(a,0)
    else:
        gamma = (k+lamb)/n
        pos0 = interpolate(posG, geod[k], geod[k+1],lamb)
        H.add_node(0, pos=pos0) 
                
        u = {} 
        for a in balls[k]:
            if a in balls[k+1]:
                   u[a] = np.array(posG[a])
            else:
                 for b in balls[k+1]:
                    if not(b in balls[k]) and (b in G.neighbors(a)):
                          u[a] = interpolate(posG,a,b,lamb)               
            H.add_node(a, pos=tuple(u[a]))
            H.add_edge(a,0)

    fade = [[1-gamma, 0, gamma]]
    green = [[0,1,0.5,0.3]]
    #node size map
    nsm = []
    for node in H:
         if node == 0:
            nsm.append(0)
         else:
            nsm.append(50)
            
    positions = nx.get_node_attributes(H, 'pos')
    nx.draw_networkx_nodes(H, positions, node_size=nsm, node_color=fade)
    if t == T:
        nx.draw_networkx_edges(H, positions, edge_color = green, width=5.0)

def graph_anim():
    G, G_vert = generateCPJ()
    posG = nx.get_node_attributes(G, 'pos')
    posG_vert = nx.get_node_attributes(G_vert, 'pos')

    #nx.draw(G,posG,node_size=20, node_color = '0.7', edge_color = '0.7')
    #nx.draw(G_vert,posG_vert,node_size=20, node_color = '0.5', edge_color = '0.5')

    fig = plt.figure(figsize=(7,7))

    ##define main geodesic here
    geod = [(0,(0,1,2)), (0,(0,1,5)), (2,(0,1,5)), (2,(1,3,5)), (4,(1,3,5)), (4,(3,4,5))]
    
    ani_pos = animation.FuncAnimation(fig, update_function, interval=100, frames=nf, repeat=False, fargs=(n, T, T_buff, G, G_vert, posG, posG_vert, geod))
    #plt.show()
    ani_pos.save('ani-CPJ.gif',writer='imagemagick')

graph_anim()

