#include <Servo.h>
#include <Romi32U4.h>
#include <PololuRPiSlave.h>
#include <stdarg.h>

struct Data
{
  bool yellow, green, red;
  bool buttonA, buttonB, buttonC;

  int16_t leftMotor, rightMotor;
  uint16_t batteryMillivolts;
  uint16_t analog[6];

  bool playNotes;
  char notes[14];

  int16_t leftEncoder, rightEncoder;
};

PololuRPiSlave<struct Data,5> slave;
PololuBuzzer buzzer;
Romi32U4Motors motors;
Romi32U4ButtonA buttonA;
Romi32U4ButtonB buttonB;
Romi32U4ButtonC buttonC;
Romi32U4Encoders encoders;

int32_t Kp = 450;
int32_t Kd = 250;

unsigned long time_target = 0;

int32_t speedControllerLeft(int32_t desired_counts) {
  static int32_t torque = 0;
  static int32_t error_last = 0;
  int32_t error;
    
  error = desired_counts - (int32_t) encoders.getCountsAndResetLeft();
  if (desired_counts == 0) {
    torque = 0;
  }
  else {
    torque += (Kp*error + Kd*(error-error_last))/1000;
  
  // Clamps to prevent the torque value from exceeding limits of motors.setLeftSpeed
    if (torque > 300) {
      torque = 300;
    }
    else if (torque < -300) {
      torque = -300;
    }
  }
  // Set motor "speed" function is misnamed - should be setLeftTorque
  motors.setLeftSpeed((int16_t) torque);
  error_last = error; // Used for the derivative term
  return(error);
}

int32_t speedControllerRight(int32_t desired_counts) {
  static int32_t torque = 0;
  static int32_t error_last = 0;
  int32_t error;
    
  error = desired_counts - (int32_t) encoders.getCountsAndResetRight();
  if (desired_counts == 0) {
    torque = 0;
  }
  else {
    torque += (Kp*error + Kd*(error-error_last))/1000;
  
  // Clamps to prevent the torque value from exceeding limits of motors.setLeftSpeed
    if (torque > 300) {
      torque = 300;
    }
    else if (torque < -300) {
      torque = -300;
    }
  }
  // Set motor "speed" function is misnamed - should be setLeftTorque
  motors.setRightSpeed((int16_t) torque);
  error_last = error; // Used for the derivative term
  return(error);
}

void setup()
{
  // Set up the slave at I2C address 20.
  slave.init(20);

  // Play startup sound.
  buzzer.play("v10>>g16>>>c16");
  time_target = micros() + 100000; // Read the number of microseconds since the program started. 
}

void loop()
{
  // Call updateBuffer() before using the buffer, to get the latest
  // data including recent master writes.
  slave.updateBuffer();

  // Write various values into the data structure.
  slave.buffer.buttonA = buttonA.isPressed();
  slave.buffer.buttonB = buttonB.isPressed();
  slave.buffer.buttonC = buttonC.isPressed();

  // Change this to readBatteryMillivoltsLV() for the LV model.
  slave.buffer.batteryMillivolts = readBatteryMillivolts();

//  for(uint8_t i=0; i<6; i++)
//  {
    //slave.buffer.analog[i] = analogRead(i);
  //}

  // READING the buffer is allowed before or after finalizeWrites().
  ledYellow(slave.buffer.yellow);
  ledGreen(slave.buffer.green);
  ledRed(slave.buffer.red);
  //motors.setSpeeds(slave.buffer.leftMotor, slave.buffer.rightMotor);

  // Playing music involves both reading and writing, since we only
  // want to do it once.
  //static bool startedPlaying = false;
  
  //if(slave.buffer.playNotes && !startedPlaying)
  //{
//    buzzer.play(slave.buffer.notes);
    //startedPlaying = true;
  //}
  //else if (startedPlaying && !buzzer.isPlaying())
  //{
//    slave.buffer.playNotes = false;
    //startedPlaying = false;
//  }

  //slave.buffer.leftEncoder = encoders.getCountsLeft();
  //slave.buffer.rightEncoder = encoders.getCountsRight();

1  // data available to I2C master.
  if (micros() >= time_target) {
    speedControllerLeft(slave.buffer.leftMotor);
    speedControllerRight(slave.buffer.rightMotor);
    time_target = micros() + 100000;
  }
  slave.finalizeWrites();
}
