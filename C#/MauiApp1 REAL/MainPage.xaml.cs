namespace MauiApp1_REAL
{
    public partial class MainPage : ContentPage
    {
        int weight;
        int age;
        int height;
        int BMR;
        int count = 0;

        public MainPage()
        {
            InitializeComponent();
        }

        private void OnCounterClicked(object? sender, EventArgs e)
        {
            count++;

            if (count == 1)
                CounterBtn.Text = $"Clicked {count} time";
            else
                CounterBtn.Text = $"Clicked {count} times";

            SemanticScreenReader.Announce(CounterBtn.Text);
        }
        public int CalculateBMR(int weight,int age, int height)
        {
            weight = 74;
            height = 175;
            BMR = weight * height;
            return BMR;
        }

    }
}
