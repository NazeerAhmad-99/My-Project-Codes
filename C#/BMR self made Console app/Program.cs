using System;

namespace BMR_Self_Made_Console_APP
{
    class Program
    {
        static void Main(string[] args)
        {


            Console.WriteLine("Please enter weight in KG:  ");
            double weight = Convert.ToDouble(Console.ReadLine());

            Console.WriteLine("Please enter height in cm:  ");
            double height = Convert.ToDouble(Console.ReadLine());

            Console.WriteLine("Please enter Age in years:  ");
            double age = Convert.ToDouble(Console.ReadLine());

            Console.WriteLine("Please select your Acitivty Level\n1-Sedentary \n2-Lightly Active\n3-Moderately Active\n4-Very Active\n5-Super Active  ");
            int activity = Convert.ToInt32(Console.ReadLine());

            Console.WriteLine(" ");

            double Maintainece = TDEE(Bmr(weight, height, age), activity);

            Console.WriteLine("Your daily calorie expenditure is: " + Maintainece);

            Console.ReadKey();
        }
        static double Bmr(double weight, double height, double age)
        {
            double bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5;
            return bmr;
        }
        static double TDEE(double bmr, int activity)
        {
            if (activity == 1)
            {
                return bmr * 1.2;
            }
            else if (activity == 2)
            {
                return bmr * 1.375;
            }
            else if (activity == 3)
            {
                return bmr * 1.55;
            }
            else if (activity == 4)
            {
                return bmr * 1.725;
            }
            else if (activity == 5)
            {
                return bmr * 1.9;
            }
            else
            {
                Console.WriteLine("You did NOT enter a correct activity level");
                return bmr; // Default return to satisfy all code paths
            }
        }


    }
}
