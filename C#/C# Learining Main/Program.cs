using System;
using System.Collections.Generic;
using System.Threading;

namespace C__Learining_Main
{
    class Program
    {

        static void Main(string[] args)
        {
            Thread mainThread = Thread.CurrentThread;
            mainThread.Name = "Main Thread";
            Console.WriteLine(mainThread.Name);

            Thread thread1 = new Thread(() => CountDown("timer #1 "));
            Thread thread2 = new Thread(() => CountUp("timer #2 "));
            thread1.Start();
            thread2.Start() ;
            
            


            

            Console.WriteLine($"{mainThread.Name} is complete!" );


            Console.ReadKey();

        }
        public static void CountDown(String name)
        {
            for (int i = 10; i >= 0; i--)
            {
                Console.WriteLine("Time #1 : " + i + "seconds");
                Thread.Sleep(1000);
            }
            Console.WriteLine("Timer #1 is complete");
        }

        public static void CountUp(String name)
        {
            for (int i = 0; i <= 10; i++)
            {
                Console.WriteLine("Time #2 : " + i + "seconds");
                Thread.Sleep(1000);
            }
            Console.WriteLine("Timer #2 is complete");
        }




    }



}




    
