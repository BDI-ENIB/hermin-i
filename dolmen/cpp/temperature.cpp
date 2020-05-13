#include "temperature.hpp"

namespace dolmen
{
  Temperature::Temperature (int id, std::string name):Sensor{id,name}{}

  void Temperature::decoding(const std::string data)
  {
    double temperature = 1.0;
    std::string tempstr;
    int id = getID();
    if (data.length() == 8 && data[7] == ';')
    {
      //we check the sign
      (data[2] == '-')? temperature = -temperature : temperature = temperature;
      //we decode each character
      if (isdigit(data[3])) {
        tempstr += data[3];
      }
      if (isdigit(data[4])) {
        tempstr += data[4];
      }

      tempstr += ".";

      if (isdigit(data[5])) {
        tempstr += data[5];
      }
      if (isdigit(data[6])) {
        tempstr += data[6];
      }

      temperature = temperature * std::stod(tempstr);

      //Temperature::temperature_ = temperature;
      insert("temperature", temperature);
    }
    else
    {
      std::cout << "\nerror: bad data format";
      //Temperature::temperature_ = 0.0;
      insert("temperature_error", 0.0);
    }
  }
} /* dolmen */
