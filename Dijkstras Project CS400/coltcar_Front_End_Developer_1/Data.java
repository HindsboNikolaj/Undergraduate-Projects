// --== CS400 File Header Information ==--
// Name: Aaron Bath
// Email: apbath@wisc.edu email address
// Team: CC
// Role: Data Wrangler
// TA: Yeping
// Lecturer: Florian

public class Data{
    /**
     * enum of all locations the user could visit
     */
    public enum Integer 
    { 
     sellery, chemestry, engineering, humanities, frats, bascom, agriculture, lakeshore; 
    }

    /**
     * CS400 graph that holds all locations and distances from one-another
     */
     public static CS400Graph<Integer> graph;
     

        /**
         * creates, fills, and then returns the graph.
         * @return the graph after it has been filled with data
         */
     public static CS400Graph<Integer> getGraph(){
         graph = new CS400Graph<>();
         createGraph();
         return graph;
     }
     
     
          
        /**
         * Instantiate graph the graph
         */
        public static void createGraph() {

             graph.insertVertex(Integer.sellery);
             graph.insertVertex(Integer.chemestry);
             graph.insertVertex(Integer.engineering);
             graph.insertVertex(Integer.humanities);
             graph.insertVertex(Integer.frats);
             graph.insertVertex(Integer.bascom);
             graph.insertVertex(Integer.agriculture);
             graph.insertVertex(Integer.lakeshore);
             
             
                   
            // insert edges 
            graph.insertEdge(Integer.lakeshore,Integer.agriculture,10);
            graph.insertEdge(Integer.agriculture,Integer.lakeshore,10);
            
            graph.insertEdge(Integer.engineering,Integer.agriculture,8);
            graph.insertEdge(Integer.agriculture,Integer.engineering,8);
            
            graph.insertEdge(Integer.bascom,Integer.agriculture,8);
            graph.insertEdge(Integer.agriculture,Integer.bascom,8);
            
            graph.insertEdge(Integer.bascom,Integer.chemestry,9);
            graph.insertEdge(Integer.chemestry,Integer.bascom,9);
            
            graph.insertEdge(Integer.bascom,Integer.humanities,7);
            graph.insertEdge(Integer.humanities,Integer.bascom,7);
            
            graph.insertEdge(Integer.chemestry,Integer.sellery,6);
            graph.insertEdge(Integer.sellery,Integer.chemestry,6);
            
            graph.insertEdge(Integer.humanities,Integer.sellery,3);
            graph.insertEdge(Integer.sellery,Integer.humanities,3);
            
            graph.insertEdge(Integer.humanities,Integer.frats,10);
            graph.insertEdge(Integer.frats,Integer.humanities,10);
            
            graph.insertEdge(Integer.bascom,Integer.frats,14);
            graph.insertEdge(Integer.frats,Integer.bascom,14);
        }
        
        
}
