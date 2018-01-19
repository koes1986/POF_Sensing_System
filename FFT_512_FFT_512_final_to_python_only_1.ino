
/*
fft_adc.pde
guest openmusiclabs.com 8.18.12
example sketch for testing the fft library.
it takes in data on ADC0 (Analog0) and processes them
with the fft. the data is sent out over the serial
port at 115.2kb.  there is a pure data patch for
visualizing the data.
*/

#define LIN_OUT 1 // use the log output function
#define FFT_N 512 // set to 256 point fft
#include <FFT_512.h>

unsigned long start;

void setup() {
  Serial.begin(115200); // use the serial port
  TIMSK0 = 0; // turn off timer0 for lower jitter
  ADCSRA = 0xe4; // set the adc to free running mode
  ADMUX = 0x40; // use adc0
  DIDR0 = 0x01; // turn off the digital input for adc0
 }

int real;
int img;
long first;
long second;
long result1;
long result2;
int f_real;
int f_img;


void loop() {
  while(1) { // reduces jitter
//    unsigned long start = millis();
//    Serial.println(start);
    cli();  // UDRE interrupt slows this way down on arduino1.0
    for (int i = 0 ; i < 1024 ; i += 2) { // save 256 samples
      while(!(ADCSRA & 0x10)); // wait for adc to be ready
      ADCSRA = 0xf4; // restart adc
      byte m = ADCL; // fetch adc data
      byte j = ADCH;
      int k = (j << 8) | m; // form into an int
      k -= 0x0200; // form into a signed int
      k <<= 6; // form into a 16b signed int
      fft_input[i] = k; // put real data into even bins
      //fft_input[i] = i/2+1;
      fft_input[i+1] = 0; // set odd bins to 0
    }

    //divide into 2 for windowing
    for(int i = 0; i < 512; i++){
          fft_input2[i]=fft_input[i+512];
    }

    //windowing
    fft_window1(); // window the data for better frequency response
    fft_window2();

    //sort into one
    for(int i = 0; i < 512; i++){
        fft_input[i+512]=fft_input2[i];
    }

      //reorder
    for(int i=0; i<480 ;i+=2) {
        int saved = fft_input[( 2*pgm_read_word_near(_reorder_table + i))];
        fft_input[( 2*pgm_read_word_near(_reorder_table + i))]= fft_input[( 2*pgm_read_word_near(_reorder_table + i+1))];
        fft_input[( 2*pgm_read_word_near(_reorder_table + i+1))]= saved;
    }
//    Serial.println(fft_input[0]);
   
    //run FFT
    for(int i =0 ; i < 512; i++){
          fft_input2[i]=fft_input[i];
    }
    fft_run();
    for(int i = 0; i < 512; i++){
          fft_input[i]=fft_input2[i];
          fft_input2[i]=fft_input[i+512];
    }
    fft_run();
    
//    //512 FFT from combination of 2x256 FFT
    for(int i = 0; i < 512; i+=2){
      real = pgm_read_word_near(_wk_constants512 + i); 
      img = pgm_read_word_near(_wk_constants512 + i+1);
      first = fft_input[i];
      second = fft_input[i+1];
      result1 = (first*real-second*img)/10000;
      result2 = (first*img+second*real)/10000;
      fft_input2[i]= fft_input2[i]+ result1;
      fft_input2[i+1]= fft_input2[i+1]+ result2;
      
    }
    fft_mag_lin(); //calculate the magnitude
    
    // 14,15,16
    //Serial.print(fft_lin_out[93]);
    //Serial.print("a");
//    Serial.print(fft_lin_out[100]);
//    Serial.print("a");
    Serial.println(fft_lin_out[173]);
//    Serial.println("stop");
//    for(int i = 0; i < 256; i++){
//          Serial.println(fft_lin_out[i]);
//    }
    sei();  
    delay(100);
  }
}
