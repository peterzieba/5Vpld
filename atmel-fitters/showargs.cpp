// Simple program which prints the name of the executable and all arguments passed to it.
// To compile you will need:
// apt-get install g++-mingw-w64-i686-win32
// i686-w64-mingw32-g++ showargs.cpp -static -o showargs.exe

//This is useful for determining how cupl.exe is calling the fitters since this output does not get echoed to the screen.
#include <iostream>
#include <fstream>
#include <string>

int main(int argc, char* argv[]) {

    // File where the arguments will be written to
    std::ofstream outfile("showargs-output.txt");

    // Check if the file opened successfully
    if (!outfile) {
        std::cerr << "Error: Unable to open output file." << std::endl;
        return 1;
    }

    // Write each argument to the file
    for (int i = 1; i < argc; ++i) {
        outfile << argv[i] << std::endl;
    }

    outfile.close();
    std::cout << "Arguments have been written to output.txt." << std::endl;
    return 0;
}