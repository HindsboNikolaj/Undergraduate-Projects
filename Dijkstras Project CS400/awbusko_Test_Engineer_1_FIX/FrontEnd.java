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
     sellery, chemistry , engineering, humanities, frats, bascom, agriculture, lakeshore; 
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
         * Instantiate the graph and distances between points
         */
        public static void createGraph() {

             graph.insertVertex(Integer.sellery);
             graph.insertVertex(Integer.chemistry );
             graph.insertVertex(Integer.engineering);
             graph.insertVertex(Integer.humanities);
             graph.insertVertex(Integer.frats);
             graph.insertVertex(Integer.bascom);
             graph.insertVertex(Integer.agriculture);
             graph.insertVertex(Integer.lakeshore);
             
             
                   
            // insert edges 
             
             //lakeshore to all
            //1 = .1 miles, 15 = 1.5 miles ect
             
             graph.insertEdge(Integer.lakeshore,Integer.agriculture,5);
            graph.insertEdge(Integer.agriculture,Integer.lakeshore,5);
            
            graph.insertEdge(Integer.lakeshore,Integer.bascom,8);
            graph.insertEdge(Integer.bascom,Integer.lakeshore,8);
            
            graph.insertEdge(Integer.lakeshore,Integer.engineering,7);
            graph.insertEdge(Integer.engineering,Integer.lakeshore,7);
            
            graph.insertEdge(Integer.lakeshore,Integer.chemistry,10);
            graph.insertEdge(Integer.chemistry,Integer.lakeshore,10);
            
            graph.insertEdge(Integer.lakeshore,Integer.humanities,11);
            graph.insertEdge(Integer.humanities,Integer.lakeshore,11);
            
            graph.insertEdge(Integer.lakeshore,Integer.frats,15);
            graph.insertEdge(Integer.frats,Integer.lakeshore,15);
            
            //sellery to all            
            graph.insertEdge(Integer.humanities,Integer.sellery,2);
            graph.insertEdge(Integer.sellery,Integer.humanities,2);
            
            graph.insertEdge(Integer.chemistry ,Integer.sellery,3);
            graph.insertEdge(Integer.sellery,Integer.chemistry ,3);
            
            graph.insertEdge(Integer.frats,Integer.sellery,7);
            graph.insertEdge(Integer.sellery,Integer.frats,7);
            
            graph.insertEdge(Integer.engineering ,Integer.sellery,6);
            graph.insertEdge(Integer.sellery,Integer.engineering ,6);
            
            graph.insertEdge(Integer.bascom,Integer.sellery,5);
            graph.insertEdge(Integer.sellery,Integer.bascom,5);
            
            graph.insertEdge(Integer.agriculture ,Integer.sellery,7);
            graph.insertEdge(Integer.sellery,Integer.agriculture ,7);
            
            
            //classes to adjacent classes
            graph.insertEdge(Integer.engineering,Integer.agriculture,4);
            graph.insertEdge(Integer.agriculture,Integer.engineering,4);
            
            graph.insertEdge(Integer.chemistry ,Integer.engineering,4);
            graph.insertEdge(Integer.engineering,Integer.chemistry,4);   
            
            graph.insertEdge(Integer.bascom,Integer.agriculture,8);
            graph.insertEdge(Integer.agriculture,Integer.bascom,8);
            
            graph.insertEdge(Integer.bascom,Integer.chemistry ,3);
            graph.insertEdge(Integer.chemistry ,Integer.bascom,3);
            
            graph.insertEdge(Integer.bascom,Integer.humanities,3);
            graph.insertEdge(Integer.humanities,Integer.bascom,3);                                    
            
            graph.insertEdge(Integer.humanities,Integer.frats,6);
            graph.insertEdge(Integer.frats,Integer.humanities,6);
            
            graph.insertEdge(Integer.bascom,Integer.frats,8);
            graph.insertEdge(Integer.frats,Integer.bascom,8);
        }
        
        
}
