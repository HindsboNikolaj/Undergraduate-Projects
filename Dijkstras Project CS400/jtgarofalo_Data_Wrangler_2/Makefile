run: compile
        java FrontEnd
compile: FrontEnd.class TestPathfinder.class
Data.class: CS400Graph.class
        javac Data.java
CS400Graph.class:
        javac CS400Graph.java
BackEnd.class: Data.class
        javac BackEnd.java
FrontEnd.class: BackEnd.class Data.class
        javac FrontEnd.java
TestPathfinder.class: FrontEnd.class BackEnd.class Data.class
        javac -cp .:junit5.jar TestPathfinder.java
test: TestPathfinder.class
        java -jar junit5.jar --class-path . --scan-classpath --details tree
        @echo "FIXME: *test* should run all your group's testing engineer's JUnit tests for the application"
clean:
        $(RM) *.class