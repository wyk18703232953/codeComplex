import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class ProcessResults {
    public static void main(String[] args) throws Exception {
        String inputFile = "d:/MyResearch/codeComplex/auto1/results.jsonl";
        String outputFile = "d:/MyResearch/codeComplex/auto1/processed_results.json";
        
        List<JsonObject> entries = new ArrayList<>();
        
        // Read and process each line from results.jsonl
        try (BufferedReader reader = Files.newBufferedReader(Paths.get(inputFile))) {
            String line;
            int lineNumber = 1;
            while ((line = reader.readLine()) != null) {
                JsonObject obj = new JsonObject(line);
                obj.sampleId = lineNumber;
                
                // Compare estimated_complexity with the original complexity field
                String originalComplexity = obj.get("complexity");
                String estimatedComplexity = obj.get("estimated_complexity");
                obj.isMatch = originalComplexity != null && originalComplexity.equals(estimatedComplexity);
                
                entries.add(obj);
                lineNumber++;
            }
        }
        
        // Calculate summary statistics
        int total = entries.size();
        int correct = 0;
        for (JsonObject obj : entries) {
            if (obj.isMatch) correct++;
        }
        int incorrect = total - correct;
        double accuracy = total > 0 ? (double) correct / total * 100 : 0.0;
        
        // Write the processed results to a new JSON file
        try (BufferedWriter writer = Files.newBufferedWriter(Paths.get(outputFile))) {
            writer.write("{");
            writer.write("\"entries\": [");
            
            // Write all entries
            for (int i = 0; i < entries.size(); i++) {
                JsonObject obj = entries.get(i);
                writer.write(obj.toJsonString());
                if (i < entries.size() - 1) {
                    writer.write(",");
                }
            }
            
            writer.write("],");
            writer.write("\"summary\": {");
            writer.write("\"total\": " + total + ",");
            writer.write("\"correct\": " + correct + ",");
            writer.write("\"incorrect\": " + incorrect + ",");
            writer.write("\"accuracy\": " + String.format("%.2f", accuracy));
            writer.write("}");
            writer.write("}");
        }
        
        System.out.println("Processing completed. Output saved to " + outputFile);
        System.out.println("Summary:");
        System.out.println("- Total entries: " + total);
        System.out.println("- Correct matches: " + correct);
        System.out.println("- Incorrect matches: " + incorrect);
        System.out.println("- Accuracy: " + String.format("%.2f", accuracy) + "%");
    }
    
    // Simple JSON object representation to handle parsing and modification
    static class JsonObject {
        private String originalJson;
        int sampleId;
        boolean isMatch;
        
        public JsonObject(String jsonString) {
            this.originalJson = jsonString;
        }
        
        // Extract value for a given key (supports string values only)
        public String get(String key) {
            int keyIndex = originalJson.indexOf("\"" + key + "\":");
            if (keyIndex == -1) return null;
            
            // Calculate value start position correctly
            int valueStart = keyIndex + ("\"" + key + "\" :").length();
            // Adjust for actual colon position (without assuming space)
            int actualColonIndex = originalJson.indexOf(":", keyIndex);
            if (actualColonIndex != -1) {
                valueStart = actualColonIndex + 1;
            }
            
            // Skip whitespace
            while (valueStart < originalJson.length() && 
                   (originalJson.charAt(valueStart) == ' ' || originalJson.charAt(valueStart) == '\t')) {
                valueStart++;
            }
            
            // Check if value is a string (starts with ")
            if (valueStart < originalJson.length() && originalJson.charAt(valueStart) == '"') {
                valueStart++;
                int valueEnd = valueStart;
                boolean inString = true;
                boolean escaped = false;
                
                while (valueEnd < originalJson.length() && inString) {
                    char c = originalJson.charAt(valueEnd);
                    if (escaped) {
                        escaped = false;
                    } else if (c == '\\') {
                        escaped = true;
                    } else if (c == '"') {
                        inString = false;
                    }
                    valueEnd++;
                }
                
                if (inString) return null;
                return originalJson.substring(valueStart, valueEnd - 1);
            }
            
            return null;
        }
        
        // Convert to JSON string with added fields
        public String toJsonString() {
            if (originalJson.endsWith("}")) {
                return originalJson.substring(0, originalJson.length() - 1) + 
                       ",\"sample_id\":" + sampleId + 
                       ",\"is_match\":" + isMatch + 
                       "}";
            }
            return originalJson;
        }
    }
}