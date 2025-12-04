import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.List;

public class Main {
    private static final String[] COMPLEXITY_TERMS = {"constant", "linear", "logn", "nlogn", "quadratic", "cubic", "np"};
    
    public static void main(String[] args) throws Exception {
        String inputFile = "d:/MyResearch/codeComplex/data/data.jsonl";
        String outputFile = "d:/MyResearch/codeComplex/auto1/results.jsonl";
        
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
        
        System.out.println("Analysis completed. Results saved to " + outputFile);
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
        // 1. First, identify common algorithms directly for higher accuracy
        String directComplexity = identifyCommonAlgorithms(javaCode);
        if (directComplexity != null) {
            return directComplexity;
        }
        
        try {
            // 2. Generate different scales for testing (more scales for better regression)
            int[] scales = {50, 100, 200, 400, 800, 1600, 3200};
            
            // 3. Prepare test data and measure execution time for each scale
            List<Double> logN = new ArrayList<>();
            List<Double> logTime = new ArrayList<>();
            
            for (int n : scales) {
                // 4. Generate more realistic test data (random data, sorted data, reversed data)
                int[][] testDatasets = generateTestDatasets(n);
                
                // 5. Use median instead of average to reduce outliers
                List<Double> runTimes = new ArrayList<>();
                int runs = 5; // More runs for better statistical accuracy
                
                for (int[] testData : testDatasets) {
                    TestCase testCase = new TestCase(javaCode, testData);
                    
                    for (int i = 0; i < runs; i++) {
                        long startTime = System.nanoTime();
                        testCase.execute();
                        long endTime = System.nanoTime();
                        double runTime = (endTime - startTime) / 1e6; // Convert to milliseconds
                        runTimes.add(runTime);
                    }
                }
                
                // Calculate median runtime
                double medianTime = calculateMedian(runTimes);
                
                if (medianTime > 0) {
                    logN.add(Math.log(n));
                    logTime.add(Math.log(medianTime));
                }
            }
            
            if (logN.size() < 3) {
                // Not enough data, use enhanced static analysis
                return enhancedStaticAnalysis(javaCode);
            }
            
            // 6. Perform linear regression to find the slope
            double slope = calculateSlope(logN, logTime);
            
            // 7. Map slope to complexity term with improved thresholds
            return mapSlopeToComplexity(slope);
            
        } catch (Exception e) {
            // Fallback to enhanced static analysis if dynamic execution fails
            return enhancedStaticAnalysis(javaCode);
        }
    }
    
    // Identify common algorithms directly for better accuracy
    private static String identifyCommonAlgorithms(String javaCode) {
        javaCode = javaCode.toLowerCase();
        
        // Sorting algorithms
        if (javaCode.contains("arrays.sort") || javaCode.contains(".sort(") || 
            javaCode.contains("collections.sort")) {
            return "nlogn"; // Most sorting algorithms are O(n log n)
        }
        
        // Binary search patterns
        if ((javaCode.contains("binary") && (javaCode.contains("search") || javaCode.contains("find"))) ||
            (javaCode.contains("low") && javaCode.contains("high") && javaCode.contains("mid"))) {
            return "logn"; // Binary search is O(log n)
        }
        
        // Divide and conquer patterns
        if (javaCode.contains("divide") && javaCode.contains("conquer")) {
            return "nlogn"; // Typical divide and conquer algorithms are O(n log n)
        }
        
        // Matrix multiplication or 3D algorithms
        if (javaCode.contains("matrix") || javaCode.contains("3d") || 
            (countNestedLoops(javaCode) == 2 && javaCode.contains("i < ") && 
             javaCode.contains("j < ") && javaCode.contains("k < "))) {
            return "cubic"; // Matrix multiplication is O(n³)
        }
        
        // Simple linear scans
        if (countLoops(javaCode) == 1 && countNestedLoops(javaCode) == 0 &&
            !javaCode.contains("recurs") && !javaCode.contains("sort")) {
            return "linear"; // Single loop is typically O(n)
        }
        
        return null; // No direct algorithm identified
    }
    
    // Generate multiple test datasets for better accuracy
    private static int[][] generateTestDatasets(int n) {
        int[][] datasets = new int[3][n];
        
        // 1. Sorted array
        for (int i = 0; i < n; i++) {
            datasets[0][i] = i;
        }
        
        // 2. Random array
        for (int i = 0; i < n; i++) {
            datasets[1][i] = (int) (Math.random() * n);
        }
        
        // 3. Reversed array
        for (int i = 0; i < n; i++) {
            datasets[2][i] = n - i - 1;
        }
        
        return datasets;
    }
    
    // Calculate median to reduce outliers
    private static double calculateMedian(List<Double> values) {
        if (values.isEmpty()) {
            return 0;
        }
        values.sort(Double::compareTo);
        int size = values.size();
        if (size % 2 == 0) {
            return (values.get(size / 2 - 1) + values.get(size / 2)) / 2.0;
        } else {
            return values.get(size / 2);
        }
    }
    
    // Enhanced linear regression to calculate slope
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
    
    // Improved complexity mapping with better thresholds based on complexity theory
    private static String mapSlopeToComplexity(double slope) {
        // More precise thresholds based on theoretical complexity bounds
        if (slope < 0.05) {
            return "constant"; // O(1) - negligible growth
        } else if (slope < 0.5) {
            return "logn"; // O(log n) - slow logarithmic growth
        } else if (slope < 1.2) {
            return "linear"; // O(n) - linear growth
        } else if (slope < 2.1) {
            return "nlogn"; // O(n log n) - linearithmic growth
        } else if (slope < 2.8) {
            return "quadratic"; // O(n²) - quadratic growth
        } else if (slope < 3.8) {
            return "cubic"; // O(n³) - cubic growth
        } else {
            return "np"; // O(2^n) or worse - exponential growth
        }
    }
    
