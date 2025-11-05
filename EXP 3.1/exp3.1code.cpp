#include <iostream>
#include <limits>
using namespace std;

#define INF 1000000  // Use a large number to represent infinity

int minDistance(int dist[], bool sptSet[], int V) {
    int min = INF, min_index;

    for (int v = 0; v < V; v++)
        if (!sptSet[v] && dist[v] <= min)
            min = dist[v], min_index = v;

    return min_index;
}

void printSolution(int dist[], int V) {
    cout << "Vertex \t Distance from Source\n";
    for (int i = 0; i < V; i++)
        cout << i << "\t\t" << dist[i] << "\n";
}

void dijkstra(int graph[][10], int src, int V) {
    int dist[10];      // Output array. dist[i] = shortest distance from src to i
    bool sptSet[10];   // sptSet[i] true if vertex i is included in shortest path tree

    // Initialize distances as INFINITE and sptSet[] as false
    for (int i = 0; i < V; i++)
        dist[i] = INF, sptSet[i] = false;

    dist[src] = 0; // Distance from source to itself is always 0

    for (int count = 0; count < V - 1; count++) {
        int u = minDistance(dist, sptSet, V);
        sptSet[u] = true;

        for (int v = 0; v < V; v++)
            if (!sptSet[v] && graph[u][v] && dist[u] + graph[u][v] < dist[v])
                dist[v] = dist[u] + graph[u][v];
    }

    printSolution(dist, V);
}

int main() {
    int V;
    cout << "Enter number of vertices: ";
    cin >> V;

    int graph[10][10];
    cout << "Enter adjacency matrix (0 if no edge exists):\n";
    for (int i = 0; i < V; i++)
        for (int j = 0; j < V; j++)
            cin >> graph[i][j];

    int src;
    cout << "Enter source vertex (0-based index): ";
    cin >> src;

    dijkstra(graph, src, V);

    return 0;
}
