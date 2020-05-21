#include <vector>
#include <iostream>
#include <memory>
#include <fstream>

#include "dolmen.hpp"

int main(int argc, char const *argv[]) {
  //creating a dolmen element
  dolmen::Dolmen DolMen;

  //reading the datas
  std::ifstream trame("trame.txt");
  std::ofstream ofs{"report.csv"};
  std::string dataTxt;

  //std::map<int, dolmen::Sensor*> sensorList = dolmen::initialise();
  //std::map<int, dolmen::Sensor*> sensorList = std::map<int, dolmen::Sensor*>();


  //creating a factory element
  /*using AFactory = dolmen::FactorySensor<std::string, std::unique_ptr<dolmen::Sensor>, int, std::string>;
  AFactory factory;*/

  //creating a map to store all the sensors
  std::map<int, std::unique_ptr<dolmen::Sensor>> sensorList;
  //std::map<int, dolmen::Sensor*> sensorList = std::map<int, dolmen::Sensor*>();
  dolmen::initialise(sensorList);

  //---

    for (const auto &elem: sensorList)
    {
      std::cout << "depuis prog------je suis une id de sensor " << elem.second->getID() << "\n";
      std::cout << "depuis prog------je suis un nom de sensor " << elem.second->getName() << "\n";
    }

  //reading the data trame
  if(trame)
  {
    //each line is a measurement of the rocket, with datas of each sensor
    std::string line;
    while(std::getline(trame,line))
    {
      //extracting data from each line
      //dataTxtLine is used to detect the empty lines
      std::string dataTxtLine;
      //data contain the unprocessed datas from one sensor
      std::string data;
      for (auto& letter : line)
      {
        data += letter;
        //detecting a sensor, which is separated from other sensors by a ';' tag
        if (letter == ';')
        {
          //adding the processed datas
          dataTxtLine += DolMen.decoding(data, sensorList);
          data = "";
        }
      }
      //if no data was processed (empty line), we don't add a \n caracter
      dataTxt += dataTxtLine;
      if (dataTxtLine != "")
      {
        dataTxt += '\n';
      }
      dataTxtLine = "";
    }
    //writing the datas in the .csv file
    ofs << dataTxt;
    //std::cout << "\n" << dataTxt;
  }
  else
  {
    //error to add later
    std::cout << "unable to open the file";
  }
  return 0;
}
