# taskforapi

Project Folder .. This is the n Finite State Machine (FSM) that manages state transitions based on
predefined conditions.
this task has the 3 three states and the four commands .

State : Idle,Running,Pasue
Commands: Start,Stop,Pause, Resume
I was developed this api function using the sonic web framework . Initially i created some id Like Instance ID and Initial Stage the ID was IDLE, After that i was changed the state using the commands start by Instance Id , Now the State was Running .. Now it has two option Stop the State or Pause The State, This action also proceeded by the instance and commands . I will show the work sample
![alt text](api_test.png)
List of TRANSITIONS
("IDLE", "Start")->"Running",
("Running", "Pause")-> "Paused",
("Running", "Stop")->"IDLE",
("Paused", "Resume")-> "Running",
("Paused", "Stop")-> "IDLE",
![alt text](<Screenshot 2025-02-23 132355.png>)

![alt text](<Screenshot 2025-02-23 132227.png>)

#The Second Task With was the LLM SQL Agent With the Financial Data
