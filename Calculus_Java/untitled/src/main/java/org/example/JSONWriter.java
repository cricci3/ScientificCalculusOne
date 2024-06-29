package org.example;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectWriter;

import java.io.File;
import java.io.IOException;
import java.util.List;

public class JSONWriter {
    public static void writeJSON(List<MatrixData> dataList) throws IOException {
        String fileName = "dati_java_" + System.getProperty("os.name").toLowerCase().replace(" ", "_") + ".json";
        ObjectMapper mapper = new ObjectMapper();
        ObjectWriter writer = mapper.writerWithDefaultPrettyPrinter();
        writer.writeValue(new File(fileName), new OutputWrapper(dataList));
        System.out.println("JSON file created: " + fileName);
    }
}