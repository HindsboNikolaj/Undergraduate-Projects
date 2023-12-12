// --== CS400 File Header Information ==--
// Name: <Colton Carlino>
// Email: <ccarlino@wisc.edu>
// Team: <the team name: two letters>
// Role: <FrontEnd>
// TA: <Yepping>
// Lecturer: <Gary Dahl>
// Notes to Grader: <optional extra notes>
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.List;
import java.util.Scanner;
import java.util.Set;

public class FrontEnd {

  public static void run() {
    
    char add = 'y';
    char remove = 'y';
    String dorms = "";
    char input = 'e';
    Scanner scan = new Scanner(System.in);
    System.out.println("Welcome to the app!");
    Set<String> addedClasses = new HashSet<String>();
    // runs till q
    while(input!= 'q') {
      List classes = Arrays.asList("chemistry","engineering", "humanities", "frats", "agriculture");
      List startingDorm = Arrays.asList("sellery","lakeshore");
      
      while(startingDorm.contains(dorms.toLowerCase())!= true) {
        System.out.println("Where would you like to start?: [Sellery, Lakeshore]");
        dorms = scan.nextLine();
      }
      ArrayList<String> classSchedule = new ArrayList<String>();
      System.out.println("commands: a to add, r to remove, q to quit, f to find shortest path");
      input = scan.nextLine().toLowerCase().charAt(0);
      // command to add to the arraylist
      if(input == 'a') {
      while(add == 'y') {
        System.out.println("please add from the following classes: chemistry, engineering, humanities, frats, agriculture: MUST ENTER 2 CLASSES");
        String pickedClass = scan.nextLine().toLowerCase();
        if(classes.contains(pickedClass) && !addedClasses.contains(pickedClass)) {
          addedClasses.add(pickedClass);
          System.out.println("Add another class y/n");
          add = scan.nextLine().toLowerCase().charAt(0);
        }
        else {
          System.out.println("Invalid class or an already added class");
        }
      }
      }
      //command to remove from arraylist
      if(input == 'r') {
        while(remove == 'y') {
        System.out.println("Remove a class");
        String pickedClass = scan.nextLine().toLowerCase();
        if(classes.contains(pickedClass) && addedClasses.contains(pickedClass)) {
          addedClasses.remove(pickedClass);
          System.out.println("Remove another class y/n");
          remove = scan.nextLine().toLowerCase().charAt(0);
        }
        else {
          System.out.println("Invalid class or list empty");
          System.out.println("Keep removing y/n");
          remove = scan.nextLine().toLowerCase().charAt(0);
        }
        }
      }
      // command to find path
      if(input =='f') {
        classSchedule.addAll(addedClasses);
        System.out.println("Your path: " +  BackEnd.findShortestPath(dorms, classSchedule));
        System.out.println("Thank you for using this program!");
        System.exit(input);
      }
      }
    scan.close();
    }
  // runs the interface
  public static void main(String[] args) {
    run();
  }
}
