package org.example.recursion;

import java.io.File;
import java.util.*;

public class Recursion08 {

    public List<File> listFilesRecursively(File folder) {
        List<File> currentAndUnderlyingLevelsFiles = new ArrayList<>();
        for (File entry : folder.listFiles()) {
            if (entry.isDirectory()) {
                currentAndUnderlyingLevelsFiles.addAll(listFilesRecursively(entry));
            } else {
                currentAndUnderlyingLevelsFiles.add(entry);
            }
        }
        return currentAndUnderlyingLevelsFiles;
    }
}