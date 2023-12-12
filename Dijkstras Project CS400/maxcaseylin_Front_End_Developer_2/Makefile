run: compile
	java FrontEnd

compile:
	javac BackEnd.java
	javac CS400Graph.java
	javac Data.java
	javac FrontEnd.java
	javac GraphADT.java

test:
	javac -cp .:junit5.jar TestPathfinder.java
	java -jar junit5.jar --class-path . --scan-classpath --details tree

clean:
	$(RM) *.class
