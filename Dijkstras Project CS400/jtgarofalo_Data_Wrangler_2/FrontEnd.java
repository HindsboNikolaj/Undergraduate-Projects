// --== CS400 File Header Information ==--
// Name: Casey Lin
// Email: cmlin@wisc.edu
// Team: CC
// TA: Yeping Wang
// Lecturer: Florian Heimerl
// Notes to Grader: <optional extra notes>

import java.util.*;

public class FrontEnd {

    public static void runFrontEnd() {
        Scanner s = new Scanner(System.in);
        char status = 'd';
        System.out.println("Welcome to the Class Schedule Creator!");
        while (status != 'q') {
            List dorms = Arrays.asList("sellery", "lakeshore");
            List classes = Arrays.asList("chemistry","engineering", "humanities", "frats", "agriculture", "bascom");
            //pick a dorm
            String dorm = "";
            while (!dorms.contains(dorm.toLowerCase())) {
                System.out.println("Choose your starting dorm: [Sellery, Lakeshore]");
                dorm = s.nextLine();
            }

            char addClass = 'y';
            Set<String> currclasses = new HashSet<String>();

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
            while (addClass == 'y') {
                System.out.println("Add a class: chemistry, agriculture, humanities, bascom, frats, engineering");
                String nextClass = s.nextLine().toLowerCase();
                if (classes.contains(nextClass) && !currclasses.contains(nextClass)) {
                    currclasses.add(nextClass);
                    System.out.println("add another class? (y/n)");
                    addClass = s.nextLine().charAt(0);
                } else {
                    System.out.println("Could not add class, try again: ");
                }

            }
            ArrayList<String> userClasses = new ArrayList<String>();
            userClasses.addAll(currclasses);

            System.out.println("Classes: " + userClasses);

            System.out.println("Your path: " + BackEnd.findShortestPath(dorm, userClasses));

            System.out.println("Press q to quit or press any key to make another path: ");
            //then create a
            //System.out.println("(a)dd a class, (r)emove a class, (g)enerate the ideal schedule, (c)lear the schedule, (q)uit: ");
            status = s.nextLine().toLowerCase().charAt(0);
        }
        s.close();
    }

    public static void main(String[] args) {
        runFrontEnd();
    }
}