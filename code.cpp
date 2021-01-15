#include <iostream>
#include <iomanip>

int main(){
  double miles;
  std::cin >> miles;
  std::cout << miles << " miles are " << std::setprecision(3) << (miles * (double) 1.609) << " kilometers" << std::endl;
}
