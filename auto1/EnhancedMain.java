import java.io.*;
import java.lang.reflect.Method;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;
import java.util.concurrent.TimeUnit;

public class EnhancedMain {
    private static final String[] COMPLEXITY_TERMS = {"constant", "linear", "logn", "nlogn", "quadratic", "cubic", "np"};
    
    public static void main(String[] args) throws Exception {
        String inputFile = "d:/MyResearch/codeComplex/data/data.jsonl";
        String outputFile = "d:/MyResearch/codeComplex/auto1/enhanced_results.jsonl";
        
        try (BufferedReader reader = Files.newBufferedReader(Paths.get(inputFile));
             BufferedWriter writer = Files.newBufferedWriter(Paths.get(outputFile))) {
            
            String line;
            while ((line = reader.readLine()) != null) {
                String src = extractSrcFromJson(line);
                
                String complexity = estimateComplexity(src);
                
                String result = addEstimatedComplexity(line, complexity);
                writer.write(result);
                writer.newLine();
            }
        }
        
        System.out.println("Enhanced analysis completed. Results saved to " + outputFile);
    }
    
    private static String extractSrcFromJson(String jsonLine) {
        int srcStart = jsonLine.indexOf("\"src\":");
        if (srcStart == -1) return "";
        
        srcStart += "\"src\":".length();
        
        while (srcStart < jsonLine.length() && (jsonLine.charAt(srcStart) == ' ' || jsonLine.charAt(srcStart) == '\t')) {
            srcStart++;
        }
        
        if (srcStart < jsonLine.length() && jsonLine.charAt(srcStart) == '"') {
            srcStart++;
            int srcEnd = srcStart;
            boolean inString = true;
            boolean escaped = false;
            
            while (srcEnd < jsonLine.length() && inString) {
                char c = jsonLine.charAt(srcEnd);
                if (escaped) {
                    escaped = false;
                } else if (c == '\\') {
                    escaped = true;
                } else if (c == '"') {
                    inString = false;
                }
                srcEnd++;
            }
            
            if (inString) return "";
            
            return jsonLine.substring(srcStart, srcEnd - 1);
        }
        
        return "";
    }
    
    private static String addEstimatedComplexity(String jsonLine, String complexity) {
        if (jsonLine.endsWith("}")) {
            return jsonLine.substring(0, jsonLine.length() - 1) + ",\"estimated_complexity\":\"" + complexity + "\"}";
        }
        return jsonLine;
    }
    
    private static String estimateComplexity(String javaCode) {
        try {
            // Generate different scales for testing
            int[] scales = {100, 200, 400, 800, 1600};
            
            // Prepare test data and measure execution time for each scale
            List<Double> logN = new ArrayList<>();
            List<Double> logTime = new ArrayList<>();
            
            for (int n : scales) {
                // Generate test data
                int[] testData = new int[n];
                for (int i = 0; i < n; i++) {
                    testData[i] = i;
                }
                
                // Create a test case that can be executed
                TestCase testCase = new TestCase(javaCode, testData);
                
                // Measure execution time (average of 3 runs)
                long totalTime = 0;
                int runs = 3;
                
                for (int i = 0; i < runs; i++) {
                    long startTime = System.nanoTime();
                    testCase.execute();
                    long endTime = System.nanoTime();
                    totalTime += (endTime - startTime);
                }
                
                double avgTime = (double) totalTime / runs;
                avgTime = avgTime / 1e6; // Convert to milliseconds
                
                if (avgTime > 0) {
                    logN.add(Math.log(n));
                    logTime.add(Math.log(avgTime));
                }
            }
            
            if (logN.size() < 2) {
                return "constant"; // Fallback to constant if not enough data
            }
            
            // Perform linear regression to find the slope
            double slope = calculateSlope(logN, logTime);
            
            // Map slope to complexity term
            return mapSlopeToComplexity(slope);
            
        } catch (Exception e) {
            // Fallback to simple static analysis if dynamic execution fails
            return simpleStaticAnalysis(javaCode);
        }
    }
    
    // Simple linear regression to calculate slope
    private static double calculateSlope(List<Double> x, List<Double> y) {
        int n = x.size();
        double sumX = 0, sumY = 0, sumXY = 0, sumX2 = 0;
        
        for (int i = 0; i < n; i++) {
            sumX += x.get(i);
            sumY += y.get(i);
            sumXY += x.get(i) * y.get(i);
            sumX2 += x.get(i) * x.get(i);
        }
        
        double denominator = n * sumX2 - sumX * sumX;
        if (denominator == 0) {
            return 0;
        }
        
        return (n * sumXY - sumX * sumY) / denominator;
    }
    
    // Map slope value to complexity term
    private static String mapSlopeToComplexity(double slope) {
        // Define thresholds for each complexity type
        if (slope < 0.1) {
            return "constant"; // O(1)
        } else if (slope < 0.6) {
            return "logn"; // O(log n)
        } else if (slope < 1.4) {
            return "linear"; // O(n)
        } else if (slope < 1.9) {
            return "nlogn"; // O(n log n)
        } else if (slope < 2.6) {
            return "quadratic"; // O(n²)
        } else if (slope < 3.6) {
            return "cubic"; // O(n³)
        } else {
            return "np"; // O(2^n) or worse
        }
    }
    
