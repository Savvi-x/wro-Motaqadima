#include <Servo.h>

// =====================================================
// WRO 2026 FUTURE ENGINEERS
// TEAM 6001
// LOW LEVEL CONTROLLER
// Raspberry Pi Pico W
// =====================================================


// =====================================================
// SERVO
// =====================================================

#define SERVO_PIN 15

#define STEER_LEFT     20
#define STEER_CENTER   83
#define STEER_RIGHT   145

Servo steering;


// =====================================================
// L293D MOTOR DRIVER
// =====================================================

#define MOTOR_IN1 16
#define MOTOR_IN2 17
#define MOTOR_EN  18


// =====================================================
// MOTOR SPEED
// =====================================================

int motorSpeed = 255;


// =====================================================
// FAILSAFE
// =====================================================

unsigned long lastCommandTime = 0;

const unsigned long COMMAND_TIMEOUT = 500;


// =====================================================
// MOTOR FORWARD
// =====================================================

void motorForward()
{
  // Direction corrected after physical testing

  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, HIGH);

  analogWrite(MOTOR_EN, motorSpeed);
}


// =====================================================
// MOTOR BACKWARD
// =====================================================

void motorBackward()
{
  digitalWrite(MOTOR_IN1, HIGH);
  digitalWrite(MOTOR_IN2, LOW);

  analogWrite(MOTOR_EN, motorSpeed);
}


// =====================================================
// MOTOR STOP
// =====================================================

void motorStop()
{
  analogWrite(MOTOR_EN, 0);

  digitalWrite(MOTOR_IN1, LOW);
  digitalWrite(MOTOR_IN2, LOW);
}


// =====================================================
// COMMAND PROCESSOR
// =====================================================

void processCommand(char cmd)
{
  lastCommandTime = millis();

  switch (cmd)
  {

    // ---------------------------------
    // Forward
    // ---------------------------------

    case 'F':

      motorForward();

      break;


    // ---------------------------------
    // Backward
    // ---------------------------------

    case 'B':

      motorBackward();

      break;


    // ---------------------------------
    // Stop
    // ---------------------------------

    case 'S':

      motorStop();

      break;


    // ---------------------------------
    // Steering Left
    // ---------------------------------

    case 'L':

      steering.write(STEER_LEFT);

      break;


    // ---------------------------------
    // Steering Right
    // ---------------------------------

    case 'R':

      steering.write(STEER_RIGHT);

      break;


    // ---------------------------------
    // Steering Center
    // ---------------------------------

    case 'C':

      steering.write(STEER_CENTER);

      break;
  }
}


// =====================================================
// SETUP
// =====================================================

void setup()
{

  // USB communication with Raspberry Pi

  Serial.begin(115200);


  // Motor pins

  pinMode(MOTOR_IN1, OUTPUT);
  pinMode(MOTOR_IN2, OUTPUT);
  pinMode(MOTOR_EN, OUTPUT);


  // Stop motor at startup

  motorStop();


  // Steering

  steering.attach(SERVO_PIN);

  steering.write(STEER_CENTER);


  delay(1000);


  lastCommandTime = millis();
}


// =====================================================
// LOOP
// =====================================================

void loop()
{

  // ==========================================
  // RECEIVE COMMAND FROM RASPBERRY PI
  // ==========================================

  while (Serial.available())
  {

    char command = Serial.read();

    processCommand(command);

  }


  // ==========================================
  // FAILSAFE
  // ==========================================

  if (millis() - lastCommandTime > COMMAND_TIMEOUT)
  {

    motorStop();

  }
}