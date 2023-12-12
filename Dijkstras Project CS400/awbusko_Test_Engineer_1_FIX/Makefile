run: compile
        java FrontEnd

compile: FrontEnd.class TestApp.class

CS400Graph.class:
        javac CS400Graph.java

Data.class: CS400Graph.class
        javac Data.java

BackEnd.class: Data.class
        javac BackEnd.java

FrontEnd.class: BackEnd.class Data.class
        javac FrontEnd.java

TestApp.class: FrontEnd.class BackEnd.class Data.class
        javac -cp .:junit5.jar TestApp.java

test: TestApp.class
        java -jar junit5.jar --class-path . --scan-classpath --details tree


clean:
        $(RM) *.class