    // Simple static analysis as fallback
    private static String simpleStaticAnalysis(String javaCode) {
        int loops = countLoops(javaCode);
        int nestedLoops = countNestedLoops(javaCode);
        boolean hasRecursion = hasRecursion(javaCode);
        boolean hasSort = hasSort(javaCode);
        
        if (loops == 0 && !hasRecursion) {
            return "constant";
        }
        
        if (nestedLoops == 0) {
            if (hasSort) {
                return "nlogn";
            }
            if (hasRecursion && (javaCode.contains("divide") || javaCode.contains("binary"))) {
                return "logn";
            }
            return "linear";
        } else if (nestedLoops == 1) {
            if (hasSort) {
                return "nlogn";
            }
            return "quadratic";
        } else if (nestedLoops == 2) {
            return "cubic";
        } else {
            return "np";
        }
    }
    
    // Helper method to count loops
    private static int countLoops(String code) {
        int count = 0;
        count += countOccurrences(code, "for (");
        count += countOccurrences(code, "while (");
        count += countOccurrences(code, "do {");
        return count;
    }
    
    // Helper method to count nested loops
    private static int countNestedLoops(String code) {
        int maxDepth = 0;
        int currentDepth = 0;
        
        String[] lines = code.split("\\n");
        for (String line : lines) {
            line = line.trim();
            if (line.startsWith("for (") || line.startsWith("while (") || line.startsWith("do {")) {
                currentDepth++;
                maxDepth = Math.max(maxDepth, currentDepth);
            } else if (line.startsWith("}") && currentDepth > 0) {
                currentDepth--;
            }
        }
        
        return Math.max(0, maxDepth - 1);
    }
    
    // Helper method to check for recursion
    private static boolean hasRecursion(String code) {
        String className = extractClassName(code);
        if (className.isEmpty()) return false;
        
        int methodStart = code.indexOf("public ");
        while (methodStart != -1) {
            int methodEnd = code.indexOf("{", methodStart);
            if (methodEnd == -1) break;
            
            String methodDeclaration = code.substring(methodStart, methodEnd);
            if (methodDeclaration.contains("static") && methodDeclaration.contains("void") && 
                !methodDeclaration.contains("main")) {
                
                String methodName = extractMethodName(methodDeclaration);
                if (!methodName.isEmpty()) {
                    int methodBodyStart = methodEnd;
                    int braceCount = 1;
                    int methodBodyEnd = methodBodyStart + 1;
                    
                    while (methodBodyEnd < code.length() && braceCount > 0) {
                        char c = code.charAt(methodBodyEnd);
                        if (c == '{') braceCount++;
                        else if (c == '}') braceCount--;
                        methodBodyEnd++;
                    }
                    
                    String methodBody = code.substring(methodBodyStart, methodBodyEnd);
                    if (methodBody.contains(methodName + "(")) {
                        return true;
                    }
                }
            }
            
            methodStart = code.indexOf("public ", methodEnd);
        }
        
        return false;
    }
    
    // Helper method to check for sort operations
    private static boolean hasSort(String code) {
        return code.contains(".sort(") || code.contains("Collections.sort") || code.contains("Arrays.sort");
    }
    
    // Helper method to count occurrences
    private static int countOccurrences(String text, String pattern) {
        int count = 0;
        int index = 0;
        while ((index = text.indexOf(pattern, index)) != -1) {
            count++;
            index += pattern.length();
        }
        return count;
    }
    
    // Helper method to extract class name
    private static String extractClassName(String code) {
        int classStart = code.indexOf("public class ");
        if (classStart == -1) {
            classStart = code.indexOf("class ");
            if (classStart == -1) return "";
        } else {
            classStart += "public class ".length();
        }
        
        int classEnd = code.indexOf("{", classStart);
        if (classEnd == -1) return "";
        
        return code.substring(classStart, classEnd).trim();
    }
    
    // Helper method to extract method name
    private static String extractMethodName(String methodDeclaration) {
        int methodNameStart = methodDeclaration.lastIndexOf(' ') + 1;
        int methodNameEnd = methodDeclaration.indexOf('(', methodNameStart);
        if (methodNameEnd == -1) return "";
        
        return methodDeclaration.substring(methodNameStart, methodNameEnd).trim();
    }
    
    // Inner class to handle test case execution
    static class TestCase {
        private String javaCode;
        private int[] testData;
        
        public TestCase(String javaCode, int[] testData) {
            this.javaCode = javaCode;
            this.testData = testData;
        }
        
        public void execute() {
            // This is a simplified implementation
            // In a real scenario, we would need to:
            // 1. Parse the Java code
            // 2. Extract the main logic
            // 3. Compile it dynamically
            // 4. Execute it with the test data
            // 5. Handle any exceptions
            
            // For now, we'll simulate execution based on code features
            // This is just a placeholder - in a real implementation, we would need a proper Java compiler API
            
            // Count loops and simulate execution time based on loop count and data size
            int loops = countLoops(javaCode);
            int nestedLoops = countNestedLoops(javaCode);
            
            // Simulate work based on loop complexity
            int n = testData.length;
            
            if (nestedLoops == 0) {
                // O(n) or O(log n)
                for (int i = 0; i < n; i++) {
                    // Simulate work
                    double dummy = Math.sqrt(i);
                }
            } else if (nestedLoops == 1) {
                // O(n²)
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        double dummy = Math.sqrt(i * j);
                    }
                }
            } else if (nestedLoops == 2) {
                // O(n³)
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        for (int k = 0; k < n; k++) {
                            double dummy = Math.sqrt(i * j * k);
                        }
                    }
                }
            }
        }
    }
}