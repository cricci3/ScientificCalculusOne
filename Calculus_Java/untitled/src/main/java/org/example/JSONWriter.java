package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.node.ArrayNode;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class JSONWriter {
    public static void writeJSON(List<MatrixData> dataList) throws IOException {
        String fileName = "..\\results.json";
        ObjectMapper mapper = new ObjectMapper();
        ObjectWriter writer = mapper.writerWithDefaultPrettyPrinter();

        // Read existing file
        File file = new File(fileName);
        ObjectNode rootNode;
        if (file.exists()) {
            rootNode = (ObjectNode) mapper.readTree(file);
        } else {
            rootNode = mapper.createObjectNode();
        }

        // Create new node for Java results
        ObjectNode javaNode = mapper.createObjectNode();

        // Add systemInfo
        ObjectNode systemInfo = javaNode.putObject("System_Info");
        systemInfo.put("Operating_System", System.getProperty("os.name"));
        systemInfo.put("Language", "Java");

        // Add Matrix_Results
        ArrayNode matrixResults = javaNode.putArray("Matrix_Results");
        for (MatrixData data : dataList) {
            ObjectNode matrixNode = matrixResults.addObject();
            matrixNode.put("File", data.getMatrixName());
            matrixNode.put("Errore_Relativo", data.getErroreRelativo());
            matrixNode.put("Time", data.getTime());
            matrixNode.put("Memory_Used", (data.getMemoryUsed() / 1024.0)/1024.0); // Convert to MB
            matrixNode.put("Status", data.getStatus());
        }

        // Add Java results to root node
        rootNode.set(System.getProperty("os.name")+"_Java", javaNode);

        // Write updated JSON back to file
        writer.writeValue(file, rootNode);
        System.out.println("JSON file updated: " + fileName);
    }
}