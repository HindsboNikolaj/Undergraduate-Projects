// --== CS400 File Header Information ==--                                                                                                                                                                             
// Name: <Chapin Pyne>                                                                                                                                                                                                 
// Email: <crpyne@wisc.edu>                                                                                                                                                                                            
// Team: <CC>                                                                                                                                                                                                          
// TA: <Yeping>                                                                                                                                                                                                        
// Lecturer: <Florian Heimerl>                                                                                                                                                                                         
// Notes to Grader: <>   
import static org.junit.Assert.assertNotNull;
import java.util.ArrayList;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.NoSuchElementException;
public class TestPathfinder {
    private CS400Graph graph;
    ArrayList<String> classes;
    BackEnd backTester;
    @BeforeEach
    public void init() {
        graph = Data.getGraph();
        backTester = new BackEnd();
        classes = new ArrayList();
        String[] temp = {"sellery", "chemistry" , "engineering", "humanities", "frats", "bascom", "agriculture", "lakeshore"};
        for(int i = 0; i<temp.length; i++){
            classes.add(temp[i]);
        }
    }
    @Test
    //Check for the correct number of vertexes and edges                                                                                                                                                               
    public void graphVertexAndEdgeAmount() {
        assertTrue(graph.getVertexCount() == 8);
        assertTrue(graph.getEdgeCount() == 38);
    }
    @Test
    //check that all vertexes have a path to all other vertexes.                                                                                                                                                       
    public void graphPathsExist() {
    	
        for(int outer = 0; outer < Data.Integer.values().length; outer++) {
            for(int inner = 0; inner < Data.Integer.values().length; inner++) {
                //throws NoSuchElementException if path or node does not exist                                                                                                                                         
                assertNotNull(graph.shortestPath(Data.Integer.values()[inner], Data.Integer.values()[outer]));
            }
        }
    }
    @Test
    //Makes sure an exception is thrown for a bad input in BackEnd                                                                                                                                                     
    public void backEndWrongInput() {
        assertThrows(NoSuchElementException.class, () -> backTester.findShortestPath("wrong input", classes));
    }
    @Test
    //Makes sure the dorms returns a string                                                                                                                                                                            
    public void dorms() {
        backTester.findShortestPath("sellery", classes);
        backTester.findShortestPath("lakeshore", classes);
    }
}
