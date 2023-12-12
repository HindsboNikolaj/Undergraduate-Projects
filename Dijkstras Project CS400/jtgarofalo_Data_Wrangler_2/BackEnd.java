import java.util.ArrayList;
import java.util.NoSuchElementException;
//--== CS400 File Header Information ==--
//Name: Nikolaj Hindsbo
//Email: hindsbo@wisc.edu
//Team: CC
//Role: BackEnd 1
//TA: Yeping
//Lecturer: Florian Heimerl
//Notes to Grader: 

/*
 * The purpose of this class is to implement the brute-force
 * approach to the traveling salesman problem to find the shortest
 * path A-->B--->C-->A that the person should take using dijkstra's algorithm
 * (I used brute force because usually you would only at MOST have 3-5 classes a day, so 
 * the number of checks is relatively low to allow for the complete accuracy.
 * E.g. 
 * User has classes at Van Vleck, Bascom, Engineering, and Chem, and lives at lakeshore.
 * This class will calculate the path that would result in him walking the least like for example
 * the min path might look like:
 * Lakeshore --> Engineering --> Chem --> Bascom --> Lakeshore
 */

public class BackEnd {
  
  /*
   * This method finds the shortest round path that the user should take: starting at their dorm, visiting
   * all of their classes, and returning back to their dorm.
   * @param dorm - the String name of the dorm that they live at
   * @param classes - the classes that the user is going to take
   * @returns - the String representation of the order of the classes
   *             the user should take to minimize distance walked.
   * @throws - NoSuchElementException - if an invalid dorm was selected.
   */
  
  public static String findShortestPath(String dorm, ArrayList<String> classes){
    
    // Mapgraph is implemented by backend, to contain appropriate nodes for classes on campus.
    CS400Graph<Data.Integer> madisonGraph = Data.getGraph();
    
    /*
     * Classes are ordered as:
     * Sellery = 1
     * Chem = 2
     * Eng = 3
     * Human. = 4
     * Frat = 5
     * Bascom = 6
     * Ag = 7
     * Lakeshore = 8
     */
    // Get all values of possible classes
    Data.Integer[] allClasses = Data.Integer.values();
    ArrayList<Integer> intValueClasses = new ArrayList<Integer>();
    Data.Integer dormDataInt;
    int dormInt;
    if(dorm.equals("sellery")) {
      dormDataInt = Data.Integer.sellery;
      dormInt = 1;
    }
    else if(dorm.equals("lakeshore")) {
      dormDataInt = Data.Integer.lakeshore;
      dormInt = 8;
    }
    else {
      throw new NoSuchElementException("Error, invalid dorm selected");
    }
    int temp = 0;
    boolean alreadyContains = false;
    // Convert strings to ints (so we can find permutations easier)
    for(int i = 0; i < allClasses.length; i++) {
      for(int j = 0; j < classes.size(); j++) {
        if(classes.get(j).equalsIgnoreCase(allClasses[i].name())) {
          alreadyContains = false;
          for(int k = 0; k < intValueClasses.size(); k++) {
            if(intValueClasses.get(k).equals(i+1)) {
                alreadyContains = true;
            }
            
            // If the value isn't already contained, add it to the int values we need to explore.
          }
          if(!alreadyContains) {
            intValueClasses.add(new Integer(i));
            temp++;
          }
          // Only adds classes that aren't added yet. E.g. 
          
        }
      }
    }
    System.out.println(intValueClasses.toString());
    // Make this Arraylist into an array of Integers
    Integer[] intClasses = new Integer[intValueClasses.size()];
    for(int i = 0; i < intClasses.length; i++) {
      intClasses[i] = intValueClasses.get(i);
    }
    
    // Number of nodes determines the number of possible paths we need to bruteforce (n!)
    // The findAllPerms finds all permutations of the possible classes.
    ArrayList<ArrayList<Integer>> allPerms = findAllPermutations(intClasses);
   
 
    // Find the shortest path possible. This will also have the path cost at the end of the List.
    ArrayList<Integer> shortestPath = findShortestPathHelper(allClasses, allPerms, 
        madisonGraph, dormDataInt, intClasses);
    
    double shortestDistance = shortestPath.get(shortestPath.size()-1);
    shortestDistance = shortestDistance/10;
    // Now delete the distance from the list.
    shortestPath.remove(shortestPath.size()-1);
    
    System.out.println("Shortest path " + shortestPath);
    
    // Convert the shortest path int combination into a string that can be returned to the user, along
    // with the distance that they need to walk.
    
    String returnString = pathHelper(shortestPath, allClasses, dormInt, shortestDistance);    
    
    return returnString;
  }
  
  /*
   * This helper method helps convert the Arraylist of Integer shortest path 
   * to a String that helps the user understand what the shortest path he should take is.
   * @param shortestPath - The Arraylist of Integer values that correspond to the order the User should 
   *                       take their classes to minimize distance.
   * @param - allClasses - The enum values of all possible classes
   * @param - dormInt - the int location of their dorm in the allClasses array
   * @param - shortestDistance - the integer value of distance the path took
   * @return - the String representation of the path passed
   */
  
