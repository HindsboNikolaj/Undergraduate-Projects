// --== CS400 File Header Information ==--
// Name: <Tony Busko>
// Email: <awbusko@wisc.edu>
// Team: <CC>
// TA: <Yeping>
// Lecturer: <Gary Dahl>
// Notes to Grader: <optional extra notes>

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.ArrayList;
import java.util.NoSuchElementException;


/**
 * Tests the methods and function of the different functions regarding this project
 */
public class TestApp {
  private CS400Graph<Data.Integer> graph;
  private ArrayList<String> classes;
  BackEnd back;
  
  /**
   * Sets up a graph from the data class, a BackEnd object to perform methods off of, and creates a set of classes
   */
  @BeforeEach
  public void createTestGraph() {
    Data d = new Data();
    graph = d.getGraph();
    classes = new ArrayList<String>();
    classes.add("engineering");
    classes.add("bascom");
    classes.add("humanities");
    classes.add("frats");
    back = new BackEnd();
  }
  
  /**
   * Creates the graph from the data class and makes sure the correct number of verticies and edges
   * are present. Also checks a couple of edges within the graph to see if they are there.
   */
  @Test
  public void testGraphCreation() {  
    assertTrue(graph.getVertexCount() == 8); 
    assertTrue(graph.getEdgeCount() == 38); 
    assertTrue(graph.containsEdge(Data.Integer.lakeshore, Data.Integer.agriculture));
    assertTrue(graph.containsEdge(Data.Integer.frats, Data.Integer.bascom));
    assertTrue(graph.containsEdge(Data.Integer.lakeshore, Data.Integer.bascom)); 
    assertTrue(graph.containsEdge(Data.Integer.bascom, Data.Integer.lakeshore)); 
    assertTrue(graph.containsEdge(Data.Integer.sellery, Data.Integer.engineering)); 
    assertTrue(graph.containsEdge(Data.Integer.engineering, Data.Integer.sellery)); 
  }
  
  
  //Tests to see of an error is thrown if an incorrect parameter is passed
  @Test 
  public void testFindShortestPathErrorThrown() {
    boolean thrown = false;
    
    try {
      back.findShortestPath("engineering", classes);
    } catch (NoSuchElementException e) {
      thrown = true;
    }
    
    assertTrue(thrown);
  }
  
  //Tests to see if the shortest path distance is calculated correctly
  @Test
  public void testFindShortestPathDistance() {
    String statement = back.findShortestPath("sellery", classes);
    int index = statement.indexOf("miles");
    assertTrue(statement.substring(index - 4, index - 1).equals("1.2")); 
    
  }
  

  /**
   * Tests to see if the provided path is the correct path. The backend is not working
   * correctly making which puts agriculture in place of where engineering should be.
   */
  @Test
  public void testFindShortestPath() {
    String statement = back.findShortestPath("sellery", classes);
    System.out.println(back.findShortestPath("sellery", classes));
    String correctStatement = "Shortest Path calculated!\nTo minimize your walk, you should take the path:\nsellery --> " +
        "agriculture --> humanities --> frats --> bascom --> sellery\nThis path takes about " + "1.2" + " miles"; 
    assertTrue(statement.equals(correctStatement));
  }



}
