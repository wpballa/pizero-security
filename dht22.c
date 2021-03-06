// compile line
// gcc -Wall -std=gnu99 dht22.c -o dht22 -l wiringPi

#include <wiringPi.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
#define MAX_TIME 85
#define ATTEMPTS 5
#define DHT22PIN 9      //physical pin 5

int dht22_val[5]={0,0,0,0,0};

int dht22_read_val()
{
    float humid=0.0;
    float tempC=0.0;
    float tempF=0.0;
    uint8_t lststate=HIGH;
    uint8_t counter=0;
    uint8_t j=0,i;
    int addr, nemail;
    char out_string[200];
    time_t current_time;
    current_time=time(NULL);
    FILE *fp;

// customize the next section for your needs
    float alarmhi=80.0;
    float alarmlo=60.0;
// to use text, here are the appropriate email addresses
// AT&T: [number]@txt.att.net
// Sprint: [number]@messaging.sprintpcs.com or [number]@pm.sprint.com
// T-Mobile: [number]@tmomail.net
// Verizon: [number]@vtext.com
// Boost Mobile: [number]@myboostmobile.com
// Cricket: [number]@sms.mycricket.com
// Metro PCS: [number]@mymetropcs.com
// Tracfone: [number]@mmst5.tracfone.com
// U.S. Cellular: [number]@email.uscc.net
// Virgin Mobile: [number]@vmobl.com

// adjust the size of email to the number of entries
    const char *email[2]={"youremail@comcast.net","anotheremail@gmail.com"};
    const char *loc="Location";

    nemail = sizeof(email)/sizeof(email[0]);

    for(i=0;i<5;i++)
         dht22_val[i]=0;

    pinMode(DHT22PIN,OUTPUT);
    digitalWrite(DHT22PIN,LOW);
    delay(18);
    digitalWrite(DHT22PIN,HIGH);
    delayMicroseconds(40);
    pinMode(DHT22PIN,INPUT);

    for(i=0;i<MAX_TIME;i++)
    {
        counter=0;
        while(digitalRead(DHT22PIN)==lststate){
            counter++;
            delayMicroseconds(1);
            if(counter==255)
                break;
        }
        lststate=digitalRead(DHT22PIN);
        if(counter==255)
             break;
        // top 3 transistions are ignored
        if((i>=4)&&(i%2==0)){
            dht22_val[j/8]<<=1;
            if(counter>16)
                dht22_val[j/8]|=1;
            j++;
        }
    }

    // verify checksum and print the verified data

    if((j>=40)&&(dht22_val[4]==((dht22_val[0]+dht22_val[1]+dht22_val[2]+dht22_val[3])& 0xFF)))
    {
        fp = fopen("/home/pi/temp.log", "a");
        humid=(256.*dht22_val[0]+dht22_val[1])/10.;
        tempC=(256.*dht22_val[2]+dht22_val[3])/10.;
        tempF=(9.*tempC/5.)+32.;

// enable next line for debug information
//        printf("%5.1f\t%5.1f\t%s",tempF,humid,ctime(&current_time));
        fprintf(fp,"%5.1f\t%5.1f\t%s",tempF,humid,ctime(&current_time));
        fclose(fp);

// send e-mail if over temperature, these are picked based on alarm levels

        if(tempF > alarmhi) {
            for (addr=0; addr<nemail; addr++) {
                sprintf(out_string,
                "echo '%s high temp %5.1f F alarm at %s' | "
                "heirloom-mailx -s '%s high temp %5.1f F alarm' %s",
                loc, tempF, ctime(&current_time), loc, tempF, email[addr]);
        	    printf("%s\n",out_string);
                system(out_string);
            } 
        } else if (tempF < alarmlo) {
            for (addr=0; addr<nemail; addr++) {
                sprintf(out_string,
                "echo '%s high temp %5.1f F alarm at %s' | "
                "heirloom-mailx -s '%s high temp %5.1f F alarm' %s",
                loc, tempF, ctime(&current_time), loc, tempF, email[addr]);
                system(out_string);
            }
        }
        return 1;
    }
    else
        return 0;
}

int main(void)
{
    int attempts=ATTEMPTS;
    if(wiringPiSetup()==-1)
        exit(1);
    while(attempts)
    {
        int success = dht22_read_val();
        if (success) {
            break;
        }
        attempts--;
        delay(500);
    }
    return 0;
}
