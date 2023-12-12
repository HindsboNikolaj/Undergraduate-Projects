import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.BeforeEach;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;
import java.util.NoSuchElementException;

public class TestPathfinder {
	private CS400Graph graph;
	String[] classes = {"chemistry" , "engineering", "humanities", "frats", "bascom", "agriculture"};
	BackEnd backTester;
	@BeforeEach
	private void init() {
		graph = Data.getGraph();
		backTester = new BackEnd();
	}
	
	@Test
	//Check for the correct number of vertexes and edges
	private void graphVertexAndEdgeAmount() {
	    assertTrue(graph.getVertexCount() == 8); 
	    assertTrue(graph.getEdgeCount() == 32);
	}
	
	@Test
    //check that all vertexes have a path to all other vertexes.
	private void graphPathsExist() {
	    for(int outer = 0; outer < Data.Integer.values().length; outer++) {
	    	for(int inner = 0; inner < Data.Integer.values().length; inner++) {
	    		//throws NoSuchElementException if path or node does not exist
	    		graph.dijkstrasShortestPath(outer, inner);
	    	}
	    }
	}
	
	@Test
	//Makes sure an exception is thrown for a bad input in BackEnd
	private void backEndWrongInput() {
		assertThrows(NoSuchElementException.class, () -> backTester.findShortestPath("wrong input", classes));
	}
	
	@Test
	//Makes sure the dorms returns a string
	private void dorms() {
		backTester.findShortestPath("sellery", classes);
		backTester.findShortestPath("lakeshore", classes);
	}
	
}
