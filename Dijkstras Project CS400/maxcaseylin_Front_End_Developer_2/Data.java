// --== Data.java ==--
// Name:John Garofalo
// Email: jtgarofalo@wisc.edu
// Team: CC
// Role: Data Wrangler
// TA: Yeping Wang
// Lecturer: Florian Heimerl

/**
 * The Data class is all the base data that the wranglers provide, making use of
 * an enum we use this class to create the starting map of vertexs(classes) and
 * the paths between them.
 * 
 * @author johnh
 *
 */
public class Data {

	/**
	 * A graph that acts as a map, holds an enum called Integer that contains
	 * locations from all around campus, these are the vertices in the graph,
	 * allowing us to find the shortest path.
	 */
	public static CS400Graph<Integer> schoolMap;

	/**
	 * enum of all locations the user could visit
	 */
	public enum Integer {
		sellery, chemistry, engineering, humanities, frats, bascom, agriculture, lakeshore;
	}

	/**
	 * creates, fills, and then returns the graph.
	 * 
	 * @return the graph after it has been filled with data
	 */
	public static CS400Graph<Integer> getGraph() {
		// Initialize the graph
		schoolMap = new CS400Graph<>();

		// Insert Vertices, these being the locations on the map
		schoolMap.insertVertex(Integer.humanities);

		schoolMap.insertVertex(Integer.sellery);

		schoolMap.insertVertex(Integer.chemistry);

		schoolMap.insertVertex(Integer.engineering);

		schoolMap.insertVertex(Integer.frats);

		schoolMap.insertVertex(Integer.agriculture);

		schoolMap.insertVertex(Integer.lakeshore);

		schoolMap.insertVertex(Integer.bascom);

		schoolMap.insertVertex(Integer.chemistry);

		schoolMap.insertVertex(Integer.engineering);
		// Finished inserting Vertices
		
		
		// Insert edges (essentially the roads that will connect our campus locations)
		
		schoolMap.insertEdge(Integer.lakeshore, Integer.humanities, 11);
		schoolMap.insertEdge(Integer.humanities, Integer.lakeshore, 11);

		schoolMap.insertEdge(Integer.lakeshore, Integer.frats, 15);
		schoolMap.insertEdge(Integer.frats, Integer.lakeshore, 15);
		
		schoolMap.insertEdge(Integer.lakeshore, Integer.agriculture, 5);
		schoolMap.insertEdge(Integer.agriculture, Integer.lakeshore, 5);

		schoolMap.insertEdge(Integer.lakeshore, Integer.bascom, 8);
		schoolMap.insertEdge(Integer.bascom, Integer.lakeshore, 8);

		schoolMap.insertEdge(Integer.humanities, Integer.sellery, 2);
		schoolMap.insertEdge(Integer.sellery, Integer.humanities, 2);

		schoolMap.insertEdge(Integer.frats, Integer.sellery, 7);
		schoolMap.insertEdge(Integer.sellery, Integer.frats, 7);

		schoolMap.insertEdge(Integer.bascom, Integer.sellery, 5);
		schoolMap.insertEdge(Integer.sellery, Integer.bascom, 5);
		
		schoolMap.insertEdge(Integer.chemistry, Integer.sellery, 3);
		schoolMap.insertEdge(Integer.sellery, Integer.chemistry, 3);
		
		schoolMap.insertEdge(Integer.lakeshore, Integer.engineering, 7);
		schoolMap.insertEdge(Integer.engineering, Integer.lakeshore, 7);

		schoolMap.insertEdge(Integer.lakeshore, Integer.chemistry, 10);
		schoolMap.insertEdge(Integer.chemistry, Integer.lakeshore, 10);

		schoolMap.insertEdge(Integer.agriculture, Integer.sellery, 7);
		schoolMap.insertEdge(Integer.sellery, Integer.agriculture, 7);

		schoolMap.insertEdge(Integer.engineering, Integer.sellery, 6);
		schoolMap.insertEdge(Integer.sellery, Integer.engineering, 6);
		
		// classes to adjacent classes
		schoolMap.insertEdge(Integer.engineering, Integer.agriculture, 4);
		schoolMap.insertEdge(Integer.agriculture, Integer.engineering, 4);

		schoolMap.insertEdge(Integer.chemistry, Integer.engineering, 4);
		schoolMap.insertEdge(Integer.engineering, Integer.chemistry, 4);

		schoolMap.insertEdge(Integer.bascom, Integer.agriculture, 8);
		schoolMap.insertEdge(Integer.agriculture, Integer.bascom, 8);

		schoolMap.insertEdge(Integer.bascom, Integer.humanities, 3);
		schoolMap.insertEdge(Integer.humanities, Integer.bascom, 3);

		schoolMap.insertEdge(Integer.humanities, Integer.frats, 6);
		schoolMap.insertEdge(Integer.frats, Integer.humanities, 6);

		schoolMap.insertEdge(Integer.bascom, Integer.frats, 8);
		schoolMap.insertEdge(Integer.frats, Integer.bascom, 8);
		
		schoolMap.insertEdge(Integer.bascom, Integer.chemistry, 3);
		schoolMap.insertEdge(Integer.chemistry, Integer.bascom, 3);

		// Finished inserting edges, our map is now connected by roads

		// return the map to the front end.
		return schoolMap;

	}

}