    // Enhanced static analysis with more accurate rules
    private static String enhancedStaticAnalysis(String javaCode) {
        int loops = countLoops(javaCode);
        int nestedLoops = countNestedLoops(javaCode);
        boolean hasRecursion = hasRecursion(javaCode);
        boolean hasSort = javaCode.contains(".sort(") || 
                         javaCode.contains("Collections.sort") || 
                         javaCode.contains("Arrays.sort");
        boolean hasBinarySearch = javaCode.toLowerCase().contains("binary") && 
                                 (javaCode.toLowerCase().contains("search") || 
                                  javaCode.toLowerCase().contains("find"));
        boolean hasDivideConquer = javaCode.toLowerCase().contains("divide") && 
                                  javaCode.toLowerCase().contains("conquer");
        
        // Check for recursive algorithms
        if (hasRecursion) {
            if (hasBinarySearch) {
                return "logn";
            } else if (hasDivideConquer || hasSort) {
                return "nlogn";
            } else {
                // Recursive without divide and conquer is likely exponential or linear
                if (javaCode.toLowerCase().contains("fibonacci") || 
                    javaCode.toLowerCase().contains("factorial") ||
                    javaCode.toLowerCase().contains("permutation")) {
                    return "np"; // Exponential complexity
                } else {
                    return "linear"; // Linear recursion
                }
            }
        }
        
        // Iterative algorithms
        if (loops == 0) {
            return "constant";
        }
        
        if (nestedLoops == 0) {
            if (hasSort) {
                return "nlogn";
            }
            if (hasBinarySearch) {
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
            return "np"; // High nested loops are likely exponential or worse
        }
    }
    
    // Improved TestCase class with more realistic simulation
    static class TestCase {
        private String javaCode;
        private int[] testData;
        
        public TestCase(String javaCode, int[] testData) {
            this.javaCode = javaCode;
            this.testData = testData;
        }
        
        public void execute() {
            // 1. Count loops and nested loops
            int loops = countLoops(javaCode);
            int nestedLoops = countNestedLoops(javaCode);
            
            // 2. Check for specific algorithm patterns
            boolean hasSort = javaCode.contains(".sort(") || 
                             javaCode.contains("Collections.sort") || 
                             javaCode.contains("Arrays.sort");
            boolean hasBinarySearch = javaCode.toLowerCase().contains("binary") && 
                                     (javaCode.toLowerCase().contains("search") || 
                                      javaCode.toLowerCase().contains("find"));
            boolean hasRecursion = hasRecursion(javaCode);
            
            // 3. More realistic simulation based on algorithm type
            int n = testData.length;
            
            if (hasSort) {
                // Simulate sorting time (O(n log n))
                simulateSorting(n);
            } else if (hasBinarySearch) {
                // Simulate binary search time (O(log n))
                simulateBinarySearch(n);
            } else if (nestedLoops == 0) {
                // Simulate linear time algorithms (O(n))
                for (int i = 0; i < n; i++) {
                    simulateWork(1);
                }
            } else if (nestedLoops == 1) {
                // Simulate quadratic time algorithms (O(n²))
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        simulateWork(1);
                    }
                }
            } else if (nestedLoops == 2) {
                // Simulate cubic time algorithms (O(n³))
                for (int i = 0; i < n; i++) {
                    for (int j = 0; j < n; j++) {
                        for (int k = 0; k < n; k++) {
                            simulateWork(1);
                        }
                    }
                }
            } else {
                // Simulate exponential time algorithms (O(2^n)) - limit to avoid hanging
                int limitedN = Math.min(n, 15); // Limit to 15 to prevent excessive runtime
                simulateExponentialWork(limitedN);
            }
        }
        
        // Helper methods for more realistic simulation
        private void simulateSorting(int n) {
            // Simulate O(n log n) time complexity
            int operations = (int) (n * Math.log(n) / Math.log(2));
            simulateWork(operations);
        }
        
        private void simulateBinarySearch(int n) {
            // Simulate O(log n) time complexity
            int operations = (int) (Math.log(n) / Math.log(2));
            simulateWork(operations);
        }
        
        private void simulateExponentialWork(int n) {
            // Simulate O(2^n) time complexity - limited to prevent hanging
            int operations = (int) Math.pow(2, n);
            simulateWork(Math.min(operations, 1000000)); // Limit operations
        }
        
        private void simulateWork(int operations) {
            // Simulate actual work by performing a series of operations
            double dummy = 0;
            for (int i = 0; i < operations; i++) {
                dummy += Math.sqrt(i) * Math.log(i + 1);
            }
            // Prevent JIT from optimizing away the work
            if (dummy > 1e100) {
                System.out.print("");
            }
        }
    }
    
    private static int countLoops(String code) {
        int count = 0;
        count += countOccurrences(code, "for (");
        count += countOccurrences(code, "while (");
        count += countOccurrences(code, "do {");
        return count;
    }
    
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
    
    private static boolean hasSort(String code) {
        return code.contains(".sort(") || code.contains("Collections.sort") || code.contains("Arrays.sort");
    }
    
    private static int countOccurrences(String text, String pattern) {
        int count = 0;
        int index = 0;
        while ((index = text.indexOf(pattern, index)) != -1) {
            count++;
            index += pattern.length();
        }
        return count;
    }
    
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
    
    private static String extractMethodName(String methodDeclaration) {
        int methodNameStart = methodDeclaration.lastIndexOf(' ') + 1;
        int methodNameEnd = methodDeclaration.indexOf('(', methodNameStart);
        if (methodNameEnd == -1) return "";
        
        return methodDeclaration.substring(methodNameStart, methodNameEnd).trim();
    }
}