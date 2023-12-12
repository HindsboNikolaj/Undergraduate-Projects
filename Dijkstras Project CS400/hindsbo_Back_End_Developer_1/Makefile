run: compile
	java FrontEnd
compile:
	javac GraphADT.java
	javac CS400Graph.java
	javac Data.java
	javac BackEnd.java
	javac FrontEnd.java
	javac -cp .:junit5.jar TestApp.java

test:
	java -jar junit5.jar --class-path . --scan-classpath --details tree

clean:
	$(RM) *.class
