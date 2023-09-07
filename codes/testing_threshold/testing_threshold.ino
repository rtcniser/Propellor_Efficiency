 int val;
 int threshold = 4;

void setup() {
   // put your setup code here, to run once:
   pinMode(A0, INPUT);
   Serial.begin(9600);
}

void loop() {
   // put your main code here, to run repeatedly:
//  Serial.println(analogRead(A0));
   if (analogRead(A0) >= threshold){
     Serial.println(1);
   }else{
     Serial.println(0);
   }
   delay(30);
}