package org.example.algo02;

class aBST {

    public Integer Tree[]; // массив ключей

    public aBST(int depth) {
        // правильно рассчитайте размер массива для дерева глубины depth:
        int tree_size = 0;
        for (int i = 0; i <= depth; i++) {
            tree_size += Math.pow(2, i);
        }

        Tree = new Integer[tree_size];
        for (int i = 0; i < tree_size; i++) Tree[i] = null;
    }

    public Integer FindKeyIndex(int key) {
        if (Tree.length == 0) {
            return null; // не найден
        }

        return FindKeyIndex(key, 0);
    }

    private Integer FindKeyIndex(int key, int index) {
        if (index > Tree.length - 1) {
            return null; // не найден
        }

        if (Tree[index] == null) {
            return -index;
        }

        if (Tree[index] == key) {
            return index;
        }

        if (key < Tree[index]) {
            return FindKeyIndex(key, 2 * index + 1);
        }
        return FindKeyIndex(key, 2 * index + 2);
    }

    public int AddKey(int key) {
        Integer findKeyIndex = FindKeyIndex(key);
        if (findKeyIndex == null) {
            return -1;
        }

        int keyIndex = Math.abs(findKeyIndex);
        Tree[keyIndex] = key;

        return keyIndex;
    }
}