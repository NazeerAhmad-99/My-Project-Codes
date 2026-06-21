using System;

namespace Human_maker
{
    class Program
    {
        static void Main(string[] args)
        {
            bool flag = true;
            Human[] humans = new Human[50];

            while (flag)
            {

                //Human human1 = new Human("Nazeer", 22, ["workout,run,code,WASTE TIME"]);
                //Human human2 = new Human("Fatima", 17, ["Bitch around, give others headache, be a retard, be the dummest bitch around"]);

                //Console.WriteLine(human1.Display_Habbits());
                //Console.WriteLine(human2.Display_Habbits());

                Console.WriteLine("This Program is make for testing the knowledge of creating new OOP class Objects");
                Console.WriteLine();

                Console.WriteLine("Please enter the name of the human you would like to create: ");
                String name = Console.ReadLine();

                Console.WriteLine("Their age: ");
                int age = Convert.ToInt32(Console.ReadLine());

                Console.WriteLine("Their Habbits: ");
                String[] habbits = { Console.ReadLine() };

                Human new_human = new Human(name, age, habbits);
                Console.WriteLine($"A new human has been created, their name is {name} They are {age} years old.");
                Console.WriteLine(new_human.Display_Habbits());
                humans.Append(new_human);


                Console.WriteLine("Would you like to continue?, Y for YES, N for NO");
                String reply = Console.ReadLine();
                reply = reply.ToUpper();
                if (reply == "Y")
                {
                    flag = true;
                }
                else if (reply == "N")
                {
                    flag = false;

                }






            }


        }


    }
    class Human
    {
        public String name;
        public int age;
        public String[] habbits;



        public Human(String name, int age, String[] habbits)
        {
            this.name = name;
            this.age = age;
            this.habbits = habbits;

        }

        public String Display_Habbits()
        {
            foreach (String habbit in habbits)
            {
                Console.WriteLine(name + " likes to : " + habbit);
            }
            return null;






        }



    }

}
