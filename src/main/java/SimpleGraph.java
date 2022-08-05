import java.util.*;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class Vertex {
    public int Value;
    public boolean Hit;

    public Vertex(int val) {
        Value = val;
        Hit = false;
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

    Deque<Vertex> stack = new LinkedList<>();

    public ArrayList<Vertex> DepthFirstSearch(int VFrom, int VTo) {
        init();

        if (!areIndexesValid(VFrom, VTo)) {
            return new ArrayList<>(stack);
        }

        if (vertex[VFrom] == null || vertex[VTo] == null) {
            return new ArrayList<>(stack);
        }

        vertex[VFrom].Hit = true;
        stack.push(vertex[VFrom]);

        find(VFrom, VTo);

        ArrayList<Vertex> result = new ArrayList<>(stack);
        Collections.reverse(result);
        return result;
    }

    private void find(int VFrom, int VTo) {
        Pair nextVertex = getNextVertex(VFrom, VTo);
        if (nextVertex != null) {
            stack.push(nextVertex.v);
            nextVertex.v.Hit = true;
            if (nextVertex.i == VTo) {
                return;
            }
            find(nextVertex.i, VTo);
            return;
        }

        stack.pop();
        if (stack.isEmpty()) {
            return;
        }
        
        find(IntStream.range(0, max_vertex)
                        .boxed()
                        .filter(i -> vertex[i].equals(stack.getFirst()))
                        .findFirst()
                        .orElse(null),
                VTo
        );
    }

    private Pair getNextVertex(int VFrom, int VTo) {
        List<Integer> adjacentVertexes = IntStream.range(0, max_vertex)
                .boxed()
                .filter(i -> m_adjacency[i][VFrom] == 1)
                .collect(Collectors.toList());

        Integer requiredVertexIndex = adjacentVertexes
                .stream()
                .filter(adjacent -> vertex[adjacent].equals(vertex[VTo]))
                .findFirst().orElse(null);

        if (requiredVertexIndex != null) {
            return new Pair(requiredVertexIndex, vertex[requiredVertexIndex]);
        }

        return adjacentVertexes.stream()
                .map(i -> new Pair(i, vertex[i]))
                .filter(p -> !p.v.Hit)
                .findFirst()
                .orElse(null);
    }

    private boolean areIndexesValid(int vFrom, int vTo) {
        if (vFrom < 0 || vTo < 0) {
            return false;
        }
        return vFrom < vertex.length && vTo < vertex.length;
    }

    private void init() {
        stack = new ArrayDeque<>();
        Arrays.stream(vertex)
                .filter(Objects::nonNull)
                .forEach(x -> x.Hit = false);
    }
}

class Pair {
    public int i;
    public Vertex v;

    public Pair(int i, Vertex v) {
        this.i = i;
        this.v = v;
    }
}
