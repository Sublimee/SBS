import java.util.stream.IntStream;

class Vertex {
    public int Value;

    public Vertex(int val) {
        Value = val;
    }
}

class SimpleGraph {
    Vertex[] vertex;
    int[][] m_adjacency;
    int max_vertex;

    public SimpleGraph(int size) {
        max_vertex = size;
        m_adjacency = new int[size][size];
        vertex = new Vertex[size];
    }

    public void AddVertex(int value) {
        int vacantIndex = IntStream.range(0, max_vertex)
                .filter(i -> vertex[i] == null)
                .findFirst()
                .orElse(-1);

        if (vacantIndex >= 0) {
            vertex[vacantIndex] = new Vertex(value);
        }
    }

    // здесь и далее, параметры v -- индекс вершины
    // в списке vertex
    public void RemoveVertex(int v) {
        // ваш код удаления вершины со всеми её рёбрами
        if (isVertexIndexIncorrect(v)) {
            return;
        }

        vertex[v] = null;

        for (int i = 0; i < max_vertex; i++) {
            m_adjacency[v][i] = 0;
            m_adjacency[i][v] = 0;
        }
    }

    public boolean IsEdge(int v1, int v2) {
        checkEdgeIndexes(v1, v2);

        // true если есть ребро между вершинами v1 и v2
        return m_adjacency[v1][v2] != 0;
    }

    public void AddEdge(int v1, int v2) {
        checkEdgeIndexes(v1, v2);

        // добавление ребра между вершинами v1 и v2
        m_adjacency[v1][v2] = 1;
        m_adjacency[v2][v1] = 1;
    }

    public void RemoveEdge(int v1, int v2) {
        checkEdgeIndexes(v1, v2);

        // удаление ребра между вершинами v1 и v2
        m_adjacency[v1][v2] = 0;
        m_adjacency[v2][v1] = 0;
    }

    private boolean isVertexIndexIncorrect(int v) {
        return v < 0 || v >= max_vertex;
    }

    private void checkEdgeIndexes(int v1, int v2) {
        if (isVertexIndexIncorrect(v1) || isVertexIndexIncorrect(v2)) {
            throw new IndexOutOfBoundsException();
        }
    }
}