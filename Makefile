animals.o: animals.cpp
	g++ -c -o animals.o animals.cpp

mybin: *.o
	g++ -o mybin animals.o