  private static String pathHelper(ArrayList<Integer> shortestPath, Data.Integer[] allClasses, 
    int dormInt, double shortestDistance) {
    // Basic message
    String builder = "Shortest Path calculated!\n";
    builder += "To minimize your walk, you should take the path:\n";
    // Add the dorm
    builder += allClasses[dormInt-1].name() + " --> ";
    for(int i = 0; i < shortestPath.size(); i++) {
      // Adds all classes to the string
      builder += allClasses[shortestPath.get(i)] + " --> ";
    }
    // Adds the dorm
    builder += allClasses[dormInt-1].name() + "\n";
    builder += "This path takes about " + shortestDistance + " miles";    
    // Now, return the full message.
    return builder;
  }

  /*
   * This is a helper method for the findShortestPath() method. It helps find the appropriate Integer
   * representation of the order (arraylist) that the user should walk to minimize distance.
   * @param - allClasses - The enum values of all possible classes
   * @param - allPerms - all permutations of possible orders that the path could be walked.
   * @param - madisonGraph - the CS400 Graph being used
   * @param - dormInt - the enum of the dorm that the user lives in
   * @param - intValueClasses - An array of Integers containing all of the user's classes (no duplicates).
   * @returns - the shortest round path available, based on the users classes to minimize distance.
   */
  
  private static ArrayList<Integer> findShortestPathHelper(Data.Integer[] allClasses, 
        ArrayList<ArrayList<Integer>> allPerms, CS400Graph<Data.Integer> madisonGraph, 
        Data.Integer dormInt, Integer[] intValueClasses){
    int shortestPathDistance = 0;
    int temp = 0;
    ArrayList<Integer> shortestPath = new ArrayList<Integer>();
    for(int i = 0; i < allPerms.size(); i++) {
      // Get one potential path
      
      temp = 0;
      ArrayList<Integer> currentPath = allPerms.get(i);
      // First, walk path from dorm --> First target
      temp+= madisonGraph.getPathCost(dormInt, allClasses[currentPath.get(0)]);
      for(int j = 0; j < currentPath.size()-1; j++) {
        // Walk path A--> B--> C --> D to find total distance for this permutation.
        temp += madisonGraph.getPathCost(allClasses[intValueClasses[j]], allClasses[currentPath.get(j+1)]);
      }
      // Last, walk path from last target --> dorm
      temp+= madisonGraph.getPathCost(allClasses[currentPath.get(currentPath.size()-1)], dormInt);
      // Replace the shortest path with current one if it took less distance, or 1st time.
      if(temp < shortestPathDistance || shortestPathDistance == 0) {
        shortestPathDistance = temp;
        shortestPath = currentPath;
      }
      
    }
    // Add the path cost to the end of the path, which will shortly be removed, so that both
    // the path and the cost are returned.
    shortestPath.add(shortestPathDistance);
    return shortestPath;
  }
  
  /*
   * This method helps find all permutations possible for an array of Integers
   * e.g. [1, 2, 3] [3, 2, 1] [2, 3, 1], etc.
   * @param - classes - an array of all classes that the user has
   * @returns - all permutations of the classes array
   */
  
  private static ArrayList<ArrayList<Integer>> findAllPermutations(Integer[] classes){
    ArrayList<ArrayList<Integer>> allPerms = new ArrayList<ArrayList<Integer>>();
    permHelper(0, classes, allPerms);
    return allPerms;
  }
  
  /*
   * Helper method for the permutations method. This is where most of the permutations are calculated.
   * @param - start - the index that the permutation function is starting at
   * @param - classes - the array of Integers that the permutations are being found for
   * @param - list - the current list of all permutations possible
   * @returns - None (it just changes the list).
   */
  
  private static void permHelper(int start, Integer[] classes, ArrayList<ArrayList<Integer>> list) {
    // This just makes sure that the original sequence is added.
    if(start==classes.length-1) {
      ArrayList<Integer> temp = new ArrayList<>();
      for(int i = 0; i < classes.length; i++) {
        temp.add(classes[i]);
      }
      list.add(temp);
    }
    // This accounts for all other permutations.
    for(int i = start; i < classes.length; i++) {
      swap(classes, i, start);
      permHelper(start + 1, classes, list);
      swap(classes, i, start);
    }
  }
  
  /*
   * Helper method for the permutations method. This just helps swap the values of two indices of the array.
   * @param - classes - the array where the swap is happening
   * @param - i - the index of one value being swapped.
   * @param - j - the index of the other value being swapped.
   * @returns None, just edits the classes array.
   */
  
  private static void swap(Integer[] classes, int i, int j) {
    int temp = classes[j];
    classes[j] = classes[i];
    classes[i] = temp;
  }
  
  
  
}


